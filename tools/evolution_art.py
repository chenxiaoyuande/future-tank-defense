"""Build five permanent evolution skins, matching projectiles and the metagame UI."""
import json
import re

from art_utils import ROOT, svg, write_json

NAMES = ["基础守护者", "青藤卫士", "冰晶射手", "赤焰战将", "雷霆守望", "星辉圣灵"]
COLORS = ["#c5df9b", "#88d7ac", "#98deff", "#ffab79", "#c5a4fa", "#ffe09a"]
COSTS = [100, 250, 500, 900, 1500]


def tint(source: str, color: str) -> str:
    """Retain source shading while shifting illuminated surfaces to the tier colour."""
    target = [int(color[n:n+2], 16) for n in [1, 3, 5]]

    def replace(match):
        original = [int(match[0][n:n+2], 16) for n in [1, 3, 5]]
        brightness = max(original)/255
        if brightness < .28 or min(original) > 230:
            return match[0]
        ratio = .45+.55*brightness
        result = [round(c*ratio) for c in target]
        if brightness > .85:
            result = [round(c*.72+255*.28) for c in result]
        return "#"+"".join(f"{c:02x}" for c in result)

    return re.sub(r"#[0-9a-fA-F]{6}", replace, source)


def overlay(source: str, body: str) -> str:
    """Add vector details without changing the original anchor or displayed bounds."""
    return source.replace("</svg>", body+"</svg>")


def skin(source: str, tier: int, player: int) -> str:
    """Change both palette and silhouette; retain a numbered player badge."""
    color = COLORS[tier]
    art = tint(source, color)
    extra = ''
    if tier == 1:
        extra += '<path d="M10 28Q0 17 2 32l10 6m18-10q10-11 8 4l-10 6" fill="#76bc8f" stroke="#c3eeb5" stroke-width=".7"/>'
        extra += '<path d="M16 5l4-5 4 5-4 3Z" fill="#a9edbb" stroke="#376653" stroke-width=".7"/>'
    if tier == 2:
        extra += '<path d="M3 30L1 19l7 5 3-7 2 16m24-3l2-11-7 5-3-7-2 16" fill="#89cbec" stroke="#d8f7ff" stroke-width=".7"/>'
        extra += '<path d="M14 6l1-6 5 4 5-4 1 6-6 3Z" fill="#c3f0ff" stroke="#4b8aa7" stroke-width=".7"/>'
    if tier == 3:
        extra += '<path d="M9 36Q0 31 5 19l3 7 4-3 2 12m17 1q9-5 4-17l-3 7-4-3-2 12" fill="#f5a06c" stroke="#ffe3a6" stroke-width=".7"/>'
        extra += '<path d="M17 7l-2-6 5 3 5-3-2 6Z" fill="#ffcc8c" stroke="#a65c52" stroke-width=".7"/>'
    if tier == 4:
        extra += '<path d="M3 15v17m34-17v17M1 20h5m-5 4h5m28-4h5m-5 4h5" stroke="#d8c5ff" stroke-width="1"/>'
        extra += '<circle cx="3" cy="13" r="2" fill="#e8dfff"/><circle cx="37" cy="13" r="2" fill="#e8dfff"/>'
        extra += '<path d="M21 0l-5 5h4l-1 5 6-7h-4Z" fill="#f3eaff" stroke="#9275c5" stroke-width=".5"/>'
    if tier == 5:
        extra += '<path d="M11 36L1 24l10 3-9-10 12 8m15 11l10-12-10 3 9-10-12 8" fill="#e7d095" stroke="#fff2c9" stroke-width=".8"/>'
        extra += '<ellipse cx="20" cy="3" rx="9" ry="2" fill="none" stroke="#ffe9a8" stroke-width="1.5"/>'
        extra += '<path d="M20 0l2 4 4 1-4 1-2 4-2-4-4-1 4-1Z" fill="#fff8d8"/>'
    extra += f'<path d="M16 32h8l-1 7h-6Z" fill="#274c54" stroke="{color}" stroke-width=".7"/>'
    extra += f'<path d="M20 32l3 3-3 4-3-4Z" fill="{color}"/>'
    badge = "#e6cf91" if player == 1 else "#9be5ff"
    extra += f'<circle cx="34" cy="37" r="4" fill="#153949" stroke="{badge}" stroke-width=".8"/>'
    # Badge strokes avoid introducing tiny font dependencies in the animated sprites.
    if player == 1:
        extra += f'<path d="M33 36l1-1v4m-1 0h2" fill="none" stroke="{badge}" stroke-width=".8"/>'
    else:
        extra += f'<path d="M33 36q0-2 2-1 1 1-2 3h3" fill="none" stroke="{badge}" stroke-width=".8"/>'
    return overlay(art, extra)


