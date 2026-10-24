"""Build the survival edition's artwork, animations, and XBuilder package."""
import math
import shutil
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image
from art_utils import ROOT, svg, write_json
from pickup_art import generate

DEFS = '''<defs>
<linearGradient id="leaf" x2=".3" y2="1"><stop stop-color="#d4f8a0"/><stop offset=".45" stop-color="#76c886"/><stop offset="1" stop-color="#236c62"/></linearGradient>
<radialGradient id="face" cx=".3" cy=".2" r=".85"><stop stop-color="#d9ffb9"/><stop offset=".55" stop-color="#8cdb9b"/><stop offset="1" stop-color="#337f75"/></radialGradient>
<linearGradient id="gold" x2=".2" y2="1"><stop stop-color="#fff4b1"/><stop offset=".4" stop-color="#ffc96a"/><stop offset="1" stop-color="#c48145"/></linearGradient>
<linearGradient id="petal" x2=".2" y2="1"><stop stop-color="#fff6c2"/><stop offset=".45" stop-color="#ffda79"/><stop offset="1" stop-color="#d88455"/></linearGradient>
<radialGradient id="skin" cx=".3" cy=".2" r=".9"><stop stop-color="#d5e3ba"/><stop offset=".5" stop-color="#9faf9a"/><stop offset="1" stop-color="#657b80"/></radialGradient>
<linearGradient id="coat" x2=".8" y2="1"><stop stop-color="#c69299"/><stop offset=".5" stop-color="#8f697e"/><stop offset="1" stop-color="#48455d"/></linearGradient>
<radialGradient id="orb" cx=".35" cy=".3"><stop stop-color="#fff7f8"/><stop offset=".35" stop-color="#d9a8ef"/><stop offset="1" stop-color="#73578f"/></radialGradient>
<linearGradient id="hedge" x2=".4" y2="1"><stop stop-color="#b5de86"/><stop offset=".25" stop-color="#6aa872"/><stop offset=".7" stop-color="#39766b"/><stop offset="1" stop-color="#225453"/></linearGradient>
<linearGradient id="stone" x2=".8" y2="1"><stop stop-color="#aebeb2"/><stop offset=".5" stop-color="#6d8790"/><stop offset="1" stop-color="#3d596a"/></linearGradient>
</defs>'''


def text(x,y,value,size=12,fill='#f7e9bf',anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{fill}">{value}</text>'


def star(x,y,r,color,opacity=1):
    return f'<path d="M{x-r} {y}Q{x} {y} {x} {y-r}Q{x} {y} {x+r} {y}Q{x} {y} {x} {y+r}Q{x} {y} {x-r} {y}Z" fill="{color}" opacity="{opacity}"/>'


def plant(direction,frame):
    wave=[0,.7,0,-.7,-1.2,.5][frame]
    recoil=1.1 if frame==4 else 0
    dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][direction]
    s=DEFS+'<ellipse cx="20" cy="40" rx="17" ry="3" fill="#102f38" opacity=".45"/><ellipse cx="20" cy="39" rx="12" ry="1.5" fill="#a0dfb7" opacity=".2"/>'
    s+='<path d="M20 36Q14 28 21 21" stroke="#164e4c" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M20 35Q16 28 21 23" stroke="#83cf86" stroke-width="2.2" fill="none"/>'
    for side in [-1,1]:
        s+=f'<path d="M20 37Q{20+side*14} {23+wave} {20+side*18} {34-wave}Q{20+side*12} 42 20 37Z" fill="url(#leaf)" stroke="#204e4a" stroke-width="1.1"/>'
        s+=f'<path d="M20 37Q{20+side*8} 33 {20+side*15} {34-wave}" stroke="#daf6ac" stroke-width=".7" fill="none"/>'
    s+=f'<g transform="translate({-dx*recoil} {wave-dy*recoil})">'
    for angle in range(0,360,45):
        a=math.radians(angle)
        x,y=20+11*math.cos(a),15+11*math.sin(a)
        s+=f'<ellipse cx="{x}" cy="{y}" rx="6" ry="4" transform="rotate({angle} {x} {y})" fill="url(#petal)" stroke="#8e6845" stroke-width=".9"/>'
        s+=f'<path d="M{x} {y}l{math.cos(a)*3} {math.sin(a)*3}" stroke="#fff5c5" stroke-width=".65"/>'
    s+='<circle cx="20" cy="15" r="10.8" fill="#205c54"/><circle cx="20" cy="14.3" r="10.2" fill="url(#face)" stroke="#ceef9c" stroke-width=".5"/>'
    s+='<path d="M13 9Q17 4 24 7" stroke="#f0ffd3" stroke-width="1.8" stroke-linecap="round" fill="none"/>'
    if frame==2:
        s+='<path d="M12 14q3 2 5-1m6 0q3 2 5-1" fill="none" stroke="#274b47" stroke-width="1.6" stroke-linecap="round"/>'
    else:
        for ex in [15,25]:
            s+=f'<ellipse cx="{ex}" cy="13.5" rx="3.1" ry="3.8" fill="#f8ffe3" stroke="#57977f" stroke-width=".6"/><ellipse cx="{ex+dx*.7}" cy="{14+dy*.5}" rx="1.7" ry="2.3" fill="#255c52"/><circle cx="{ex-.4}" cy="12.7" r=".8" fill="white"/>'
    s+='<path d="M12 8l6 1m5 0l5-1" stroke="#407655" stroke-width="1.2" stroke-linecap="round"/><ellipse cx="11" cy="18" rx="2.4" ry="1.2" fill="#f6b18a" opacity=".6"/><ellipse cx="29" cy="18" rx="2.4" ry="1.2" fill="#f6b18a" opacity=".6"/>'
    mx,my=20+dx*12,17+dy*11
    s+=f'<path d="M{20+dx*4} {17+dy*4}L{mx} {my}" stroke="#275a52" stroke-width="8" stroke-linecap="round"/><path d="M{20+dx*4} {16+dy*4}L{mx} {my-1}" stroke="#8fcb86" stroke-width="5" stroke-linecap="round"/>'
    s+=f'<ellipse cx="{mx}" cy="{my}" rx="{4 if dx else 5}" ry="{5 if dx else 3.8}" fill="url(#leaf)" stroke="#2f5b4d" stroke-width="1.2"/><ellipse cx="{mx+dx}" cy="{my+dy}" rx="{2.4 if frame<4 else 3.2}" ry="{2.6 if frame<4 else 3.2}" fill="#234c45"/>'
    if frame>=4:
        s+=f'<circle cx="{mx+dx*2}" cy="{my+dy*2}" r="2.2" fill="#f6ffb1"/>'
        s+=star(mx+dx*5,my+dy*5,4,'#fff6ad')
    s+='</g>'
    s+=star(5,18,1.7,'#e8ffe4',.8)+star(34,9,1.5,'#ffe3a4',.85)
    return svg(40,44,s)


