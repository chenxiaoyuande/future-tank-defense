"""Generate English outlined UI variants while preserving artwork and text layout."""
import json
import re
from xml.etree import ElementTree as ET

from art_utils import ROOT, SVG_NS, outline_font, outline_text, write_json
from campaign_art import BOSSES, NAMES, THEMES
from evolution_art import NAMES as EVOLUTION_NAMES

THEMES_EN = ["Twilight Garden", "Frost Court", "Lava Ruins", "Storm Sanctum"]
BOSSES_EN = ["Thorncaller", "Frost Queen", "Magma Behemoth", "Storm Judge"]
LEVELS_EN = ["Grove Outpost","Vine Corridor","Flower Crossroads","Thorn Gallery","Thorn Throne","Snow Frontier","Frozen Dam","Crystal Maze","Frost Fortress","Frost Palace","Ash Gate","Furnace Line","Scorched Rift","Flame Citadel","Magma Core","Thunder Border","Arc Barrier","Storm Maze","Thunder Gallery","Storm Temple"]
EVOLUTION_EN = ["Seed Guardian","Vine Guard","Frost Archer","Flame Knight","Storm Warden","Star Seraph"]

TEXT = {
    **dict(zip(THEMES,THEMES_EN)), **dict(zip(BOSSES,BOSSES_EN)), **dict(zip(NAMES,LEVELS_EN)), **dict(zip(EVOLUTION_NAMES,EVOLUTION_EN)),
    "暮光花园 · 四境远征":"Twilight Garden",
    "守住脑子，让光留下。":"Protect the brain.",
    "得分":"Score", "生命":"Lives", "击退僵尸":"Defeated",
    "WASD/空格/E · 方向键/J/K · P暂停 · R重试 · M首页 · O存档 · T语言":"WASD/Space/E · Arrows/J/K · P Pause · R Retry · M Home · O Save · T EN/ZH",
    "ENTER 前往下一关 · M 返回首页":"ENTER Next stage · M Home",
    "R 重试本关 · M 返回首页":"R Retry stage · M Home",
    "P 继续 · M 返回首页":"P Continue · M Home",
    "S 存档 / B 进化":"S Saves / B Evolve",
    "1  单人作战":"1  Solo", "2  双人合作":"2  Local Co-op",
    "方向键选关 · F/G/H/L 跳转主题 · 金色边框为当前选择":"Arrows: select · F/G/H/L: theme · Gold border: selected",
    "N 继续存档    ENTER 新游戏    B 进化":"N Resume    ENTER New Game    B Evolve",
    "S 存档 · T 中文/EN · 1P WASD/空格/E · 2P 方向键/J/K":"S Saves · T EN/ZH · 1P WASD/Space/E · 2P Arrows/J/K",
    "WASD/空格/E · 方向键/J/K · P暂停 · R重试 · M选关 · O存档 · T语言":"WASD/Space/E · Arrows/J/K · P Pause · R Retry · M Menu · O Save · T EN/ZH",
    "守城":"Defend", "召唤主题":"Summon", "寒冰主题":"Ice", "火焰主题":"Fire", "雷电主题":"Storm",
    "关卡完成":"Stage Clear", "四境远征胜利":"Expedition Complete", "守护结束":"Game Over", "远征暂停":"Paused",
    "脑子安全！下一关恢复双方生命与技能。":"Brain safe! Next stage restores lives and skills.",
    "二十关突破！四大领主已全部击败。":"20 stages cleared. All four lords defeated!",
    "脑子被毁，或所有守护者耗尽生命。":"Brain destroyed or all guardians defeated.",
    "战斗、区域预警和所有冷却计时均已暂停。":"Combat, warning zones and cooldowns are paused.",
    "ENTER 前往下一关 · M 返回选关":"ENTER Next stage · M Menu",
    "R 再战本关 · M 选择新的远征":"R Retry stage · M New expedition",
    "R 重试本关 · M 返回选关":"R Retry stage · M Menu",
    "P 继续 · M 返回选关":"P Continue · M Menu",
    "符阵召唤 · 小心援军":"Summoning · Watch for reinforcements",
    "冰晶预警 · 离开减速区":"Ice warning · Leave the slow zone",
    "火线预警 · 离开燃烧范围":"Fire warning · Leave the marked area",
    "落雷锁定 · 立即离开标记":"Lightning locked · Leave the marker",
    "花园进化研究所":"Evolution Lab",
    "基础形态 + 五档永久进化 · 双人共享 · 仅战斗外升级":"Base + five permanent tiers · Shared · Upgrade outside combat",
    "已解锁":"Unlocked", "已达最高进化":"Maximum evolution",
    "持有金币：":"Coins:", "累计收入：":"Earned:",
    "U 进化  C 备份  V 恢复  M 返回  T 语言":"U Upgrade  C Backup  V Restore  M Back  T EN/ZH",
    "金币":"Coins", "待存":"Unsaved", "损坏":"Invalid",
    "正在读取本机存档":"Loading local save",
    "本机自动存档正常 · 清理浏览器数据会删除存档":"Local autosave ready · Clearing site data deletes saves",
    "保存未成功 · 请用 C 备份，稍后自动重试":"Save failed · C Backup · Retrying automatically",
    "存档损坏，已保留原数据 · 请用 V 恢复备份":"Invalid save preserved · V Restore a valid backup",
    "进化成功！新造型与攻击已解锁":"Evolution complete! Skin and attacks unlocked",
    "金币不足，继续闯关积累金币":"Not enough coins. Defeat more enemies",
    "已到达第五档最高进化":"Maximum evolution tier reached",
    "数据无效或损坏，未替换原存档":"Invalid backup. Original save unchanged",
    "浏览器限制了操作，请检查存储或对话框权限":"Browser blocked storage or dialogs",
    "备份恢复成功":"Backup restored",
    "关卡存档已保存，可在选关界面按 N 继续":"Checkpoint saved. N Resume from the menu",
    "尚无可继续存档，请先开始任意关卡":"No checkpoint yet. Start any stage first",
    "闯关存档中心":"Save Centre",
    "自动保存关卡进度 · O 手动存档 · N 继续游戏":"Stage autosave · O Save checkpoint · N Resume",
    "尚无可继续存档，先开始一局":"No checkpoint yet. Start a game",
    "最高通关：":"Best clear:", "继续模式：单人":"Saved mode: Solo", "继续模式：双人合作":"Saved mode: Local Co-op",
    "开始任意关卡后自动建立存档。":"Starting any stage creates a checkpoint.",
    "继续从关卡起点恢复生命，敌人和道具重新生成。":"Resume at stage start; enemies and pickups reset.",
    "T 切换中文 / English · 自动保存语言选择":"T English / Chinese · Language preference is saved",
    "N 继续  O 存档  C 备份  V 恢复  M 返回  T 语言":"N Resume  O Save  C Backup  V Restore  M Back  T EN/ZH",
    "武器进化！三发扇形导弹已解锁":"Weapon upgraded! Triple missiles unlocked",
    "三发扇形导弹 · 已进化":"Triple missiles · Unlocked", "爆裂种子":"Burst Seed",
    "坚果盾！可抵挡三次伤害":"Nut Shield! Blocks three hits",
    "樱桃炸弹！范围爆炸":"Cherry Bomb! Area blast",
    "蘑菇！移动速度提高":"Mushroom! Move faster",
    "辣椒！火焰弹伤害提高":"Pepper! Increased shot damage",
    "大招就绪 · 按 E 发射":"Ultimate ready · Press E",
}


