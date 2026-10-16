"""Replay B04 source-scoped manuscript corrections; no model code is executed."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
REPORT='續核來源與發現_B04_20261016.md'
PAIRS=[
('**現實**這是今天最廉價的真實超能力：模型合併。任務向量算術（Task Arithmetic）、TIES-Merging、DARE、演化式合併、KnOTS 正交分解，全部開源，程序包 mergekit 即可跑，在權重空間直接把多個微調模型合成一個，推理成本不變。',
 '**現實（B04訂正）**模型合併可作為「融合」的計算研究類比。mergekit提供多種權重合併工具；不能據此保證所有列名方法均內建、所有模型相容或能力相加。同形狀的稠密權重合併通常不增加參數張量形狀，但端到端延遲、記憶體及能耗仍須在固定硬體與推理設定下量測；MoE、層拼接及詞彙擴充另核。開源工具不等於零成本或模型授權可任意組合。'),
('**鐵律**合併不是免費午餐。一項系統性評測（arXiv 2511.21437）發現多數子空間合併法在大語言模型上基本失效，六法之中只有最老最簡單的任務向量算術站得住；合併數量從 2 增至 8 時災難性干擾急升，需 KnOTS 一類正交化才壓得下。合體有代價，原作沒騙人。',
 '**研究範圍（B04訂正）**arXiv:2511.21437v2在共用基座的異質微調檢查點設定下比較六法：Task Arithmetic、TIES-Merging、Model Stock、TSV-M、Iso-C及Subspace Boosting；作者報告其中Task Arithmetic最穩定獲益，不能外推為其他設定下所有方法均失效。KnOTS未列入這六種受測方法，不能用此文支持「必須用KnOTS才能抑制干擾」。KnOTS另見ICLR 2025原研究，主要處理LoRA更新對齊；本包未在本機重現兩篇研究。'),
('1. **融合（A，零成本）**模型合併是唯一一項開源程序包今天就能完整復現的「超能力」。從任務向量算術起步，別一上來堆六種子空間法——評測顯示最老的那個反而最穩。',
 '1. **融合類比：模型合併（研究候選）**先檢查基座、張量、tokenizer及模型使用條件，再以未合併基座、單一專家與簡單合併作基線；記錄精度、任務回歸、延遲、記憶體及能耗。本包未執行模型合併，不標為零成本、完整復現或原作能力實現。'),
('最值得注意的反而是沒人當成超能力的那兩項：**精神時光屋**與**融合**。它們在今天不但實現了，而且是當前 AI 工程最便宜、最可復現的兩條路——一個叫並行仿真訓練，一個叫模型合併。這兩條，個人與小機構就能跑。',
 '**精神時光屋**與**融合**可分別啟發並行仿真與模型合併。這些是功能類比；本包未建立最便宜的比較，也未量測個人設備可行性，不視為原作物理效果已實現。'),
('第一，**融合與精神時光屋是整張表裡唯二個人就能完整復現的超能力**——mergekit 與並行仿真訓練，今天開源可跑，成本只有 GPU；而且原作「合體有代價」是對的，arXiv 2511.21437 的系統性評測發現多數子空間合併法在大語言模型上基本失效，只有最老最簡單的任務向量算術站得住。',
 '第一，模型合併與並行仿真是研究類比；開源可取得不代表原作超能力可完整復現，也未建立「唯二」或「成本只有GPU」的比較。arXiv:2511.21437v2的結果限於其共用基座、異質檢查點及既定評測設定，詳見本包B04續核。')]

def main():
    logpath=HERE/'正文修訂追溯_20261016.json'
    log=json.loads(logpath.read_text(encoding='utf-8'))
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md']:
        p=HERE/name;t=p.read_text(encoding='utf-8')
        for old,new in PAIRS:
            if old in t:
                log.append({'file':name,'as_of':'2026-10-16','batch':'B04','old':old,'new':new,'occurrences':t.count(old),'reason':'區分不同論文受測方法與適用範圍，撤回未實測成本及原作能力外推'})
                t=t.replace(old,new)
        p.write_text(t,encoding='utf-8')
    logpath.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sources=[
      ['MM01','https://arxiv.org/html/2511.21437v2','ORIGINAL_METHODS_AND_CONCLUSIONS_CHECKED','2026-03-29','MERGEVAL','研究範圍及六法清單；未重算實驗'],
      ['MM02','https://proceedings.iclr.cc/paper_files/paper/2025/hash/0d4f8a5109c5083b5307fcd0bddae7a7-Abstract-Conference.html','CONFERENCE_ABSTRACT_CHECKED','2025','KNOTS','LoRA更新對齊；未重查全部資料'],
      ['MM03','https://arxiv.org/html/2403.13257v3','TOOL_PAPER_DESCRIPTION_CHECKED','','MERGEKIT','工具架構描述；不是本機實測'],
      ['MM04','https://arxiv.org/html/2603.09938v2','SURVEY_TAXONOMY_CHECKED','2026-03-30','FUSE_SURVEY','綜述分類；未逐條核引文'],
      ['MM05','https://github.com/arcee-ai/mergekit','MAINTAINER_DOCUMENTATION_CHECKED','','MERGEKIT','浮動倉庫，未固定commit，未安裝或執行']]
    keys=['id','url','access_depth','source_version_date_or_year','project_group','limitation']
    receipt={'batch':'B04','checked_as_of':'2026-10-16','model_experiment_run':False,
             'sources':[dict(zip(keys,row)) for row in sources],
             'project_groups_are_not_independent_studies':True,
             'correction_records':sum(r.get('batch')=='B04' for r in log)}
    (HERE/'模型合併核查回執_B04_20261016.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    marker='## 第四輪續核 B04（2026-10-16）'
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md','諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md','交流科技三文件_查證交付說明_20261014.md','跨領域核查與修訂總覽_20261016.md']:
        p=HERE/name;t=p.read_text(encoding='utf-8')
        if marker not in t:p.write_text(t+'\n\n'+marker+'\n\n模型合併論文與工具的限定核查見[第四輪續核]('+REPORT+')。撤回把KnOTS列為另一篇評測必需解法，以及零成本、推理成本必然不變、原作能力完整復現等推論；未下載權重或執行模型實驗。\n',encoding='utf-8')
    print('B04 manuscript source-scope corrections applied; no model experiment run.')

if __name__=='__main__':main()
