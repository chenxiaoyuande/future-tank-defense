"""Build the four-theme, twenty-stage campaign artwork from tested map data."""
import json

from art_utils import ROOT, svg, write_json
from boss_art import POSES, boss_art

THEMES = ["暮光花园", "寒霜庭院", "熔岩遗迹", "雷鸣圣域"]
BOSSES = ["荆棘召唤者", "寒霜女王", "熔岩巨兽", "雷霆审判者"]
COLORS = ["#365d4e", "#294c69", "#613540", "#3f3a68"]
ACCENTS = ["#b5e493", "#a5eaff", "#ffbb7b", "#d8bcff"]
WARNINGS = ["符阵召唤 · 小心援军", "冰晶预警 · 离开减速区", "火线预警 · 离开燃烧范围", "落雷锁定 · 立即离开标记"]
NAMES = [
    "林间前哨", "藤蔓长廊", "花影岔路", "荆棘回廊", "荆棘王座",
    "初雪边境", "冰封堤坝", "碎晶迷阵", "霜环要塞", "寒霜王庭",
    "灰烬入口", "熔炉防线", "焦土裂隙", "赤焰堡垒", "熔岩核心",
    "雷云边境", "电弧屏障", "风暴迷阵", "天雷回廊", "雷霆圣殿",
]


def zone_art(kind: int, active: bool, frame: int) -> str:
    """Match visible warning footprints to the collision geometry."""
    color = ACCENTS[kind]
    opacity = .24 if active else [.08, .16][frame]
    if kind == 2:
        body = f'<rect x="15" y="15" width="50" height="50" rx="4" fill="{color}" fill-opacity="{opacity}" stroke="{color}" stroke-width="2" stroke-dasharray="5 3"/>'
        if active:
            for x in [24, 40, 56]:
                body += f'<path d="M{x} 61q-12-13 0-28l3 11 5-7q10 19-8 24Z" fill="#ffc386" stroke="#ff7954"/>'
        else:
            body += '<path d="M30 48l10-20 10 20Z" fill="none" stroke="#ffdca4" stroke-width="2"/>'
    else:
        radius = [24, 36, 25, 30][kind]
        body = f'<circle cx="40" cy="40" r="{radius}" fill="{color}" fill-opacity="{opacity}" stroke="{color}" stroke-width="2" stroke-dasharray="5 3"/>'
        body += f'<circle cx="40" cy="40" r="{radius-5}" fill="none" stroke="{color}" opacity=".5"/>'
        if kind == 0:
            body += '<path d="M40 18l19 33H21Zm0 44L21 29h38Z" fill="none" stroke="#c4ed9f"/>'
        if kind == 1:
            body += '<path d="M40 17v46M20 28l40 24M20 52l40-24m-29-6l9 10 9-10m-18 36l9-10 9 10" stroke="#bdeeff" stroke-width="2" fill="none"/>'
        if kind == 3:
            body += '<path d="M6 40h15m38 0h15M40 6v15m0 38v15" stroke="#e2c6ff" stroke-width="2"/>'
            if active:
                body += '<path d="M45 3L29 38h14L32 72l23-42H41Z" fill="#fff2ff" stroke="#caa9ff" stroke-width="2"/>'
            else:
                body += '<path d="M43 26L33 42h8l-3 13 11-19h-8Z" fill="#e7d0ff"/>'
    return svg(80, 80, body)


