# 图片与动图来源

[返回项目说明](../../README.md) · [重建媒体的方法](../DEVELOPMENT.md)

本文媒体由项目矢量素材、原创生成插画与实际逻辑快照合成，不使用参考仓库的截图或动图。首页底图的生成方式与提示词见 [首页美术记录](../SPLASH_ART.md)。

| 文件 | 展示内容 | 生成方式 |
| --- | --- | --- |
| [brain-barrier.png](brain-barrier.png) | 脑子与屏障状态 | 使用实际完整、半耐久与暴露造型合成 |
| [animated-home.gif](animated-home.gif) | 动态首页 | 按 `Splash` / `HomeDecor` 动画公式及真实按钮素材合成，36 帧，每帧 100 毫秒 |
| [profession-evolution.gif](profession-evolution.gif) | 三职业 × 六形态动作 | 真实玩家造型逐帧合成，6 帧，每帧 160 毫秒 |
| [profession-routes.png](profession-routes.png) | 三条进化路线总览 | 新版 SVG 原始造型放大 |
| [class-select.png](class-select.png) | 双人分别选职业 | 新版页面和职业卡合成 |
| [language-settings.png](language-settings.png) | 英文设置页面 | 新版双语页面与按钮合成 |
| [boss-poses.gif](boss-poses.gif) | 四个领主的待机、施法、受击、狂暴 | 按实际造型索引拼接帧；28 帧、每帧 140 毫秒、循环播放 |
| [boss-warnings.gif](boss-warnings.gif) | 召唤 / 冰区 / 火线 / 雷电的预警与生效阶段 | 使用实际区域素材与规则预警时长生成示意；50 帧、每帧 100 毫秒 |
| [level-select.png](level-select.png) | 20 关选择界面 | 实际菜单 SVG 与场景合成 |
| [coop-garden.png](coop-garden.png) | 双人花园战场 | 实际素材和逻辑测试快照合成 |
| [four-bosses.png](four-bosses.png) | 四个主题的 Boss 战场 | 四张实际素材快照预览拼合 |
| [boss-detail.png](boss-detail.png) | 精修造型放大图与游戏原尺寸 | 使用实际 Boss SVG 绘制联系表 |
| [thunder-arena.png](thunder-arena.png) | 最终雷电领主场景 | 实际素材和逻辑快照合成 |

除标注的本地浏览器存档验证截图外，这些媒体用于项目介绍、布局检查和规则说明，不是在线实机截图或录像。技能动图中的角色移动仅示意如何离开标记，不运行完整战斗模拟，也不证明实际帧率、操作手感或游戏平衡。

GIF 使用共享调色板以减少闪烁。临时帧位于工程的 `.build/previews/`，不随 `.xbp` 项目分发；最终 PNG 与 GIF 保存在此目录，并随说明文档打包。

## 进化与存档媒体

| 文件 | 来源 |
| --- | --- |
| [evolution-lineup.png](evolution-lineup.png) | 历史单路线版本，保留作迭代记录；新版见三职业路线图 |
| [evolution-shop.png](evolution-shop.png) | 实际进化面板与示例余额合成，非赠送金币 |
| [progress-browser-proof.png](progress-browser-proof.png) | 实际浏览器截图，开发检查页运行游戏 Go / WebAssembly 存档模块 |

## 中英文与关卡存档

- [bilingual-save.png](bilingual-save.png)：历史 TG2 版本的中英文存档面板、英文选关与进化素材合成。
- [checkpoint-browser-proof.png](checkpoint-browser-proof.png)：本地浏览器运行实际 Go / WebAssembly 存档代码，刷新并继续第7关双人模式与英文选择后的真实截图。开发验证页不等于 XBuilder 在线完整对局。