def zombie(direction,frame,variant):
    phase=[-1,0,1,0,-.5,.7,0,2][frame]
    flip='translate(40 0) scale(-1 1)' if direction==3 else ''
    s=DEFS+'<ellipse cx="20" cy="41" rx="18" ry="3" fill="#102b35" opacity=".5"/>'
    if frame==7:
        s+='<path d="M1 15h18M3 22h12M0 29h17" stroke="#ffb899" stroke-width="2" opacity=".7"/>'
    s+=f'<g transform="{flip}">'
    if variant==0:
        # Barrel-shaped, riveted heavy armor, broad shoulders and heavy boots.
        s+='<path d="M10 31v8H6v3h13V31m4 0v11h13l-3-4-1-7" fill="#354751" stroke="#19343d"/>'
        s+='<path d="M5 17l9-4h14l8 5 1 17-8 4H12L4 34Z" fill="url(#stone)" stroke="#324850" stroke-width="1.5"/>'
        s+='<path d="M7 19l8-3h12l7 4-4 13H11Z" fill="#a48b62" stroke="#e1c899"/><path d="M15 17v18m11-18v18M9 26h23" stroke="#45585b" stroke-width="2"/>'
        s+='<path d="M3 17l7-2 3 7-8 4-4-3m29-5l7-3 3 8-6 4-5-3" fill="url(#stone)" stroke="#354b52"/>'
        for x,y in [(9,21),(30,21),(12,31),(28,31)]: s+=f'<circle cx="{x}" cy="{y}" r="1.2" fill="#ffe0a4"/>'
    elif variant==1:
        # Lean runner, long limbs, orange sportswear and cyan goggles.
        s+=f'<path d="M17 26l{-phase*3-3} 12-6 2 9 1 7-12m-1-3l{phase*3+5} 11 6 2-10 2-7-13" fill="#73b49d" stroke="#2b5557" stroke-width="2"/>'
        s+='<path d="M13 18l10-3 6 5-6 11-9-2Z" fill="#de9c68" stroke="#745951"/><path d="M18 18l-3 9m6-8l-3 9" stroke="#ffe2a1" stroke-width="1.4"/>'
        s+=f'<path d="M14 20l-7 {3+phase*2}-4-4m23 2l8 {-3-phase*2} 2 5" stroke="#8ac5ad" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
        s+='<path d="M7 39h10m10 1h9" stroke="#f2ddb4" stroke-width="2.8"/>'
    else:
        # Horned, low stance with glowing crimson core and claw gauntlets.
        s+='<path d="M13 29l-6 10h10l4-9m1-1l4 12h10l-7-13" fill="#5e4c69" stroke="#2c354c" stroke-width="1.5"/>'
        s+='<path d="M10 17l10-4 11 5 2 16-11 3-11-4Z" fill="#804d68" stroke="#403b54"/><path d="M11 20l-7 7 5 5m20-12l7 7-5 5" stroke="#a3788e" stroke-width="5" fill="none"/>'
        s+='<path d="M3 26l-2 6 7-2m26-4l5 6-8-2" fill="#d5c8b0" stroke="#655873"/>'
        s+=f'<circle cx="22" cy="26" r="{6 if frame>=6 else 4}" fill="#ff927e" opacity=".4"/><path d="M22 20l4 6-4 6-4-6Z" fill="#ffd7a2" stroke="#ff8c85"/>'
    # The faces share a family resemblance, but silhouette and equipment differ.
    hx=20 if variant!=1 else 23
    s+=f'<g transform="translate({hx-20} 0)"><path d="M10 7Q11 0 21 1Q32 2 30 13l-4 8-11-1-5-8Z" fill="url(#skin)" stroke="#47696a" stroke-width="1.2"/>'
    if variant==0:
        s+='<path d="M8 8L11 1h19l3 9-10-2Z" fill="url(#stone)" stroke="#354b52"/><path d="M13 3h14" stroke="#ccd7bd"/><path d="M12 14v7h17v-6l-4 2h-8Z" fill="#5d797b" stroke="#354c51"/>'
    elif variant==1:
        s+='<path d="M10 7l3-6 6 2 5-3 5 6" fill="#584b67"/><path d="M9 10h23v5H9Z" fill="#3c4b67"/><path d="M12 10h7v5h-7m10-5h7v5h-7" fill="#94eef0" stroke="#d3fdf2"/>'
        s+='<path d="M13 5l-8-2 3 7" fill="#df9b6d"/>'
    else:
        s+='<path d="M11 7L5 0l1 10 7 2m14-5l7-7 1 10-7 2" fill="#e5ccaa" stroke="#7e536e"/><path d="M12 5l7-4 10 4-4 6H15Z" fill="#725473"/>'
    if variant!=1:
        for x in [15,25]: s+=f'<ellipse cx="{x}" cy="12" rx="3" ry="3.4" fill="#f7e4c5"/><circle cx="{x+.6}" cy="12" r="1.6" fill="{["#a39565","#72d6c8","#ed8b8b"][variant]}"/><circle cx="{x+.6}" cy="12" r=".7" fill="#2d4052"/>'
    if variant!=0: s+='<path d="M15 18q6 4 12-1l-2 5-9-1Z" fill="#3f4053"/><path d="M17 18v3h3v-2m3-1v3h2v-3" fill="#eee4c5"/>'
    s+='</g>'
    if frame==4: s+='<circle cx="34" cy="24" r="6" fill="url(#orb)"/>'+star(34,24,8,'#e7b4f2',.5)
    if frame==5: s+='<path d="M8 4l28 30m-25 0L32 3" stroke="#fff6d2" stroke-width="2" opacity=".8"/>'
    if frame==6: s+='<path d="M20 1v9m0 3v2" stroke="#ffda9b" stroke-width="2.6"/>'
    s+='</g>'
    return svg(40,44,s)


