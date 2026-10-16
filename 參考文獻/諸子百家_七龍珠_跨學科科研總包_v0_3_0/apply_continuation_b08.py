"""Replay B08 source checks; classical ideal-state algebra is verified separately."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PAIRS=[
('**現實**量子隱形傳態傳的是**量子態**，不是物質，而且必須配一條經典信道傳兩位元，因此不超光速。傳態成功的門檻是保真度超過經典極限 1/2，超過無複製極限 2/3 才算進入真正的量子區；原粒子在過程中必被摧毀，這正是它不違反無複製定理的原因。',
 '**現實（B08訂正）**量子傳態傳送量子資訊，不是將原物質搬到接收端。標準單qubit協議使用共享糾纏及兩個經典位元；不能將此資源計數套到所有連續變量或高維協議。保真度基準取決於輸入態集合、先驗、維度及評估方式；相干態研究的1/2及其無複製基準2/3不是所有傳態的統一門檻。測量改變原輸入態，並非原粒子在每種實作中都必然被物理摧毀；也沒有留下任意未知態的完美第二份副本。'),
('**缺口**宏觀物體的完整量子態無法測量、無法儲存、無法重建。這不是工程問題。',
 '**缺口（B08訂正）**本包沒有原作級人體或物質瞬移的可重複實證。不能把任意未知量子態的完美複製限制，直接改寫成所有宏觀態皆不可儲存或所有物質運輸均被禁止。量子傳態也不要求先將未知態完整讀成經典描述；其糾纏資源、經典通訊及實作誤差須分別核對。宏觀可行性未由這些小系統研究建立。')]

def main():
    p=HERE/'正文修訂追溯_20261016.json';log=json.loads(p.read_text(encoding='utf-8'))
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md']:
        f=HERE/name;t=f.read_text(encoding='utf-8')
        for old,new in PAIRS:
            if old in t:
                log.append({'batch':'B08','as_of':'2026-10-16','file':name,'old':old,'new':new,'occurrences':t.count(old),'reason':'區分協議、輸入態集合、保真度基準與粒子／量子態，限制宏觀外推'})
                t=t.replace(old,new)
        f.write_text(t,encoding='utf-8')
    p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=[
      ['QT01','https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation','OFFICIAL_PROTOCOL_AND_ALGEBRA_CHECKED','SINGLE_QUBIT_IDEAL_PROTOCOL','兩經典位元與一糾纏對；不代表所有傳態協議或硬體實測'],
      ['QT02','https://arxiv.org/abs/quant-ph/0501086','AUTHOR_ABSTRACT_CHECKED','CONTINUOUS_VARIABLE_COHERENT_STATE','相干態無複製基準2/3；未核全部實驗資料'],
      ['QT03','https://pmc.ncbi.nlm.nih.gov/articles/PMC8694421/','ORIGINAL_ABSTRACT_AND_INTRODUCTION_CHECKED','PROPAGATING_COHERENT_MICROWAVE','原文分開相干態與qubit基準；未重算保真度或驗證裝置'],
      ['QT04','https://www.nature.com/articles/299802a0','PUBLISHER_BIBLIOGRAPHY_CHECKED','NO_CLONING_ORIGINAL_REFERENCE','1982書目可核；本輪未通讀原論文，定理說明另依QT01']]
    keys=['id','url','access_depth','scope','limitation']
    receipt={'batch':'B08','checked_as_of':'2026-10-16','quantum_hardware_run':False,'physical_teleportation_run':False,
             'local_check_scope':'IDEAL_CLASSICAL_STATEVECTOR_ALGEBRA_ONLY',
             'sources':[dict(zip(keys,r)) for r in rows],'correction_records':sum(r.get('batch')=='B08' for r in log)}
    (HERE/'量子傳態核查回執_B08_20261016.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    marker='## 第八輪續核 B08（2026-10-16）'
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md','諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md','交流科技三文件_查證交付說明_20261014.md','跨領域核查與修訂總覽_20261016.md']:
        f=HERE/name;t=f.read_text(encoding='utf-8')
        if marker not in t:f.write_text(t+'\n\n'+marker+'\n\n量子傳態的協議與保真度口徑見[第八輪報告](續核來源與發現_B08_20261016.md)。修正粒子必被摧毀及通用保真度門檻的說法；本地只檢查理想協議代數，未測量子硬體或物質瞬移。\n',encoding='utf-8')
    print('B08 source-scope corrections saved; no quantum hardware run.')

if __name__=='__main__':main()