def projectile(source: str, tier: int, width: int, height: int, name: str) -> str:
    """Use faceted, flame, electric and star details on matching tinted ballistics."""
    color = COLORS[tier]
    art = tint(source, color)
    cx, cy = width/2, height/2
    radius = min(width, height)*(.32 if name.startswith("burst") else .22)
    extra = ''
    if tier == 1:
        extra = f'<ellipse cx="{cx}" cy="{cy}" rx="{radius}" ry="{radius*.7}" fill="none" stroke="{color}" stroke-width="1"/>'
    elif tier == 2:
        extra = f'<path d="M{cx} {cy-radius}l{radius} {radius} {-radius} {radius} {-radius} {-radius}Z" fill="none" stroke="#e4fcff" stroke-width="1"/>'
    elif tier == 3:
        extra = f'<path d="M{cx} {cy-radius}q{-radius} {radius} 0 {radius*2} {radius} {-radius} 0 {-radius*2}Z" fill="none" stroke="#ffebbd" stroke-width="1"/>'
    elif tier == 4:
        extra = f'<path d="M{cx+radius/2} {cy-radius}l{-radius} {radius}h{radius}l{-radius} {radius}" fill="none" stroke="#f0e4ff" stroke-width="1.2"/>'
    else:
        extra = f'<path d="M{cx-radius} {cy}Q{cx} {cy} {cx} {cy-radius}Q{cx} {cy} {cx+radius} {cy}Q{cx} {cy} {cx} {cy+radius}Q{cx} {cy} {cx-radius} {cy}Z" fill="#fff4ce" opacity=".85"/>'
    return overlay(art, extra)