def sprite(name,frames):
    directory=ROOT/'assets/sprites'/name
    directory.mkdir(parents=True,exist_ok=True)
    costumes=[]
    for title,w,h,content in frames:
        (directory/f'{title}.svg').write_text(content,encoding='utf-8')
        costumes.append({'name':title,'path':title+'.svg','x':w/2,'y':h/2,'faceRight':0,'bitmapResolution':1,'imageWidth':w,'imageHeight':h})
    write_json(f'assets/sprites/{name}/index.json',{'x':0,'y':0,'heading':90,'size':1,'visible':False,'rotationStyle':'normal' if name in ['Atmosphere','Actor'] else 'none','physicsMode':'no','collisionShapeType':'none','costumes':costumes})


frames=[]
for d,direction in enumerate(['up','right','down','left']):
    for f in range(6):
        frames.append((f'plant-{direction}-{f}',40,44,plant(d,f)))
    for f in range(8):
        for variant in range(3):
            frames.append((f'zombie-{variant}-{direction}-{f}',40,44,zombie(d,f,variant)))
hedge=DEFS+'<ellipse cx="13" cy="26" rx="13" ry="3" fill="#18383a" opacity=".5"/><path d="M1 15l23-1v12L2 28Z" fill="#294f4c"/><path d="M2 16l21-1-1 8-19 2Z" fill="url(#hedge)" stroke="#214b46"/><path d="M1 13Q-2 6 5 5Q4 0 12 2Q19-1 23 5Q28 10 23 16Q17 20 11 17Q3 20 1 13Z" fill="url(#hedge)" stroke="#285749" stroke-width="1.1"/><path d="M3 9q3-5 8-2m2-3q6-1 8 4M6 15q3-3 6-1m5-3q4-2 6 0" stroke="#c8e99b" stroke-width=".9" stroke-linecap="round" fill="none"/><path d="M7 20v4m7-5v4m6-6v4" stroke="#668e69" stroke-width=".6"/><circle cx="20" cy="15" r="2.2" fill="#e8ad9c"/><circle cx="20" cy="15" r=".6" fill="#fff0af"/>'
stone=DEFS+'<ellipse cx="13" cy="26" rx="12" ry="3" fill="#18383a" opacity=".5"/><path d="M1 19L4 7l12-5 10 10-3 13-16 3Z" fill="url(#stone)" stroke="#334b59" stroke-width="1.2"/><path d="M4 7l8 10 14-5M12 17l-5 11" stroke="#d7d8bc" stroke-width=".9" fill="none"/><path d="M8 8l7-3 4 4-6 3Z" fill="#b4c2ae" opacity=".65"/><path d="M14 16l4-3 2 4-3 4z" fill="none" stroke="#8bdfbe" stroke-width="1.2"/><path d="M2 23q6-6 10-2v5H4m15-5q4-3 6 1l-2 4h-5" fill="#5f8b63"/>'
house=DEFS+'<ellipse cx="23" cy="43" rx="21" ry="4" fill="#122f3b" opacity=".5"/><circle cx="23" cy="30" r="20" fill="#e5d291" opacity=".06"/><path d="M6 18h33v24H6Z" fill="#596b68" stroke="#2c4a52" stroke-width="1.2"/><path d="M7 19h29v20H7Z" fill="#d7cda1"/><path d="M5 20L22 2l20 18-6 3L22 10 9 23Z" fill="#3f7e80" stroke="#2f4c57" stroke-width="1.5"/><path d="M8 17L22 4l15 14M13 12l19 6M17 8l10 5" fill="none" stroke="#8ac2b0" stroke-width="1"/><path d="M11 22h21v18H11Z" fill="#88c8b1" stroke="#597c73"/><path d="M11 23h21v16H11Z" fill="url(#gold)" opacity=".8"/><path d="M22 22v18M11 31h21" stroke="#f0e5b4" stroke-width="1.6"/><path d="M21 38v-9m0 7l-4-3m4 0l4-3" stroke="#4e8b5f" stroke-width="1.8"/><circle cx="21" cy="29" r="3.6" fill="#f5dd8e"/><circle cx="21" cy="29" r="1.5" fill="#b39857"/><path d="M34 25q12-6 7-13m-5 19q10-3 9-10" fill="none" stroke="#6ca571" stroke-width="2"/>'
frames.extend([('hedge',26,30,svg(26,30,hedge)),('stone',28,30,svg(28,30,stone)),('house',46,48,svg(46,48,house))])
for f in range(2):
    s=DEFS+f'<circle cx="9" cy="9" r="{8-f}" fill="#b6f5ba" opacity=".06"/><circle cx="9" cy="9" r="{6.5-f}" fill="#b6f5ba" opacity=".13"/><circle cx="9" cy="9" r="4.2" fill="url(#face)" stroke="#dbf9b3" stroke-width=".6"/><ellipse cx="7.8" cy="7.8" rx="1.5" ry=".8" fill="#f6ffd1"/>'
    frames.append((f'seed-{f}',18,18,svg(18,18,s)))
    s=DEFS+f'<circle cx="10" cy="10" r="{9-f}" fill="#d09fe8" opacity=".08"/><circle cx="10" cy="10" r="6" fill="#bb7fda" opacity=".2"/><circle cx="10" cy="10" r="4" fill="url(#orb)" stroke="#ecd3f1" stroke-width=".5"/>'+star(5,6,1.3,'#edb5f1')
    frames.append((f'spore-{f}',20,20,svg(20,20,s)))
