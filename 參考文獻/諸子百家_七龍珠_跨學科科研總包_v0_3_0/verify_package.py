"""Verify package integrity and reconciliation, not scientific truth."""
from pathlib import Path
import csv, hashlib, json, math

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def read(name):
    with (HERE/name).open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);rows=list(reader)
        assert len(reader.fieldnames)==len(set(reader.fieldnames)),f'Duplicate headers: {name}'
        assert all(None not in r and None not in r.values() for r in rows),f'Invalid CSV: {name}'
        return rows

def main():
    for p in HERE.glob('*.json'): json.loads(p.read_text(encoding='utf-8-sig'))
    for p in HERE.glob('*.csv'): read(p.name)
    rows=read('寰宇交流科技_證據註冊表_20261014.csv')
    ids={r['evidence_id'] for r in rows}
    assert len(rows)==60 and ids=={f'EV{i:02d}' for i in range(1,61)}
    by_id={r['evidence_id']:r for r in rows}
    audit=read('科研證據_來源與獨立性審核_v0_3_0.csv')
    assert len(audit)==60 and {r['evidence_id'] for r in audit}==ids
    for r in audit:
        e=by_id[r['evidence_id']]
        for k in ['maturity','audit_status','audit_source_url','source_group_id','event_group_id']:
            assert r[k]==e[k],f'{r["evidence_id"]} cross-file mismatch: {k}'
        assert r['source_date']==e['source_date_confirmed']
    assert by_id['EV23']['publication_year']=='2024'
    assert by_id['EV38']['maturity']=='THEORETICAL'
    assert by_id['EV21']['source_group_id']==by_id['EV41']['source_group_id']
    for name,key,count in [('七龍珠110項技能_逐項待核_v0_3_0.csv','skill_id',110),
                           ('全球145位人物_身份與貢獻待核_v0_3_0.csv','record_id',145),
                           ('諸子百家14類思想_史料待核_v0_3_0.csv','school',14)]:
        seeds=read(name);assert len(seeds)==count and len({r[key] for r in seeds})==count
        p=ROOT/seeds[0]['source_file']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==seeds[0]['source_sha256']
        with p.open(encoding='utf-8-sig',newline='') as f: original=list(csv.DictReader(f))
        for old,new in zip(original,seeds):
            assert all(new[k]==v for k,v in old.items()),f'Seed original changed: {new[key]}'
            for ev in new.get('candidate_evidence_ids','').split(';'):
                if ev: assert ev in ids
    for r in read('全球科研機構_公司平台_關聯登錄_v0_3_0.csv'):
        assert not r['supporting_evidence_id'] or r['supporting_evidence_id'] in ids
    receipt=json.loads((HERE/'來源核查回執_20261016.json').read_text(encoding='utf-8'))
    assert set(receipt['checks'])=={str(i) for i in range(1,61)}
    # Independent arithmetic of the explicitly labelled point-mass thought experiment.
    mass=9.80665*(0.1**2)/6.67430e-11
    energy=mass*299792458**2
    assert math.isclose(mass,1.4693e9,rel_tol=1e-4)
    assert math.isclose(energy,1.3206e26,rel_tol=1e-4)
    manifest=read('交付現況_SHA256_20261016.csv')
    assert len(manifest)==len({r['file'] for r in manifest})
    for r in manifest:
        p=HERE/r['file'];data=p.read_bytes()
        assert len(data)==int(r['bytes']) and hashlib.sha256(data).hexdigest()==r['sha256'],f'Stale hash: {p.name}'
    j=json.loads((HERE/'交流跨領域科研_增訂審核清單_20261014.json').read_text(encoding='utf-8'))
    assert not j['current_verification']['full_semantic_fact_verification']
    summary={'result':'PASS_LOCAL_INTEGRITY_ONLY','evidence_rows':60,'seed_rows':[110,145,14],
             'manifest_entries_checked':len(manifest),'gravity_example_mass_kg':mass,
             'rest_energy_equivalent_J':energy,'all_facts_verified':False}
    print(json.dumps(summary,ensure_ascii=True,indent=2))

if __name__=='__main__':main()
