# 开发、构建与发布

[返回项目说明](../README.md) · [项目架构](ARCHITECTURE.md) · [版本与下载](VERSIONS.md)

## 目录约定

| 目录 / 文件 | 职责 |
| --- | --- |
| 根目录 `main.spx` / `*.spx` | XBuilder 舞台和精灵入口，保持引擎原生布局 |
| `assets/` | 运行时图像、双语造型、字体与索引 |
| `tools/` | 资源生成、构建、文档、预览与检查脚本 |
| `tests/` | `.go.txt` 测试源，避免被游戏引擎当作运行代码 |
| `data/` | 从实际规则导出的地图目录 |
| `docs/` / `docs/media/` | 最终文档与展示媒体 |
| `.build/` | 可重新生成的测试工程、快照、临时帧与编译结果 |
| 工作区 `dist/` | 带版本号的项目包；工作区旧文件名保留为兼容副本 |

路径由 `tools/project_paths.py` / `project_paths.cjs` 管理，依据脚本位置定位工程。`xgo_autogen.go` 为引擎自动生成文件，不手工修改；它和 `.build/`、缓存均已加入忽略规则。

## 开发环境

玩家只需在 XBuilder 导入 `.xbp`。下表用于重建工程。

| 工具 | 当前工作区 |
| --- | --- |
| XGo / SPX | v1.7.5 / v3.3.0 |
| Go | 模块声明 1.25.0，本机工具链 1.27.3；可用 `GARDEN_GO` 指定可执行文件 |
| Python | WSL Python 3；依赖见 `tools/requirements.txt` |
| 字体 | `/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc` |
| Node / Sharp | 渲染在 Windows 运行；依赖见 `tools/package.json`，支持 `GARDEN_SHARP_MODULE` 指定模块 |

当前 Python / Go 工作流在 WSL 中运行，工作目录为 `/mnt/e/Code/tank/garden-survival`；Windows 渲染工作目录为 `E:\Code\tank\garden-survival`。现有依赖可直接使用，迁移电脑时可执行 `python3 -m pip install -r tools/requirements.txt`，并在 Windows 执行 `npm --prefix tools install`。

## 常用命令

在工程根目录执行 `python3 tools/project.py --help` 查看入口。

| 命令 | 结果 |
| --- | --- |
| `python3 tools/project.py test` | 74 项实际规则测试 + 4 项 WebAssembly 存储测试 |
| `python3 tools/project.py build` | 生成文档、全部资源与当前版本项目包 |
| `python3 tools/project.py compile` | 编译到 `.build/bin/game.wasm` |
| `python3 tools/project.py docs` | 同步 README、中英文指南与版本索引 |
| `python3 tools/project.py preview` | 生成首页、职业、脑子状态的 SVG 预览 |
| `python3 tools/project.py media` | 编码渲染后的 PNG / GIF 到 `docs/media/` |
| `python3 tools/project.py package` | 打包已生成文件，更新版本清单与兼容副本 |
| `python3 tools/project.py check --releases` | 检查文档、当前包和六份历史包的版本身份 |

只有重新生成资源时才需要 `build`；仅修改文档可执行 `docs → package → check`。修改版本后必须重建资源，才能更新首页的版本文字。

## 完整发布顺序

WSL，工程根目录：

```bash
python3 tools/project.py test
python3 tools/project.py build
python3 tools/project.py compile
python3 tools/project.py preview
```

Windows PowerShell，同一个工程目录：

```powershell
node tools/render_frontend.cjs
```

WSL：

```bash
python3 tools/project.py media
python3 tools/project.py docs
python3 tools/project.py package
python3 tools/project.py check --releases
```

前后两次打包的目的不同：`build` 先生成可运行资源；最后的 `package` 收入最新媒体与文档，不重复生成资源。所有检查通过后，在 XBuilder 导入 `dist/` 中的当前版本继续实机验收。

## 文档内容入口

- README / REAMD：修改 `tools/write_docs.py`，不要只修改生成文件。
- 职业、存档、英文指南：修改 `tools/write_profession_docs.py`。
- 版本表：修改 `releases.json`，由 `tools/write_versions.py` 生成。
- 玩法、架构、FAQ、开发说明及更新记录：直接修改对应 `docs/*.md`。

`docs` 命令会生成工作区与工程内两套 README，各自使用正确的相对链接。`REAMD.md` 是兼容命名，与同目录 README 内容一致。

## 版本管理

版本从 v1.0.0 到当前 v1.5.0，按现有项目包追补，没有虚构独立历史包或发布日期。`releases.json` 是唯一版本配置；`version.json`、项目名称、首页页脚和包文件名均由它生成。

发布新功能时追加版本记录并更新 `currentVersion`，不要重用已有的带版本号归档。`python3 tools/project.py number-archives` 用于已有历史包补号，会逐文件确认历史游戏脚本和素材未改变。

游戏版本与 TG1 / TG2 / TG3 存档格式是不同概念。调整版本号不会清空玩家进度，也不改变浏览器存储键。

## 其他媒体

正式图片 / GIF 位于 `docs/media/`；临时 SVG / PNG 位于 `.build/previews/`，战斗快照位于 `.build/snapshots/`。首页底图保留在 `assets/splash-garden-v1.png`，构建时无需重新生成，提示词见 [美术记录](SPLASH_ART.md)。

更新战斗预览可在 Windows 执行 `node tools/render_campaign.cjs`。更新 Boss 动图依次执行 WSL `python3 tools/build_docs_media.py` → Windows `node tools/render_docs_media.cjs` → WSL `python3 tools/encode_docs_gifs.py`。

Boss 媒体脚本包含历史选关图片来源；最后再完成首页 / 职业的 `preview → render → media`，避免旧选关图覆盖新版。旧的 `preview_evolution.py` 与 `preview_bilingual.py` 保留作历史展示，不是当前主入口。

## 检查范围

| 检查 | 能确认 |
| --- | --- |
| 规则与存储测试 | 真实舞台规则、三职业、屏障、Boss、锁关、存档及网页适配 |
| WebAssembly 编译 | 当前 XGo / SPX 下的语法和构建兼容性 |
| 资源校验 | 造型、字体、地图、双语索引和文件路径完整 |
| 文档与版本校验 | 链接、图片 / GIF、版本清单、文件名与历史兼容副本一致 |
| 素材合成预览 | 布局、造型辨识与技能时序示意 |

这些检查不替代 XBuilder 在线运行。在线整体验收仍待完成，应继续实际检查：首页四入口、锁关、双人分选职业、攻击、屏障三秒计时、升级扣费、刷新继续和语言保存。受控测试通关也不等于真人平衡性试玩。
