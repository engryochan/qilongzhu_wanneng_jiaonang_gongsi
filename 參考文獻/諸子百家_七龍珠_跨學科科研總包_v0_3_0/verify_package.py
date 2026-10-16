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

def ideal_teleportation_check():
    # Classical arithmetic, basis |Q A B>; never accesses quantum hardware.
    s=2**-.5
    inputs=[(1,0),(0,1),(s,s),(s,-s),(s,1j*s),(s,-1j*s),(math.sqrt(.3),1j*math.sqrt(.7))]
    branches_checked=0
    for psi in inputs:
        state=[0j]*8
        for q in range(2):
            for a in range(2):state[4*q+2*a+a]=psi[q]*s
        cnot=[0j]*8
        for index,amp in enumerate(state):
            q=index//4;a=(index//2)%2;b=index%2
            cnot[4*q+2*(a^q)+b]+=amp
        after=[0j]*8
        for a in range(2):
            for b in range(2):
                lo=2*a+b;hi=4+lo
                after[lo]=(cnot[lo]+cnot[hi])*s
                after[hi]=(cnot[lo]-cnot[hi])*s
        rho=[[0j]*2 for _ in range(2)]
        for q in range(2):
            for a in range(2):
                v=after[4*q+2*a:4*q+2*a+2]
                prob=sum(abs(z)**2 for z in v)
                assert math.isclose(prob,.25,abs_tol=1e-12)
                for i in range(2):
                    for j in range(2):rho[i][j]+=v[i]*v[j].conjugate()
                if a:v=[v[1],v[0]] # X, followed by Z
                if q:v=[v[0],-v[1]]
                overlap=sum(complex(psi[i]).conjugate()*v[i]/math.sqrt(prob) for i in range(2))
                assert math.isclose(abs(overlap)**2,1,abs_tol=1e-12)
                branches_checked+=1
        for i in range(2):
            for j in range(2):assert abs(rho[i][j]-(.5 if i==j else 0))<1e-12
    return branches_checked

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
    assert by_id['EV42']['maturity']=='CLINICAL_REVIEW'
    for ev in ['EV04','EV05','EV07','EV42']:
        assert by_id[ev]['audit_status']=='PUBLISHER_INDEX_ABSTRACT_CHECKED'
    people=read('全球145位人物_身份與貢獻待核_v0_3_0.csv')
    pr=json.loads((HERE/'人物核查回執_20261016.json').read_text(encoding='utf-8'))
    assert len(pr['checks'])==49
    assert set(pr['checks']) <= {r['record_id'] for r in people}
    for r in people:
        item=pr['checks'].get(r['record_id'])
        if item:
            refs=item[0].split(';')
            assert all(k in pr['sources'] for k in refs)
            assert r['checked_source_ids']==item[0]
            assert r['checked_source_urls']==';'.join(pr['sources'][k][0] for k in refs)
            assert r['audit_status']=='PARTIAL_EXTERNAL_SOURCE_CHECKED'
        else: assert r['external_review_status']=='NOT_REVIEWED'
    assert sum(r['external_review_status']=='NOT_REVIEWED' for r in people)==96
    # Illustrative assumptions only, not measured research-field error rates.
    assert math.isclose((.8*.1)/(.8*.1+.05),8/13)
    assert math.isclose((.8*.01)/(.8*.01+.05),4/29)
    assert math.isclose(1-.95**20,.6415140775914581)
    schools=read('諸子百家14類思想_史料待核_v0_3_0.csv')
    assert sum(r['classification_review']=='EDITORIAL_EXTENSION_NOT_ONE_OF_TEN_SCHOOLS' for r in schools)==4
    supplemental=read('補充事實核查_B02_20261016.csv')
    assert len(supplemental)==11 and len({r['claim_id'] for r in supplemental})==11
    assert all(r['source_url'].startswith('https://') for r in supplemental)
    b04=json.loads((HERE/'模型合併核查回執_B04_20261016.json').read_text(encoding='utf-8'))
    assert {s['id'] for s in b04['sources']}=={f'MM{i:02d}' for i in range(1,6)}
    assert b04['model_experiment_run'] is False
    traces=json.loads((HERE/'正文修訂追溯_20261016.json').read_text(encoding='utf-8'))
    b04traces=[r for r in traces if r.get('batch')=='B04']
    assert len(b04traces)==b04['correction_records'] and len(b04traces)>=6
    for r in b04traces:
        text=(HERE/r['file']).read_text(encoding='utf-8')
        assert r['old'] not in text and r['new'] in text,'B04 correction missing or reverted'
    b05=json.loads((HERE/'細胞重編程核查回執_B05_20261016.json').read_text(encoding='utf-8'))
    assert {s['id'] for s in b05['sources']}=={f'RP{i:02d}' for i in range(1,9)}
    assert b05['experiment_run'] is False and b05['registry_details_verified'] is False
    assert b05['sources'][0]['evidence_level']=='MOUSE_DERIVED_CELLS_IN_VITRO'
    assert b05['sources'][7]['access_depth']=='REGISTRY_ENTRY_NOT_SUBSTANTIVELY_RETRIEVED'
    b05traces=[r for r in traces if r.get('batch')=='B05']
    assert len(b05traces)==b05['correction_records'] and len(b05traces)==5
    for r in b05traces:
        text=(HERE/r['file']).read_text(encoding='utf-8')
        assert r['old'] not in text and r['new'] in text,'B05 correction missing or reverted'
    b06=json.loads((HERE/'並行仿真核查回執_B06_20261016.json').read_text(encoding='utf-8'))
    assert {s['id'] for s in b06['sources']}=={f'SIM{i:02d}' for i in range(1,7)}
    assert not b06['simulation_run'] and not b06['robot_deployment_run']
    assert b06['sources'][0]['research_or_document_group']==b06['sources'][1]['research_or_document_group']
    b06traces=[r for r in traces if r.get('batch')=='B06']
    assert len(b06traces)==b06['correction_records']==6
    for r in b06traces:
        text=(HERE/r['file']).read_text(encoding='utf-8')
        assert r['old'] not in text and r['new'] in text,'B06 correction missing or reverted'
    inputs=b06['illustration'];assert inputs['status']=='ASSUMED_INPUTS_NOT_MEASURED'
    q=inputs['aggregate_transitions_per_wall_second'];dt=inputs['control_step_sim_seconds']
    duration=inputs['wall_seconds'];envs=inputs['environments']
    assert q*duration==360000000 and math.isclose(q*duration*dt,7200000)
    assert math.isclose(q*duration*dt/envs,1757.8125)
    assert math.isclose(q*dt/envs,.48828125)
    assert math.isclose(q*duration*dt/(inputs['year_days']*86400),.228310502283105)
    b07=json.loads((HERE/'遙視與情報用途核查回執_B07_20261016.json').read_text(encoding='utf-8'))
    assert {s['id'] for s in b07['sources']}=={f'RV{i:02d}' for i in range(1,7)}
    assert not b07['experiment_run'] and not b07['memo_quote_verified']
    assert sum(s['access_depth']=='REDIRECTED_TO_READINGROOM_NO_DOCUMENT' for s in b07['sources'])==3
    b07traces=[r for r in traces if r.get('batch')=='B07']
    assert len(b07traces)==b07['correction_records'] and len(b07traces)>=7
    for r in b07traces:
        text=(HERE/r['file']).read_text(encoding='utf-8')
        assert r['old'] not in text and r['new'] in text,'B07 correction missing or reverted'
    b08=json.loads((HERE/'量子傳態核查回執_B08_20261016.json').read_text(encoding='utf-8'))
    assert {r['id'] for r in b08['sources']}=={f'QT{i:02d}' for i in range(1,5)}
    assert not b08['quantum_hardware_run'] and not b08['physical_teleportation_run']
    b08traces=[r for r in traces if r.get('batch')=='B08']
    assert len(b08traces)==b08['correction_records']==4
    for r in b08traces:
        text=(HERE/r['file']).read_text(encoding='utf-8')
        assert r['old'] not in text and r['new'] in text,'B08 correction missing or reverted'
    ideal_branches=ideal_teleportation_check();assert ideal_branches==28
    # Independent arithmetic of the explicitly labelled point-mass thought experiment.
    mass=9.80665*(0.1**2)/6.67430e-11
    energy=mass*299792458**2
    assert math.isclose(mass,1.4693e9,rel_tol=1e-4)
    assert math.isclose(energy,1.3206e26,rel_tol=1e-4)
    manifest=read('交付現況_SHA256_20261016.csv')
    assert len(manifest)==len({r['file'] for r in manifest})
    expected={str(p.relative_to(HERE)) for p in HERE.rglob('*')
              if p.is_file() and p.name!='交付現況_SHA256_20261016.csv' and '__pycache__' not in p.parts}
    assert {r['file'] for r in manifest}==expected,'Manifest has missing or extra files'
    for r in manifest:
        p=HERE/r['file'];data=p.read_bytes()
        assert len(data)==int(r['bytes']) and hashlib.sha256(data).hexdigest()==r['sha256'],f'Stale hash: {p.name}'
    j=json.loads((HERE/'交流跨領域科研_增訂審核清單_20261014.json').read_text(encoding='utf-8'))
    assert not j['current_verification']['full_semantic_fact_verification']
    summary={'result':'PASS_LOCAL_INTEGRITY_ONLY','evidence_rows':60,'seed_rows':[110,145,14],
             'manifest_entries_checked':len(manifest),'gravity_example_mass_kg':mass,
             'rest_energy_equivalent_J':energy,'ideal_quantum_protocol_algebra_branches':ideal_branches,
             'quantum_hardware_run':False,'all_facts_verified':False}
    print(json.dumps(summary,ensure_ascii=True,indent=2))

if __name__=='__main__':main()
