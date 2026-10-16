"""Local, read-only source scan; writes traceable audit tables in this package.

No text line or URL is deemed verified merely because it is inventoried.
Run with Python 3.11+ from any directory. Does not execute source code.
"""
from pathlib import Path
import csv, hashlib, json, re
from collections import Counter
from urllib.parse import urlsplit, urlunsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATE = '2026-10-16'
EXCLUDE = {'.git', '.quarto', '.Rproj.user', '__pycache__', 'node_modules'}
OUTPUTS = {'專案文件掃描_20261016.csv', '全專案待核斷言_20261016.csv',
           '掃描摘要_20261016.json', '交付現況_SHA256_20261016.csv'}
TEXT = {'.md', '.qmd', '.csv', '.json', '.py', '.ps1', '.scss', '.rproj', '.gitignore', ''}

def write_csv(name, rows, fields):
    with (HERE / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)

def safe_text(text):
    # Do not duplicate expiring signed tokens into audit tables.
    return re.sub(r'https?://[^\s<>"\)]+', lambda m: urlunsplit(
        (*urlsplit(m[0])[:3], '', '')) if 'X-Amz-' in m[0] else m[0], text)

def scan():
    inventory, claims, issues = [], [], []
    seen = Counter()
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if not path.is_file() or any(p in EXCLUDE for p in rel.parts): continue
        if path.parent == HERE and path.name in OUTPUTS: continue
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        suffix = path.suffix.lower()
        generated = suffix == '.html' or any(p.endswith('_files') for p in rel.parts)
        status, lines, urls = 'BINARY_NOT_CONTENT_VERIFIED', 0, 0
        if not generated and suffix in TEXT:
            try:
                text = data.decode('utf-8-sig')
            except UnicodeDecodeError:
                status = 'ENCODING_REQUIRES_REVIEW'
            else:
                status = 'TEXT_FULLY_SCANNED_NOT_FACT_VERIFIED'
                source_lines = text.splitlines(); lines = len(source_lines)
                urls = len(re.findall(r'https?://', text))
                if suffix == '.json':
                    try: json.loads(text)
                    except ValueError as e: issues.append({'file':str(rel),'issue':str(e)})
                if suffix == '.csv':
                    rows = list(csv.reader(text.splitlines()))
                    if rows:
                        for n,row in enumerate(rows[1:],2):
                            if len(row) != len(rows[0]):
                                issues.append({'file':str(rel),'line':n,'issue':'CSV_COLUMN_COUNT'})
                if suffix in {'.md', '.qmd', '.csv'} and path.name not in OUTPUTS:
                    for n,line in enumerate(source_lines,1):
                        if len(line.strip()) < 15 or not re.search(r'[\w\u4e00-\u9fff]',line): continue
                        # Line-level candidates, not semantic claim extraction.
                        key = hashlib.sha256(line.strip().encode()).hexdigest()
                        seen[key] += 1
                        claims.append({'candidate_id':'L-'+hashlib.sha256((str(rel)+':'+str(n)).encode()).hexdigest()[:16],
                            'source_file':str(rel),'line':n,'text_sha256':key,
                            'candidate_excerpt':safe_text(line.strip())[:900],
                            'status':'UNREVIEWED_LINE_CANDIDATE',
                            'extraction_scope':'line candidate; may contain multiple claims; headings/code included'})
        elif generated:
            status = 'GENERATED_DERIVATIVE_HASHED_NOT_SEPARATELY_FACT_VERIFIED'
        inventory.append({'file':str(rel),'bytes':len(data),'sha256':sha,'scan_status':status,
                          'lines':lines,'url_occurrences':urls})
    write_csv('專案文件掃描_20261016.csv',inventory,list(inventory[0]))
    write_csv('全專案待核斷言_20261016.csv',claims,list(claims[0]))
    summary={'as_of':DATE,'file_count':len(inventory),'scan_status_counts':dict(Counter(r['scan_status'] for r in inventory)),
             'line_candidates':len(claims),'unique_candidate_texts':len(seen),
             'syntax_issues':issues,'semantic_verification_complete':False,
             'exclusions':sorted(EXCLUDE),'candidate_extraction':'all source MD/QMD/CSV; outputs excluded; line candidates are not atomic claims',
             'warning':'all files inventoried, text scanned; not all assertions externally verified'}
    (HERE/'掃描摘要_20261016.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

def manifest():
    rows=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file() and p.name != '交付現況_SHA256_20261016.csv' and '__pycache__' not in p.parts:
            b=p.read_bytes(); rows.append({'file':str(p.relative_to(HERE)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    write_csv('交付現況_SHA256_20261016.csv',rows,['file','bytes','sha256'])

if __name__ == '__main__':
    import sys
    manifest() if '--manifest' in sys.argv else scan()
