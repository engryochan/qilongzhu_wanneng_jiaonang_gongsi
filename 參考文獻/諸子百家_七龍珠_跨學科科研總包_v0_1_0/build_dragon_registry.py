from pathlib import Path
import csv, hashlib, json, textwrap
out=Path('/mnt/data')
# Each seed item: name|association|focus. Country is historical/geographic affiliation, NOT individually verified citizenship.
groups={
'力學與流體': '''伽利略 Galileo Galilei|義大利|落體及運動;牛頓 Isaac Newton|英國|運動定律與引力;歐拉 Leonhard Euler|瑞士|流體方程;拉格朗日 Joseph-Louis Lagrange|義大利／法國|分析力學;哈密頓 William Rowan Hamilton|愛爾蘭|哈密頓力學;伯努利 Daniel Bernoulli|瑞士|流體能量;納維 Claude-Louis Navier|法國|黏性流體;斯托克斯 George Gabriel Stokes|愛爾蘭／英國|黏性流體;雷諾 Osborne Reynolds|英國|湍流;普朗特 Ludwig Prandtl|德國|邊界層;馮卡門 Theodore von Kármán|匈牙利／美國|渦街及航空;周培源 Zhou Peiyuan|中國|湍流;吳仲華 Wu Zhonghua|中國|葉輪機械;Morteza Gharib|伊朗／美國|渦環及生物流體;Detlef Lohse|德國／荷蘭學術背景|湍流及多相流;Howard A. Stone|美國|微流體;George K. Batchelor|澳大利亞／英國|湍流;Jean-Baptiste le Rond d'Alembert|法國|流體力學;Hassan Aref|埃及出生／美國學術背景|渦動力學;James Lighthill|英國|生物流體及聲學''',
'大氣氣象與電磁': '''Vilhelm Bjerknes|挪威|動力氣象;Edward Lorenz|美國|混沌氣象;Jule Charney|美國|數值天氣預報;真鍋淑郎 Syukuro Manabe|日本／美國|氣候模式;Kerry Emanuel|美國|熱帶氣旋;Eugenia Kalnay|阿根廷／美國|資料同化;法拉第 Michael Faraday|英國|電磁感應;馬克士威 James Clerk Maxwell|英國|電磁場;赫茲 Heinrich Hertz|德國|電磁波;洛侖茲 Hendrik Lorentz|荷蘭|電磁力;尼古拉·特斯拉 Nikola Tesla|塞爾維亞裔／美國|交流電;Charles P. Steinmetz|德國／美國|電力工程;Hannes Alfvén|瑞典|磁流體;Irving Langmuir|美國|電漿;Aurélien Houard|法國|雷射引導閃電;Jean-Pierre Wolf|瑞士|大氣光學;Francisca Nneka Okeke|奈及利亞|地磁與電離層;Edward Appleton|英國|電離層;John B. Goodenough|美國|電池電化學;Tebello Nyokong|南非|光化學與光動力研究''',
'引力與時空': '''愛因斯坦 Albert Einstein|德國／瑞士／美國|廣義相對論;羅傑·潘洛斯 Roger Penrose|英國|黑洞時空;基普·索恩 Kip Thorne|美國|引力波;Rainer Weiss|德國／美國|LIGO;Andrea Ghez|美國|銀河中心;Reinhard Genzel|德國|銀河中心;Stephen Hawking|英國|黑洞理論;Subrahmanyan Chandrasekhar|印度／美國|恆星結構;Gabriela González|阿根廷／美國學術背景|引力波實驗;Clifford Will|美國|相對論檢驗;John Archibald Wheeler|美國|量子引力思想;Abhay Ashtekar|印度／美國學術背景|圈量子引力;Nergis Mavalvala|巴基斯坦／美國學術背景|引力波儀器''',
'量子物理與資訊': '''普朗克 Max Planck|德國|量子論;波耳 Niels Bohr|丹麥|原子理論;海森堡 Werner Heisenberg|德國|矩陣力學;薛丁格 Erwin Schrödinger|奧地利|波動力學;狄拉克 Paul Dirac|英國|相對論量子;費曼 Richard Feynman|美國|量子電動力學;Alain Aspect|法國|量子糾纏;Anton Zeilinger|奧地利|量子態傳送;潘建偉 Pan Jianwei|中國|量子通訊;丁致良 Julian J.-L. Ting|臺灣學術背景|量子通道及光學;John S. Bell|北愛爾蘭／英國|貝爾不等式;Charles H. Bennett|美國|量子資訊;Gilles Brassard|加拿大|量子密碼;Peter Shor|美國|量子演算法;David Deutsch|以色列出生／英國學術背景|量子計算理論;Artur Ekert|波蘭／英國學術背景|量子密碼''',
'光學聲學': '''菲涅耳 Augustin-Jean Fresnel|法國|波動光學;Arthur Ashkin|美國|光學鑷子;Gérard Mourou|法國|超強雷射;Donna Strickland|加拿大|超快光學;中村修二 Shuji Nakamura|日本／美國|藍光LED;Federico Capasso|義大利／美國|超表面光學;Lord Rayleigh|英國|聲學與散射;Asier Marzo|西班牙|聲學全像;Bruce Drinkwater|英國|超聲波操作;Sriram Subramanian|印度／英國學術背景|超聲波觸覺;John Pendry|英國|超材料;Steven Cummer|美國|聲學超材料;Andrea Alù|義大利／美國學術背景|電磁超材料;Evelyn Hu|美國|奈米光子學;Jocelyn Bell Burnell|北愛爾蘭／英國|射電天文''',
'生物與再生': '''Margaret Dayhoff|美國|生物資訊;Michael Waterman|美國|生物序列;David Haussler|美國|基因組計算;Ewan Birney|英國|基因組資訊;陳潤生 Chen Runsheng|中國|生物資訊;Jennifer Doudna|美國|CRISPR;Emmanuelle Charpentier|法國|CRISPR;山中伸彌 Shinya Yamanaka|日本|iPSC;David Liu|美國|基因編輯;Hans Clevers|荷蘭|類器官;Robert Langer|美國|生物材料;竹內昌治 Shoji Takeuchi|日本|生物混合機器人;Niels Ryberg Finsen|丹麥|光療;Aziz Sancar|土耳其／美國|DNA修復;Russell Foster|英國|晝夜節律;Anthony Atala|美國|再生醫學;George Church|美國|合成生物學;James Collins|美國|合成生物學;Feng Zhang|中國出生／美國學術背景|基因編輯;David Baker|美國|蛋白質設計;John Jumper|美國|蛋白質結構預測;Tu Youyou 屠呦呦|中國|天然藥物研究''',
'神經人工智能與計算': '''Santiago Ramón y Cajal|西班牙|神經元;Karl Deisseroth|美國|光遺傳;Edward Boyden|美國|神經技術;Miguel Nicolelis|巴西|腦機介面;Grégoire Courtine|法國|腦脊髓介面;Jocelyne Bloch|瑞士|神經外科;John Donoghue|美國|BrainGate;John Hopfield|美國|神經網絡;Geoffrey Hinton|英國／加拿大|深度學習;Yoshua Bengio|法國／加拿大|深度學習;Yann LeCun|法國／美國|卷積網絡;李飛飛 Fei-Fei Li|中國出生／美國|電腦視覺;Alan Turing|英國|計算理論;Claude Shannon|美國|資訊論;Edsger Dijkstra|荷蘭|演算法;Donald Knuth|美國|演算法分析;John von Neumann|匈牙利／美國|計算架構;陶哲軒 Terence Tao|澳大利亞／美國|數學分析;Demis Hassabis|英國|深度學習與蛋白質AI;Judea Pearl|以色列／美國|因果推論;Michael Jordan|美國|機器學習;Rodney Brooks|澳大利亞／美國|機械人;Marc Raibert|美國|腿式機械人;Daniela Rus|羅馬尼亞／美國學術背景|機械人;Pieter Abbeel|比利時／美國學術背景|機械人強化學習;Sergey Levine|美國學術背景|機械人學習;Anima Anandkumar|印度／美國學術背景|人工智能;Regina Barzilay|以色列／美國學術背景|人工智能醫學''',
'研究檢驗與哲學': '''Shawn Carlson|美國|占星雙盲檢驗;Susan Blackmore|英國|超心理學檢驗;Richard Wiseman|英國|異常心理學;Christopher French|英國|異常心理學;Rupert Sheldrake|英國|有爭議超心理假說;Karl Popper|奧地利／英國|可證偽性;Thomas Kuhn|美國|科學史;John Ioannidis|希臘／美國學術背景|可重現性;Deborah Mayo|美國|統計哲學;David Spiegelhalter|英國|不確定性與風險;Barbara McClintock|美國|細胞遺傳學'''
}
people=[]
for field, entries in groups.items():
 for s in entries.replace('\n','').split(';'):
  s=s.strip()
  if not s:continue
  arr=s.split('|')
  if len(arr)!=3:print('BAD',arr);continue
  name,region,focus=arr
  people.append(dict(record_id=f'SCI-{len(people)+1:04}',name=name,field=field,region_association=region,contribution=focus,era='歷史或現代（個別待判）',citizenship='UNKNOWN_NOT_VERIFIED',orcid='',orcid_status='NOT_CHECKED',affiliation='',identity_source_url='',representative_doi='',paper_source_url='',claim_evidence='SEED_NOT_INDIVIDUALLY_VERIFIED',last_verified_date='',notes='國別欄屬通行歷史／學術背景，不能視為目前護照國籍'))
