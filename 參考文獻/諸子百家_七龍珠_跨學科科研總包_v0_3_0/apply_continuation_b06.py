"""Replay B06 documented source checks; no simulator or robot is run."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PAIRS=[
('**現實**這是整張表裡實現度最高、最被低估的一項。GPU 並行物理仿真讓機器人策略在數千個同步環境中以遠超實時的倍率訓練：數小時牆鐘時間可累積以年計的仿真經驗，再配合域隨機化遷移到實體。整個具身智能產業就建在這間時光屋上。',
 '**現實（B06訂正）**GPU並行仿真可加速特定機器人策略的資料收集與訓練；PMLR所載ANYmal研究及NVIDIA的Spot案例提供各自限定設定的結果。多環境累積模擬時間、單環境實時倍率與牆鐘訓練時間須分列；不能將前者視為單一個體連續經歷多年，也不能由少數案例判定本表實現度排名或整個產業的共同路線。域隨機化不保證實體轉移成功。'),
('**缺口**只對可仿真的物理與可微的獎勵有效；仿真與現實之間的差距仍是失敗的主因。人類本體無法進入。',
 '**缺口（B06訂正）**PPO等以採樣資料估計策略梯度的方法，不要求獎勵函數或物理引擎本身可微；這與對模擬器反向傳播的可微仿真不同。效果仍取決於任務、觀測、獎勵設計、系統辨識及模擬偏差，實體轉移須另驗。本包未量化各失敗原因占比，也未提供人體進入時光屋或物理時間加速的證據。'),
('2. **精神時光屋（A，GPU 成本）**並行仿真訓練是把時間換算成算力的機制。一台工作站能跑出的仿真經驗量，決定了你的迭代速度上限。',
 '2. **精神時光屋類比：並行仿真（研究候選）**固定任務、硬體、版本、模擬步長與控制頻率，再比較資料吞吐、達到同一品質門檻的牆鐘時間及實體轉移結果；另計資產建模、調參、評測、儲存與能耗。吞吐量不單獨決定學習品質或整體迭代速度，本包未執行仿真基準測試。')]

def main():
    logpath=HERE/'正文修訂追溯_20261016.json';log=json.loads(logpath.read_text(encoding='utf-8'))
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md']:
        p=HERE/name;text=p.read_text(encoding='utf-8')
        for old,new in PAIRS:
            if old in text:
                log.append({'batch':'B06','as_of':'2026-10-16','file':name,'old':old,'new':new,'occurrences':text.count(old),'reason':'校正獎勵可微性與並行模擬時間口徑，限定研究結果與成本範圍'})
                text=text.replace(old,new)
        p.write_text(text,encoding='utf-8')
    logpath.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sources=[
      ['SIM01','https://proceedings.mlr.press/v164/rudin22a.html','PUBLISHER_ABSTRACT_CHECKED','2022','ANYMAL_RUDIN','ANYmal限定任務；未核全文實驗設定及原始資料'],
      ['SIM02','https://arxiv.org/abs/2109.11978','AUTHOR_ABSTRACT_AND_VERSION_CHECKED','v3 2022-08-19','ANYMAL_RUDIN','與SIM01同一研究，非獨立重現'],
      ['SIM03','https://developer.nvidia.com/blog/closing-the-sim-to-real-gap-training-spot-quadruped-locomotion-with-nvidia-isaac-lab/','VENDOR_CASE_TEXT_CHECKED','','SPOT_NVIDIA','廠商案例；4096環境、RTX4090、約4小時，非本機實測'],
      ['SIM04','https://isaac-sim.github.io/IsaacLab/v2.0.0/source/setup/faq.html','VERSIONED_MAINTAINER_DOCUMENTATION_CHECKED','v2.0.0','ISAAC_ECOSYSTEM','歷史版本文件，不將當時架構或授權敘述冒充最新狀態'],
      ['SIM05','https://docs.isaacsim.omniverse.nvidia.com/5.1.0/isaac_lab_tutorials/troubleshooting.html','VERSIONED_MAINTAINER_DOCUMENTATION_CHECKED','5.1.0','ISAAC_ECOSYSTEM','版本化故障排除；不是各類失敗原因的統計排名'],
      ['SIM06','https://arxiv.org/abs/1707.06347','ORIGINAL_ALGORITHM_ABSTRACT_CHECKED','2017','PPO','採樣與策略目標優化；本輪未重現演算法或核全部推導']]
    keys=['id','url','access_depth','source_version_or_year','research_or_document_group','limitation']
    receipt={'batch':'B06','checked_as_of':'2026-10-16','simulation_run':False,'robot_deployment_run':False,
             'sources':[dict(zip(keys,row)) for row in sources],
             'correction_records':sum(r.get('batch')=='B06' for r in log),
             'illustration':{'status':'ASSUMED_INPUTS_NOT_MEASURED','environments':4096,'aggregate_transitions_per_wall_second':100000,'control_step_sim_seconds':0.02,'wall_seconds':3600,'year_days':365}}
    (HERE/'並行仿真核查回執_B06_20261016.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    marker='## 第六輪續核 B06（2026-10-16）'
    for name in ['七龍珠能力技術對照冊_v1_1_0_交流科技增訂.md','神經網絡學_交流跨領域研究增訂_20261014.md','諸子百家_寰宇科學_七龍珠全技能研究總綱_v0_2_0_增訂.md','交流科技三文件_查證交付說明_20261014.md','跨領域核查與修訂總覽_20261016.md']:
        p=HERE/name;text=p.read_text(encoding='utf-8')
        if marker not in text:p.write_text(text+'\n\n'+marker+'\n\n並行仿真、策略梯度與時間／吞吐口徑見[第六輪報告](續核來源與發現_B06_20261016.md)。修正「獎勵必須可微」及未限定的實現度排名；未執行仿真或實體機器人部署。\n',encoding='utf-8')
    print('B06 corrections saved; illustrative arithmetic only, no simulation run.')

if __name__=='__main__':main()
