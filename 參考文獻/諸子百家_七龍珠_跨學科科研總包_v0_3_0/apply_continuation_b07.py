"""Replay B07 remote-viewing scope checks; no paranormal experiment performed."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PAIRS=[
('**最高規格的檢驗**美國政府從 1975 到 1995 年投入約兩千萬美元運行 Stargate 計劃（前身包括 Grill Flame、Sun Streak、SCANATE），由陸軍情報與安全司令部、國防情報局先後主管，最後移交 CIA。1995 年 CIA 委託美國研究院（AIR）做回溯評估。',
 '**歷史研究（B07訂正）**CIA官方2021回顧及AIR 1995報告可追溯政府遙視研究與情報應用評估。正文原列的精確起訖、總支出及各代號沿革尚未逐項核對，不沿用為確定數字，也不稱為已建立跨研究比較的「最高規格」。AIR英文全名為American Institutes for Research。'),
('**結論**AIR 的原文是：遙視提供的資訊「模糊而歧義，難以甚至不可能產出足夠品質與準確度的可行動情報」；且「仍不清楚遙視這一超常現象的存在是否已被證實」。CIA 內部備忘錄更直白：按科學與超心理學兩套標準衡量，遙視的論據「不只是很弱，而是幾近不存在」。計劃當年終止並解密。普林斯頓 PEAR 實驗室於 2007 年關閉。',
 '**結論範圍（B07訂正）**AIR 1995-09-29報告執行摘要記載受評實驗有統計偏離，但未能清楚確立其超常成因；情報應用缺少足夠具體、可靠及可行動的資訊，因此不建議繼續此情報用途。這是轉述，不是逐字引語。CIA備忘錄的「幾近不存在」本輪未取得原件核字，撤回確定引語。PEAR的2006校友刊物預告關閉，本輪未取得關閉聲明原件；機構是否結束亦不能直接證明所有相關現象成立或不存在。'),
('第二，**超能力團體那一項不是「尚未證實」，是已經測完了**：Stargate 跑了二十年、兩千萬美元，CIA 內部備忘錄原話是遙視的論據「幾近不存在」。',
 '第二，AIR對特定遙視研究及情報用途的評估不能替代所有念力、特異功能或相關團體的逐項檢驗；支出、歷史年數及未取得的備忘錄引語維持待核。當前採信範圍見本包B07續核。'),
('- **物理禁止（D，6 項）**— 萬能膠囊的物質壓縮、時光機、物質瞬間轉移、念力與遙視、無接觸發勁。',
 '- **未提供原作級可重複實證；分項判定待核**— 萬能膠囊、時光機、物質瞬移、念力、遙視與無接觸發勁不能共用一個「物理禁止」標籤；特定定理、工程限制及缺乏證據須分開。'),
('真正被封死的只有四樣：**物質瞬間轉移**、**時光機**、**萬能膠囊的物質壓縮**、**無接觸念力**。前三樣撞的是無複製定理、時序保護與費米簡並壓力；最後一樣撞的是四十年受控實驗的空集合——1995 年 CIA 內部備忘錄的原話是遙視的論據「幾近不存在」。',
 '本包未提供物質瞬移、時光機、原作膠囊壓縮或無裝置念力的可重複原作級實證；不得用未限定的定理或猜想統一裁定永久不可能。遙視屬資訊獲取主張，與以念力改變物體運動不同；AIR情報用途評估不能互相替代這些檢驗。'),
('D 念力、遙視、特異功能團體','待分項驗證：念力、遙視、特異功能團體')]

def main():
    p=HERE/'正文修訂追溯_20261016.json';log=json.loads(p.read_text(encoding='utf-8'))
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md']:
        f=HERE/name;t=f.read_text(encoding='utf-8')
        for old,new in PAIRS:
            if old in t:
                log.append({'batch':'B07','as_of':'2026-10-16','file':name,'old':old,'new':new,'occurrences':t.count(old),'reason':'區分統計結果、超常成因及情報用途；撤回未核引語、數字及普遍禁止裁決'})
                t=t.replace(old,new)
        f.write_text(t,encoding='utf-8')
    p.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=[
      ['RV01','https://www.cia.gov/stories/story/ask-molly-did-cia-really-study-psychic-powers/','2021-10-27','AGENCY_RETROSPECTIVE_TEXT_CHECKED','歷史回顧，不是1995報告原件或全部研究的獨立重現'],
      ['RV02','https://www.alice.id.tue.nl/references/mumford-rose-goslin-1995.pdf','1995-09-29','ORIGINAL_REPORT_UNIVERSITY_MIRROR_EXECUTIVE_SUMMARY_CHECKED','讀取183頁報告文本的封面及執行摘要E-1至E-5；未逐頁審計附錄或比對CIA副本雜湊'],
      ['RV03','https://www.cia.gov/readingroom/document/cia-rdp96-00791r000100150004-8','','REDIRECTED_TO_READINGROOM_NO_DOCUMENT','備忘錄及PDF入口均未取得原件，幾近不存在引語待核'],
      ['RV04','https://www.cia.gov/readingroom/document/cia-rdp96-00791r000200180006-4','','REDIRECTED_TO_READINGROOM_NO_DOCUMENT','報告CIA入口失效；未比對鏡像與CIA副本'],
      ['RV05','https://www.cia.gov/readingroom/document/cia-rdp96-00791r000200180005-5','','REDIRECTED_TO_READINGROOM_NO_DOCUMENT','草稿入口失效；不將草稿與9月29日報告混成同一版本'],
      ['RV06','https://www.princeton.edu/~paw/archive_new/PAW06-07/04-1108/notebook.html','2006-11-08','UNIVERSITY_ALUMNI_PUBLICATION_TEXT_CHECKED','當時預告次年關閉；不是事後關閉公告，未確證完成日期']]
    keys=['id','url','source_date','access_depth','limitation']
    receipt={'batch':'B07','checked_as_of':'2026-10-16','experiment_run':False,'memo_quote_verified':False,
             'sources':[dict(zip(keys,r)) for r in rows],'correction_records':sum(r.get('batch')=='B07' for r in log)}
    (HERE/'遙視與情報用途核查回執_B07_20261016.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    marker='## 第七輪續核 B07（2026-10-16）'
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md','諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md','交流科技三文件_查證交付說明_20261014.md','跨領域核查與修訂總覽_20261016.md']:
        f=HERE/name;t=f.read_text(encoding='utf-8')
        if marker not in t:f.write_text(t+'\n\n'+marker+'\n\n遙視研究、超常成因與情報用途須分開。已撤回未核CIA備忘錄引語及所有超能力都已測完的外推，詳見[第七輪報告](續核來源與發現_B07_20261016.md)。\n',encoding='utf-8')
    print('B07 corrections saved; memo quotation and blocked archive entries remain pending.')

if __name__=='__main__':main()
