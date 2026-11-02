# 代码架构

[返回项目说明](../README.md) · [开发与验证](DEVELOPMENT.md)

## 工程结构

```text
tank/
├── README.md / REAMD.md       # 工作区介绍与兼容命名
├── dist/                     # 带版本号的发布包
└── garden-survival/
    ├── main.spx               # 舞台规则与流程
    ├── *.spx                 # XBuilder 精灵脚本，保留原生根目录布局
    ├── assets/               # 运行时造型、场景与字体
    ├── builder-meta.json     # XBuilder 项目身份
    ├── version.json          # 自动生成的当前版本清单
    ├── releases.json         # 唯一版本配置与历史记录
    ├── go.mod / gop.mod      # 引擎依赖与项目入口
    ├── data/level-catalog.json # 规则测试导出的二十关地图目录
    ├── tools/                # 美术、构建、文档、预览与校验工具
    │   ├── project.py        # 统一命令入口
    │   ├── project_paths.py  # Python 工具路径约定
    │   ├── build_survival.py # 生成素材与项目包
    │   ├── release_info.py   # 读取版本身份
    │   ├── package_project.py # 打包与兼容副本
    │   └── verify_*.py       # 规则、文档、资源与版本检查
    ├── tests/*.go.txt        # 74 项规则 / 4 项存储测试源
    ├── docs/                 # 玩法、FAQ、架构、开发、版本与最终媒体
    └── .build/               # 临时测试工程、快照、预览与 WebAssembly
```

SPX 项目使用根目录 `main.spx` 及 `*.spx` 声明舞台和精灵，因此运行文件保留在原生位置。开发工具与测试移出根目录，避免和游戏入口混淆。`.build/`、Python 缓存及 `node_modules/` 不进入发布包。

## 状态与主循环

[main.spx](../main.spx) 每次循环先处理菜单、暂停与重试输入，再在战斗状态更新规则。逻辑以约 0.02 秒一帧计时，文档中的秒数按标称每秒 50 个逻辑帧换算。

| `state` | 含义 | 主要入口 / 后续动作 |
| --- | --- | --- |
| `6` | 动态首页 | 默认入口，开始 / 读档 / 设置 / 实验室 |
| `7` | 职业选择 | 双方分别选职业，确认后 `startWithClasses` |
| `8` | 设置 | 点击中英文并保存 |
| `1` | 选关 | `StageCard` 点击选择，`canStartStage` 检查锁定，Enter 进入职业页 |
| `5` | 存档中心 | S 从战斗外进入；N 继续，O 手动存档，C/V 备份恢复 |
| `4` | 进化研究所 | B 从战斗外进入，U 购买；M 返回进入前的界面 |
| `0` | 战斗 | `updateGame` 更新；`paused` 为独立暂停标记 |
| `2` | 过关 | Enter 调用 `nextLevel` |
| `3` | 远征胜利 | 第 20 关获胜；R 重试或 M 首页 |
| `-1` | 失败 | 脑子被毁或全员出局；R 重试或 M 首页 |

`updateGame` 在非战斗或暂停状态直接返回。区域预警、道具、敌人、树篱生长等都使用同一逻辑时钟，因此暂停不会让预警在后台结束。

## 实体槽与数据

舞台使用长度 192 的并行数组保存实体位置、种类、朝向、年龄、生命、速度等状态。槽 `1` 为 1P，槽 `191` 为 2P，`addEntity` 只分配 `2–190`，返回 `0` 表示没有空槽。

| `entity` 编号 | 用途 |
| --- | --- |
| `0` | 空槽 |
| `1` | 玩家 |
| `2` | 普通敌人或 Boss；`zombieType == 3` 表示 Boss |
| `3 / 4 / 5` | 树篱 / 符文石 / 脑子 |
| `6 / 7 / 9` | 己方普通弹 / 历史敌方弹（不再生成） / 大招弹 |
| `8 / 10 / 15` | 命中特效 / 大招爆炸 / 樱桃爆炸 |
| `11 / 12 / 13` | 再生树桩 / 敌人消散或等待补充 / 传送 |
| `14 / 16` | 道具 / Boss 技能区域 |
| `17 / 18` | 蘑菇持续孢子云 / 西瓜抛射弹体 |

`summoned` 标记区分 Boss 召唤物和关卡先锋。召唤物可以增加得分与团队击退数，但不会改变 `stageKills`。

## 关卡与难度

关键入口：`mapTile`、`restart`、`spawnZombie`、`damageZombie`、`nextLevel`。

- `mapTile(stage, col, row)` 通过主题与布局生成固定地图，返回空地、树篱或符文石。通道、边界与出生位置保留空位。
- `restart` 先清理状态，再创建玩家、脑子和地图；每五关的 Boss 关直接调用 `startBoss`，普通关创建三个先锋槽。
- 普通关目标为 `5 + level`；`waveSpawned` 限制生成总量，`stageKills` 记录实际清理进度。
- 主题为 `(level - 1) / 5`；普通敌人的生命随主题增长，移动速度与冲锋间隔逐关调整。
- `nextLevel` 保存总分与击退数，初始化下一关后恢复团队进度和已解锁的导弹。

测试导出的 [level-catalog.json](../data/level-catalog.json) 记录实际地图。`unlockedLevel` 由最高通关推算下一关，开始、确认、继续和手动选关存档都检查锁定。

## Boss 技能生命周期

```text
updateBoss
  → planBossAttack：按主题安排符阵 / 冰区 / 火线 / 落雷
  → addHazard：分配实体，写入类型、位置、预警帧和持续帧
  → Actor：在同一坐标显示对应预警素材
  → updateHazard：预警结束后生效，再到期清理
  → clearBossEffects：通关时清理区域、召唤物与敌方弹道
```

