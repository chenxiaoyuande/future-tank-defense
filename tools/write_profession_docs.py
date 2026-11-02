"""Write current profession and save specifications alongside the main README."""
from art_utils import ROOT
from release_info import current_release, package_name

DOCUMENTS={
"EVOLUTION.md":'''# 职业、金币与独立进化

[返回项目说明](../README.md) · [存档与语言](SAVES_AND_LANGUAGE.md)

## 选择职业

首页点击开始游戏，在已解锁关卡中选择一关，再选职业。单人选择 1P；双人可分别为 1P、2P 选职业，点击“正在选择”或按 Tab 切换当前玩家。职业页的 1 / 2 / 3 对应豌豆、蘑菇、西瓜；Enter 确认开战。

![双人职业选择，1P 与 2P 可选不同路线](media/class-select.png)

金币是团队共享钱包。每个职业分别拥有基础形态和五档永久进化；同职业的两名玩家共用该职业档位，不同职业互不影响。选定职业不会消耗金币，不会重置另外两条路线。

## 六形态路线

| 档位 | 本次费用 | 豌豆 | 蘑菇 | 西瓜 |
| --- | --- | --- | --- | --- |
| 基础 | 免费 | 豌豆幼苗 | 蘑菇幼苗 | 西瓜幼苗 |
| 进化 1 | 100 | 豌豆射手 | 喷孢蘑菇 | 西瓜投手 |
| 进化 2 | 250 | 加特林豌豆 | 荧光大喷菇 | 双瓜投手 |
| 进化 3 | 500 | 双头加特林 | 三生孢子菇 | 重装瓜炮 |
| 进化 4 | 900 | 钢叶炮台 | 幻夜巫师菇 | 寒霜西瓜 |
| 进化 5 | 1500 | 日曜豌豆要塞 | 星穹菌王 | 泰坦瓜城 |

一条路线升满消耗 3250 金币；三条全部升满合计 9750 金币。逐档购买，金币不足或已满档不会扣费。结构变化包括炮管 / 头部数量、履带、菌盖、发光菌褶、长袍、法杖、抛射机械与冰晶，不依赖单纯换色。

![三条路线与动作帧预览](media/profession-evolution.gif)

## 攻击规则

以下数值以 50 个逻辑帧为一秒，t 表示当前进化档位（0–5）。

| 职业 | 普通攻击 | 射击间隔 | 专属大招 | 大招冷却 |
| --- | --- | --- | --- | --- |
| 豌豆 | 每弹 1+⌊t/2⌋ 点；t≥2 双发；团队三杀后 3 发散射 | t=0/1 为 14−t 帧；t≥2 为 10−t 帧 | 爆裂种子，3 点范围伤害 | 250−15t 帧 |
| 蘑菇 | 每弹 1+⌊t/2⌋ 点；可额外穿透 1+⌊t/2⌋ 个目标；t≥3 双发 | 22−t 帧 | 前方孢子云持续 150 帧，每 25 帧造成 1+⌊t/3⌋ 点范围伤害 | 300−15t 帧 |
| 西瓜 | 越墙抛射，30 帧落地；每次 3+⌊t/2⌋ 点、半径 30+4t | 38−3t 帧 | 巨型西瓜，40 帧落地；8+t 点、半径 65+4t | 350−20t 帧 |

蘑菇每发孢子对同一目标最多命中一次；石墙仍会挡住孢子。西瓜优先选择朝向前方 185 距离内最近的敌人，找不到则投向前方；只在落地位置判伤，不追踪敌人后续移动。西瓜第四档起，命中目标减速至 55%，持续 80 帧，Boss 也可受影响。冷却和移速效果不等于冻结敌人。

己方攻击不会伤害队友或脑子。辣椒给普通弹 / 普通西瓜额外加一点伤害。飞行中的弹体记录发射时职业、档位、伤害，切换 UI 或升级不会修改已发出的攻击。

## 实验室与收入

首页点击实验室，顶部选择路线，下方购买下一档。也可在战斗外按 B，按 1 / 2 / 3 切路线、U 购买、M 返回来源页面；战斗中不能购买。

![蘑菇路线的实验室](media/mushroom-lab.png)

疾跑 / 重甲 / 冲锋先锋分别奖励 10 / 15 / 12 金币；召唤物 2 金币；四个 Boss 分别奖励 100 / 150 / 200 / 250 金币。每个敌人只结算一次。重试、失败、返回首页或下一关不会清空钱包与路线。

## 保存与迁移

三条路线与钱包自动存到本机。TG1 / TG2 的旧进化档位迁移到豌豆路线，保留旧钱包，蘑菇与西瓜为基础形态。读档页可点击导出 / 恢复备份。清理站点数据或换设备不会自动同步，详见存档指南。

动图与图片为实际素材合成预览，示例余额不代表赠送金币，也不是 XBuilder 实机录像。
''',
"SAVES_AND_LANGUAGE.md":'''# 闯关存档与中英文

[返回项目说明](../README.md) · [English guide](README.en.md)

## 首页与语言

首页有开始游戏、读档、设置、实验室四个按钮。设置中点击中文 / English，或任意页面按 T，语言会保存到本机。菜单、职业、进化、关卡、Boss、增益、存档状态和浏览器备份对话框都提供双语。

![英文设置页面](media/language-settings.png)

## 关卡解锁

新档仅第一关开放，通关当前关卡后开放下一关，已经通过的关卡可以重玩。选关可浏览锁定关，但开始、确认职业、手动建立检查点和继续游戏都会检查解锁范围。主题快捷键也不能绕过锁定。

旧 TG2 如果保存了尚未通关解锁的高关卡，迁移时将检查点限制到“最高通关 + 1”，并清空那个检查点的起点得分 / 击退数；已有最高通关记录保留。TG1 没有关卡记录，从第一关开始。

## 存档范围

自动保存金币、累计收入、豌豆 / 蘑菇 / 西瓜三条进化档位、最高通关、语言。开始 / 重试 / 通关保存关卡起点、单双人模式、双方职业以及起点得分与击退数。只有一个检查点，开始新局会覆盖它。

首页读档 → 继续存档，或在首页 / 选关 / 读档页按 N。继续从本关起点恢复双方生命与满耐久脑子屏障、重建敌人与道具，保留永久收入和路线。不会恢复半途位置、子弹、临时增益、屏障损耗或 Boss 半途血量。

O 手动保存本关起点；选关时仅可把已解锁的选择写成新检查点。读档页可点击导出备份 / 恢复备份，也支持 C / V。恢复替换本机钱包、路线、检查点、解锁和语言，取消或无效码不会修改原进度。

## TG3 与旧档兼容

存储键仍为 `twilight-garden.progress.v1`。新码格式为 `TG3|金币|豌豆档|累计收入|检查点关卡|起点得分|起点击退|双人标记|最高通关|语言|蘑菇档|西瓜档|1P职业|2P职业|校验`。职业 0/1/2 分别对应豌豆 / 蘑菇 / 西瓜，语言 0/1 对应中文 / English。

TG1、TG2 继续可读，旧进化迁移到豌豆，另外两路线为 0。TG3 检查字段范围、规范格式、校验和三条路线的总花费，发现损坏时保留旧数据。校验用于意外损坏检测，不是防作弊加密。

浏览器存储写入后会读回确认；失败会显示待存并重试。启动无法读取旧档时，先阻止购买与覆盖，恢复可读后合并期间收益，并保留主动选择的新语言和检查点。

这是同浏览器配置、同站点来源的本机存档；不是账号登录或云同步。清理站点数据会删除进度，换设备 / 浏览器需备份迁移。同来源多个副本会共用这份数据，没有多标签页冲突合并。
''',
"README.en.md":'''# Twilight Garden — Three Paths Awakening

Three plant classes, five independent evolution tiers per class, 20 sequential stages, four elemental bosses, local co-op, English / Chinese UI and local saves.

[中文说明](../README.md) · [Download project](../../暮光花园-三职业觉醒版.xbp) · [Evolution details](EVOLUTION.md) · [Troubleshooting (Chinese)](FAQ.md)

## Start playing

Import `暮光花园-三职业觉醒版.xbp` into [XBuilder](https://x.qiniu.com/). The animated home has Start Game, Load Game, Settings and Laboratory buttons. Settings or T switches language.

Start Game → unlocked stage → class selection → Enter Battle. A new save starts with only Stage 1 unlocked; clearing each stage unlocks the next. Locked stages cannot be started through keyboard shortcuts or checkpoints. In co-op, select a different class for each player by clicking the player selector or pressing Tab. Keys 1 / 2 / 3 select classes on that page.

| Home button | Purpose |
| --- | --- |
| Start Game | Choose an unlocked stage, player mode and classes; create a new checkpoint |
| Load Game | Resume the existing checkpoint or export / restore a backup |
| Settings | Choose English or Chinese and save the preference |
| Laboratory | Choose a class route and buy its next permanent evolution |

| Class | Normal attack | Ultimate |
| --- | --- | --- |
| Pea Gunner | Fast shots, Gatling and spread upgrades | Explosive seed |
| Spore Mage | Piercing spores, twin shots at tier 3 | Lingering spore cloud |
| Melon Artillery | Lob over walls, impact area damage; slow at tier 4 | Giant melon bombardment |

| Action | Player 1 | Player 2 |
| --- | --- | --- |
| Move | WASD | Arrow keys |
| Shoot | Space | J |
| Ultimate | E | K |

P pauses, R retries, M returns home (or back from a submenu). Enter advances after a stage clear. N resumes a checkpoint. Outside combat, B opens the laboratory and S opens the save panel. O saves a stage-start checkpoint. C / V exports or restores a backup in the save or laboratory page.

## Evolution and persistence

The wallet is shared; classes evolve independently. Players choosing the same class share its tier. Each path has a free base plus five paid tiers costing 100 / 250 / 500 / 900 / 1500 coins. Select a route in the Laboratory, then click Evolve or press U. Changing class does not erase other routes.

TG3 saves include all three tiers, both players' classes, coins, unlocks, checkpoint, stage-entry score / kills and language. There is one checkpoint; starting a new game replaces it. Export a backup first if you want to keep the previous run. TG1 / TG2 remain readable; old evolution becomes the pea route. Old checkpoints beyond the unlocked stage are clamped to the next uncleared stage.

Load resumes the stage from its beginning, restoring health and rebuilding enemies. It does not restore positions, projectiles, temporary buffs or a mid-fight boss. Storage belongs to the same browser profile and site origin. Clearing site data deletes it; use Backup / Restore to migrate.

## Campaign

Protect the brain. Each stage starts with a full barrier. Zombies stop nearby and gnaw: three accumulated seconds of active biting remove the barrier, regardless of how many zombies bite together. Interrupted biting preserves remaining durability; pauses and menus stop the timer. The next contact after the barrier breaks destroys the brain. Retrying or resuming a stage restores the barrier. Friendly attacks and boss zones do not damage it.

Zombies and bosses do not shoot projectiles; contact hurts players. Bosses retain their summoning, frost, fire and lightning skills. Boss stages are 5 / 10 / 15 / 20. Clear a quota or defeat the boss to advance. The run fails when the brain is destroyed or all players lose their lives.

![Class selection composed from actual game assets](media/class-select.png)

Art previews are asset compositions, not engine recordings. WebAssembly compilation, logic tests and storage tests do not replace full XBuilder online acceptance testing.
'''
}

if __name__=="__main__":
    for name,body in DOCUMENTS.items():
        body=body.replace("暮光花园-三职业觉醒版.xbp",package_name())
        body=body.replace("../../"+package_name(),"../../dist/"+package_name())
        if name=="README.en.md":
            body=body.replace("# Twilight Garden — Three Paths Awakening",f"# Twilight Garden — Three Paths Awakening · v{current_release()['version']}")
        (ROOT/"docs"/name).write_text(body,encoding="utf-8")
