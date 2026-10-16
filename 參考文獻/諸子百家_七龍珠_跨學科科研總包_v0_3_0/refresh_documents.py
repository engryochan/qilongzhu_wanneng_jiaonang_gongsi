"""Apply documented local corrections and refresh current delivery metadata."""
from pathlib import Path
import csv, hashlib, json, re

HERE=Path(__file__).resolve().parent
DATE='2026-10-16'
INDEX='跨領域核查與修訂總覽_20261016.md'
MARKER='<!-- audit-20261016 -->'
NOTICE=f'''{MARKER}
> **2026-10-16 核查增訂**：本文件包含歷史研究及多模型對話。請先讀[跨領域核查與修訂總覽]({INDEX})；目前有效的來源核查深度、日期及去重以本包CSV的`audit_status`、`audit_note`及`source_group_id`為準。未逐條核對的舊數字與「已核實／永久封死／世界最頂尖」等措辭不作現行結論。已完成文件掃描，不等於所有事實皆已查證。

'''

def main():
    log=[]
    oldlog=HERE/'正文修訂追溯_20261016.json'
    if oldlog.exists(): log=json.loads(oldlog.read_text(encoding='utf-8'))
    paths=[p for p in HERE.glob('*.md') if p.name != INDEX and not p.name.startswith('README')]
    for p in paths:
        text=p.read_text(encoding='utf-8-sig')
        if MARKER not in text:
            pos=0
            if text.startswith('---\n'):
                end=text.find('\n---',4)
                if end >= 0: pos=text.find('\n',end+1)+1
            text=text[:pos]+'\n'+NOTICE+text[pos:]
        if p.name.startswith('七龍珠能力技術對照冊'):
            replacements=[
                ('逐項查證：天下現役最頂尖的公司、軍團、研究所、論文與程序包，究竟能把哪幾項「超能力」做出來、做到幾成、哪幾項被物理學永久封死。每一條都標明證據與缺口，不標明的一律不寫。',
                 '研究對照：將原作能力拆為可量測效果，分開登錄功能類比、工程原型、理論模型及未證實主張。候選企業、研究所與程序包不代表已完成全球排名或逐條查證；現行查證深度見本包證據表。'),
                ('把「超能力」拆成**效果**而非**機制**之後，絕大多數紅緞帶軍團的能力在 2026 年已經有人在工廠裡、戰場上或實驗室裡跑起來了——只是功率來自燃氣輪機與氮化鎵放大器，不是丹田。',
                 '部分原作能力可以找到機器人、感測、模擬或生物醫學的功能類比。類比不證明原作能力已實現，亦未有可計算的母體支持「絕大多數已實現」之比例判斷。'),
                ('真正被封死的只有四樣：**物質瞬間轉移**、**時光機**、**萬能膠囊的物質壓縮**、**無接觸念力**。前三樣撞的是無複製定理、時序保護與費米簡並壓力；最後一樣撞的是四十年受控實驗的空集合——1995 年 CIA 內部備忘錄的原話是遙視的論據「幾近不存在」。',
                 '物質瞬移、回到過去、原作萬能膠囊壓縮與無裝置念力，本包尚未提供可重複的原作級實證。不得把缺乏證據、工程尺度限制、特定定理與未獲普遍證明的猜想合併成「只有四樣永久不可能」。無複製定理限制任意未知量子態的完美複製，不是所有物質運輸或壓縮情形的通用否定。量子傳態需共享糾纏及經典通訊，傳送的是量子資訊：[IBM官方教材](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation)。遙視研究也不能直接代替物理念力的實驗定義。'),
                ('最值得注意的反而是沒人當成超能力的那兩項：**精神時光屋**與**融合**。它們在今天不但實現了，而且是當前 AI 工程最便宜、最可復現的兩條路——一個叫並行仿真訓練，一個叫模型合併。這兩條，個人與小機構就能跑。',
                 '**精神時光屋**可啟發並行仿真訓練，**融合**可啟發模型合併；這是研究類比，不是原作物理效果實現，也未建立「最便宜」的成本比較。mergekit等工具的實際能力取決於基座相容性、資料、硬體及評測。'),
                ('投入再多資源也不會發生','只有在明確定理、假設及適用範圍支持時才能標為理論禁止；其餘分列未證實或工程受限')]
            for old,new in replacements:
                if old in text:
                    log.append({'file':p.name,'as_of':DATE,'old':old,'new':new,'reason':'避免將類比、缺乏證據與理論禁止混為一談'})
                    text=text.replace(old,new)
            pattern=r'\*\*現實\*\*2026 年人形機器人已從展演進入計費作業。[^\n]+'
            m=re.search(pattern,text)
            if m:
                new='**現實（2026-10-16訂正）**Figure官方2025-11-19報告的11個月、30,000輛以上BMW X3生產協作，對象是Figure 02；Figure 03在2026-06-30另有到Spartanburg的公告。BMW Leipzig使用Hexagon AEON，不能寫成Figure 03由美國同案擴展。每小時25美元、Optimus千台、Unitree出貨量及全球在役總數，本輪未逐條取得可比的一手依據，暫不採為結論。[Figure 02](https://www.figure.ai/news/production-at-bmw)；[Figure 03](https://www.figure.ai/news/f-03-at-bmw)；[BMW](https://www.bmwgroup.com/en/news/general/2026/humanoid-robot-in-leipzig.html)。'
                log.append({'file':p.name,'as_of':DATE,'old':m[0],'new':new,'reason':'機型、工廠與時間線混用；缺來源數字保留於追溯表待核'})
                text=text[:m.start()]+new+text[m.end():]
        text=re.sub(r'(\| \[EV23\]\([^\n]+?\) \| )2025( \|)',r'\g<1>2024\2',text)
        appendix='\n\n## 2026-10-16 本文件專項補強\n\n'
        if appendix not in text:
            if p.name.startswith('神經網絡學'):
                text+=appendix+'''神經與臨床採信分三層：訊號／同步效果、功能或認知效果、疾病治療效果。EV20的11位癲癇受試者及490接點屬生理訊號證據；不能把接點當作樣本數或把同步當作阿茲海默症療效。EV21／41是同一縱向研究的兩個入口，14人入組、11人完成三月、6人延續至六月；失訪與缺乏大型對照限制必須保留。EV40／59的單次光聲刺激未見認知增益，不等於所有長期方案均無效。EV56有n=15的先導對照研究，但不能當作大型確證試驗。

腦脊髓橋接EV26為植入式個案；BrainNet EV25傳遞的是限定任務決策，並不支持任意讀心。每筆後續神經研究須分列受試者、電極／接點、試次、訓練與測試拆分、假陽性、帶寬、延遲及外部校準。歷史例數、國內器械批准與Meta相關性能數字本輪尚未逐條重驗，仍是待核素材。來源及支持範圍見60列證據表和核查回執。
'''
            elif p.name.startswith('諸子百家_寰宇'):
                text+=appendix+'''已從本專案v0.1.0原始CSV對賬並補入110技能、145人物、14類思想的完整種子表，分別保留ID、原資料位置與SHA-256。這解決了清單缺席，不代表完成逐項外部核實。145名人物仍需逐人官方身份／史料與代表論文；地理關聯不得回填為法定國籍。14類分類包含擴展研究門類，不等同14個《漢書》九流十家。

110技能新增逐類建議的可量測指標、研究族與候選證據入口，全部明示為PROPOSED_CATEGORY_ANALOGY_NOT_ABILITY_VALIDATION。原作章回、版本連續性和直接能力證據仍待逐項補充。科學類比不可用於把模擬、物理工程與原作效果合併。

跨尺度審核擴至社會人類分類、物種與細胞、粒子與量子、元宇宙及行星內部。參見核查總覽的領域矩陣與計量口徑；宇宙尺度、機構所有制及各行各業完整覆蓋仍未具備可驗收母體，不作完成宣告。
'''
            elif p.name.startswith('七龍珠能力'):
                text+=appendix+'''原26項敘述與110項種子不同粒度；後者現已完整納入本包，不能沿用「本地未有110項清單」。新增表保留每項的原作定位空缺與待核狀態，給出研究方向、量測指標與候選文獻，不代表逐項能力已實現。

本輪明確訂正Figure 02／03及BMW工廠混用，並撤回「只有四樣被永久封死」「絕大多數已實現」「模型合併就是原作融合」等無充分比較或定理支持的裁決。完整原句及訂正保留在正文修訂追溯JSON。其餘歷史正文內價格、出貨、部署量、CL1／FinalSpark、再生及前沿排名，未獲本輪逐條來源支持者均維持待核，不因A／B／C／D舊標籤而升格。
'''
            elif p.name.startswith('交流科技三文件'):
                text+=appendix+'''本輪實際交付以README、核查回執及本輪統計為準；前文「共10檔」「35筆」「完整ZIP CRC PASS」「前綴未變」屬歷史交付敘述。現有60個唯一證據ID保留，新增核查與分組欄位；CSV欄位修改及正文訂正使歷史雜湊不再是現行雜湊。當前全部文件雜湊另存獨立manifest。

110技能、145人物及14思想分類原始表已在本專案找到並完整對賬；本包新表是待核名冊，不是全體內容已查證證書。現行SOURCE_UNAVAILABLE列及索引／入口層查核不能寫成全文審閱或獨立復現。
'''
        (p).write_text(text,encoding='utf-8')
    oldlog.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    readme=HERE/'README_跨領域交流科技_v0_3_0.md'
    readme.write_text('''# 研究封包 v0.3.0 · 2026-10-16 核查增訂

請先讀[跨領域核查與修訂總覽](跨領域核查與修訂總覽_20261016.md)。本包已完成全專案文件盤點與文字掃描，並核對核心來源；**尚非全專案所有事實均已外部核實**。

最新進度見[續核來源與發現B08](續核來源與發現_B08_20261016.md)：校正量子傳態的保真度門檻與粒子／量子態混用，新增理想協議的本地線性代數檢查；未使用量子硬體。[第七輪B07](續核來源與發現_B07_20261016.md)區分遙視研究與情報用途；此前報告保留當輪歷史進度。人物進度仍為49列限定來源核對、96列未外部核查。

- 三份主文保留研究脈絡，對高影響錯誤作明示修訂，原文變更保留在`正文修訂追溯_20261016.json`。歷史「前綴完全不變」只描述舊交付，不再作現行保證。
- 原60筆證據逐列分開記錄來源日期、核查日期、核查深度及來源群；來源群不是獨立研究數。取不到正文、僅索引或僅入口者明確標記。
- 新納入110項技能、145位人物與14類思想的完整本地種子；行數與ID已對賬，內容逐項外部查證仍待完成。
- 組件表分開官方版本、入口、硬體類別及本機測試；機構表分開研究關聯、法律身份、所有制與所在地。
- `來源核查回執_20261016.json`記錄實際來源與核查範圍；`本輪核查統計_20261016.json`記錄計數。
- `專案文件掃描_20261016.csv`記錄逐檔雜湊；`全專案待核斷言_20261016.csv`是候選行索引，並非已驗證斷言名冊。
- `交流跨領域科研_增訂審核清單_20261014.json`保留歷史欄位與現行核查說明；現行文件雜湊請用`交付現況_SHA256_20261016.csv`。

## 重現本地檢查

使用Python 3.11以上，從本資料夾執行：

```text
python apply_continuation_b02.py
python apply_continuation_b03.py
python apply_continuation_b04.py
python apply_continuation_b05.py
python apply_continuation_b06.py
python apply_continuation_b07.py
python apply_continuation_b08.py
python integrate_audit.py
python refresh_documents.py
python audit_project.py
python audit_project.py --manifest
python verify_package.py
```

前九步是回填保存的人工查證回執與正文訂正，不會重新上網或產生新的實驗證據。verify_package另執行明確標示的理想協議代數檢查，不是量子硬體測試。渲染報告後須重建校驗清單。不要以執行日期冒充來源查證更新日期。
''',encoding='utf-8')
    p=HERE/'交流跨領域科研_增訂審核清單_20261014.json'
    j=json.loads(p.read_text(encoding='utf-8-sig'))
    if 'historical_delivery_claims' not in j:
        keys=['source_files_sha256','current_files_before_audit_refresh','qa_checks','main_docs_immutability']
        j['historical_delivery_claims']={k:j.pop(k) for k in keys if k in j}
    j['as_of']=DATE
    j['scope_limit']='全專案文字掃描與核心來源分級完成；尚未逐條核實所有歷史事實、人物或原作能力。'
    j['current_verification']={'source_receipt':'來源核查回執_20261016.json','counts':'本輪核查統計_20261016.json',
        'manifest':'交付現況_SHA256_20261016.csv','manifest_excludes_itself':True,
        'historical_zip_not_reverified':True,'full_semantic_fact_verification':False,
        'main_docs_exact_prefix_preserved_this_revision':False,'raw_source_versions_untouched':True}
    p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Updated {len(paths)+2} documents; {len(log)} traceable textual corrections')

if __name__=='__main__': main()