for f in range(7):
    radius=4+f*3.5
    opacity=max(.1,1-f*.13)
    s=f'<circle cx="30" cy="30" r="{radius+7}" fill="#f4d799" opacity="{opacity*.09}"/><circle cx="30" cy="30" r="{radius}" stroke="#fff0b3" stroke-width="{2.3-f*.25}" fill="none" opacity="{opacity}"/>'
    if f<3:
        s+=star(30,30,13-f*2,'#fff1c6',opacity)
    for a in range(0,360,45):
        r=radius+3
        x,y=30+r*math.cos(math.radians(a+f*7)),30+r*math.sin(math.radians(a+f*7))
        s+=star(x,y,3.3-f*.35,'#8ee6b6' if a%90 else '#e2acdb',opacity)
    frames.append((f'pop-{f}',60,60,svg(60,60,s)))
for f in range(4):
    s=DEFS+'<ellipse cx="27" cy="16" rx="25" ry="15" fill="#e6e9a5" opacity=".05"/>'
    s+='<path d="M0 16L26 6v20Z" fill="#d4e9b0" opacity=".17"/><path d="M6 16L26 12v8Z" fill="#eff9c8" opacity=".4"/>'
    s+=f'<ellipse cx="27" cy="16" rx="{12+f%2}" ry="{10+f%2}" fill="url(#gold)" stroke="#fff0bd" stroke-width="1"/><ellipse cx="27" cy="16" rx="8.5" ry="7" fill="url(#face)"/><path d="M21 16q5-7 12 0q-6 6-12 0Z" fill="#f4f8c5"/><ellipse cx="24" cy="12" rx="3" ry="1.2" fill="#ffffdc"/>'
    s+=star(27,16,5,'#fff8d4')
    for a in range(0,360,90):
        x,y=27+15*math.cos(math.radians(a+f*20)),16+13*math.sin(math.radians(a+f*20))
        s+=star(x,y,2,'#fff0b7',.8)
    frames.append((f'mega-{f}',54,32,svg(54,32,s)))