def extend(sprite, text):
    """Generate campaign resources using maps exported by the actual SPX tests."""
    catalog = json.loads((ROOT / "data/level-catalog.json").read_text(encoding="utf-8"))
    assert len(catalog) == 20
    actor_dir = ROOT / "assets/sprites/Actor"
    actor = json.loads((actor_dir / "index.json").read_text())
    for costume in list(actor["costumes"]):
        if costume["name"].startswith("plant-"):
            duplicate = dict(costume)
            duplicate["name"] = costume["name"].replace("plant-", "partner-")
            source = actor_dir / costume["path"]
            target = source.with_name("partner-" + source.name)
            artwork = source.read_text()
            for old, new in [("#ffda79", "#89dfff"), ("#d88455", "#6378ce"), ("#fff6c2", "#ddf8ff"), ("#8cdb9b", "#8cd1ec")]:
                artwork = artwork.replace(old, new)
            target.write_text(artwork, encoding="utf-8")
            duplicate["path"] = target.name
            actor["costumes"].append(duplicate)
    extras = [(f"boss-{n}", 72, 76, boss_art(n)) for n in range(4)]
    for theme in range(4):
        for pose, frame in POSES:
            extras.append((f"boss-{theme}-{pose}-{frame}", 72, 76, boss_art(theme, pose, frame)))
    for kind in range(4):
        for active in [False, True]:
            for frame in range(2):
                extras.append((f"zone-{kind}-{'active' if active else 'warn'}-{frame}", 80, 80, zone_art(kind, active, frame)))
    for name, width, height, content in extras:
        (actor_dir / f"{name}.svg").write_text(content, encoding="utf-8")
        actor["costumes"].append({"name": name, "path": f"{name}.svg", "x": width/2, "y": height/2, "bitmapResolution": 1, "imageWidth": width, "imageHeight": height, "faceRight": 0})
    write_json("assets/sprites/Actor/index.json", actor)
    scenes = []
    for stage in catalog:
        level, theme = stage["level"], stage["theme"]
        art = f'<rect x="12" y="48" width="456" height="275" rx="5" fill="{COLORS[theme]}" opacity=".88"/>'
        for y in range(54, 320, 24):
            art += f'<path d="M14 {y}h452" stroke="{ACCENTS[theme]}" stroke-opacity=".07"/>'
        for x in range(24, 468, 24):
            art += f'<path d="M{x} 50v270" stroke="{ACCENTS[theme]}" stroke-opacity=".07"/>'
        for n in range(24):
            x, y = 24+(n*83+level*11)%430, 59+(n*37+level*7)%250
            if theme == 0:
                art += f'<path d="M{x} {y}q7-9 11-2-8 8-11 2" fill="#a3c886" opacity=".16"/>'
            if theme == 1:
                art += f'<path d="M{x} {y}l6 8-6 8-6-8Z" fill="#c8f0ff" opacity=".18"/>'
            if theme == 2:
                art += f'<path d="M{x} {y}l9 7-3 9 8 6" fill="none" stroke="#ffb27d" opacity=".25"/>'
            if theme == 3:
                art += f'<path d="M{x} {y}h12v8h9m-10 0v9" fill="none" stroke="#d8bfff" opacity=".2"/>'
        scenes.append((f"scene-{level}", 480, 360, svg(480, 360, art)))
    sprite("Scene", scenes)
    menus = []
    for mode in [1, 2]:
        for selected in catalog:
            level, theme = selected["level"], selected["theme"]
            art = '<rect width="460" height="320" rx="16" fill="#122c38" stroke="#b7be91" stroke-width="2"/>'
            art += text(20, 30, "暮光花园 · 四境远征", 22)
            art += text(440, 29, "S 存档 / B 进化", 10, "#ffe09a", "end")
            for m, label in [(1, "1  单人作战"), (2, "2  双人合作")]:
                x = 20+(m-1)*214
                art += f'<rect x="{x}" y="41" width="206" height="27" rx="6" fill="{"#526e60" if mode == m else "#233f4a"}" stroke="{"#e9d99e" if mode == m else "#48616a"}"/>'
                art += text(x+103, 59, label, 12, anchor="middle")
            art += text(20, 83, "方向键选关 · F/G/H/L 跳转主题 · 金色边框为当前选择", 9, "#a9c1b7")
            for stage in catalog:
                n, t = stage["level"], stage["theme"]
                x, y = 20+((n-1)%5)*85, 91+((n-1)//5)*38
                stroke = "#ffe2a0" if n == level else "#57717a"
                art += f'<rect x="{x}" y="{y}" width="79" height="33" rx="5" fill="{COLORS[t]}" stroke="{stroke}" stroke-width="{2.5 if n == level else .8}"/>'
                art += text(x+6, y+14, f"{n:02d}", 12, ACCENTS[t])
                art += text(x+5, y+27, "BOSS" if stage["boss"] else "守城", 7, "#e1dfc1")
                for r, row in enumerate(stage["rows"]):
                    for c, cell in enumerate(row):
                        if cell != "0":
                            art += f'<rect x="{x+31+c*2.1:.1f}" y="{y+7+r*2.5}" width="1.8" height="2.1" fill="{ACCENTS[t]}" opacity=".8"/>'
            detail = BOSSES[theme] if selected["boss"] else f'先锋 {selected["target"]} 只'
            art += text(20, 254, f"第 {level:02d} 关 · {THEMES[theme]} · {NAMES[level-1]}", 12, ACCENTS[theme])
            art += text(20, 273, detail + " · " + ["召唤主题", "寒冰主题", "火焰主题", "雷电主题"][theme], 10, "#c6d7c5")
            art += text(230, 296, "N 继续存档    ENTER 新游戏    B 进化", 13, "#ffe6ab", "middle")
            art += text(230, 313, "S 存档 · T 中文/EN · 1P WASD/空格/E · 2P 方向键/J/K", 8, "#a9c1b7", "middle")
            menus.append((f"menu-{mode}-{level}", 460, 320, svg(460, 320, art)))
    for name, title, subtitle, action in [
        ("clear", "关卡完成", "脑子安全！下一关恢复双方生命与技能。", "ENTER 前往下一关 · M 返回首页"),
        ("win", "四境远征胜利", "二十关突破！四大领主已全部击败。", "R 再战本关 · M 选择新的远征"),
        ("lose", "守护结束", "脑子被毁，或所有守护者耗尽生命。", "R 重试本关 · M 返回首页"),
        ("pause", "远征暂停", "战斗、区域预警和所有冷却计时均已暂停。", "P 继续 · M 返回首页"),
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
            for cooldown in range(8):
                art = '<rect width="158" height="20" rx="5" fill="#152e3b" opacity=".94"/>'
                art += text(6, 14, f"{p}P 生命 {life}   大招 " + ("就绪" if cooldown == 0 else f"{cooldown}秒"), 11, "#e8dbac" if p == 1 else "#abe3ff")
                hud.append((f"p{p}-{life}-{cooldown}", 158, 20, svg(158, 20, art)))
    for stage in catalog:
        n, theme, target = stage["level"], stage["theme"], stage["target"]
        for kills in range(target+1):
            label = f"第{n:02d}/20关 · {NAMES[n-1]} · "
            label += "领主战" if stage["boss"] else f"{kills}/{target}"
            art = '<rect width="218" height="20" rx="5" fill="#152e3b"/>'
            art += text(109, 14, label, 10, ACCENTS[theme], "middle")
            hud.append((f"stage-{n}-{kills}", 218, 20, svg(218, 20, art)))
    for theme in range(4):
        for health in range(11):
            art = '<rect width="284" height="22" rx="5" fill="#252a3a" stroke="#9c95aa"/>'
            art += text(7, 15, BOSSES[theme], 10, ACCENTS[theme])
            art += '<rect x="74" y="7" width="200" height="8" rx="4" fill="#4d455c"/>'
            if health:
                art += f'<rect x="74" y="7" width="{200*health/10}" height="8" rx="4" fill="{ACCENTS[theme]}"/>'
            hud.append((f"boss-{theme}-{health}", 284, 22, svg(284, 22, art)))
        art = '<rect width="218" height="20" rx="5" fill="#263448" stroke="'+ACCENTS[theme]+'"/>'
        art += text(109, 14, WARNINGS[theme], 11, ACCENTS[theme], "middle")
        hud.append((f"warning-{theme}", 218, 20, svg(218, 20, art)))
    sprite("Campaign", hud)
    data = json.loads((ROOT / "assets/index.json").read_text())
    data["zorder"].insert(0, "Scene")
    data["zorder"].insert(-1, "Campaign")
    write_json("assets/index.json", data)
    write_json("builder-meta.json", {
        "displayName": "暮光花园 · 20关中英文存档版",
        "description": "20张地图、四主题领主、本地双人、五阶进化。保存关卡起点、单双人、得分、金币与进化，兼容旧存档；T键中英文切换并记住语言。",
        "instructions": "T中英文；选关N继续存档，Enter新游戏；战斗外S存档中心，B进化；O手动保存关卡起点，C备份/V恢复（存档或进化界面），M返回。1P WASD+空格+E；2P方向键+J+K；P暂停；R重试。使用同浏览器同站点本机存储，非云存档。",
    })
