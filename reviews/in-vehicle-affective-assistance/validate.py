"""Offline integrity checks only: these do not validate a review's scientific conclusions."""
import csv
import json
from collections import Counter
from pathlib import Path


def validate(root):
    root=Path(root)
    records=json.loads((root/'records.json').read_text())
    by_id={p['id']:p for p in records}
    if len(by_id)!=len(records):raise ValueError('Duplicate versioned record')
    if len({p['id'].split('v')[0] for p in records})!=len(records):raise ValueError('Duplicate arXiv base ID')
    for paper in records:
        if paper['url']!='https://arxiv.org/abs/'+paper['id']:raise ValueError('Unverified link construction')
        if not all(paper[k] for k in ('title','authors','abstract','published','retrieved_at')):raise ValueError('Missing metadata')
    screened=list(csv.DictReader((root/'screening.csv').open()))
    evidence=list(csv.DictReader((root/'evidence-map.csv').open()))
    if {r['id'] for r in screened}!=set(by_id):raise ValueError('Screening ledger mismatch')
    primary={r['id'] for r in screened if r['pilot_decision']=='pilot_primary'}
    if {r['id'] for r in evidence}!=primary or len(evidence)!=len(primary):raise ValueError('Coded evidence mismatch')
    for row in evidence:
        if row['url']!=by_id[row['id']]['url']:raise ValueError('Evidence reference mismatch')
        if not row['source_locator'] or not row['limitations']:raise ValueError('Missing traceability')
        if 'human_check_pending' not in row['verification_status']:raise ValueError('Unexpected verification claim')
    audit=json.loads((root/'audit.json').read_text())
    if dict(Counter(r['pilot_decision'] for r in screened))!=audit['screening_decisions']:raise ValueError('Count discrepancy')
    if len(records)!=audit['total_records_with_seeds'] or len(evidence)!=audit['pilot_primary_studies']:raise ValueError('Audit count mismatch')
    actual=json.loads((root/'search-log.json').read_text())
    if sum(len(q['records']) for q in actual.values())!=audit['returned_search_records']:raise ValueError('Retrieval count mismatch')
    if len({p['id'].split('v')[0] for q in actual.values() for p in q['records']})!=audit['unique_search_records']:raise ValueError('Dedup count mismatch')
    report={'status':'integrity_checks_passed','records':len(records),'pilot_studies':len(evidence),
            'human_verification':'pending','systematic_search_complete':False,'submission_ready':False}
    return report


def validate_expansion(root):
    root=Path(root)
    records=json.loads((root/'expanded-records.json').read_text())
    by_id={p['id']:p for p in records}
    if len(by_id)!=len(records) or len({p['id'].split('v')[0] for p in records})!=len(records):
        raise ValueError('Duplicate expanded identifier')
    for p in records:
        if p['url']!='https://arxiv.org/abs/'+p['id']:
            raise ValueError('Expanded reference mismatch')
    screening=list(csv.DictReader((root/'expanded-screening.csv').open()))
    evidence=list(csv.DictReader((root/'expanded-evidence-map.csv').open()))
    if len(screening)!=len(records) or {r['id'] for r in screening}!=set(by_id):
        raise ValueError('Expanded screening coverage mismatch')
    coded={r['id'] for r in screening if r['expanded_decision'] in ('method_comparator','primary_or_historical_comparator')}
    if len(evidence)!=len(coded) or {r['id'] for r in evidence}!=coded:
        raise ValueError('Expanded coding count mismatch')
    for r in evidence:
        if r['url']!=by_id[r['id']]['url'] or not r['source_locator'] or not r['limitations']:
            raise ValueError('Expanded evidence traceability error')
        if 'human_check_pending' not in r['verification_status']:
            raise ValueError('Unsupported verification claim')
    audit=json.loads((root/'expanded-audit.json').read_text())
    if audit['records_with_review_seeds']!=len(records) or audit['coded_original_studies']!=len(evidence):
        raise ValueError('Expanded audit total mismatch')
    if audit['coded_roles']!=dict(Counter(r['scope_role'] for r in evidence)):
        raise ValueError('Expanded role count mismatch')
    if audit['screening_decisions']!=dict(Counter(r['expanded_decision'] for r in screening)):
        raise ValueError('Expanded decision count mismatch')
    logs=[json.loads((root/name).read_text()) for name in ('search-log.json','expanded-search-log.json')]
    retrieved=[p for log in logs for q in log.values() for p in q['records']]
    if len(retrieved)!=audit['returned_records_all_searches'] or len({p['id'].split('v')[0] for p in retrieved})!=audit['unique_search_ids']:
        raise ValueError('Expanded retrieval/dedup mismatch')
    if audit['database_search_complete'] or audit['human_verification_complete']:
        raise ValueError('Completion claims need independent verification')
    return {'status':'integrity_checks_passed','candidate_records':len(records),'coded_publications':len(evidence),
            'human_verification':'pending','systematic_search_complete':False,'submission_ready':False}


if __name__=='__main__':
    root=Path(__file__).parent
    result={'pilot':validate(root)}
    if (root/'expanded-audit.json').exists():result['expansion']=validate_expansion(root)
    print(json.dumps(result,indent=2))
