"""Build a neutral single-column academic review using local tools; no network calls."""
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent


def cite(match):
    value = match.group(1)
    if not re.fullmatch(r'[SR]\d+(?:, [SR]\d+)*(?:; abstract-only comparison here)?', value):
        return match.group(0)
    suffix = ', abstract-only comparison here' if ';' in value else ''
    keys = value.split(';')[0].split(', ')
    return '[' + '; '.join('@'+key for key in keys) + suffix + ']'


def prepare():
    text = (SOURCE/'manuscript.md').read_text()
    title = text.splitlines()[0].removeprefix('# ')
    abstract = text.split('## Abstract\n', 1)[1].split('**Keywords:**', 1)[0].strip()
    keyword_text = text.split('**Keywords:**',1)[1].split('\n',1)[0].strip().rstrip('.')
    body = text[text.index('## 1. Introduction'):text.index('## References')]
    body = re.sub(r'^(#{2,3}) \d+(?:\.\d+)*\.?\s+', r'\1 ', body, flags=re.M)
    body = body.replace('## Declarations and author-review status', '## Declarations and author-review status {.unnumbered}')
    body = re.sub(r'\[([^\]\n]+)\]', cite, body)
    body = body.replace('Emotion/risk/intervention generation', 'Emotion, risk and intervention generation')
    captions = [
        'Proposed claim-to-measurement framework. The layers are distinct evaluation questions, not a quality ranking.',
        'Selected support and historical-comparison publications. Settings and measured outcomes limit the interpretation of each claim.',
        'Evaluation-method comparators and the boundaries of their reference judgments.']
    lines = body.splitlines()
    out=[]; table=False; count=0
    for line in lines+['']:
        if table and not line.startswith('|'):
            out.extend(['', 'Table: '+captions[count], ''])
            count+=1;table=False
        if line.startswith('|'):table=True
        out.append(line)
    if count!=3:
        raise ValueError('Expected exactly three review tables; update captions for source changes')
    body='\n'.join(out).strip()+'\n'
    metadata={'title':title,'abstract':abstract,'keywords':keyword_text.split('; ')}
    (ROOT/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'paper-input.md').write_text('---\n'+json.dumps(metadata,ensure_ascii=False,indent=2)+'\n---\n\n'+body)
    bib=(SOURCE/'manuscript-references.bib').read_text()
    sources=json.loads((SOURCE/'manuscript-sources.json').read_text())
    # BibTeX/natbib styles do not uniformly print eprint. Explicitly identify the preprint source.
    for key,source in sources.items():
        pattern=r'(@misc\{'+re.escape(key)+r',\n)'
        bib=re.sub(pattern,lambda m:m.group(1)+'  howpublished={arXiv preprint arXiv:'+source['id']+'},\n',bib,count=1)
    (ROOT/'references.bib').write_text(bib)
    return sources


