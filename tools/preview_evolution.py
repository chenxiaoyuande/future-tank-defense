from project_paths import PREVIEW_DIR, FRONT_FRAMES, prepare_outputs
prepare_outputs()
"""Render an evolution comparison and a populated shop from the shipped SVG assets."""
import json

from art_utils import ROOT, svg
from evolution_art import COLORS, COSTS, NAMES


def image(folder: str, name: str, x: float, y: float, scale: float = 1) -> str:
    directory=ROOT/"assets/sprites"/folder
    data=json.loads((directory/"index.json").read_text())
    item=next(c for c in data["costumes"] if c["name"]==name)
    return f'<g transform="translate({x} {y}) scale({scale})">{(directory/item["path"]).read_text()}</g>'


def label(x: float, y: float, value: str, size: int, color: str) -> str:
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{color}">{value}</text>'


def build() -> None:
    art='<rect width="1080" height="300" fill="#122c38"/>'
    for tier in range(6):
        x=tier*180+5
        art+=f'<rect x="{x}" y="5" width="170" height="290" rx="12" fill="#213b46" stroke="{COLORS[tier]}"/>'
        art+=label(x+85,31,NAMES[tier],16,COLORS[tier])
        name="plant-up-0" if tier==0 else f"evo-{tier}-p1-up-0"
        art+=image("Actor",name,x+41,49,2.2)
        if tier:
            art+=image("Actor",f"evo-{tier}-p2-up-0",x+65,160,.8)
        bullet="seed-0" if tier==0 else f"evo-{tier}-seed-0"
        missile="missile-0" if tier==0 else f"evo-{tier}-missile-0"
        art+=image("Actor",bullet,x+31,206,1.3)+image("Actor",missile,x+92,206,1.3)
        art+=label(x+85,255,f"普攻 {1+tier//2}  ·  大招 {5-tier*.3:.1f}s",12,"#d3ddca")
        art+=label(x+85,279,"初始形态" if tier==0 else f"进化消耗 {COSTS[tier-1]} 金币",11,COLORS[tier])
    (PREVIEW_DIR/"preview-evolution-lineup.svg").write_text(svg(1080,300,art),encoding="utf-8")
    art='<rect width="480" height="360" fill="#122c38"/>'
    art+=image("Notice","evolution-2",10,20)
    for y,value in [(229,"0001250"),(252,"0001600")]:
        for n,digit in enumerate(value):
            art+=image("Wallet","coin-"+digit,109+n*10,y-9)
    art+=image("Wallet","save-1",25,261)
    art+=image("Wallet","notice-1",25,283)
    (PREVIEW_DIR/"preview-evolution-shop.svg").write_text(svg(480,360,art),encoding="utf-8")


if __name__=="__main__":
    build()