seen=set();dup=[]
for p in people:
 key=p['name'].split(' ')[0]
 if key in seen:dup.append(p['name'])
 seen.add(key)
# allow e.g Planck duplicated once manual dedupe exact folded Chinese or English
unique=[]; u=set()
for p in people:
 if p['name'] in u:continue
 u.add(p['name']);unique.append(p)
people=unique
for i,p in enumerate(people,1):p['record_id']=f'SCI-{i:04}'
fields=list(people[0])
csvname=out/'諸子百家_七龍珠科研_全球科學家名錄_初始種子_v0_1_0.csv'
with csvname.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(people)
print('PEOPLE',len(people), 'GROUPS', {k:len([p for p in people if p['field']==k]) for k in groups})

# Categorical representative skill registry, conceptual with clear evidence status.
skillgroups={
'01 武藝、運動、訓練': '龜仙流基礎武術;舞空術;高速移動與殘像拳;瞬間反應／自在極意功;界王拳;重力修煉室;精神時光屋;氣的感知;戰鬥力探測器;氣的隱藏;念動／意念操作;超人力量;超人耐力;超高速恢復;自動閃避',
'02 氣流、能量與結界': '龜派氣功;元氣彈;魔貫光殺炮;氣圓斬;伽力克炮;終極閃光;大爆炸攻擊;多重能量彈;氣功護罩;氣功推進;能量感知;能量吸收;能量儲存;從遠方匯聚能量;氣的傳授;破壞神破壞術;能量治癒',
'03 生物、變身與再生': '巨猿化／普魯茲波;超級賽亞人1至3;超級賽亞人4;超級賽亞人之神;超級賽亞人藍;自在極意功變身;自我極意／特殊形態;布羅利爆發形態;人造人16機械身軀;人造人17與18改造;人造人19與20能量系統;賽魯再生;吸收其他生命;魔人布歐再生;魔人布歐變形;那美克星人再生;融合／合體舞;波特拉耳環融合;生物培養艙;仙豆;基因與細胞改造;壽命延長',
'04 神經、認知、靈異': '心靈感應;讀心;讀取記憶;技能模仿;瞬間學會技藝;記憶移植;腦控機械臂;多人意識融合;靈魂交換;神識分身;心智控制;預知未來;氣與意識同步;集體協作同步',
'05 空間、時空、宇宙': '瞬間移動;時間跳躍;時間暫停;時光機穿越過去;相對論時間膨脹;異次元空間;空間封印／魔封波;異次元儲物;界王神遠距傳送;太空飛行;無重力運動;人造月亮;龍珠定位;星際通訊',
'06 生命、神祇、魔法': '神龍許願;復活死者;恢復被毀星球;治癒重創;物質創造;物質消失;物體縮小並恢復;瞬間變衣;石化;變物能力;靈魂／來世;能量生命;超級龍珠願望;完美封印',
'07 萬能膠囊與人造技術': '萬能膠囊收納房車;折疊展開建築;自重構機器人;生物混合機器人;仿生皮膚自我修復;外骨骼;強化視覺;可穿戴光學感測;虛擬訓練場;星際運載;人工重力訓練;生物資訊建模;神經網絡技能遷移;AI數字分身'
}
# evidence triad levels: F physical feature analogue, P partial, H hypothesis, X no evidence original feat.
skills=[]
for group,items in skillgroups.items():
 for name in items.split(';'):
  # deterministic default statuses curated by key controls
  x_terms=['復活死者','恢復被毀星球','超級龍珠','時光機穿越過去','人造月亮','靈魂','預知未來','瞬間學會技藝','完整封印','物質消失','物質創造','超級賽亞人','巨猿化','布羅利爆發','魔人布歐','神龍許願','神識分身','破壞神破壞術','異次元','自我極意']
  status='ORIGINAL_UNVERIFIED' if any(t in name for t in x_terms) else 'FUNCTIONAL_ANALOGUE_ONLY'
  if '量子' in name:status='PHYSICAL_LIMITATION'
  skills.append(dict(skill_id=f'DB-{len(skills)+1:04}',category=group,ability=name,canonical_scope='',continuity='',status=status,anime_exact_replication='NOT_ESTABLISHED',scientific_family='',primary_canon_source='',research_paper='',measurement='',energy_source='',risk='',notes='功能類比不等於還原動畫能力；原著／動畫／遊戲版本須進一步標註'))