def translate(value: str) -> str:
    """Translate all current UI patterns; reject missing entries instead of mixing languages."""
    if value in TEXT:
        return TEXT[value]
    m=re.fullmatch(r"第 (\d+) 关 · (.+) · (.+)",value)
    if m:
        return f"Stage {m[1]} · {TEXT[m[2]]} · {TEXT[m[3]]}"
    m=re.fullmatch(r"第(\d+)/20关 · (.+) · (.+)",value)
    if m:
        return f"{m[1]}/20 · {TEXT[m[2]]} · {'Boss' if m[3]=='领主战' else m[3]}"
    m=re.fullmatch(r"(\d)P 生命 (\d)   大招 (.+)",value)
    if m:
        return f"{m[1]}P Lives {m[2]}  Ult {'Ready' if m[3]=='就绪' else m[3].replace('秒','s')}"
    m=re.fullmatch(r"当前：(.+)  ·  普攻 (\d+) 点  ·  大招冷却 ([\d.]+) 秒",value)
    if m:
        return f"{TEXT[m[1]]} · Damage {m[2]} · Ult {m[3]}s"
    patterns=[
        (r"先锋 (\d+) 只 · (.+)",lambda m:f"{m[1]} enemies · {TEXT[m[2]]}"),
        (r"下一档需要 (\d+) 金",lambda m:f"Next tier: {m[1]} coins"),
        (r"第 (\d+) 档",lambda m:f"Tier {m[1]}"),
        (r"(\d+) 金",lambda m:f"{m[1]} coins"),
        (r"继续关卡：第 (\d+) / 20 关",lambda m:f"Checkpoint: Stage {m[1]} / 20"),
        (r"击退 (\d+) / (\d+) · 解锁三发导弹",lambda m:f"Defeated {m[1]}/{m[2]} · Unlock triple missiles"),
        (r"坚果盾 ×(\d+) · (\d+)秒",lambda m:f"Shield x{m[1]} · {m[2]}s"),
        (r"蘑菇加速 \+(\d+)% · (\d+)秒",lambda m:f"Speed +{m[1]}% · {m[2]}s"),
        (r"辣椒增伤 \+(\d+) · (\d+)秒",lambda m:f"Damage +{m[1]} · {m[2]}s"),
        (r"大招冷却：(\d+) 秒",lambda m:f"Ultimate: {m[1]}s"),
    ]
    for pattern,render in patterns:
        match=re.fullmatch(pattern,value)
        if match:
            return render(match)
    for key in sorted(TEXT,key=len,reverse=True):
        value=value.replace(key,TEXT[key])
    assert not re.search(r"[\u4e00-\u9fff]",value),f"Missing translation: {value}"
    return value


