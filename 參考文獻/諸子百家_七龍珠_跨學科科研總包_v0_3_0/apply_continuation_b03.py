"""Replay saved B03 source checks; no network, experiments or new verification."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def main():
    path=HERE/'人物核查回執_20261016.json'
    receipt=json.loads(path.read_text(encoding='utf-8'))
    sources={
      'P26':['https://catalogue.museogalileo.it/indepth/GravitationalAcceleration.html','MUSEUM_TEXT_CHECKED','伽利略博物館：落體與斜面；不是現代無限條件普適實驗'],
      'P27':['https://newtonproject.ox.ac.uk/texts/introduction','UNIVERSITY_EDITORIAL_TEXT_CHECKED','牛頓文稿編輯計畫，De motu與Principia形成史；未逐卷核原作'],
      'P28':['https://www.nature.com/articles/318419a0','PUBLISHER_METADATA_ONLY','Shawn Carlson，Nature 318,419–425(1985)，DOI10.1038/318419a0；沒有可讀摘要'],
      'P29':['https://www.susanblackmore.uk/biography/','AUTHOR_SELF_DESCRIPTION_CHECKED','本人自述研究轉向；不當作獨立履歷或超常現象裁決'],
      'P30':['https://www.herts.ac.uk/research/centres/psychology/behaviour-change-in-health-and-business/public-understanding-of-psychology','INSTITUTIONAL_TEXT_CHECKED','Richard Wiseman，大眾參與心理學研究；未逐項驗證實驗結論'],
      'P31':['https://www.gold.ac.uk/psychology/staff/french/','INSTITUTIONAL_INDEX_CHECKED','Christopher French，異常心理學；頁面直接讀取失敗，使用校方索引'],
      'P32':['https://www.sheldrake.org/research/morphic-resonance','PROPONENT_TEXT_AND_HOSTED_COUNTERARGUMENT_CHECKED','Rupert Sheldrake假說與其網站所收Steven Rose反駁；相反詮釋非獨立重現'],
      'P33':['https://www.lse.ac.uk/philosophy/research/sir-karl-popper','INSTITUTIONAL_TEXT_CHECKED','Karl Popper與可證偽性；未通讀全部原著'],
      'P34':['https://news.mit.edu/1996/kuhn','INSTITUTIONAL_HISTORICAL_TEXT_CHECKED','Thomas Kuhn，1962科學革命的結構；歷史訃告非現任名單'],
      'P35':['https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124','ORIGINAL_ARTICLE_TEXT_CHECKED','John P. A. Ioannidis 2005條件式模型，非全球論文真偽普查'],
      'P36':['https://liberalarts.vt.edu/departments-and-schools/department-of-philosophy/faculty/deborah-mayo.html-.html','INSTITUTIONAL_TEXT_CHECKED','Deborah Mayo，統計哲學與推論；校方頁面稱emerita'],
      'P37':['https://www.cambridge.org/core/books/statistical-inference-as-severe-testing/D9DF409EF568090F3F60407FF2B973B2','PUBLISHER_DESCRIPTION_AND_METADATA_CHECKED','Mayo 2018嚴格檢驗著作與書介；未取得全書'],
      'P38':['https://www.dpmms.cam.ac.uk/~ds28/','UNIVERSITY_HOSTED_AUTHOR_TEXT_CHECKED','David Spiegelhalter，不確定性與風險溝通；本人頁面稱emeritus'],
      'P39':['https://www.spr.ac.uk/about-spr','ORGANIZATION_SELF_DESCRIPTION_CHECKED','SPR不持機構統一立場；會員資格不等同接受超常現象真實性']}
    checks={
      'SCI-0001':['P26','Galileo Galilei：博物館記述落體速度隨時間及由靜止位移隨時間平方的關係；需保留重力及阻力條件。'],
      'SCI-0002':['P27','Isaac Newton：編輯計畫說明運動定律雛形與萬有引力的發展；不是當代所有尺度均適用的保證。'],
      'SCI-0135':['P28','Shawn Carlson：1985占星雙盲論文作者與書目已核；本輪僅出版頁書目，未重算原始資料，不由題名推定全部結果。'],
      'SCI-0136':['P29','Susan Blackmore：本人自述曾研究超心理學，後轉向意識研究；個人未找到有說服力證據，不等於證明所有可能現象不存在。'],
      'SCI-0137':['P30','Richard Wiseman：校方列大眾參與心理學實驗與科普；本輪未逐項核其超常主張實驗。'],
      'SCI-0138':['P31','Christopher French：校方索引可支持異常心理學、超常信念及體驗研究；不是已證明超能力存在。'],
      'SCI-0139':['P32','Rupert Sheldrake：可追溯形態共振假說及與Steven Rose的相反詮釋；僅核提出與爭論存在，不採信超常機制成立。'],
      'SCI-0140':['P33','Karl Popper：LSE紀念頁將可證偽性列為其科學劃界主張；可檢驗不等於已證實，未通讀原著。'],
      'SCI-0141':['P34','Thomas Kuhn：MIT歷史資料確認1962著作與科學變遷研究；範式轉移不替代特定假說所需實證。'],
      'SCI-0142':['P35','John P. A. Ioannidis：2005原文建模統計功效、研究前勝算及偏誤對陽性預測值的影響；非實測全球過半論文為假。'],
      'SCI-0143':['P36;P37','Deborah G. Mayo：統計哲學及嚴格檢驗著作；書介層，不宣稱通讀全書或方法普遍優於其他方法。'],
      'SCI-0144':['P38','David Spiegelhalter：大學網域本人頁支持不確定性、風險及統計溝通方向；完整履歷與法定國籍未核。']}
    receipt['sources'].update(sources)
    receipt['checks'].update(checks)
    receipt['latest_batch']='B03_20261016'
    path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    marker='## 第三輪續核 B03（2026-10-16）'
    note='本輪補查方法論與異常現象研究十位人物，以及伽利略、牛頓兩位歷史人物；人物表累計49列有範圍受限的來源核對，96列仍未外部核查。書目、本人陳述、機構介紹、原文模型及獨立重現分開記錄。詳見[第三輪核查與研究驗證規程](續核來源與發現_B03_20261016.md)。'
    for name in ['諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md','七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md','交流科技三文件_查證交付說明_20261014.md','跨領域核查與修訂總覽_20261016.md']:
        p=HERE/name;text=p.read_text(encoding='utf-8')
        if marker not in text:p.write_text(text+'\n\n'+marker+'\n\n'+note+'\n',encoding='utf-8')
    print('B03: 12 additional limited person checks saved; 49 total, 96 pending.')

if __name__=='__main__':main()
