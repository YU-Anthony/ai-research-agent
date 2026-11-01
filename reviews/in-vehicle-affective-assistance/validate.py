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


if __name__=='__main__':
    result=validate(Path(__file__).parent)
    print(json.dumps(result,indent=2))