| `hazardKind` | 预警帧 | 生效方式 |
| --- | --- | --- |
| `0` 召唤 | 75 | 位置空闲且未超数量上限时生成援军 |
| `1` 冰区 | 75 | `onIce` 检查半径 36，移动速度乘以 0.5，持续 150 帧 |
| `2` 火焰 | 60 | 半宽 25 的方区，持续 100 帧，每 20 帧尝试伤害 |
| `3` 雷电 | 85 | 半径 30，仅生效瞬间判伤，保留 16 帧特效 |

区域只有成功分配实体后才会出现和生效，避免不可见攻击。区域伤害调用与普通攻击相同的玩家受击逻辑，因此尊重护盾和受伤保护。

## 双人边界

1P 与 2P 拥有独立生命、射击延迟、技能冷却及道具增益；团队共用得分、击退数和导弹升级。

`updateSecondPlayer` 处理 2P 输入；`hitPlayer` 和 `hitSecondPlayer` 分别受击。`respawnPlayer` 在空地寻找接近默认出生点的位置，避免队友或墙体堵住重生点。敌人会朝最近的存活玩家转向。

`fire` 仅允许存活玩家调用，普通僵尸与 Boss 的更新函数均不发射子弹。`zombieContact` 处理玩家接触伤害并复用护盾 / 重生保护。`brainContact` / `bitingBrain` 判断接近守护目标的啃咬者；`updateBrainDefenses` 每个战斗帧在实体更新后统一结算脑子屏障。

编号 5 的 `hp` / `maxHP` 表示屏障耐久，创建时均为 150。存在活着的啃咬者时，每帧只扣一次；归零当帧保留脑子，下帧仍被接触则失败。离开、死亡、暂停与菜单不会继续扣减，重建关卡会恢复屏障。`brain_art.py` 生成脑子、十档屏障裂纹与耐久条，`Brain.spx` 按耐久选择造型并显示在树篱上方。己方攻击忽略脑子，Boss 区域不攻击它；编号 7 的旧弹体不再由游戏生成，也不能绕过完整屏障。

## 造型与动画

[boss_art.py](../tools/boss_art.py) 为四个 Boss 绘制不同轮廓和材质。内部按更精细的坐标构图，最终仍输出 72×76 SVG、中心锚点 `(36, 38)`；细节增加不会改变碰撞规则。

每个主题具有 4 帧待机、2 帧施法、1 帧受击、4 帧狂暴造型。`Actor.spx` 的选择优先级为 **受击 → 施法预警 → 半血狂暴 → 待机**，暂停时帧时钟停止推进。

中文 UI 由 `art_utils.py` 转换为 SVG 字形路径，并附字体子集。已有普通敌人血条按剩余生命比例映射到分段造型，适配后期生命增长。

## 修改入口

永久进度由 `loadProfile`、`awardCoins`、`buyEvolution`、`persistProfile` 管理，独立于 `restart`。`profileCode` / `decodeProfile` 使用版本前缀、数值范围和校验；浏览器桥接通过 `syscall/js` 调用 `localStorage`，带异常捕获与写后读回核对。读取失败时保留旧存档，稍后读取成功再合并本次收益，不用零进度覆盖旧数据。

`playerClass` / `playerClass2` 分别保存职业；`evolution` 保留旧豌豆档位，`routeTiers[1/2]` 保存蘑菇 / 西瓜档位。`projectileTier`、`projectileClass`、`projectileDamage` 保存攻击快照；`sporeHits` 避免穿透重复判伤；西瓜以 `landingX/Y` 与 `lobDuration` 延迟结算。`classes_art.py` 生成 18 种结构造型与弹体，`front_end_art.py` 生成双语可点击页面。`Splash` / `HomeDecor` 使用独立 `uiTicks` 驱动动态首页，菜单不会推进战斗时钟。

| 想修改什么 | 先看哪里 |
| --- | --- |
| 地图障碍 | `main.spx` 的 `mapTile`；修改后重新导出地图目录 |
| 先锋数量与难度 | `restart`、`spawnZombie`、`updateZombie` |
| Boss 生命与技能 | `startBoss`、`updateBoss`、`planBossAttack` |
| 预警范围或时间 | `addHazard`、`updateHazard`、`onIce`；同步调整 `zone_art` 的可见范围 |
| Boss 外观 | `boss_art.py` 与 `Actor.spx`；保持造型命名、尺寸和锚点一致 |
| 菜单文案与地图名 | 新版菜单 `front_end_art.py`；地图名 `campaign_art.py`，英文地图名 `localization.py` |
| README 与 GIF | `write_docs.py`、`build_docs_media.py`、`docs/media/README.md` |

`xgo_autogen.go` 是工具生成产物，规则应修改 `.spx` 源码，再通过构建与测试重新生成。

## TG3 与双语资源

`encodeRosterSave` / `decodeRosterSave` 管理 TG3，在 TG2 字段上增加另外两条路线和双方职业，校验三条路线总花费。`decodeSave` 继续分派 TG1 / TG2 迁移，旧进化映射豌豆，旧检查点限制在解锁范围。`recordCheckpoint` 记录起点，`continueCheckpoint` 重建关卡并恢复累计进度，不序列化战斗中的实体数组。

`localization.py` 统一翻译和生成 `-en` 造型变体，按原文本槽宽度适配字形。`langSuffix` 驱动菜单、状态栏、边框、增益和存档文案；`tr` 翻译浏览器对话框。`save_art.py` 生成存档中心面板。资源检查要求每个含中文文案的运行时造型具有英文变体，英文变体不混入中文标签。
