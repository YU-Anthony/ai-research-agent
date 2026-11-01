"""Offline bibliography/citation checks; not scientific or editorial peer review."""
import json
from pathlib import Path
import re


def validate(root):
    root=Path(root)
    manuscript=(root/'manuscript.md').read_text()
    body, references=manuscript.split('## References',1)
    registry=json.loads((root/'manuscript-sources.json').read_text())
    records={p['id']:p for p in json.loads((root/'expanded-records.json').read_text())}
    cited=set()
    for group in re.findall(r'\[([^\]\n]+)\]',body):
        cited.update(re.findall(r'\b[SR]\d+\b',group))
    if cited-set(registry):
        raise ValueError('Unregistered manuscript citation')
    reference_keys=re.findall(r'^\[([SR]\d+)\]',references,re.M)
    if len(reference_keys)!=len(set(reference_keys)) or set(reference_keys)!=set(registry):
        raise ValueError('Reference list and registry differ')
    if set(registry)-cited:
        raise ValueError('Uncited selected reference')
    bib=(root/'manuscript-references.bib').read_text()
    for key,source in registry.items():
        if source['id'] not in records:
            raise ValueError('Source missing from retrieved record ledger')
        p=records[source['id']]
        line=next(x for x in references.splitlines() if x.startswith('['+key+']'))
        if p['url'] not in line or p['id'] not in line:
            raise ValueError('Reference does not resolve to verified record')
        if not re.search(r'@\w+\{'+re.escape(key)+r',',bib):
            raise ValueError('BibTeX source missing')
    audit=json.loads((root/'expanded-audit.json').read_text())
    for value in [audit['returned_records_all_searches'],audit['unique_search_ids'],audit['records_with_review_seeds']]:
        if str(value) not in body:
            raise ValueError('Audit totals require manuscript update')
    if 'not be represented or submitted as a completed systematic review' not in body or 'Human checking' not in body:
        raise ValueError('Working-draft boundaries missing')
    if 'abstract-only' not in body and registry['R4']['depth']=='abstract_only':
        raise ValueError('Abstract-only reference depth not disclosed')
    return {'status':'citation_integrity_passed','selected_sources':len(registry),'cited_sources':len(cited),
            'body_words':len(body.split()),'scientific_verification':'human_review_pending',
            'submission_ready':False}


if __name__=='__main__':
    print(json.dumps(validate(Path(__file__).parent),indent=2))