def localize(source: str, folder: str, name: str) -> str:
    """Replace outlined label groups with fitted English glyphs in the same slots."""
    document=ET.fromstring(source)
    font=outline_font();units=font["head"].unitsPerEm;cmap=font.getBestCmap()
    def measure(value,size):
        return sum(font["hmtx"][cmap[ord(c)]][0] for c in value)*size/units
    for parent in list(document.iter()):
        for group in list(parent):
            original=group.get("aria-label")
            if not original:
                continue
            english=translate(original)
            first=next(iter(group.iter(f"{{{SVG_NS}}}path")),None)
            if first is None:
                continue
            values=re.search(r"translate\(([-\d.]+) ([-\d.]+)\) scale\(([-\d.]+)",first.get("transform",""))
            assert values is not None,(name,original)
            x,y,scale=map(float,values.groups());size=scale*units
            width=measure(original,size)
            available=width
            if folder=="Notice" and name.startswith("evolution-") and original in EVOLUTION_NAMES:
                available=69
            if folder=="Campaign" and name.startswith("boss-") and original in BOSSES:
                available=64
            new_size=min(size,available/max(measure(english,size),.01)*size)
            left=x+(width-measure(english,new_size))/2
            if folder=="Campaign" and name.startswith("boss-"):
                left=x
            node=ET.Element(f"{{{SVG_NS}}}text",{"x":str(left),"y":str(y),"font-size":str(new_size),"fill":group.get("fill","#f3e6c1")})
            node.text=english
            index=list(parent).index(group);parent.remove(group);parent.insert(index,node)
    return outline_text(ET.tostring(document,encoding="unicode"))


def extend() -> None:
    """Append language variants only to text-bearing runtime costumes."""
    for folder in ["Frame","Notice","Campaign","Wallet","Atmosphere","Buff","Ability"]:
        directory=ROOT/"assets/sprites"/folder
        data=json.loads((directory/"index.json").read_text())
        registered={item["name"] for item in data["costumes"]}
        for item in list(data["costumes"]):
            if item["name"].endswith("-en") or item["name"]+"-en" in registered:
                continue
            source=(directory/item["path"]).read_text()
            if not any(n.get("aria-label") and re.search(r"[\u4e00-\u9fff]",n.get("aria-label")) for n in ET.fromstring(source).iter()):
                continue
            new=dict(item);new["name"]+="-en";new["path"]=new["name"]+".svg"
            (directory/new["path"]).write_text(localize(source,folder,item["name"]),encoding="utf-8")
            data["costumes"].append(new)
        write_json(f"assets/sprites/{folder}/index.json",data)
