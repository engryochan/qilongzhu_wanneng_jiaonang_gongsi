"""Replay saved B05 evidence scope corrections; not a biological experiment."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PAIRS=[
('**現實**體內部分重編程（OSKM 山中因子週期性短時表達）已在小鼠身上延長壽命、逆轉 DNA 損傷、把表觀遺傳時鐘撥回去；肝、肌肉、視神經、皮層神經元均有在體再生證據。Altos Labs 聚集山中伸彌與 Izpisua Belmonte，但尚未公佈候選藥物；Life Biosciences 的部分表觀重編程平台 ER-100 預計 2026 年初進入早期臨床。',
 '**現實（B05訂正）**不同部分重編程研究須分開：2016研究摘要報告早衰小鼠模型的壽命延長；ERCC1論文的DNA損傷與表觀遺傳指標結果主要來自小鼠來源纖維母細胞的體外實驗；2020視網膜研究使用OSK三因子，不能統稱OSKM四因子。Life Biosciences於2026-06-09公告ER-100首位受試者已給藥，10-08公布三位青光眼受試者的早期觀察；此為公司披露，不是人體療效確證。肝、肌肉、皮層等逐器官論述與Altos候選藥物現況本輪未逐項核實，保留待核，不以企業人才名單代替療效證據。'),
('**缺口**全系統持續表達 OSKM 在小鼠身上的結局多半是畸胎瘤。人類在體再生目前僅見於器官層級的修復，不是斷肢重生，更不是「受創後變強」。',
 '**缺口（B05訂正）**體內重編程已有畸胎瘤及其他不良結果的動物研究，但不能在未定義劑量、組織、表達方式與研究母體時斷言「多半」。OSK與OSKM亦不可互換。表觀遺傳時鐘、損傷標誌或局部功能改善，均不能直接證明人體延壽、全身再生或受創後變強。ER-100的早期、小樣本、開放標籤公司觀察不足以確立療效與長期安全。'),
('美國 Life Biosciences 公布 ER-100 第一期臨床試驗初步數據：3 名青光眼受試者在給藥後第 56 日的安全觀察結果支持升高劑量，其中 2 人出現視野測試改善的初步訊號。',
 '依Life Biosciences於2026-10-08的公司公告，ER-100第一期開放標籤試驗三位開角型青光眼受試者於第56日有早期耐受性觀察，其中兩人出現視野測試改善訊號；公司稱資料安全監測委員會建議升高劑量。此處核對的是公司披露內容，未取得完整個體資料、對照結果或獨立重現，不能據此計算確定療效或認定長期安全。')]

def main():
    p=HERE/'正文修訂追溯_20261016.json';log=json.loads(p.read_text(encoding='utf-8'))
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md']:
        f=HERE/name;text=f.read_text(encoding='utf-8')
        for old,new in PAIRS:
            if old in text:
                log.append({'batch':'B05','as_of':'2026-10-16','file':name,'old':old,'new':new,'occurrences':text.count(old),'reason':'區分體外、動物、人體早期公司觀察及OSK/OSKM，撤回未核比例與時程'})
                text=text.replace(old,new)
        f.write_text(text,encoding='utf-8')
    p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=[
      ['RP01','https://www.frontiersin.org/journals/aging/articles/10.3389/fragi.2023.1323194/full','2024-01-23','ORIGINAL_RESULTS_AND_METHODS_CHECKED','MOUSE_DERIVED_CELLS_IN_VITRO','ERCC1研究：關鍵結果不可寫成整隻小鼠再生；卷年2023與上線日2024分開'],
      ['RP02','https://pubmed.ncbi.nlm.nih.gov/27984723/','2016','ORIGINAL_ABSTRACT_AND_FIGURE_CAPTIONS_CHECKED','PROGEROID_MOUSE','早衰模型壽命，非人體延壽；未核全部原始資料'],
      ['RP03','https://www.nature.com/articles/s41586-020-2975-4','2020','PUBLISHER_ABSTRACT_INDEX_CHECKED','MOUSE_RETINAL_GANGLION_CELLS','OSK三因子；直接全文讀取失敗，未重現'],
      ['RP04','https://pubmed.ncbi.nlm.nih.gov/24025773/','2013','ORIGINAL_ABSTRACT_CHECKED','MOUSE_IN_VIVO','多器官畸胎瘤實驗不能推出所有方案的發生率'],
      ['RP05','https://www.lifebiosciences.com/life-biosciences-announces-fda-clearance-of-ind-application-for-er-100-in-optic-neuropathies/','2026-01-28','SPONSOR_ANNOUNCEMENT_CHECKED','HUMAN_TRIAL_AUTHORIZATION_REPORTED','公司報告IND獲准；不是FDA原始決定或上市批准'],
      ['RP06','https://www.lifebiosciences.com/life-biosciences-announces-first-patient-dosed-in-phase-1-trial-of-er-100-for-optic-neuropathies/','2026-06-09','SPONSOR_ANNOUNCEMENT_CHECKED','FIRST_PARTICIPANT_DOSING_REPORTED','公告日不冒充實際給藥日'],
      ['RP07','https://www.lifebiosciences.com/life-biosciences-announces-first-in-human-data-from-ongoing-phase-1-trial-evaluating-er-100-in-optic-neuropathies/','2026-10-08','SPONSOR_INTERIM_DATA_ANNOUNCEMENT_CHECKED','HUMAN_PHASE1_OPEN_LABEL','三人第56日；兩人視野改善訊號，不是確證療效或長期安全'],
      ['RP08','https://clinicaltrials.gov/study/NCT07290244','','REGISTRY_ENTRY_NOT_SUBSTANTIVELY_RETRIEVED','REGISTRY_PENDING','頁面僅殼層，API失敗；試驗ID見公司公告，未獨立核登錄詳細內容']]
    keys=['id','url','source_date_or_year','access_depth','evidence_level','limitation']
    receipt={'batch':'B05','checked_as_of':'2026-10-16','experiment_run':False,'registry_details_verified':False,
             'sources':[dict(zip(keys,r)) for r in rows],'correction_records':sum(r.get('batch')=='B05' for r in log)}
    (HERE/'細胞重編程核查回執_B05_20261016.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    marker='## 第五輪續核 B05（2026-10-16）'
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md','諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md','交流科技三文件_查證交付說明_20261014.md','跨領域核查與修訂總覽_20261016.md']:
        f=HERE/name;text=f.read_text(encoding='utf-8')
        if marker not in text:f.write_text(text+'\n\n'+marker+'\n\n細胞重編程與ER-100的研究層級、來源日期及待核項目見[第五輪報告](續核來源與發現_B05_20261016.md)。體外指標、動物結果、公司人體早期公告與確證療效分開；未執行實驗，未取得試驗登錄詳細內容。\n',encoding='utf-8')
    print('B05: source-scoped corrections saved; registry detail review remains pending.')

if __name__=='__main__':main()
