"""Clickable, bilingual front end using the game's native sprite system."""
import json
import shutil
from classes_art import hero, ROUTES_ZH, ROUTES_EN, ROLES_ZH, ROLES_EN, COLORS
from art_utils import ROOT, svg, write_json, outline_font
from save_art import append
from campaign_art import NAMES
from localization import LEVELS_EN
from release_info import current_release


def t(x, y, value, size=12, color="#e9e8ce", anchor="start", width=440):
    font=outline_font(); cmap=font.getBestCmap()
    measured=sum(font["hmtx"][cmap[ord(c)]][0] for c in value)*size/font["head"].unitsPerEm
    size=min(size,size*width/max(measured,1))
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{value}</text>'


def plant(role, tier, x, y, scale=1, frame=0):
    body=hero(role,tier,1,1,frame).split(">",1)[1].rsplit("</svg>",1)[0]
    return f'<svg x="{x}" y="{y}" width="{48*scale}" height="{52*scale}" viewBox="0 0 48 52">{body}</svg>'


def panel():
    return '<rect x="10" y="10" width="460" height="340" rx="18" fill="#102b32" fill-opacity=".97" stroke="#7e9676"/><path d="M30 66H450" stroke="#48685e"/>'


def button(label, active=False, w=190, h=36, accent="#bdd594"):
    return svg(w,h,f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="8" fill="{"#47634e" if active else "#1a3b3c"}" stroke="{accent if active else "#627b68"}" stroke-width="{2 if active else 1}"/>'+t(w/2,h/2+4,label,13,accent if active else "#d4dec7","middle",w-16))


def extend(sprite, _text):
    release=current_release()
    ui=[]; cards=[]
    stage_en=LEVELS_EN
    desc_zh=[("高速直射 / 多管连射","E：爆裂种子"),("穿透孢子 / 群体消耗","E：持续孢子云"),("越墙抛射 / 范围伤害","E：巨型西瓜轰炸")]
    desc_en=[("Rapid shots / Multi-barrel","E: Explosive seed"),("Piercing spores / Area DoT","E: Lingering spore cloud"),("Lob over walls / Area impact","E: Giant melon bombardment")]
    for en in [False,True]:
        suffix="-en" if en else ""
        role_names=ROLES_EN if en else ROLES_ZH; routes=ROUTES_EN if en else ROUTES_ZH
        descriptions=desc_en if en else desc_zh
        def notice(name,art):append("Notice",name+suffix,480,360,svg(480,360,art))
        home='<defs><linearGradient id="shade"><stop stop-color="#071c23" stop-opacity=".96"/><stop offset=".48" stop-color="#102b30" stop-opacity=".78"/><stop offset=".82" stop-color="#102b30" stop-opacity="0"/></linearGradient></defs><rect width="480" height="360" fill="url(#shade)"/>'
        home+=t(24,35,"TWILIGHT GARDEN",10,"#b8c6a0")
        home+=t(24,77,"暮光花园" if not en else "Twilight Garden",30,"#f0e0ad",width=224)
        home+=t(26,99,"三职业觉醒 · 在暮色中守护最后的脑子" if not en else "Three paths. One brain to protect.",10,"#afc5b4",width=220)
        home+=t(26,323,"↑ ↓ 选择 · Enter 确认 · T 切换语言" if not en else "↑ ↓ Navigate  /  Enter Select  /  T Language",9,"#a6bfae",width=255)
        home+=t(26,342,f"v{release['version']} · "+("本机存档 · 20关远征 · 单人 / 双人" if not en else "Local save · 20 stages · Solo / Co-op"),8,"#799b91",width=250)
        notice("home",home)
        for n,label in enumerate((["开始游戏","读档","设置","实验室"] if not en else ["Start Game","Load Game","Settings","Laboratory"])):
            for active in range(2):ui.append((f"home-{n}-{active}"+suffix,190,36,button(label,bool(active))))
        for n in range(1,21):
            art=panel()+t(26,40,"花园远征" if not en else "Garden Expedition",24,"#f0e0ad")
            art+=t(450,39,"20 STAGES / 4 REGIONS",9,"#99b8a4","end")
            art+=t(26,58,"通关解锁下一关 · 每五关迎战领主" if not en else "Clear each stage to unlock the next. Boss every 5 stages.",10,"#aec5b4",width=420)
            title=f"第 {n:02d} 关 · {NAMES[n-1]}" if not en else f"Stage {n:02d} · {stage_en[n-1]}"
            art+=t(240,303,title,12,"#e5d6a8","middle",420)
            for theme,label in enumerate((["召唤之森","寒冰回廊","熔火花园","雷霆要塞"] if not en else ["SUMMON","FROST","EMBER","STORM"])):
                art+=t(20,94+theme*52,label,8,["#afce91","#a5d9dc","#e5ad89","#c5b0e2"][theme],width=57)
            notice(f"stage-view-{n}",art)
        for n in range(1,21):
            for status in range(5):
                locked=status in [0,4]; selected=status in [2,4]
                color=["#b2c995","#a1dadd","#e0ad8d","#c4b2e6"][(n-1)//5]
                art=f'<rect x="1" y="1" width="69" height="42" rx="7" fill="{"#193034" if locked else "#34554a"}" stroke="{color if selected else "#4f6a60"}" stroke-width="{2 if selected else 1}"/>'
                art+=t(14,28,f"{n:02d}",18,"#708d83" if locked else color,width=30)
                if locked:art+='<rect x="48" y="21" width="12" height="10" rx="2" fill="#799088"/><path d="M50 21v-4a4 4 0 018 0v4" fill="none" stroke="#799088" stroke-width="2"/>'
                elif status==3:art+='<path d="M47 23l5 5 9-12" fill="none" stroke="#bedea0" stroke-width="2"/>'
                elif n%5==0:art+='<path d="M46 28l-2-11 6 5 4-8 4 8 6-5-2 11Z" fill="#e3c18e"/>'
                else:art+='<path d="M50 18l7 6-7 6Z" fill="#a4be9d"/>'
                cards.append((f"stage-{n}-{status}"+suffix,71,44,svg(71,44,art)))
        for name,label,w in [("stage-start","选择职业" if not en else "Choose Class",180),("back","返回" if not en else "Back",100),("battle","进入战场" if not en else "Enter Battle",180),("load-0","继续存档" if not en else "Continue",98),("load-1","导出备份" if not en else "Backup",98),("load-2","恢复备份" if not en else "Restore",98)]:
            ui.append((name+suffix,w,34,button(label,name in ["battle","stage-start","load-0"],w,34)))
        art=panel()+t(26,39,"选择守护者" if not en else "Choose a Guardian",24,"#f0e0ad")
        art+=t(26,58,"三条独立进化路线 · 双人可分别选择职业" if not en else "Three independent paths. Co-op players may choose different classes.",10,"#adc2b2",width=425)
        art+=t(240,309,"1 / 2 / 3 选职业 · Tab 切换玩家 · Enter 开战" if not en else "1 / 2 / 3 Class  ·  Tab Switch player  ·  Enter Battle",9,"#9fb9a9","middle",420)
        notice("class-select",art)
        for role in range(3):
            for tier in range(6):
                for bits in range(4):
                    art=f'<rect x="1" y="1" width="134" height="168" rx="12" fill="#1b3a3b" stroke="{COLORS[role] if bits else "#4e6b60"}" stroke-width="{2 if bits else 1}"/>'
                    art+=t(68,25,role_names[role],17,COLORS[role],"middle",122)+plant(role,tier,35,33,1.35)
                    art+=t(68,115,routes[role][tier],10,"#d7dec1","middle",124)
                    art+=t(68,137,descriptions[role][0],9,"#b4cabb","middle",124)+t(68,154,descriptions[role][1],9,COLORS[role],"middle",124)
                    if bits:art+=t(122,100,["","1P","2P","1P/2P"][bits],9,"#f0dda9","end",54)
                    ui.append((f"class-{role}-{tier}-{bits}"+suffix,136,170,svg(136,170,art)))
            for active in range(2):ui.append((f"tab-{role}-{active}"+suffix,132,30,button(role_names[role],bool(active),132,30,COLORS[role])))
        for mode in [1,2]:
            ui.append((f"mode-{mode}"+suffix,150,30,button(("单人模式" if mode==1 else "双人合作") if not en else ("Solo" if mode==1 else "Local Co-op"),True,150,30)))
            ui.append((f"member-{mode}"+suffix,150,30,button(("正在选择 1P" if mode==1 else "正在选择 2P") if not en else f"Editing Player {mode}",False,150,30)))
        art=panel()+t(26,40,"设置" if not en else "Settings",24,"#f0e0ad")
        art+=t(240,116,"界面语言 / LANGUAGE" if not en else "LANGUAGE",13,"#b6ccb8","middle")
        art+=t(240,223,"语言选择会自动保存在本机。" if not en else "Your language preference is saved on this device.",11,"#9cb8a8","middle",420)
        art+=t(240,250,"可随时按 T 切换中英文" if not en else "Press T at any time to switch languages.",10,"#91ab9e","middle",420)
        notice("settings",art)
        for lang,label in enumerate(["简体中文","English"]):
            if en and lang==0:label="Simplified Chinese"
            for active in range(2):ui.append((f"language-{lang}-{active}"+suffix,170,42,button(label,bool(active),170,42)))
        for role in range(3):
            for tier in range(6):
                art=panel()+t(26,39,"进化实验室" if not en else "Evolution Laboratory",23,"#f0e0ad")
                art+=t(450,38,"金币" if not en else "COINS",9,"#cfbf92","end",70)
                art+=t(26,58,"共享金币 · 各职业独立成长 · 先选职业，再购买进化" if not en else "Shared wallet. Each class evolves independently.",10,"#aac3b0",width=330)
                for step in range(6):
                    x=24+step*73
                    art+=f'<rect x="{x}" y="111" width="66" height="110" rx="8" fill="{"#304b41" if step<=tier else "#172f32"}" stroke="{COLORS[role] if step==tier else "#3f5d50"}"/>'
                    art+=plant(role,step,x+6,121,1.1)+t(x+33,192,routes[role][step],9,COLORS[role] if step==tier else "#b2c5ad","middle",60)
                    art+=t(x+33,210,("初始" if step==0 else f"进化 {step}") if not en else ("Base" if step==0 else f"Tier {step}"),8,"#8fac9d","middle",60)
                art+=t(240,245,descriptions[role][0]+"  /  "+descriptions[role][1],12,COLORS[role],"middle",420)
                price=[100,250,500,900,1500,0][tier]
                label=(f"下一次进化：{price} 金币" if tier<5 else "已达到最终形态") if not en else (f"Next evolution: {price} coins" if tier<5 else "Final form reached")
                art+=t(240,262,label,12,"#e6d6aa","middle",400)
                notice(f"class-lab-{role}-{tier}",art)
        ui.append(("buy"+suffix,180,34,button("购买进化" if not en else "Evolve",True,180,34)))
        for mode in [1,2]:
            for stage in range(21):
                art=panel()+t(26,39,"读档与备份" if not en else "Load and Backup",24,"#f0e0ad")
                art+=t(26,58,"本机自动存档 · 从关卡起点继续" if not en else "Local auto-save. Continue from the start of the saved stage.",10,"#aec4b5",width=420)
                art+=t(30,104,(f"继续第 {stage:02d} 关" if stage else "尚无存档，先开始游戏") if not en else (f"Continue Stage {stage:02d}" if stage else "No checkpoint yet. Start a game first."),20,"#e5d6a8",width=410)
                art+=t(30,135,("单人模式" if mode==1 else "双人合作") if not en else ("Solo" if mode==1 else "Local Co-op"),12,"#adc5b2")
                art+=t(30,164,"通关记录保留，生命与敌人会在关卡起点重置。" if not en else "Stage unlocks persist. Health and enemies reset on resume.",11,"#abc3b2",width=420)
                art+=t(30,190,"金币和三条进化路线自动保存。" if not en else "Coins and all three evolution paths save automatically.",11,"#abc3b2",width=420)
                art+=t(30,221,"持有金币：" if not en else "Coins:",12,"#d5c593")
                art+=t(30,245,"累计收入：" if not en else "Earned:",12,"#b0c5b7")
                art+=t(240,340,"N 继续 · C 备份 · V 恢复 · M 返回" if not en else "N Continue  /  C Backup  /  V Restore  /  M Back",9,"#94b2a0","middle",420)
                # Replace the earlier panel in place rather than duplicate names.
                directory=ROOT/"assets/sprites/Notice"
                (directory/f"savepanel-{mode}-{stage}{suffix}.svg").write_text(svg(480,360,art),encoding="utf-8")
                data=json.loads((directory/"index.json").read_text())
                old=next((i for i in data["costumes"] if i["name"]==f"savepanel-{mode}-{stage}{suffix}"),None)
                if old:old.update(x=240,y=180,imageWidth=480,imageHeight=360)
                else:data["costumes"].append({"name":f"savepanel-{mode}-{stage}{suffix}","path":f"savepanel-{mode}-{stage}{suffix}.svg","x":240,"y":180,"imageWidth":480,"imageHeight":360,"bitmapResolution":1})
                write_json("assets/sprites/Notice/index.json",data)
        for prefix in ["notice-","notice-toast-"]:
            label="该关卡尚未解锁，请先通关前一关。" if not en else "Stage locked. Clear the previous stage first."
            append("Wallet",prefix+"9"+suffix,430,18,svg(430,18,'<rect width="430" height="18" rx="5" fill="#173443"/>'+t(215,13,label,11,"#f3d59e","middle",416)))
    sprite("UIAction",ui);sprite("StageCard",cards)
    decor=[]
    decor.append(("mote",18,18,svg(18,18,'<circle cx="9" cy="9" r="9" fill="#d1e5a5" opacity=".05"/><circle cx="9" cy="9" r="4" fill="#e4edba" opacity=".15"/><circle cx="9" cy="9" r="1.3" fill="#f4f5d3"/>')))
    sprite("HomeDecor",decor)
    directory=ROOT/"assets/sprites/Splash";directory.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/"assets/splash-garden-v1.png",directory/"splash.png")
    write_json("assets/sprites/Splash/index.json",{"costumes":[{"name":"splash","path":"splash.png","x":724,"y":543,"imageWidth":1448,"imageHeight":1086,"bitmapResolution":3}],"costumeIndex":0,"size":1.04,"rotationStyle":"none","visible":False})
    config=json.loads((ROOT/"assets/index.json").read_text())
    config["zorder"].insert(0,"Splash");config["zorder"].insert(1,"HomeDecor")
    config["zorder"].insert(config["zorder"].index("Health"),"Brain")
    config["zorder"].extend(["StageCard","UIAction"])
    # Status messages and currency should remain above page panels and buttons.
    config["zorder"].remove("Wallet");config["zorder"].append("Wallet")
    write_json("assets/index.json",config)
    write_json("builder-meta.json",{"displayName":"暮光花园 · 三职业觉醒版","description":"豌豆、蘑菇、西瓜三职业，独立五阶进化与专属攻击；动态首页、可点击菜单、顺序解锁20关、四主题领主、本地双人、中英文与旧存档迁移。","instructions":"首页点击开始→选关→选职业→进入战场。新档只开放第1关，通关开放下一关。1P WASD/空格/E，2P方向键/J/K；P暂停，M主页，B实验室，S读档，O存档，T语言。实验室1/2/3切路线、U购买；职业页Tab切玩家。"})