for f in range(10):
    r=[8,20,35,52,68,80,88,88,88,88][f]
    opacity=max(.1,1-max(0,f-3)*.14)
    s=f'<circle cx="100" cy="100" r="{r+10}" fill="#eed795" opacity="{opacity*.07}"/><circle cx="100" cy="100" r="{r}" fill="#d1eda6" opacity="{opacity*.08}"/><circle cx="100" cy="100" r="{r}" fill="none" stroke="#ffedaa" stroke-width="{max(.7,4-f*.35)}" opacity="{opacity}"/><circle cx="100" cy="100" r="{r*.77}" fill="none" stroke="#a7e3ba" stroke-width="1.2" opacity="{opacity*.65}"/>'
    if f < 6:
        s+=star(100,100,30-f*3,'#fff4c5',opacity)
    for a in range(0,360,30):
        x,y=100+(r*.92)*math.cos(math.radians(a+f*8)),100+(r*.92)*math.sin(math.radians(a+f*8))
        s+=f'<ellipse cx="{x}" cy="{y}" rx="{6-f*.35}" ry="2.2" transform="rotate({a+f*8} {x} {y})" fill="{["#fce8a4","#a8e5b9","#e5bae1"][a//30%3]}" opacity="{opacity}"/>'
        s+=star(x,y,3,'#fff4c7',opacity)
    frames.append((f'burst-{f}',200,200,svg(200,200,s)))
for f in range(2):
    s=DEFS+'<path d="M1 10L10 5v10Z" fill="#ffb47e" opacity=".7"/><path d="M8 10L22 4l8 6-8 6Z" fill="url(#gold)" stroke="#fff2c3"/><path d="M12 8l-2-5 9 3m-7 6l-2 5 9-3" fill="#83cda1" stroke="#d6edb0"/><ellipse cx="24" cy="10" rx="4" ry="3" fill="#d9ffd3"/>'+star(3,10,3+f,'#ffe0ad')
    frames.append((f'missile-{f}',32,20,svg(32,20,s)))
for f in range(5):
    s=DEFS+'<ellipse cx="16" cy="29" rx="14" ry="3" fill="#193c3b" opacity=".5"/><path d="M6 28l4-8 5 5 6-5 4 8Z" fill="#795e47"/><ellipse cx="16" cy="28" rx="11" ry="2" fill="#b89964"/>'
    if f>0:
        scale=f/4
        s+=f'<g transform="translate({16*(1-scale)} {29*(1-scale)}) scale({scale})">'+hedge+'</g>'
        for x,y in [(5,18),(25,14),(17,6)]: s+=star(x,y,1+f*.35,'#d3f2a6',.75)
    frames.append((f'grow-{f}',32,34,svg(32,34,s)))
for f in range(6):
    r=7+f*4; opacity=1-f*.16
    s=f'<ellipse cx="24" cy="37" rx="{r}" ry="{r*.3}" fill="#b79bd3" opacity="{opacity*.3}"/>'
    for n in range(6):
        a=n*math.pi/3+f*.3; x=24+math.cos(a)*r; y=25+math.sin(a)*r*.65-f*2
        s+=star(x,y,4-f*.4,['#e3c1ec','#a6debd','#f7dba3'][n%3],opacity)
    frames.append((f'death-{f}',48,48,svg(48,48,s)))
for f in range(5):
    r=8+f*3
    s=f'<ellipse cx="23" cy="32" rx="{r}" ry="{r*.4}" fill="#b68cdb" opacity=".2"/><ellipse cx="23" cy="32" rx="{r}" ry="{r*.4}" fill="none" stroke="#dcbae9"/><path d="M12 31Q14 {28-f*5} 23 {27-f*5}Q32 {28-f*5} 34 31" fill="#b991d5" opacity=".18"/>'
    s+=star(8,25-f,3,'#f5ddaf')+star(35,24-f,2,'#c3f1cd')
    frames.append((f'portal-{f}',46,46,svg(46,46,s)))
pickup_frames,pickup_effects,pickup_panels=generate(svg,text,star,DEFS)
frames.extend(pickup_frames)
sprite('Actor',frames)
sprite('Buff',pickup_panels)

effects=[]
effects.append(('firefly',10,10,svg(10,10,'<circle cx="5" cy="5" r="5" fill="#ffe1a0" opacity=".04"/><circle cx="5" cy="5" r="3" fill="#ffe1a0" opacity=".14"/><circle cx="5" cy="5" r="1" fill="#ffe9b2"/>')))
for name,color in [('seed-trail','#b5e6a0'),('spore-trail','#d89deb')]:
    s=f'<path d="M1 7L37 1v12Z" fill="{color}" opacity=".06"/><path d="M5 7L37 4v6Z" fill="{color}" opacity=".14"/><path d="M13 7h22" stroke="{color}" stroke-width="1" opacity=".6"/><circle cx="9" cy="7" r=".7" fill="{color}"/>'
    effects.append((name,40,14,svg(40,14,s)))
