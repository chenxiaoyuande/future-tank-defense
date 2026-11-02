from project_paths import FRONT_FRAMES
"""Publish static and animated asset previews after render_frontend.cjs."""
import shutil
from PIL import Image
from art_utils import ROOT

def encode(pattern,output,size,duration):
    sources=sorted((FRONT_FRAMES).glob(pattern))
    frames=[];palette=None
    for source in sources:
        with Image.open(source) as image:
            rgb=image.convert("RGB").resize(size,Image.LANCZOS)
            if palette is None:palette=rgb.quantize(colors=192)
            frames.append(rgb.quantize(palette=palette,dither=0))
    frames[0].save(ROOT/"docs/media"/output,save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=False,disposal=2)

if __name__=="__main__":
    encode("home-*.png","animated-home.gif",(720,540),100)
    encode("routes-*.png","profession-evolution.gif",(1080,660),160)
    for source,dest in [("home-00","home-screen"),("stage-locked","level-select"),("class-select","class-select"),("routes-0","profession-routes"),("class-lab-0","evolution-shop"),("class-lab-1","mushroom-lab"),("class-lab-2","melon-lab"),("settings-1","language-settings")]:
        shutil.copyfile(FRONT_FRAMES/(source+".png"),ROOT/"docs/media"/(dest+".png"))
    print("Published 2 animated previews and 8 stills.")