def extend(sprite, text) -> None:
    """Append evolution assets and layer the wallet above menus."""
    actor_dir = ROOT / "assets/sprites/Actor"
    actor = json.loads((actor_dir / "index.json").read_text())
    original = list(actor["costumes"])
    for tier in range(1, 6):
        for item in original:
            name = item["name"]
            if name.startswith("plant-"):
                for player in [1, 2]:
                    new = dict(item)
                    new["name"] = f"evo-{tier}-p{player}-"+name.removeprefix("plant-")
                    new["path"] = new["name"]+".svg"
                    source = (actor_dir / item["path"]).read_text()
                    (actor_dir / new["path"]).write_text(skin(source,tier,player), encoding="utf-8")
                    actor["costumes"].append(new)
            elif re.match(r"^(seed|missile|fire-seed|fire-missile|mega|burst)-\d+$", name):
                new = dict(item)
                new["name"] = f"evo-{tier}-"+name
                new["path"] = new["name"]+".svg"
                source = (actor_dir / item["path"]).read_text()
                art = projectile(source,tier,item["imageWidth"],item["imageHeight"],name)
                (actor_dir / new["path"]).write_text(art, encoding="utf-8")
                actor["costumes"].append(new)
    write_json("assets/sprites/Actor/index.json",actor)
    # Append trails to the existing atmosphere sprite without changing its anchors.
    directory = ROOT / "assets/sprites/Atmosphere"
    effects = json.loads((directory / "index.json").read_text())
    for item in list(effects["costumes"]):
        if item["name"] in ["seed-trail","missile-trail","mega-trail","fire-trail"]:
            for tier in range(1,6):
                new = dict(item); new["name"] = f'evo-{tier}-'+item["name"]; new["path"] = new["name"]+".svg"
                (directory / new["path"]).write_text(tint((directory/item["path"]).read_text(),COLORS[tier]),encoding="utf-8")
                effects["costumes"].append(new)
    write_json("assets/sprites/Atmosphere/index.json",effects)
    notice_path = ROOT / "assets/sprites/Notice/index.json"
    notice = json.loads(notice_path.read_text())
    for tier in range(6):
        art = '<rect width="460" height="320" rx="16" fill="#122c38" stroke="#d5c28d" stroke-width="2"/>'
        art += text(20,30,"花园进化研究所",22)
        art += text(20,49,"基础形态 + 五档永久进化 · 双人共享 · 仅战斗外升级",10,"#b4cdbf")
        for n in range(1,6):
            x=20+(n-1)*86
            art += f'<rect x="{x}" y="64" width="77" height="105" rx="7" fill="{"#304f50" if n<=tier else "#203846"}" stroke="{COLORS[n] if n<=tier else "#526772"}" stroke-width="{2 if n==tier else 1}"/>'
            art += text(x+38,81,NAMES[n],10,COLORS[n],"middle")
            source=(actor_dir/f"evo-{n}-p1-up-0.svg").read_text()
            art += f'<g transform="translate({x+18} 87)">{source}</g>'
            art += text(x+38,150,"已解锁" if n<=tier else f"{COSTS[n-1]} 金",10,COLORS[n],"middle")
            art += text(x+38,162,f"第 {n} 档",8,"#b4c9bf","middle")
        art += text(20,188,f"当前：{NAMES[tier]}  ·  普攻 {1+tier//2} 点  ·  大招冷却 {5-tier*.3:.1f} 秒",11,COLORS[tier])
        art += text(20,214,"持有金币：",12,"#ffe09a")
        art += text(255,214,"已达最高进化" if tier==5 else f"下一档需要 {COSTS[tier]} 金",11,"#d5dfc4")
        art += text(20,237,"累计收入：",12,"#b4c9bf")
        art += text(230,312,"U 进化  C 备份  V 恢复  M 返回  T 语言",12,"#ffe09a","middle")
        name=f"evolution-{tier}"
        (notice_path.parent/f"{name}.svg").write_text(svg(460,320,art),encoding="utf-8")
        notice["costumes"].append({"name":name,"path":name+".svg","x":230,"y":160,"bitmapResolution":1,"imageWidth":460,"imageHeight":320})
    write_json("assets/sprites/Notice/index.json",notice)
    wallet=[]
    for n in range(10):
        wallet.append((f"coin-{n}",10,18,svg(10,18,text(5,14,str(n),12,"#ffe3a1","middle"))))
    for n,label in enumerate(["金币","金币","待存","损坏"]):
        wallet.append((f"coin-label-{n}",46,18,svg(46,18,'<rect width="46" height="18" rx="4" fill="#173443"/>'+text(23,13,label,11,"#ffe3a1" if n<2 else "#ffb68f","middle"))))
    for n,label in enumerate(["正在读取本机存档", "本机自动存档正常 · 清理浏览器数据会删除存档", "保存未成功 · 请用 C 备份，稍后自动重试", "存档损坏，已保留原数据 · 请用 V 恢复备份"]):
        wallet.append((f"save-{n}",430,18,svg(430,18,text(215,13,label,10,"#a3d6b7" if n==1 else "#ffc19b","middle"))))
    for n,label in enumerate(["", "进化成功！新造型与攻击已解锁", "金币不足，继续闯关积累金币", "已到达第五档最高进化", "数据无效或损坏，未替换原存档", "浏览器限制了操作，请检查存储或对话框权限", "备份恢复成功"]):
        wallet.append((f"notice-{n}",430,18,svg(430,18,text(215,13,label,11,"#ffe3a1","middle"))))
    sprite("Wallet",wallet)
    data=json.loads((ROOT/"assets/index.json").read_text());data["zorder"].append("Wallet");write_json("assets/index.json",data)