for f in range(4):
    s='<ellipse cx="28" cy="16" rx="26" ry="12" fill="#b2ddb1" opacity=".04"/><ellipse cx="28" cy="16" rx="22" ry="9" fill="none" stroke="#d1de9c" stroke-width=".7" opacity=".5"/><ellipse cx="28" cy="16" rx="17" ry="6.5" fill="none" stroke="#98cfb0" stroke-width=".6" opacity=".4"/>'
    for a in range(0,360,60):
        x,y=28+22*math.cos(math.radians(a+f*15)),16+9*math.sin(math.radians(a+f*15))
        s+=star(x,y,1.7,'#efe4a6',.8)
    effects.append((f'aura-{f}',56,32,svg(56,32,s)))
effects.append(('muzzle',40,40,svg(40,40,'<circle cx="20" cy="20" r="18" fill="#f2e7a1" opacity=".07"/><circle cx="20" cy="20" r="11" fill="#eaf2ba" opacity=".12"/><circle cx="20" cy="20" r="9" fill="none" stroke="#fff0b7" stroke-width="1.5"/>'+star(20,20,13,'#fff5c4')+star(8,10,2,'#c7e8b4')+star(33,27,2,'#c7e8b4'))))
effects.append(('shield',64,64,svg(64,64,'<circle cx="32" cy="32" r="28" fill="#8ecec5" opacity=".04"/><circle cx="32" cy="32" r="27" fill="none" stroke="#bcefd6" stroke-width="1" opacity=".65"/><path d="M13 21Q21 5 39 9" fill="none" stroke="#ecffec" stroke-width="2" stroke-linecap="round"/>'+star(52,17,3,'#ffffdf'))))
effects.append(('reward',64,22,svg(64,22,text(32,16,'+100',17,'#ffe9ac','middle'))))
effects.append(('mega-trail',72,28,svg(72,28,'<path d="M0 14L64 1v26Z" fill="#e6e8a5" opacity=".08"/><path d="M10 14L65 8v12Z" fill="#d7efb6" opacity=".2"/><path d="M16 14h47" stroke="#fff1c2" stroke-width="2"/>'+star(31,14,3,'#ffeabc'))))
for f in range(11):
    s='<rect x="1" y="1" width="17" height="11" rx="2" fill="#4c6657" stroke="#b7c393" stroke-width=".7"/>'+text(9,10,'E',9,'#f6e5b1','middle')+text(23,10,'爆裂种子',8,'#dbe4bc')
    s+='<rect x="66" y="3" width="153" height="7" rx="3.5" fill="#162f3b" stroke="#567469" stroke-width=".7"/>'
    if f>0:
        s+=f'<rect x="68" y="5" width="{149*f/10}" height="3" rx="1.5" fill="{["#9cc8ad","#efe1a4"][int(f==10)]}"/>'
    effects.append((f'cooldown-{f}',220,12,svg(220,12,s)))
effects.append(('missile-trail',40,14,svg(40,14,'<path d="M0 7L37 2v10Z" fill="#ffce8a" opacity=".22"/><path d="M13 7h22" stroke="#ffe6ad" stroke-width="1.4"/>'+star(10,7,2,'#c7efb0'))))
effects.append(('dash-warning',82,24,svg(82,24,'<path d="M3 4h64l12 8-12 8H3Z" fill="#ed8d82" opacity=".18" stroke="#f2ae92" stroke-dasharray="4 3"/><path d="M53 7l10 5-10 5m-24-10l10 5-10 5" fill="none" stroke="#ffe0ab" stroke-width="1.4"/>')))
effects.append(('dash-trail',82,24,svg(82,24,'<path d="M0 12L79 2v20Z" fill="#ed9d9f" opacity=".17"/><path d="M18 8h51M8 15h62M31 20h40" stroke="#ffd7af" stroke-width="1.1" opacity=".7"/>')))
for name,label in [('upgrade','武器进化！三发扇形导弹已解锁'),('weapon-ready','三发扇形导弹 · 已进化'),('weapon-0','击退 0 / 3 · 解锁三发导弹'),('weapon-1','击退 1 / 3 · 解锁三发导弹'),('weapon-2','击退 2 / 3 · 解锁三发导弹')]:
    s='<rect x="1" y="1" width="218" height="17" rx="8" fill="#1c3842" opacity=".88" stroke="#9baf83" stroke-width=".5"/>'+text(110,13,label,9,'#ffe6ad' if name=='upgrade' else '#d5dfb9','middle')
    effects.append((name,220,20,svg(220,20,s)))
effects.extend(pickup_effects)
sprite('Atmosphere',effects)
ability=[('ready',210,14,svg(210,14,text(105,11,'大招就绪 · 按 E 发射',9,'#cfe3ab','middle'))),('ready-lit',210,14,svg(210,14,text(105,11,'大招就绪 · 按 E 发射',9,'#fff1b5','middle')))]
for seconds in range(1,6):
    ability.append((f'wait-{seconds}',210,14,svg(210,14,text(105,11,f'大招冷却：{seconds} 秒',9,'#b5cabc','middle'))))
sprite('Ability',ability)

