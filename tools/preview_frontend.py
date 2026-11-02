from project_paths import PREVIEW_DIR, FRONT_FRAMES, prepare_outputs
prepare_outputs()
"""Compose preview frames from shipped assets; these are not engine recordings."""
import base64
import json
import math
from pathlib import Path
from art_utils import ROOT, svg
from preview_evolution import image
from front_end_art import t
from classes_art import ROUTES_ZH, COLORS


def centered(folder,name,x,y,scale=1):
    data=json.loads((ROOT/f"assets/sprites/{folder}/index.json").read_text())
    item=next(c for c in data["costumes"] if c["name"]==name)
    return image(folder,name,x-item["imageWidth"]*scale/2,y-item["imageHeight"]*scale/2,scale)


def build():
    media=ROOT/"docs/media";media.mkdir(exist_ok=True)
    frames=FRONT_FRAMES;frames.mkdir(exist_ok=True)
    background=base64.b64encode((ROOT/"assets/splash-garden-v1.png").read_bytes()).decode()
    manifest=[]
    def backdrop(tick=0):
        dx=math.sin(tick*.006)*3;dy=math.cos(tick*.005)*2
        return f'<image x="{-11+dx}" y="{-8+dy}" width="502" height="376" href="data:image/png;base64,{background}"/>'
    def emit(name,art,w=480,h=360):
        target=frames/(name+".svg");target.write_text(svg(w,h,art),encoding="utf-8")
        manifest.append({"source":str(target),"output":str(frames/(name+".png")),"width":w*2,"height":h*2})
    for f in range(36):
        tick=f*5;art=backdrop(tick)
        for n in range(18):
            x=240+(n*71)%450-225+math.sin((tick+n*37)*.014)*14
            y=180-((n*47)%290-145+math.cos((tick+n*23)*.017)*11)
            scale=.5+(1+math.sin((tick+n*31)*.05))*.4
            art+=centered("HomeDecor","mote",x,y,scale)
        art+=image("Notice","home",0,0)
        for n in range(4):art+=centered("UIAction",f"home-{n}-{int(n==0)}",115,140+n*45)
        emit(f"home-{f:02d}",art)
    art=backdrop()+image("Notice","stage-view-1",0,0)
    for n in range(1,21):art+=centered("StageCard",f"stage-{n}-{2 if n==1 else 0}",116+(n-1)%5*76,104+(n-1)//5*52)
    art+=centered("UIAction","stage-start",325,328)+centered("UIAction","back",110,328)
    emit("stage-locked",art)
    art=backdrop()+image("Notice","class-select",0,0)
    for role in range(3):art+=centered("UIAction",f"class-{role}-{role+1}-{[1,0,2][role]}",95+role*145,168)
    art+=centered("UIAction","mode-2",140,281)+centered("UIAction","member-2",340,281)
    art+=centered("UIAction","battle",325,330)+centered("UIAction","back",110,330)
    emit("class-select",art)
    for role in range(3):
        art=backdrop()+image("Notice",f"class-lab-{role}-2",0,0)
        for n in range(3):art+=centered("UIAction",f"tab-{n}-{int(n==role)}",95+n*145,88)
        for n,digit in enumerate("0001250"):art+=centered("Wallet","coin-"+digit,350+n*10,55)
        art+=centered("Wallet","save-1",240,280)
        art+=centered("UIAction","buy",325,329)+centered("UIAction","back",110,329)
        emit(f"class-lab-{role}",art)
    for lang in [0,1]:
        suffix="-en" if lang else ""
        art=backdrop()+image("Notice","settings"+suffix,0,0)
        for n in range(2):art+=centered("UIAction",f"language-{n}-{int(n==lang)}"+suffix,145+n*190,165)
        art+=centered("UIAction","back"+suffix,240,315)
        emit(f"settings-{lang}",art)
    for f in range(6):
        art='<rect width="1080" height="660" fill="#102b32"/>'+t(25,37,"三条成长路线 / THREE EVOLUTION PATHS",25,"#eddfb1",width=1020)
        for role in range(3):
            y=56+role*200
            for tier in range(6):
                x=15+tier*178
                art+=f'<rect x="{x}" y="{y}" width="166" height="187" rx="12" fill="#1d3b3b" stroke="{COLORS[role]}" stroke-opacity=".5"/>'
                art+=centered("Actor",f"hero-{role}-{tier}-p1-right-{f}",x+83,y+76,2.3)
                art+=t(x+83,y+149,ROUTES_ZH[role][tier],15,COLORS[role],"middle",156)
                art+=t(x+83,y+172,"初始形态" if tier==0 else f"进化 {tier}",11,"#9ebba8","middle",150)
        emit(f"routes-{f}",art,1080,660)
    (PREVIEW_DIR/"front-preview-manifest.json").write_text(json.dumps(manifest),encoding="utf-8")

if __name__=="__main__":build()
