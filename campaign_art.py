"""Generate outlined campaign menus, scenes, cooperative HUD and boss artwork."""
import json
from art_utils import ROOT, svg, write_json


def extend(sprite, text):
    """Extend the original artwork with campaign assets."""
    actor = json.loads((ROOT / "assets/sprites/Actor/index.json").read_text())
    for costume in list(actor["costumes"]):
        if costume["name"].startswith("plant-"):
            duplicate = dict(costume)
            duplicate["name"] = costume["name"].replace("plant-", "partner-")
            source = ROOT / "assets/sprites/Actor" / costume["path"]
            target = source.with_name("partner-" + source.name)
            artwork = source.read_text()
            for old, new in [("#ffda79", "#89dfff"), ("#d88455", "#6378ce"), ("#fff6c2", "#ddf8ff"), ("#8cdb9b", "#8cd1ec")]:
                artwork = artwork.replace(old, new)
            target.write_text(artwork)
            duplicate["path"] = target.name
            actor["costumes"].append(duplicate)
    boss = svg(72,76, '''<ellipse cx="36" cy="68" rx="32" ry="7" fill="#122b36" opacity=".6"/>
<path d="M14 42L8 66h20l8-16 8 16h20L58 42" fill="#455469" stroke="#192f42" stroke-width="3"/>
<path d="M9 25l27-11 27 11-4 28-23 7-23-7Z" fill="#75566d" stroke="#efb783" stroke-width="2"/>
<path d="M8 29L2 43l10 6 8-15m44-5l6 14-10 6-8-15" fill="#98a0a3" stroke="#364451" stroke-width="3"/>
<path d="M22 17L15 2l15 8h12L57 2l-7 16" fill="#ebc886" stroke="#704c5d" stroke-width="2"/>
<path d="M21 14h30l-3 17-12 7-12-7Z" fill="#899b8c" stroke="#304654" stroke-width="2"/>
<path d="M25 22l8 2m6 0l8-2" stroke="#fff1b3" stroke-width="4"/>
<circle cx="36" cy="44" r="10" fill="#452f50" stroke="#e99b9f" stroke-width="2"/>
<path d="M36 35l6 9-6 9-6-9Z" fill="#ffbd9c"/>''')
    (ROOT / "assets/sprites/Actor/boss.svg").write_text(boss)
    actor["costumes"].append({"name": "boss", "path": "boss.svg", "x": 36, "y": 38, "bitmapResolution": 1, "imageWidth": 72, "imageHeight": 76, "faceRight": 0})
    write_json("assets/sprites/Actor/index.json", actor)
    titles = ["暮光花园", "寒霜庭院", "熔岩遗迹"]
    colors = ["#426a58", "#345a76", "#663d47"]
    scenes = []
    for index, color in enumerate(colors, 1):
        art = f'<rect x="12" y="48" width="456" height="275" rx="5" fill="{color}" opacity=".84"/>'
        for y in range(54, 320, 24):
            art += f'<path d="M14 {y}h452" stroke="#e0e6c4" stroke-opacity=".07"/>'
        for x in range(24, 468, 24):
            art += f'<path d="M{x} 50v270" stroke="#e0e6c4" stroke-opacity=".07"/>'
        for n in range(24):
            x, y = 24+(n*83)%430, 59+(n*37)%250
            if index == 2:
                art += f'<path d="M{x} {y}l7 9-7 9-7-9Z" fill="#c8f0ff" opacity=".19"/>'
            elif index == 3:
                art += f'<path d="M{x} {y}l9 7-3 9 8 6" fill="none" stroke="#ffb27d" opacity=".28"/>'
        scenes.append((f"scene-{index}", 480, 360, svg(480, 360, art)))
    sprite("Scene", scenes)
    menus = []
    for mode in [1, 2]:
        for level in [1, 2, 3]:
            art = '<rect width="460" height="312" rx="18" fill="#122c38" stroke="#b7be91" stroke-width="2"/>'
            art += text(24, 37, "暮光花园 · 并肩远征", 23)
            art += text(24, 61, "守住花房，击退军团，挑战三大领主", 11, "#b8cfc2")
            for m, label in [(1, "1  单人作战"), (2, "2  双人合作")]:
                x = 24+(m-1)*210
                art += f'<rect x="{x}" y="78" width="202" height="32" rx="7" fill="{"#526e60" if mode == m else "#233f4a"}" stroke="{"#e9d99e" if mode == m else "#48616a"}"/>'
                art += text(x+101, 99, label, 13, anchor="middle")
            for n, title in enumerate(titles, 1):
                x = 24+(n-1)*140
                art += f'<rect x="{x}" y="124" width="132" height="83" rx="8" fill="{colors[n-1]}" stroke="{"#ffe3a0" if n == level else "#6c8786"}" stroke-width="{3 if n == level else 1}"/>'
                art += text(x+12, 146, ["F", "G", "H"][n-1]+f"  第 {n} 关", 11)
                art += text(x+12, 171, title, 16)
                art += text(x+12, 192, f"{3+n*3} 只先锋 + 领主", 10, "#dce5ca")
            art += text(230, 233, "ENTER  开始远征", 17, "#ffe6ab", "middle")
            art += text(24, 259, "1P  WASD 移动 / 空格射击 / E 大招", 11, "#d5e4ba")
            art += text(24, 279, "2P  方向键移动 / J 射击 / K 大招", 11, "#b4e5ff")
            art += text(24, 298, "P 暂停 · R 重开当前关 · M 返回选关 · 队友之间免伤", 10, "#9db7b5")
            menus.append((f"menu-{mode}-{level}", 460, 312, svg(460, 312, art)))
    for name, title, subtitle, action in [
        ("clear", "领主已击败", "花房安全！下一关恢复双方生命与技能。", "ENTER 前往下一关 · M 返回选关"),
        ("win", "远征胜利", "三大领主已倒下，花园重获安宁。", "R 再战本关 · M 选择新的远征"),
        ("lose", "守护结束", "花房被毁，或所有守护者耗尽生命。", "R 重试本关 · M 返回选关"),
        ("pause", "远征暂停", "战斗与所有冷却计时均已暂停。", "P 继续 · M 返回选关"),
    ]:
        art = '<rect width="420" height="168" rx="15" fill="#182f3c" stroke="#c1b78c" stroke-width="2"/>'
        art += text(210, 52, title, 26, anchor="middle")
        art += text(210, 88, subtitle, 12, "#c4d8cb", "middle")
        art += text(210, 133, action, 14, "#ffe4ab", "middle")
        menus.append((name, 420, 168, svg(420, 168, art)))
    sprite("Notice", menus)
    hud = []
    for p in [1, 2]:
        for life in range(4):
            for cooldown in range(6):
                art = '<rect width="158" height="20" rx="5" fill="#152e3b" opacity=".94"/>'
                art += text(6, 14, f"{p}P 生命 {life}   大招 " + ("就绪" if cooldown == 0 else f"{cooldown}秒"), 11, "#e8dbac" if p == 1 else "#abe3ff")
                hud.append((f"p{p}-{life}-{cooldown}", 158, 20, svg(158, 20, art)))
    for level in range(1, 4):
        for kills in range(13):
            art = '<rect width="218" height="20" rx="5" fill="#152e3b"/>'
            art += text(109, 14, f"第{level}关 · {titles[level-1]}   先锋 {kills}/{3+level*3}", 11, anchor="middle")
            hud.append((f"stage-{level}-{kills}", 218, 20, svg(218, 20, art)))
    for health in range(11):
        art = '<rect width="284" height="22" rx="5" fill="#2d2639" stroke="#cf9490"/>'+text(8, 15, "领主", 11, "#ffd0ad")
        art += '<rect x="42" y="7" width="232" height="8" rx="4" fill="#594454"/>'
        if health:
            art += f'<rect x="42" y="7" width="{232*health/10}" height="8" rx="4" fill="#efaa9a"/>'
        hud.append((f"boss-{health}", 284, 22, svg(284, 22, art)))
    hud.append(("warning", 142, 20, svg(142, 20, '<rect width="142" height="20" rx="5" fill="#813d48"/>'+text(71, 14, "领主蓄力 · 注意弹幕", 11, "#ffe9b9", "middle"))))
    sprite("Campaign", hud)
    data = json.loads((ROOT / "assets/index.json").read_text())
    data["zorder"].insert(0, "Scene")
    data["zorder"].insert(-1, "Campaign")
    write_json("assets/index.json", data)
    write_json("builder-meta.json", {
        "displayName": "暮光花园 · 双人闯关版",
        "description": "本地双人合作，花园、寒霜、熔岩三种场景，自由选关。有限先锋波次后挑战领主，半血狂暴弹幕。",
        "instructions": "1/2选择人数；F/G/H选关；Enter开始/下一关。1P WASD+空格+E；2P方向键+J+K。P暂停，R重开本关，M选关。每人3条生命，花房被毁或全员出局失败。",
    })
