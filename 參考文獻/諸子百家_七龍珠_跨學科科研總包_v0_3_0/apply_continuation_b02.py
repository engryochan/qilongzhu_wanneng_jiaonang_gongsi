"""Integrate the explicitly recorded second source-review batch; no network IO."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
UPDATES={
    '1':['INSTITUTIONAL_ABSTRACT_CHECKED','https://authors.library.caltech.edu/records/xzy5y-mpw80','1998','Caltech原作者庫摘要：活塞／圓筒水槽與DPIV，特定條件形成數約4，不是所有噴流的固定通則；未重算原始資料。'],
    '4':['PUBLISHER_INDEX_ABSTRACT_CHECKED','https://www.nature.com/articles/ncomms9661','2015-10-27','出版社索引核題名、作者及聲學全像摘要；正式頁重導失敗，未全文審閱，不能外推人體懸浮。'],
    '5':['PUBLISHER_INDEX_ABSTRACT_CHECKED','https://www.nature.com/articles/ncomms6033','2014-09-25','出版社索引摘要支持各向異性液晶、扭曲區域電荷分離及AC穩態流；限特定微尺度系統，正式頁未取得。'],
    '7':['PUBLISHER_INDEX_ABSTRACT_CHECKED','https://www.mdpi.com/2311-5521/9/12/290','2024-12-06','出版商索引題名作者摘要：零淨質量通量可傳動量但仍需驅動功率；Toronto／Concordia作者機構。不是獨立實驗。'],
    '42':['PUBLISHER_INDEX_ABSTRACT_CHECKED','https://pubmed.ncbi.nlm.nih.gov/42575228/','2026-08-10','PMID42575228、DOI10.1016/j.ctim.2026.103419；6項RCT共232人。疼痛SMD=-0.355、95%CI[-0.625,-0.084]；睡眠SMD=0.004、95%CI[-0.310,0.317]未顯著。兩終點證據確定性低；僅索引摘要，未重做統合分析。']
}

def main():
    p=HERE/'來源核查回執_20261016.json'
    receipt=json.loads(p.read_text(encoding='utf-8'))
    history=receipt.setdefault('superseded_checks_before_B02',{})
    for key,value in UPDATES.items():
        if key not in history:history[key]=receipt['checks'][key]
        receipt['checks'][key]=value
    receipt['latest_batch']='B02-2026-10-16'
    p.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sections={
        '神經網絡學_交流跨領域研究增訂_20261014.md':'''本輪核到Neuralink 21人為2026-01-28公司試驗入組說法；北腦40餘例在2026-08-13已有轉載公司人士的報導，不能只標為九月新數，更不能寫成獨立臨床登記。博睿康2026-03-13國家藥監局公告為特定手部抓握代償系統，含氣動手套及限定適應症，不是讀心或全身神經恢復批准。Meta Brain2Qwerty v2的9人、各10小時、61%詞準確率及最佳78%是主動打字MEG任務的官方研究報告，不是自由思想讀取。來源與日期逐項見[第二輪核查](續核來源與發現_B02_20261016.md)。

EV42現已由PubMed索引定位：疼痛與睡眠結果需分開，6項RCT共232人，睡眠未達統計顯著，兩終點證據確定性均低；來源摘要不構成臨床確證。''',
        '諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md':'''人物表新增37列部分來源核對，包含4位華夏科研人物、機構人物頁、原論文作者與官方授獎資料；SCI-0063僅英文署名可追溯，中文身份關聯未升格。其餘108列仍待逐人外部核驗，全部145列國籍與完整履歷均未宣稱完成。

思想表以漢書卷三十核對「諸子略十類」與編輯擴充四類；兵書、術數、方技分列於原典，工藝博物屬本研究擴充。這不驗證每位代表人物、原典官職起源說或全部著作歸屬。沈括、宋應星等後世人物不可混列為春秋戰國同時代人物。詳見[第二輪核查](續核來源與發現_B02_20261016.md)。''',
        '七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md':'''EV04聲學全像、EV05液晶電滲、EV07合成射流綜述已補到出版商索引摘要層。聲學操控不能擴成任意人體懸浮，液晶微流體不能無條件外推人體循環，零淨質量通量不等於零能耗。神經能力對照新增Meta主動打字MEG與博睿康抓握代償的任務邊界；所有原作級能力仍按110項表逐項等待原作定位與直接實證。來源見[第二輪核查](續核來源與發現_B02_20261016.md)。''',
        '交流科技三文件_查證交付說明_20261014.md':'''第二輪補查五列核心來源（含EV01作者機構庫），並核到四筆舊失敗來源的出版商／PubMed索引摘要。失敗數降為零只表示「無資料」狀態已解除，不表示所有來源全文與全部主張皆已核實。人物名冊37列具有部分來源核對，其餘108列未核；資料與書目日期均保留原時點，不冒充最新總量。現行統計及雜湊請用最新生成檔。'''
    }
    marker='## 第二輪續核 B02（2026-10-16）'
    for name,section in sections.items():
        p=HERE/name;text=p.read_text(encoding='utf-8')
        if marker not in text:p.write_text(text+'\n\n'+marker+'\n\n'+section+'\n',encoding='utf-8')
    # Correct a second high-impact historical paragraph without discarding it.
    p=HERE/'七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md'
    text=p.read_text(encoding='utf-8')
    import re
    log_path=HERE/'正文修訂追溯_20261016.json'
    log=json.loads(log_path.read_text(encoding='utf-8'))
    m=re.search(r'\*\*現實\*\*兩條路並行。[^\n]+',text)
    if m:
        replacement='**現實（B02訂正）**矽基人工神經網絡與培養神經元—晶片系統是不同研究路線。Cortical Labs的CL1官方產品及[Python API文件](https://docs.corticallabs.com/)支持培養神經元的讀取、刺激與閉環研究介面；FinalSpark的[Neuroplatform](https://finalspark.com/neuroplatform/)官方頁列共享／獨享類器官遠端研究服務，現行定價為聯絡詢價。本輪未核定原稿CL1三萬五千美元、二十萬至八十萬細胞、Doom示範日期、120／千模組部署或FinalSpark每月約一千美元等數據。它們保留於修訂追溯記錄，不能混入已核欄位。'
        log.append({'file':p.name,'as_of':'2026-10-16','batch':'B02','old':m[0],'new':replacement,'reason':'把已定位功能與未核價格／規模分開；現行定價不可沿用歷史傳聞'})
        text=text[:m.start()]+replacement+text[m.end():]
    old='濕件目前只做到儲備池運算等級的任務，與矽基模型不在同一能力量級；賣點是功耗，不是智能。'
    new='本包尚無同口徑任務、全系統能耗及統計比較，不能斷言所有濕件「只做到儲備池運算」或在一般能力上優於矽基。需記錄培養維持與外部計算能耗、任務基線、重複性及模型適用範圍。'
    if old in text:
        log.append({'file':p.name,'as_of':'2026-10-16','batch':'B02','old':old,'new':new,'reason':'未提供支持一概能力排名的比較母體'})
        text=text.replace(old,new)
    old='每小時25美元、Optimus千台、Unitree出貨量及全球在役總數，本輪未逐條取得可比的一手依據，暫不採為結論。'
    new='宇樹2026-01-22官方公告稱2025純人形機器人向終端實售交付逾5500台、產出逾6500台，兩者不得混計。每小時25美元、Optimus千台及全球在役總數仍未核定；Tesla七月報告的安裝產線及預計投產亦不能當成實際部署量。詳見補充事實核查B02表。'
    if old in text:
        log.append({'file':p.name,'as_of':'2026-10-16','batch':'B02','old':old,'new':new,'reason':'新增宇樹一手公告及Tesla七月報告，按資料時點及口徑回填'})
        text=text.replace(old,new)
    p.write_text(text,encoding='utf-8')
    log_path.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p=HERE/'跨領域核查與修訂總覽_20261016.md'
    text=p.read_text(encoding='utf-8')
    text=text.replace('1. `SOURCE_UNAVAILABLE`四列及全文未取得的光學、器官晶片和臨床綜述；核題名、年份、作者歸屬、是否更正／撤稿、研究設計及原始數值。',
        '1. 原四列`SOURCE_UNAVAILABLE`在B02已補到出版商／PubMed索引摘要層；光學、器官晶片和臨床綜述等尚需全文、原始數值及更正／撤稿查核，不能據此宣稱全數已驗證。')
    if marker not in text:
        text+='\n\n'+marker+'\n\n新增五列來源進展、37位人物的部分來源核對、十四類分類的原典層區分，及四項腦機介面資料時點核查。詳見[第二輪續核](續核來源與發現_B02_20261016.md)。未核部分仍保留待核標記；37位人物並非完整身份或全部研究已驗證。\n'
    p.write_text(text,encoding='utf-8')

if __name__=='__main__':main()