def write_reading_versions(aux, sources, work):
    numbering = {key:int(number) for key,number in re.findall(r'\\bibcite\{([^}]+)\}\{\{(\d+)\}', aux)}
    if set(numbering) != set(sources) or set(numbering.values()) != set(range(1,len(sources)+1)):
        raise SystemExit('Reference numbering is not a complete consecutive mapping')
    text=(SOURCE/'manuscript.md').read_text()
    body, references=text.split('## References',1)
    def numeric(match):
        value=match.group(1)
        if not re.fullmatch(r'[SR]\d+(?:, [SR]\d+)*(?:; abstract-only comparison here)?', value):
            return match.group(0)
        suffix=', abstract-only comparison here' if ';' in value else ''
        numbers=sorted(numbering[k] for k in value.split(';')[0].split(', '))
        return '['+', '.join(map(str,numbers))+suffix+']'
    body=re.sub(r'\[([^\]\n]+)\]',numeric,body)
    listed={}
    for line in references.splitlines():
        match=re.match(r'\[([SR]\d+)\]',line)
        if match:
            key=match.group(1)
            listed[key]=re.sub(r'^\[[SR]\d+\]',f'[{numbering[key]}]',line)
    if set(listed)!=set(sources):raise SystemExit('Readable reference list does not match the registry')
    ordered=[listed[k] for k in sorted(numbering,key=numbering.get)]
    (ROOT/'paper.md').write_text(body.rstrip()+'\n\n## References\n\n'+'\n\n'.join(ordered)+'\n')
    tex=(ROOT/'paper.tex').read_text()
    marker=r'\bibliographystyle{unsrtnat}'+ '\n' + r'\bibliography{references}'
    if marker not in tex:raise SystemExit('Bibliography marker not found')
    standalone=tex.replace(marker,(work/'paper.bbl').read_text())
    if r'\begin{thebibliography}' not in standalone:raise SystemExit('Inline bibliography missing')
    (ROOT/'paper-standalone.tex').write_text(standalone)
    shutil.copy2(ROOT/'paper-standalone.tex',work/'paper-standalone.tex')
    for _ in range(2):
        result=subprocess.run(['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
            'paper-standalone.tex'],cwd=work,capture_output=True,text=True)
        if result.returncode:raise SystemExit('Standalone XeLaTeX build failed; inspect logs')
    log=(work/'paper-standalone.log').read_text(errors='replace')
    if any(x in log for x in ['There were undefined references','Citation `','Missing character:','Overfull \\hbox']):
        raise SystemExit('Standalone build has unresolved bibliography or layout issues')
    actual=re.findall(r'\\bibcite\{([^}]+)\}',(work/'paper-standalone.aux').read_text())
    if len(actual)!=len(sources) or set(actual)!=set(sources):raise SystemExit('Standalone references differ')


def build():
    required=['pandoc','xelatex','bibtex']
    if any(not shutil.which(tool) for tool in required):
        raise SystemExit('Local Pandoc, XeLaTeX and BibTeX are required; no automatic installation performed')
    sources=prepare()
    subprocess.run(['pandoc',str(ROOT/'paper-input.md'),'--from=markdown+citations+table_captions',
                    '--to=latex','--standalone','--number-sections','--shift-heading-level-by=-1','--natbib',
                    '--bibliography=references.bib','--template='+str(ROOT/'template.tex'),
                    '--output='+str(ROOT/'paper.tex')],cwd=ROOT,check=True,capture_output=True)
    if '#tbl:' in (ROOT/'paper.tex').read_text():
        raise SystemExit('Unrendered table-attribute syntax detected')
    if r'\section{Introduction}' not in (ROOT/'paper.tex').read_text():
        raise SystemExit('Top-level section hierarchy is incorrect')
    work=ROOT/'build';work.mkdir(exist_ok=True)
    for name in ['paper.tex','references.bib']:
        shutil.copy2(ROOT/name,work/name)
    commands=[['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','paper.tex'],
              ['bibtex','paper'],
              ['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','paper.tex'],
              ['xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','paper.tex']]
    for command in commands:
        result=subprocess.run(command,cwd=work,capture_output=True,text=True)
        if result.returncode:
            print(result.stdout[-5000:])
            raise SystemExit(f'Local build failed at {command[0]}; inspect paper/build logs')
    log=(work/'paper.log').read_text(errors='replace')
    bad=['Citation `','There were undefined references','undefined on input line','Missing character:','Overfull \\hbox']
    if any(message in log for message in bad):
        raise SystemExit('Build has unresolved citations, missing glyphs or overflowing lines; inspect paper/build/paper.log')
    aux=(work/'paper.aux').read_text()
    labels=re.findall(r'\\bibcite\{([^}]+)\}',aux)
    if len(labels)!=len(sources) or set(labels)!=set(sources):
        raise SystemExit('Compiled reference labels differ from the selected source registry')
    shutil.copy2(work/'paper.pdf',ROOT/'paper.pdf')
    write_reading_versions(aux, sources, work)
    summary={'status':'compiled','selected_references':len(labels),'tables':3,
             'format':'generic single-column article; numbered sections and numeric natbib references',
             'readable_markdown_references':len(labels),'standalone_tex_verified':True,
             'submission_ready':False}
    (ROOT/'build-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    build()
