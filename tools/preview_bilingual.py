from project_paths import PREVIEW_DIR, FRONT_FRAMES, prepare_outputs
prepare_outputs()
"""Compose Chinese and English save, menu and evolution previews from actual assets."""
from art_utils import ROOT, svg
from preview_evolution import image


def panel(name: str, english: bool, save: bool) -> str:
    suffix="-en" if english else ""
    art='<rect width="480" height="360" fill="#122c38"/>'
    art+=image("Frame","frame"+suffix,0,0)
    art+=image("Notice",name+suffix,10,20)
    if save or name.startswith("evolution"):
        for y,value in [(229,"0001250"),(252,"0001600")]:
            for n,digit in enumerate(value):
                art+=image("Wallet","coin-"+digit,109+n*10,y-9)
        art+=image("Wallet","save-1"+suffix,25,261)
        art+=image("Wallet","notice-7"+suffix,25,283)
        if save:
            art+=image("Wallet","coin-0",121,110)+image("Wallet","coin-6",131,110)
    else:
        art+=image("Wallet","coin-label-1"+suffix,313,23)
        for n,digit in enumerate("0001250"):
            art+=image("Wallet","coin-"+digit,360+n*10,23)
    return art


def build() -> None:
    panels=[("savepanel-2-7",False,True),("savepanel-2-7",True,True),("menu-2-7",True,False),("evolution-2",True,False)]
    body='<rect width="960" height="720" fill="#122c38"/>'
    for n,(name,en,saved) in enumerate(panels):
        art=panel(name,en,saved)
        (PREVIEW_DIR/f"preview-bilingual-{n}.svg").write_text(svg(480,360,art),encoding="utf-8")
        body+=f'<g transform="translate({n%2*480} {n//2*360})">{art}</g>'
    (PREVIEW_DIR/"preview-bilingual.svg").write_text(svg(960,720,body),encoding="utf-8")


if __name__=="__main__":
    build()