skcsv=out/'諸子百家_七龍珠全技能_研究分類註冊表_v0_1_0.csv'
with skcsv.open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(skills[0]));w.writeheader();w.writerows(skills)
print('SKILLS',len(skills))

# Philosophy historical registry
schools=[
('儒家','孔子、孟子、荀子、曾子、子思','《論語》《孟子》《荀子》','教育、倫理、知識論','不當作物理實驗'),
('道家','老子／李耳／老聃、莊子、列子','《老子》《莊子》《列子》','師法自然、控制哲學','老子史實與《老子》成書有爭議'),
('陰陽家','鄒衍','《史記》人物記載、陰陽五行文獻','周期模型、時序檢驗','五行非現代化學元素或物理力'),
('法家','商鞅、申不害、慎到、韓非、李斯','《商君書》《韓非子》','制度、標準化、審計','荀子不應歸入法家'),
('名家','惠施、公孫龍、鄧析','《公孫龍子》','邏輯、分類、知識圖譜','與科學方程非等價'),
('墨家','墨子、後期墨者（多匿名）','《墨子》《墨經》','力學、光學、幾何、工程','後期《墨經》成書作者不宜一概歸墨子'),
('縱橫家','蘇秦、張儀、鬼谷子傳統','《戰國策》《鬼谷子》','策略、博弈、談判','人物年代與文本成書分開'),
('雜家','呂不韋及編撰群體','《呂氏春秋》','跨學科綜合','需分辨多作者來源'),
('農家','許行及農家傳統','《孟子》所載農家論爭','農業、能源、資源','文獻多間接轉述'),
('小說家','先秦漢代稗官傳聞傳統','《漢書·藝文志》','敘事資料批判','非現代小說家職業分類'),
('兵家','孫武、孫臏、吳起、尉繚','《孫子》《孫臏兵法》','運籌、決策、模擬','不與九流十家等同'),
('醫家','扁鵲傳說、張仲景、華佗、孫思邈','《傷寒雜病論》《千金要方》','醫學史、臨床證據','古方需現代安全與療效試驗'),
('天文曆算與術數','甘德、石申、張衡、祖沖之、郭守敬','古代曆法及天文文獻','天文、數學、測量','與占星預測可靠性分開'),
('工藝與博物','魯班傳統、沈括、宋應星','《夢溪筆談》《天工開物》','機械、材料、實驗觀察','傳說、歷史、技術需分證')
]
with (out/'諸子百家_學派思想註冊表_v0_1_0.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['school','figures','texts','methodological_relevance','scholarly_caveat']);w.writerows(schools)

sources=[
 ('漢書藝文志','https://ctext.org/han-shu/yi-wen-zhi'),
 ('SEP Xunzi','https://plato.stanford.edu/entries/xunzi/'),
 ('SEP Laozi','https://plato.stanford.edu/entries/laozi/'),
 ('SEP Zhuangzi','https://plato.stanford.edu/entries/zhuangzi/'),
 ('SEP Mohist Canons','https://plato.stanford.edu/entries/mohist-canons/'),
 ('SEP Chinese Legalism','https://plato.stanford.edu/entries/chinese-legalism/'),
 ('Dragon Ball Original Official Kamehameha','https://en.dragon-ball-official.com/news/01_659.html'),
 ('Dragon Ball Official Blutz Waves','https://en.dragon-ball-official.com/news/01_2131.html'),
 ('Dragon Ball Official techniques game','https://en.dragon-ball-official.com/news/01_3039.html'),
 ('OpenAlex Authors official','https://help.openalex.org/data/authors/'),
 ('OpenAlex ORCID limitation','https://help.openalex.org/data/authors/orcid/'),
 ('OpenAlex API docs','https://help.openalex.org/api/'),
 ('Biohybrid review 2025','https://www.nature.com/articles/s44182-025-00056-x'),
 ('1998 vortex ring','https://doi.org/10.1017/S0022112097008410'),
 ('2018 ionic wind flight','https://doi.org/10.1038/s41586-018-0707-9'),
 ('2015 acoustic levitation','https://doi.org/10.1038/ncomms9661'),
 ('2023 laser-guided lightning','https://doi.org/10.1038/s41566-022-01139-z'),
 ('1999 quantum channel Ding','https://doi.org/10.1103/PhysRevE.59.2801'),
 ('2026 Ting image sensor','https://arxiv.org/abs/2608.12729'),
 ('2005 optogenetics','https://doi.org/10.1038/nn1525'),
 ('2023 brain-spine interface','https://doi.org/10.1038/s41586-023-06094-5'),
 ('2025 biohybrid hand','https://doi.org/10.1126/scirobotics.adr5512'),
 ('2017 extracorporeal premature lamb','https://doi.org/10.1038/ncomms15112'),
 ('1985 astrology double blind','https://doi.org/10.1038/318419a0')]
science32={
 'A 經典物理':['古典力學','分析力學','流體力學','空氣動力學','氣象動力學'],
 'B 場與能量':['電磁學','磁學','電動力學','高電壓工程','電漿物理','聲學'],
 'C 重力與時空':['萬有引力及廣義相對論','天體力學','引力波與精密測量'],
 'D 量子與光學':['量子力學','量子資訊','量子場論','光學','光子學'],
 'E 生命科學':['生物流體力學','生物資訊學','分子生物學','再生醫學','光生物學'],
 'F 神經與智能':['神經科學','腦機介面','人工神經網絡','機械人學'],
 'G 數學計算':['離散數學','數值計算與多物理場模擬'],
 'H 跨學科檢驗':['科學哲學與實驗設計','超心理學及玄學主張的實證檢驗']}
assert sum(map(len,science32.values()))==32

lines=[]
def add(s=''):
 lines.append(s)
add('---')
add('title: "諸子百家 × 全球科研人物 × 《七龍珠》全技能：研究總綱"')
add('subtitle: "歷史思想、現代物理、工程驗證與證據註冊表"')
add('date: 2026-10-14')
add('lang: zh-TW')
add('format: html')
add('toc: true')
add('number-sections: true')
add('---')
add('')
add('> **性質**：研究構想與逐項證據註冊表；不是超能力已被證實的宣告、實驗操作手冊或特定企業能力背書。版本 v0.1.0。')
add('')
add('## 一、研究目標、可行性及邊界')
add('')
add('**北極星目標**：盡可能完整地索引《七龍珠》原著、動畫、電影與遊戲技能，為每項技能找到最接近的物理、生物、計算或人機工程子問題。**全部研究覆蓋**不等於**全部原樣實現**。')
add('')
add('1. **原型實現**：具有可重複實驗支持的功能。')
add('2. **工程等價**：外觀或使用目的相似，但作用原理不同，例如腦機介面≠念力、飛行服≠徒手飛行。')
add('3. **理論探索**：模型可能具有數學意義，尚未有原作級實驗證據。')
add('4. **目前未證實或與已知物理相衝突**：不得將希望當成已成立的技術路線。')
add('')
add('## 二、諸子百家完整分類（九流十家 + 跨類補全）')
add('')
add('依《漢書·藝文志》區分九流十家，並在研究框架中額外納入兵家、醫家、天文術數、工藝博物。荀子屬儒家；韓非、商鞅與申不害等屬法家；老子生平及《老子》成書有文本史爭議。')
add('')
add('| 學派 | 重要人物 | 典籍與研究用途 | 史料或方法限制 |')
add('|---|---|---|---|')
for a,b,c,d,e in schools:
 add(f'| {a} | {b} | {c}；{d} | {e} |')
add('')
add('**方法學原則**：道家「道法自然」作觀察啟發；墨家重測量、邏輯與光學；陰陽家作古代分類與週期思想史；儒家作倫理治理；兵家作策略推演；現代科學實證必以可測量定義、守恆定律與對照實驗獨立判定。')
add('')
add('## 三、八學群32項科研學科')
add('')
add('| 學群 | 核心學科 | 對應技能 |')
add('|---|---|---|')
related=['肢體運動、渦環、氣流','離子風、磁浮、光電磁、聲場','飛行、軌道、時光房','量子態、光採集、感測','人造人、再生、變身','意念控制、機械學習','建模、假說、模擬','證據鑑別、科學倫理']
for (k,fields32),rel in zip(science32.items(),related): add(f'| {k} | {"、".join(fields32)} | {rel} |')
add('')
add('## 四、《七龍珠》全技能研究框架（開放世界版本）')
add('')
add(f'此版本先建立 **{len(skills)} 項候選技能**，橫跨七大能力群。由於原著、Z、超、GT、劇場版、遊戲及衍生作品存在不同設定，嚴禁宣稱已窮盡「全部技能」。每項設獨立 `canonical_scope` 及 `continuity` 欄位以便後續補完。')
add('')
add('| 分類 | 所含能力（研究入口） | 現實對應與主要限制 |')
add('|---|---|---|')
explanations=['運動生理、機械人平衡、外骨骼；原作速度與力量不可直接還原','流體渦旋、電磁、聲學與能源網路；無徒手高能氣功實證','類器官、基因編輯、再生醫學；無賽亞人瞬時變身實證','BCI、神經介面、模仿學習；不等於讀心、記憶下載、靈魂','量子通訊、相對論、軌道、VR；無人體瞬移或回到過去證據','醫學急救、材料、化學與數位世界；無願望改寫宇宙定律實證','折疊構造、生物混合機械人、AR與工程模組化']
for (k,items),exp in zip(skillgroups.items(),explanations): add(f'| {k} | {"、".join(items.split(";"))} | {exp} |')
add('')
add('**研究台帳CSV**：`諸子百家_七龍珠全技能_研究分類註冊表_v0_1_0.csv`，以能力條目為粒度；每一個名詞不應被視作已具實驗成熟度。')
add('')
add('## 五、丁致良跨學科研究主線')
add('')
add('保留前輪已提及的著作群：**《古典力學》《量子力學》《物理數學》《生物流體力學》《電動力學解答》《量子場論題解》《占星學量子》《長生不老秘方》《甲骨文拓樸學》《超摩擦》**。學術論文須比對期刊、DOI、作者身份；書籍存在≠內容各主張都經驗證；博士學位與教授職稱亦不可混為一談。')
add('')
add('代表研究：1999年 Physical Review E **Stochastic Resonance for Quantum Channels**，DOI 10.1103/PhysRevE.59.2801；2026年光學感測器預印本 arXiv:2608.12729。量子通道與人體移動不可混同。')
add('')
add('## 六、全球科研人物名冊與國籍審核')
add('')
add(f'初始研究者資料表包含 **{len(people)} 個不重複命名條目**、涵蓋 {len(groups)} 個學科群，另設 **{len(schools)} 家／門**歷史思想分類。這是待審計種子，不是已完全核實的現任科學家、法定國籍名冊。')
add('')
add('| 學群 | 初始研究者人數 | 保留的學術核心 |')
add('|---|---:|---|')
for k in groups:
 subset=[p for p in people if p['field']==k]
 add(f'| {k} | {len(subset)} | {"、".join(p["name"].split(" ")[0] for p in subset[:5])} 等 |')
add('')
add('### 全球名錄裁定（必讀）')
add('')
add('- `region_association` 只代表常見歷史國別、出生或學術活動關聯；`citizenship` 一律保留 UNKNOWN_NOT_VERIFIED，除非有可靠、明確證據核定。')
add('- 不得把現任大學所在地當成個人法律國籍；雙重國籍／國籍變化須有來源與核實時點。')
add('- ORCID 是研究者識別碼，不是國籍證書。古代科學家與未擁有 ORCID 者不可偽造號碼。')
add('- 分開 `researcher_id`、ORCID、OpenAlex Author ID、ROR機構、DOI論文與國籍證據來源；同性同名不能自動合併。')
add('- 本名錄**無人**完成個別 ORCID 或現任機構實查。CSV 中留空是誠實的缺值，不代表不存在。')
add('- 預備覆蓋全球數千人時，以 OpenAlex、ORCID、Crossref、ROR 交叉比對，但不能僅依被引量或國別判定科學品質。')
add('')
add('### 增量擴展工作流')
add('')
add('**學科分類→文獻導入→作者去歧義→ID交叉驗證→機構/國別拆分→代表論文核實→方法與可重現性評估→專家覆核→版本凍結。**')
add('')
add('建議不以自然人法律國籍作為排除或科研能力標準；國別只是來源、合作及制度研究的客觀欄位。')
add('')
add('## 七、三大原創構想：假說、模型、局限及安全驗收')
add('')
add('### 7.1 交流電類比交流氣流')
add('')
add('`V(t)=V0 sin(2πft)` 與 `Q(t)=Q0 sin(2πft + φ)` 可作不同物理量的週期形式類比，但不是相同控制律；空氣具有密度、可壓縮性、黏性、能量耗散與渦量。')
add('')
add('合成射流（Synthetic Jet）在一週期內穿越開口的淨質量交換可近乎為零，仍能透過渦環向外傳播動量；此現象不代表憑空增加能量。研究目標是安全地模擬週期吸排、渦度、相位、流速與動量效率。禁止直接跳到危險高壓/高能定向發射實驗。')
add('')
add('### 7.2 萬有引力與飛行')
add('')
add('`F = G M m / r²`；普通物質皆有引力作用，地表約 `g = 9.81 m/s²`。引力輔助、自由落體、衛星軌道及浮力已存在，但反轉局部地球引力或無能量來源徒手飛行未證實。70公斤懸停所需最低向上支撐力約 687 N。')
add('')
add('### 7.3 普魯茲波與光生物學')
add('')
add('《七龍珠》官方訪問大阪大學寺田健太郎，討論月光反射與虛構普魯茲波的類比。藍光黃疸療法、UVB誘導維生素D、光遺傳學確有不同的光學與生理作用，但無現實賽亞人巨猿變身證據。維生素E不等於光誘導維生素D。研究對象須限定安全的資料分析／公開細胞實驗成果，禁止人體或嬰幼兒未批准光照實驗。')
add('')
add('## 八、模型、設備與軟件候選')
add('')
add('| 領域 | 工具 | 研究邊界 |')
add('|---|---|---|')
for x in [('流體／空氣','OpenFOAM、SU2、FEniCSx','CFD、離線數值驗證'),('電磁／光學','MEEP、COMSOL、Elmer FEM','耦合電磁與光學模型'),('聲場','k-Wave、pyroomacoustics','聲傳播與小尺度操控'),('量子','QuTiP、Qiskit、PennyLane','量子態而非人體傳送'),('引力與軌道','REBOUND、Orekit','天體運動與重力助推'),('生命與資料','R/Bioconductor、Biopython、Scanpy','資料與文獻，不是臨床治療'),('神經與機械','PyTorch、JAX、ROS 2、MuJoCo','模擬與有界機械控制'),('統計與科研驗證','R targets/brms、Python scipy/statsmodels','假說檢驗、信賴區間、註冊對照')]:
 add('| '+' | '.join(x)+' |')
add('')
add('## 九、分階段研究路線與不退化驗收')
add('')
phases=[
('P0 歸檔與消歧','九流十家、32學科、全技能條目與版本規範；所有來源指紋','史料來源齊全、身份誤配=0、不得把想像當成果'),
('P1 公開科研證據查核','每種技能≥1來源；優先原論文與獨立綜述','可查證DOI/期刊/實驗設備/反證'),
('P2 數值復現','渦環、飛行軌道、光學、聲學、量子態、神經控制','版本鎖定、基線/靈敏度/誤差/能量守恆'),
('P3 安全的小尺度驗證','低能量物理現象、公開資料、授權設備','預註冊、假設、對照組、第三方安全審閱'),
('P4 工程等價樣機','機械人、BCI醫療機構、仿生皮膚、VR時光屋、折疊建築','功能驗收、可靠性、風險與法規'),
('P5 成熟度提升','通用性、長期可靠性、不同場景遷移','獨立復驗、可回滾、成本效益'),
('P∞ 長期科學探索','未證實的元氣彈／巨猿／人體瞬移／復活等','未證實保留UNKNOWN；不得保證實現日期')]
add('| 階段 | 工作內容 | 退出閘門 |');add('|---|---|---|')
for x in phases:add('| '+' | '.join(x)+' |')
add('')
add('## 十、redteam / critic / killcritic / blindspot / cheatsheet / blueprint / actionplan')
add('')
add('| 模組 | 必問問題 |')
add('|---|---|')
for x in [('redteam','有哪些違反能量守恆、測量錯誤、樣本偏差或動畫設定偷換？'),('critic','論文是否真正驗證了所聲稱功能？'),('killcritic','何種預先設定的負面結果可以否證核心假說？'),('blindspot','漏了哪些安全、尺度、熱負荷、材料、倫理、環境能量變量？'),('cheatsheet','中文／英文名稱、SI單位、版本、來源、閾值是否一致？'),('blueprint','把每項技能分為作用機制、輸入、輸出、測量、誤差與工程基線'),('actionplan','先做成本最低、安全、資訊增益最大的實驗或計算')]:add('| '+' | '.join(x)+' |')
add('')
add('## 十一、優先文獻與原始來源索引')
add('')
for n,u in sources:add(f'- {n}：<{u}>')
add('')
add('## 十二、正式裁定')
add('')
add(f'- 現行研究資料庫種子：**{len(people)}位科學家候選**、**{len(schools)}門傳統知識分類**、**32學科**、**{len(skills)}項《七龍珠》候選技能**；都不應稱為人類或原作的完整總量。')
add('- 「全部技能」是長期**覆蓋目標**；未證實能力保持研究課題，不承諾其在現有物理條件下工程實現。')
add('- 全球名錄下一階段是將每位候選人補齊一手人物履歷、ORCID（如有）、最近機構、代表論文、國籍證據、研究成熟度；目前此步尚未逐人完成。')
add('- 切忌憑學者的歷史族裔、國籍或語言推定科研能力。研究品質以方法、證據、可重現性決定。')
add('- 下一科研起點：交流氣流／合成射流的可重現數值模型；與重力軌道、光生物模型平行推進。')

add('')
add('## 附錄甲、全球科學家初始名冊逐人列示（全部145筆）')
add('')
add('**此附錄保留姓名、國別／學術背景與研究主題，但國籍、ORCID、學術機構尚未逐人驗證。名錄是候選種子而非認證名冊。**')
add('')
add('| 編號 | 學科群 | 人物 | 出生／歷史／學術背景（非已核實法律國籍） | 研究貢獻 |')
add('|---|---|---|---|---|')
for p in people:
 add(f'| {p["record_id"]} | {p["field"]} | {p["name"]} | {p["region_association"]} | {p["contribution"]} |')
add('')
add('## 附錄乙、丁致良書目／研究組織待核事項')
add('')
add('先前對話提及臺北萬華**進源書局**、臺中**傳說中的落魄秀才書屋**與丁致良出版著作；兩書店／出版品牌不得當成同一法人。研究所名稱 **De Font Institute for Advanced Studies** 僅屬研究者學術檔案線索，法定機構狀態待核。臺大學士、清大物理博士、博士後或海外研究經歷與正式教授任職職級應分案查核。')
add('')
add('### 丁致良著作保留清單')
add('')
for book in ['古典力學','量子力學','物理數學（二版）','生物流體力學','電動力學解答','量子場論題解','占星學量子：理論模型及實驗證據','長生不老秘方','甲骨文拓樸學','超摩擦','離散數學','針灸筆記','中藥筆記','諾貝爾的榮耀：物理桂冠（合著）']:
 add('- 《'+book+'》：前輪提及或與人物相關之候選書目，具體版次、ISBN、篇章與真實作者署名須依獨立書目逐本覆核。')

qmd=out/'諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_1_0.qmd'
qmd.write_text('\n'.join(lines)+'\n',encoding='utf-8')
manifest=[]
for p in [qmd,csvname,skcsv,out/'諸子百家_學派思想註冊表_v0_1_0.csv']:
 raw=p.read_bytes();manifest.append({'file':p.name,'bytes':len(raw),'lines':raw.count(b'\n'),'sha256':hashlib.sha256(raw).hexdigest(),'encoding':'UTF-8 BOM for CSV; UTF-8 for QMD'})
(out/'諸子百家_七龍珠研究_交付校驗表_v0_1_0.json').write_text(json.dumps({'as_of':'2026-10-14','candidate_scientists':len(people),'candidate_abilities':len(skills),'schools':len(schools),'disciplines':32,'files':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
for f in manifest:print(f['file'],f['bytes'], f['lines'])