notices=[]
for name,title,subtitle,tint in [('lose','花园仍在等你','躲开孢子，守住花房，再出发一次。','#ebb7b5'),('pause','风停了一会儿','按 P 键，继续守护花园。','#b7e2ce')]:
    s=DEFS+'<rect x="6" y="10" width="326" height="166" rx="18" fill="#0c2430" opacity=".45"/><path d="M20 2H318l17 18v128l-17 18H20L2 148V20Z" fill="#2c4b50" stroke="#9f956c" stroke-width="1.5"/><path d="M22 8H316l12 15v121l-13 15H23L9 144V24Z" fill="#223b45" stroke="#627c70" stroke-width=".7"/>'
    s+='<path d="M14 35Q22 15 41 17M294 17q21-1 30 20M18 143q12 15 30 10m243 0q25 0 32-18" fill="none" stroke="#b4b27c" stroke-width="1"/>'
    s+=star(168,23,9,'#d9d69b')+text(168,63,title,23,tint,'middle')+text(168,94,subtitle,12,'#b6ccc2','middle')
    s+='<rect x="78" y="114" width="180" height="30" rx="8" fill="#576b52" stroke="#c9c18c" stroke-width=".9"/>'
    s+=text(168,134,'按 R 键重新开始',13,'#f5e7b6','middle')
    notices.append((name,338,180,svg(338,180,s)))
sprite('Notice',notices)
sprite('Hud',[(f'd{i}',12,16,svg(12,16,text(6,12,str(i),12,'#f4e3ad','middle'))) for i in range(10)])

health=[]
for kind,total in [(0,5),(1,1),(2,3)]:
    color=['#edd092','#a9e6c2','#f5a0a7'][kind]
    for current in range(total+1):
        s='<rect x="1" y="1" width="38" height="7" rx="3" fill="#17323d" stroke="#7b9b8c" stroke-width=".5"/>'
        for n in range(total):
            w=34/total-1
            fill=color if n<current else '#314d53'
            s+=f'<rect x="{3+n*34/total}" y="3" width="{w}" height="3" rx=".7" fill="{fill}"/>'
        health.append((f'hp-{kind}-{current}',40,10,svg(40,10,s)))
sprite('Health',health)

bg='''<defs>
<linearGradient id="ground" x2=".3" y2="1"><stop stop-color="#547d69"/><stop offset=".6" stop-color="#3d735d"/><stop offset="1" stop-color="#335b53"/></linearGradient>
<linearGradient id="frame" x2=".2" y2="1"><stop stop-color="#566c65"/><stop offset=".45" stop-color="#324d53"/><stop offset="1" stop-color="#233e4b"/></linearGradient>
<linearGradient id="header" x2=".8" y2="1"><stop stop-color="#4b5551"/><stop offset=".5" stop-color="#354c50"/><stop offset="1" stop-color="#263f4b"/></linearGradient>
<radialGradient id="light" cx=".75" cy=".1" r=".9"><stop stop-color="#b8d5a5" stop-opacity=".24"/><stop offset="1" stop-color="#183744" stop-opacity="0"/></radialGradient>
<radialGradient id="violet"><stop stop-color="#8f83b5" stop-opacity=".18"/><stop offset="1" stop-color="#7a6a91" stop-opacity="0"/></radialGradient>
</defs><rect width="480" height="360" fill="#243c45"/>
<rect x="5" y="42" width="470" height="287" rx="10" fill="url(#frame)" stroke="#82947b" stroke-width="1"/>
<rect x="12" y="48" width="456" height="275" rx="5" fill="url(#ground)"/>
<rect x="12" y="48" width="456" height="275" rx="5" fill="url(#light)"/>
<ellipse cx="90" cy="73" rx="95" ry="58" fill="url(#violet)"/>
<path d="M399 48L253 322h54L454 48Z" fill="#e9e1b0" opacity=".025"/>
<path d="M354 48L196 322h12L368 48Z" fill="#e9e1b0" opacity=".035"/>
'''
for row in range(12):
    for col in range(19):
        x,y=12+col*24,48+row*23
        if y<320:
            color=['#89ae83','#779c78','#b3bf8e'][(row*7+col)%3]
            if (row+col)%2==0:
                bg+=f'<path d="M{x+4} {y+14}l2-4 1 4 3-3m3 5l1-3 2 3" stroke="{color}" stroke-width=".6" fill="none" opacity=".35"/>'
            if (row*13+col)%11==0:
                bg+=f'<ellipse cx="{x+11}" cy="{y+10}" rx="7" ry="3" fill="#a6b790" opacity=".08"/>'
for y in range(55,321,29):
    bg+=f'<path d="M6 {y}l4 5-3 7m463-10l-3 5 4 9" fill="none" stroke="#a2aa83" stroke-width=".6" opacity=".7"/>'
for x,y in [(19,62),(460,315),(20,312),(455,61)]:
    for a in [0,60,120,180,240,300]:
        dx,dy=math.cos(math.radians(a))*5,math.sin(math.radians(a))*5
        bg+=f'<ellipse cx="{x+dx}" cy="{y+dy}" rx="3.5" ry="1.5" transform="rotate({a} {x+dx} {y+dy})" fill="#9fae79" opacity=".8"/>'
    bg+=f'<circle cx="{x}" cy="{y}" r="2" fill="#d4bf8b"/>'
