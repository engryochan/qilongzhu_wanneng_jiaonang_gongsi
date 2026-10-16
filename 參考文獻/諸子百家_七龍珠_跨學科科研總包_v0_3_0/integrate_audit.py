"""Reconcile the saved 2026-10-16 source receipts into this package only.

This is a local integration, not a new external verification. Historical source
values are retained alongside corrected values. Reruns are idempotent.
"""
from pathlib import Path
import csv, hashlib, json
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATE = '2026-10-16'

def read(name):
    with (HERE/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def write(name,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (HERE/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def run():
    checks=json.loads((HERE/'來源核查回執_20261016.json').read_text(encoding='utf-8'))['checks']
    groups={58:3,54:10,55:17,41:21,45:28,47:29,53:16,60:36,59:40,57:50}
    evidence=read('寰宇交流科技_證據註冊表_20261014.csv')
    for r in evidence:
        n=int(r['evidence_id'][2:]); status,url,source_date,note=checks[str(n)]
        r.setdefault('legacy_publication_year',r['publication_year'])
        r.setdefault('legacy_verification_scope',r['verification_scope'])
        r['source_date_confirmed']=source_date
        r['audit_as_of']=DATE; r['audit_status']=status
        r['audit_source_url']=url; r['audit_note']=note
        r['source_group_id']=f'SRC-{groups.get(n,n):02d}'
        r['event_group_id']='REG-LUA-P230042' if n in {15,16,53} else r['source_group_id']
        r['independent_replication']='NOT_ASSESSED'
        r['verification_scope']='核查深度以audit_status及audit_note為準；未核全篇、未獨立復現、未核法定國籍'
        if n == 23: r['publication_year']='2024'
        if n == 48: r['publication_year']='2025'
        if n == 34: r['publication_year']='2019'
        if n == 16 or n in {27,29,30,31,32,33,43,49,50,52,53,57}:
            r['publication_year']='' # Live documents are not necessarily first published in 2026.
        if n == 38:
            r['maturity']='THEORETICAL'; r['source_type']='同行評議理論研究'
        if n == 39:
            r['maturity']='LAB'; r['domain']='時間調變微波超表面'
        if n == 37:
            r['source_title']='Nonreciprocal scattering and implications for thermal emission control on a mid-infrared spatiotemporally modulated metasurface'
        if n == 42:
            r['maturity']='UNVERIFIED' if status=='SOURCE_UNAVAILABLE' else 'CLINICAL_REVIEW'
            r['boundary_or_limitation']=note
        if n == 5:
            r['source_title']='Liquid crystal-enabled electro-osmosis through spatial charge separation in distorted regions as a novel mechanism of electrokinetics'
        if n == 7:
            r.setdefault('legacy_institution_context',r['country_or_institution_context_not_citizenship'])
            r['country_or_institution_context_not_citizenship']='加拿大：University of Toronto／Concordia作者機構，非國籍'
        if n == 15:
            r['boundary_or_limitation']=note
        if n == 35:
            r['publication_year']='2021'
            r['boundary_or_limitation']='PRISMA 2020為指引名稱；聲明論文2021-03-29發表。報告規範不保證研究有效性。'
    write('寰宇交流科技_證據註冊表_20261014.csv',evidence)
    by_id={r['evidence_id']:r for r in evidence}
    audit=read('科研證據_來源與獨立性審核_v0_3_0.csv')
    for r in audit:
        e=by_id[r['evidence_id']]
        r.setdefault('legacy_audit_status',r['audit_status'])
        r.setdefault('legacy_source_date',r['source_date'])
        r['source_date']=e['source_date_confirmed']
        r['audit_status']=e['audit_status'];r['audit_as_of']=DATE
        r['source_layer']='2026-10-16查核；深度逐列記錄'
        r['maturity']=e['maturity'];r['title']=e['source_title']
        r['source_group_id']=e['source_group_id'];r['event_group_id']=e['event_group_id']
        r['audit_source_url']=e['audit_source_url'];r['audit_note']=e['audit_note']
    write('科研證據_來源與獨立性審核_v0_3_0.csv',audit)
    tools=read('科研軟硬體與計數尤物_組件註冊表_v0_3_0.csv')
    versioned={'OpenFOAM Foundation':('14 (2026-07-14)','EV44'), 'FEniCSx':('0.11 (2026-06)','EV28'), 'QuTiP':('5.3.1 (2026-08-04)','EV46')}
    limited={'Elmer FEM','NEURON','ROS 2','PennyLane','Scanpy'}
    for r in tools:
        product=r['product_or_category'];r['audit_as_of']=DATE
        r['local_test']='NOT_RUN';r['model_or_version_pinned']='NO'
        if product in versioned:
            r['version_as_of'],r['evidence_id']=versioned[product]
            r['audit_status']='RELEASE_CHECKED'
        elif r['domain']=='硬體類型':
            r['audit_status']='CATEGORY_ONLY_NO_DEVICE_VERIFIED';r['evidence_id']=''
        else:
            r['audit_status']='ACCESS_LIMITED_REQUIRES_REVIEW' if product in limited else 'OFFICIAL_ENTRY_ONLY'
            r['evidence_id']=''
        r['verification_scope']='入口或發佈資料核對；不等於安裝、性能、授權全文、作業系統相容性驗證'
    write('科研軟硬體與計數尤物_組件註冊表_v0_3_0.csv',tools)
    entities=read('全球科研機構_公司平台_關聯登錄_v0_3_0.csv')
    mapping={'NASA Glenn Research Center':'EV43','MIT':'EV03','NIH NCATS':'EV49','FDA':'EV36','Novocure':'EV36','IBM Quantum':'EV48',
             'University of Michigan':'EV10','四川大學與華西醫院':'EV17','南京大學':'EV39','東京大學竹內研究室':'EV52',
             'Säntis雷電試驗跨國團隊':'EV08','EPFL':'EV26','國立臺灣大學':'EV40','European Commission JRC / EURL ECVAM':'EV50'}
    for r in entities:
        r['audit_as_of']=DATE;r['supporting_evidence_id']=mapping.get(r['entity'],'')
        r['audit_status']='RESEARCH_RELATION_ONLY_IDENTITY_NOT_FULLY_CHECKED' if r['supporting_evidence_id'] else 'UNREVIEWED_ENTITY_CANDIDATE'
        r['legal_identity_status']='NOT_VERIFIED';r['ownership_status']='UNKNOWN_NOT_VERIFIED'
        r['geographic_scope']='機構／試驗所在地線索；不是法定國籍、公司註冊地或所有制認定'
    write('全球科研機構_公司平台_關聯登錄_v0_3_0.csv',entities)

    seed_dir=ROOT/'參考文獻/諸子百家_七龍珠_跨學科科研總包_v0_1_0'
    person_receipt_path=HERE/'人物核查回執_20261016.json'
    person_receipt=json.loads(person_receipt_path.read_text(encoding='utf-8')) if person_receipt_path.exists() else {'checks':{},'sources':{}}
    reviewed_people=0
    seed_counts={}
    for old,new,key,expected in [
        ('諸子百家_七龍珠全技能_研究分類註冊表_v0_1_0.csv','七龍珠110項技能_逐項待核_v0_3_0.csv','skill_id',110),
        ('諸子百家_七龍珠科研_全球科學家名錄_初始種子_v0_1_0.csv','全球145位人物_身份與貢獻待核_v0_3_0.csv','record_id',145),
        ('諸子百家_學派思想註冊表_v0_1_0.csv','諸子百家14類思想_史料待核_v0_3_0.csv','school',14)]:
        p=seed_dir/old
        with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
        assert len(rows)==expected and len({r[key] for r in rows})==expected
        for n,r in enumerate(rows,2):
            r['source_file']=str(p.relative_to(ROOT));r['source_csv_record']=n
            r['source_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
            r['audit_as_of']=DATE;r['audit_status']='LOCAL_SEED_RECONCILED_EXTERNAL_CLAIMS_PENDING'
            r['next_check']='逐項核身份／原作定位／原始研究／限制，不以種子行數宣稱完成查證'
            if key=='skill_id':
                plans={
                    '01':('運動生理／控制／力學','速度m/s、負載N、延遲s、功率W','EV03;EV26','供能、運動尺度、控制穩定性'),
                    '02':('流體／聲場／電磁／能源','推力N、壓力Pa、能量J、效率及距離','EV02;EV06;EV08;EV43','驅動能量、耦合介質、損耗與熱'),
                    '03':('細胞／再生／生物工程','物種、存活率、效應量、觀察時窗','EV17;EV24;EV51','細胞與整體生物、短期與長期結果分開'),
                    '04':('神經介面／資訊與認知','樣本n、準確率分母、bit/s、延遲、假陽性','EV20;EV25;EV26;EV40','解碼任務、受試者校準、資料洩漏與泛化'),
                    '05':('相對論／空間系統／量子資訊','距離m、時間s、時鐘精度、通訊延遲','', '數位模擬與物理時空區分；量子態與物質分開'),
                    '06':('生命研究／材料與物理假說','先定義可觀測事件、背景率及對照條件','', '原作設定不是已證實的自然現象；先定義可否證問題'),
                    '07':('機械／材料／計算／模組化工程','尺寸m、質量kg、展開比、能耗與循環壽命','EV27;EV28;EV29;EV51','功能類比、材料與工具能力均需個別驗收')}
                family,measurement,refs,limits=plans[r['category'][:2]]
                r['proposed_research_family']=family;r['proposed_measurement']=measurement
                r['candidate_evidence_ids']=refs;r['mapping_status']='PROPOSED_CATEGORY_ANALOGY_NOT_ABILITY_VALIDATION'
                r['validation_boundary']=limits
            elif key=='record_id':
                r['identity_acceptance_rule']='官方履歷或可靠史料確認同一人；再核原論文作者及貢獻，不從所在地填國籍'
                item=person_receipt['checks'].get(r['record_id'])
                r['external_review_status']='NOT_REVIEWED'
                r['checked_source_ids']='';r['checked_source_urls']='';r['checked_contribution']=''
                if item:
                    refs,note=item
                    source_ids=refs.split(';')
                    sources=[person_receipt['sources'][source_id] for source_id in source_ids]
                    r['external_review_status']='LATIN_AUTHOR_ONLY_CHINESE_ALIAS_PENDING' if r['record_id']=='SCI-0063' else 'PARTIAL_NAME_AND_CONTRIBUTION_SOURCE_CHECKED'
                    r['checked_source_ids']=refs;r['checked_source_urls']=';'.join(s[0] for s in sources)
                    r['source_access_depth']=';'.join(sorted({s[1] for s in sources}))
                    r['checked_contribution']=note
                    r['audit_status']='PARTIAL_EXTERNAL_SOURCE_CHECKED'
                    r['next_check']='未核法定國籍、完整履歷、當前職稱及全部研究；按checked_contribution限定採信'
                    reviewed_people+=1
            else:
                r['primary_text_check']='原典版本、篇章、成書及作者歸屬待逐項核；歷史思想啟發不作自然科學實證'
                r['classification_source_url']='https://zh.wikisource.org/wiki/漢書/卷030'
                if r['school'] in {'儒家','道家','陰陽家','法家','名家','墨家','縱橫家','雜家','農家','小說家'}:
                    r['classification_review']='HANSHU_CATEGORY_TEXT_CHECKED_FIGURES_AND_ATTRIBUTIONS_PENDING'
                    r['classification_note']='僅確認諸子略分類；官職起源敘述是原典觀點，非已證歷史起源。'
                else:
                    r['classification_review']='EDITORIAL_EXTENSION_NOT_ONE_OF_TEN_SCHOOLS'
                    r['classification_note']='兵書、術數、方技在漢書另列；工藝博物為本研究擴充，不是古代第十四家。人物年代及具體著作另核。'
        write(new,rows);seed_counts[new]=len(rows)
    report={'as_of':DATE,'evidence_rows':len(evidence),'source_groups':len({r['source_group_id'] for r in evidence}),
            'source_groups_are_not_independent_studies':True,'audit_status_counts':dict(Counter(r['audit_status'] for r in evidence)),
            'seed_counts':seed_counts,'people_with_partial_source_review':reviewed_people,
            'people_still_without_external_review':145-reviewed_people,
            'all_claims_verified':False}
    (HERE/'本輪核查統計_20261016.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__': run()
