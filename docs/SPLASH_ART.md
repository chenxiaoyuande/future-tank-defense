# 首页美术制作记录

首页底图由本会话内置 `image_gen.imagegen` 工具生成。模型为工具默认模型，未指定额外模型、尺寸或质量参数；不透明背景，无参考图片。实际输出为 1448×1086 PNG。

项目素材：`assets/splash-garden-v1.png`；运行时副本：`assets/sprites/Splash/splash.png`。这是原创植物与僵尸主题插画，不使用《植物大战僵尸》的官方图片。

底图本身是静态插画。游戏通过 `Splash.spx` 的镜头缓移和 `HomeDecor.spx` 的漂浮光点组成动态首页；右下角叠加的三名植物角色已移除。首页不依赖 GIF 播放或网络请求。

## 生成提示词

```text
Use case: stylized-concept. Asset type: hand-painted splash-art background for a 4:3 fantasy botanical defense game, intended for a subtly animated title screen. Create a polished 1536x1152 landscape illustration. Moonlit ruined greenhouse and lush twilight garden, turquoise fog, jade leaves, amber lanterns. On the RIGHT HALF a dramatic standoff between three original botanical heroes (a mechanical multi-barrel pea sprout with layered leaves and brass turret, a luminous purple mushroom alchemist with a broad star-speckled cap, and a heavy striped watermelon artillery plant with vine trebuchet) and distant comically menacing armored undead emerging from a ruined stone arch. Detailed appealing painterly forms and rich material shading, sophisticated illustrated game key art, readable silhouettes, hopeful magical atmosphere. LEFT 45 percent is dark low-detail blue-green mist and subtle greenhouse architecture with calm negative space for title and menu buttons; leave that area unobstructed. Keep key plants and undead on the right, lower-right and middle-right; foreground leaves frame the bottom. Separate visual depth planes through mist, suitable for slow camera drift and floating firefly overlays. No typography, no text, no UI, no watermarks, no existing franchise character likenesses. Original pea/mushroom/watermelon archetypes with distinctive craftsmanship, not copies of existing game sprites.
```