# Keep the hand-painted ground separate from the transparent, outlined UI.
painted=ROOT/'assets/painted-ground.png'
if painted.exists():
    bg=bg.split('</defs>')[0]+'</defs>'
bg+='''<path d="M14 2h452l11 9v24l-11 9H14L3 35V11Z" fill="url(#header)" stroke="#9b946f" stroke-width="1.2"/>
<path d="M17 6h446l8 7v19l-8 7H17L9 32V13Z" fill="none" stroke="#647c72" stroke-width=".6"/>
<path d="M31 9l10 6-3 12-11 4-10-7 2-12Z" fill="#516c61" stroke="#b7b681"/>
<circle cx="29" cy="20" r="7" fill="none" stroke="#e5d6a0" stroke-width="1"/>
'''+star(29,20,5,'#e5d6a0')
bg+=text(48,21,'暮光花园',17,'#f5dfab')+text(459,19,'守住花房，让光留下。',9,'#b6cdc0','end')
bg+=text(38,37,'得分',9,'#b9ccb9')+text(164,37,'生命',9,'#b9ccb9')+text(285,37,'击退僵尸',9,'#b9ccb9')
bg+='<path d="M191 30c-4-5-8 1 0 6 8-5 4-11 0-6" fill="#d99d9e" stroke="#d9b8a3" stroke-width=".5"/>'
bg+='<path d="M12 330h456l7 8v15l-8 5H13l-8-5v-15Z" fill="#2a454b" stroke="#6e8474" stroke-width=".8"/>'
bg+=text(240,353,'1P WASD / 空格 / E　2P 方向键 / J / K　P 暂停　R 重开　M 选关',9,'#d8dfbd','middle')
(ROOT/'assets/arena.svg').write_text(svg(480,360,bg),encoding='utf-8')
sprite('Frame',[('frame',480,360,svg(480,360,bg))])
image_width,image_height=Image.open(painted).size
write_json('assets/index.json',{'backdrops':[{'name':'暮光花园','path':'painted-ground.png','x':image_width/2,'y':image_height/2,'bitmapResolution':max(1,round(image_width/480)),'imageWidth':image_width,'imageHeight':image_height}], 'backdropIndex':0,'map':{'width':480,'height':360},'run':{'width':480,'height':360},'physics':False,'stretchMode':True,'maxFPS':60,'fontPreferences':['garden-chinese','default'],'zorder':['Atmosphere','Actor','Health','Frame','Hud','Ability','Buff','Notice']})
write_json('builder-meta.json',{'displayName':'暮光花园 · 僵尸进化生存版','description':'三种专属造型僵尸持续随机刷新：重甲5血慢速、疾跑1血高速、冲锋3血每3秒冲刺3格。树篱破坏6秒后渐进生长，三杀解锁扇形导弹。新增随机坚果盾、樱桃炸弹、蘑菇和辣椒道具，具备专属造型、特效和中文增益提示。','instructions':'方向键 / WASD 移动；空格射击；E 爆裂种子（5秒冷却，范围伤害3点）；P 暂停；R 重开。靠近道具自动拾取：坚果盾抵挡3次伤害/10秒；樱桃立即范围伤害5点；蘑菇加速55%/8秒；辣椒普通攻击伤害+1/8秒，可叠加三发导弹。角色3条生命，生命耗尽或花房被毁时结束；持续生存，无固定通关数量。'})
from campaign_art import extend
extend(sprite, text)
font_dir=ROOT/'assets/fonts/garden-chinese'
font_dir.mkdir(parents=True,exist_ok=True)
all_text='0123456789'
for image in (ROOT/'assets').rglob('*.svg'):
    doc=ET.fromstring(image.read_text())
    all_text+=''.join(node.get('aria-label','') for node in doc.iter())
font=TTFont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',fontNumber=0)
sub=subset.Subsetter(); sub.populate(text=all_text); sub.subset(font); font.save(font_dir/'font.ttf')
shutil.copyfile('/usr/share/doc/fonts-wqy-zenhei/copyright',font_dir/'LICENSE.txt')
(font_dir/'NOTICE.txt').write_text('WenQuanYi Zen Hei subset; glyph outlines used in SVG artwork. Source: Ubuntu fonts-wqy-zenhei package. See LICENSE.txt for license and font embedding exception.\n')
write_json('assets/fonts/garden-chinese/index.json',{'faces':[{'path':'font.ttf'}]})
out=ROOT.parent/'暮光花园-双人闯关版.xbp'
with ZipFile(out,'w',ZIP_DEFLATED) as archive:
    for file in ROOT.rglob('*'):
        if file.is_file() and file.suffix in {'.spx','.svg','.json','.ttf','.txt','.png','.md'} and not file.name.startswith(('preview-','demo-','logic_test','campaign_test','campaign-frames')):
            archive.write(file,file.relative_to(ROOT).as_posix())
print(out)
