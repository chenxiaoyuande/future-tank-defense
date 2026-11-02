"""Original illustrated pea, mushroom and melon professions with structural evolution."""
import json
import math

from art_utils import ROOT, svg, write_json

ROLES_ZH = ["豌豆射手", "灵孢蘑菇", "西瓜投手"]
ROLES_EN = ["Pea Gunner", "Spore Mage", "Melon Artillery"]
ROUTES_ZH = [
    ["豌豆幼苗","豌豆射手","加特林豌豆","双头加特林","钢叶炮台","日曜豌豆要塞"],
    ["蘑菇幼苗","喷孢蘑菇","荧光大喷菇","三生孢子菇","幻夜巫师菇","星穹菌王"],
    ["西瓜幼苗","西瓜投手","双瓜投手","重装瓜炮","寒霜西瓜","泰坦瓜城"],
]
ROUTES_EN = [
    ["Pea Sprout","Peashooter","Gatling Pea","Twin Gatling","Steel Bastion","Solar Citadel"],
    ["Fungal Sprout","Spore Shroom","Glow Shroom","Triple Shroom","Night Alchemist","Astral Mycelium"],
    ["Melon Sprout","Melon Pult","Twin Melon","Siege Melon","Winter Melon","Titan Orchard"],
]
COLORS = ["#acd68a","#c4a1ed","#e8bd86"]
DEFS = '''<defs>
<radialGradient id="pea" cx=".28" cy=".22" r=".9"><stop stop-color="#e2f4af"/><stop offset=".35" stop-color="#9acb75"/><stop offset=".72" stop-color="#548c62"/><stop offset="1" stop-color="#254a47"/></radialGradient>
<linearGradient id="leaf" x2=".7" y2="1"><stop stop-color="#d0e8a0"/><stop offset=".4" stop-color="#74a873"/><stop offset="1" stop-color="#28534e"/></linearGradient>
<linearGradient id="metal" x2=".8" y2=".8"><stop stop-color="#e8dca7"/><stop offset=".3" stop-color="#a6ad87"/><stop offset=".6" stop-color="#577c70"/><stop offset="1" stop-color="#294a4e"/></linearGradient>
<linearGradient id="brass" x2=".7" y2="1"><stop stop-color="#ffedb7"/><stop offset=".4" stop-color="#bfa26b"/><stop offset="1" stop-color="#685d52"/></linearGradient>
<radialGradient id="cap" cx=".25" cy=".2" r=".95"><stop stop-color="#e5c8ec"/><stop offset=".3" stop-color="#ad83bf"/><stop offset=".7" stop-color="#635881"/><stop offset="1" stop-color="#303b5b"/></radialGradient>
<linearGradient id="stem" x2=".9" y2=".3"><stop stop-color="#dbd7c4"/><stop offset=".4" stop-color="#b2b7b5"/><stop offset="1" stop-color="#6b8190"/></linearGradient>
<linearGradient id="gills" x2="0" y2="1"><stop stop-color="#d0bae4"/><stop offset=".5" stop-color="#8a76a9"/><stop offset="1" stop-color="#4f526f"/></linearGradient>
<radialGradient id="melon" cx=".3" cy=".25" r=".85"><stop stop-color="#d4e4a0"/><stop offset=".4" stop-color="#8cb779"/><stop offset=".75" stop-color="#4e8166"/><stop offset="1" stop-color="#294e4b"/></radialGradient>
<radialGradient id="icefruit" cx=".3" cy=".2" r=".9"><stop stop-color="#e3fbf1"/><stop offset=".4" stop-color="#a8d6d2"/><stop offset="1" stop-color="#386a86"/></radialGradient>
<linearGradient id="wood" x2=".7" y2="1"><stop stop-color="#ceb58a"/><stop offset=".4" stop-color="#8d7b61"/><stop offset="1" stop-color="#4c5652"/></linearGradient>
<radialGradient id="glow"><stop stop-color="#fffde5"/><stop offset=".35" stop-color="#d3e9a4"/><stop offset="1" stop-color="#85b481" stop-opacity="0"/></radialGradient>
<radialGradient id="violet"><stop stop-color="#fff4ff"/><stop offset=".35" stop-color="#d6b3ed"/><stop offset="1" stop-color="#8478bb" stop-opacity="0"/></radialGradient>
</defs>'''


def p(d: str, fill: str, stroke: str = "#25434b", width: float = 1.5, extra: str = "") -> str:
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def leaf(x: float, y: float, side: int, size: float = 1) -> str:
    return f'<g transform="translate({x} {y}) scale({side*size} {size})">'+p("M0 0Q-13-20-28-11q-1 20 28 11Z","url(#leaf)")+p("M-2-1l-20-9m11 4l-2-6m-3 4l-5 3","none","#c7dfa0",.8)+'</g>'


def eyes(x: float, y: float, frame: int, size: float = 1, color: str = "#254b4d") -> str:
    if frame == 2:
        return p(f"M{x-9*size} {y}q{3*size} {2*size} {6*size} 0m{6*size} 0q{3*size} {2*size} {6*size} 0","none",color,1.6)
    art=''
    for side in [-1,1]:
        cx=x+side*6*size
        art+=f'<ellipse cx="{cx}" cy="{y}" rx="{4*size}" ry="{5*size}" fill="#f4f6db" stroke="#6e9c80" stroke-width=".7"/><ellipse cx="{cx+size*.5}" cy="{y+size}" rx="{2*size}" ry="{3*size}" fill="{color}"/><circle cx="{cx-size}" cy="{y-size}" r="{size}" fill="#fffef4"/>'
    return art


def pea_head(x: float, y: float, radius: float, barrels: int, direction: int, frame: int, plated: bool) -> str:
    dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][direction]
    recoil=2 if frame>=4 else 0
    weapon=''
    for n in range(barrels):
        offset=(n-(barrels-1)/2)*5.5
        sx=x-dy*offset+dx*4;sy=y+5+dx*offset+dy*4
        ex=sx+dx*(radius+4-recoil);ey=sy+dy*(radius+4-recoil)
        weapon+=p(f"M{sx} {sy}L{ex} {ey}","none","#294a4b",7 if barrels==1 else 5)
        weapon+=p(f"M{sx-1} {sy-1}L{ex-1} {ey-1}","none","#b4cc94" if barrels==1 else "#b9b792",4 if barrels==1 else 2.8)
        weapon+=f'<ellipse cx="{ex}" cy="{ey}" rx="{3 if dx else 4}" ry="{4 if dx else 2.8}" fill="#233f46" stroke="#d1d9a5" stroke-width=".8"/>'
        if frame>=4:
            weapon+=f'<circle cx="{ex+dx*3}" cy="{ey+dy*3}" r="3" fill="#f0f5bd"/>'
    head=f'<circle cx="{x}" cy="{y}" r="{radius}" fill="url(#pea)" stroke="#294d4d" stroke-width="1.8"/>'
    head+=p(f"M{x-radius*.6} {y-radius*.5}q{radius*.4} {-radius*.4} {radius*.9} {-radius*.2}","none","#eff5c2",1.8)
    head+=eyes(x,y-3,frame,.8)
    if plated:
        head+=p(f"M{x-radius} {y-7}l4-10 {radius-4}-5 {radius-4} 5 4 10-8-4-10 2-10-2Z","url(#metal)",width=1.2)
        for side in [-1,1]:
            head+=f'<circle cx="{x+side*(radius-3)}" cy="{y-5}" r="1.6" fill="#f4e5b1"/>'
    return weapon+head if direction==0 else head+weapon


def pea(tier: int, direction: int, frame: int) -> str:
    art=leaf(45,91,1)+leaf(51,91,-1)
    art+=p("M48 88q-11-14 0-32","none","#31554c",10)+p("M47 84q-6-13 1-24","none","#a3cd86",3)
    art+=leaf(37,72,1,.7)+leaf(60,72,-1,.7)
    if tier>=1:
        art+=p("M32 69l16-7 16 7-3 14-13 5-13-5Z","url(#metal)",width=1.5)
        art+=p("M36 73l12 5 12-5m-12 5v8","none","#d4dbaa",1)
    if tier>=4:
        art+=p("M20 85l9-12h38l10 12-5 10H25Z","url(#metal)",width=2)
        for x in [30,42,54,66]:
            art+=f'<circle cx="{x}" cy="90" r="5" fill="#29484d" stroke="#a9bd94"/>'
    if tier<3:
        art+=pea_head(48,36,19 if tier else 16,4 if tier>=2 else 1,direction,frame,tier>=2)
        art+=leaf(49,15,-1,.45)
    elif tier<5:
        art+=p("M48 70V54m-1 1L31 46m18 9l16-9","none","#50775c",8)
        art+=pea_head(29,38,15,3,direction,frame,True)+pea_head(67,38,15,3,direction,frame,True)
        if tier==4:
            art+=p("M41 52l7-7 7 7-7 10Z","url(#brass)")
            art+=f'<circle cx="48" cy="53" r="4" fill="#e6efb6"/>'
    else:
        art+=pea_head(26,43,14,3,direction,frame,True)+pea_head(70,43,14,3,direction,frame,True)
        art+=pea_head(48,26,17,4,direction,frame,True)
        art+=p("M33 13l2-11 13 7 13-7 2 11","url(#brass)","#e4cf92",1)
        art+=f'<ellipse cx="48" cy="7" rx="19" ry="4" fill="none" stroke="#f0d995" stroke-width="1.4"/>'
        for x in [13,83]:
            art+=leaf(x,75,-1 if x==13 else 1,.55)
    return art


def cap(x: float, y: float, radius: float, tier: int, frame: int) -> str:
    art=f'<ellipse cx="{x}" cy="{y+5}" rx="{radius}" ry="{radius*.23}" fill="url(#gills)" stroke="#3f405b" stroke-width="1.2"/>'
    for n in range(9):
        xx=x-radius+3+n*(radius*2-6)/8
        art+=p(f"M{xx} {y+4}L{x+(xx-x)*.3} {y+radius*.24}","none","#e3c4e9",.6)
    art+=p(f"M{x-radius} {y}Q{x-radius*.75} {y-radius*.9} {x} {y-radius*.82}Q{x+radius*.8} {y-radius*.8} {x+radius} {y}Q{x} {y+radius*.24} {x-radius} {y}Z","url(#cap)","#3e435c",1.6)
    art+=p(f"M{x-radius*.7} {y-radius*.33}q{radius*.35} {-radius*.35} {radius*.7} {-radius*.23}","none","#f0d1ec",1.3)
    for n in range(6):
        xx=x+math.cos(n*1.7)*radius*.64;yy=y-radius*.25+math.sin(n*1.7)*radius*.23
        art+=f'<ellipse cx="{xx:.2f}" cy="{yy:.2f}" rx="{2+n%2}" ry="1.5" fill="{"#dfc1e9" if tier<4 else "#e8e2ff"}" opacity=".8"/>'
    if tier>=4:
        art+=p(f"M{x-radius*.7} {y-2}l5-4 5 4 5-4 5 4m5 0l5-4 5 4", "none","#d2b5ee",1)
    return art


def mushroom(tier: int, direction: int, frame: int) -> str:
    art=leaf(42,93,1,.8)+leaf(54,93,-1,.8)
    if tier>=4:
        art+=p("M31 56Q18 73 24 95l24-7 25 7q5-25-10-39Z","#485371","#a99cc7",1.4)
        for x in [29,37,60,67]:
            art+=p(f"M{x} 70l{(48-x)*.3} 19","none","#bdacd8",.8)
    art+=p("M38 50Q30 71 34 89q13 12 29 0 4-24-6-39Z","url(#stem)",width=1.8)
    art+=p("M39 68l-1 17m8-27v30m10-24l2 20","none","#e1e0cb",.9)
    art+=eyes(48,64,frame,.8,"#4e486e")
    art+=p("M43 76q5 3 10-1","none","#6f6b80",1)
    radius=23+tier*2.4
    if tier==0: radius=20
    art+=cap(48,44,radius,tier,frame)
    if tier>=1:
        for n in range(7):
            x=35+n*4.3
            art+=p(f"M{x} 54l2 7 2-7Z","#c9aedb","#6a6387",.6)
    if tier>=2:
        art+=f'<ellipse cx="48" cy="48" rx="{radius+2}" ry="7" fill="none" stroke="#e5c8ff" stroke-width="1.1"/>'
        for x,y in [(18,40),(79,43),(26,83),(73,83)]:
            art+=f'<circle cx="{x}" cy="{y}" r="5" fill="url(#violet)"/><circle cx="{x}" cy="{y}" r="1.3" fill="#e9ccfa"/>'
    if tier>=2:
        for x,side in [(25,1),(72,-1)]:
            art+=p(f"M{x} 64q{-side*9} 10 {-side*4} 20","none","#9ca5b3",3)
    if tier>=3:
        art+=p("M28 87q-9-15-10-23m49 23q10-15 12-23","none","#9e9dbb",4)
        art+=cap(15,63,12,tier,frame)+cap(81,63,12,tier,frame)
    if tier>=4:
        art+=p("M79 93L82 41","none","#65758b",4)+p("M81 92L83 40","none","#d1b1df",1)
        art+=f'<circle cx="83" cy="34" r="10" fill="url(#violet)"/><circle cx="83" cy="34" r="5" fill="#d6b5ed" stroke="#f0d7ff"/>'
    if tier==5:
        art+=cap(48,20,23,tier,frame)
        art+=f'<ellipse cx="48" cy="18" rx="32" ry="7" fill="none" stroke="#d6c8f6" stroke-width="1.2"/>'
        for side in [-1,1]:
            art+=p(f"M{48+side*17} 76q{side*20} -1 {side*20} 18m{-side*12} -13q{side*16} 0 {side*13} 14","none","#b7a8d9",2)
    if frame>=4:
        dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][direction]
        art+=f'<circle cx="{48+dx*31}" cy="{62+dy*27}" r="12" fill="url(#violet)"/>'
    return art


def fruit(x: float, y: float, rx: float, ry: float, icy: bool = False) -> str:
    art=f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#{"icefruit" if icy else "melon"})" stroke="#2a4e4c" stroke-width="1.5"/>'
    for factor in [-.65,-.28,.15,.58]:
        xx=x+rx*factor
        art+=p(f"M{xx} {y-ry*.83}q{-rx*.38} {ry*.7} 0 {ry*1.65}","none","#4c8490" if icy else "#3b7259",rx*.12)
    art+=p(f"M{x-rx*.5} {y-ry*.58}q{rx*.32} {-ry*.25} {rx*.56} {-ry*.1}","none","#e5efb8" if not icy else "#eeffff",1.5)
    return art


def melon(tier: int, direction: int, frame: int) -> str:
    art=leaf(35,92,1,.8)+leaf(61,92,-1,.8)
    art+=p("M23 72h49l8 17-10 8H26l-9-8Z","url(#wood)",width=2)
    for x in [26,36,48,60,70]:
        art+=p(f"M{x} 77l1 16","none","#d5bf93",1)
    if tier>=3:
        for x in [23,73]:
            art+=f'<circle cx="{x}" cy="90" r="10" fill="url(#wood)" stroke="#284b4c" stroke-width="2"/><circle cx="{x}" cy="90" r="4" fill="#567b6b" stroke="#d0bd8b"/>'
        art+=p("M18 74l12-10h35l14 10-6 10H24Z","url(#metal)",width=1.5)
    if tier<2:
        art+=fruit(48,52,19+tier*6,19+tier*4)
        art+=eyes(48,53,frame,.8)
    elif tier<5:
        art+=fruit(31,52,19,22,tier==4)+fruit(65,52,19,22,tier==4)
        art+=eyes(31,53,frame,.65)+eyes(65,53,frame,.65)
        if tier>=3:
            art+=fruit(48,33,14,13,tier==4)
    else:
        art+=fruit(48,38,28,25,True)
        art+=fruit(20,65,15,16,True)+fruit(76,65,15,16,True)
        art+=eyes(48,39,frame,1)
        art+=p("M24 24l3-15 13 7 9-12 9 12 13-7 2 15-25 6Z","url(#brass)","#d8c58d",1.2)
        art+=p("M29 65h38l-3 17H33Z","url(#metal)")
    # The lever and cup change aim without rotating the fruit or its chassis.
    dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][direction]
    recoil=3 if frame>=4 else 0
    ex=48+dx*(32-recoil);ey=64+dy*(28-recoil)
    art+=p(f"M39 79L{ex} {ey}","none","#304e49",7)+p(f"M39 77L{ex} {ey-1}","none","#c7b58a",3)
    art+=p(f"M{ex-9} {ey-3}q9 17 18 0m-13 7l-4 8","none","#b3c78c",2)
    art+=fruit(ex,ey-4,7,6,tier>=4)
    art+=p("M39 79l15-2m-10-4l-1 13","none","#e5d49e",1)
    if tier==4:
        for x,y in [(12,39),(83,39),(48,15)]:
            art+=p(f"M{x} {y-7}l5 7-5 8-5-8Z","#b6e0e3","#eefcfa",.7)
    return art


def hero(role: int, tier: int, player: int, direction: int, frame: int) -> str:
    breathe=[0,1,0,-1,0,.5][frame]
    art=DEFS+'<g transform="scale(.5)"><ellipse cx="48" cy="98" rx="37" ry="5" fill="#153441" opacity=".5"/>'
    form=[pea,mushroom,melon][role](tier,direction,frame)
    if tier==0:form='<g transform="translate(10.56 19.8) scale(.78)">'+form+'</g>'
    art+=f'<g transform="translate(0 {breathe})">'+form+'</g>'
    badge="#ebd49d" if player==1 else "#a7e8ff"
    art+=f'<circle cx="80" cy="91" r="6" fill="#1c3c47" stroke="{badge}" stroke-width="1.2"/>'
    art+=p("M78 90l2-2v7m-2 0h4" if player==1 else "M78 90q0-4 4-2 2 2-4 5h5","none",badge,1.1)
    return svg(48,52,art+'</g>')


def shot(role: int, tier: int, frame: int, heavy: bool = False) -> str:
    if role==2:
        decor=''
        if tier>=2:decor+=p("M13 18l-5-8m79 8l5-8M9 73l-5 7","none","#e6d49e",3)
        if tier>=4:decor+=p("M50 5V16m-5-5h10M12 45v10m-5-5h10M88 45v10m-5-5h10","none","#ddfffa",3)
        if tier==5:decor+='<ellipse cx="50" cy="50" rx="47" ry="20" fill="none" stroke="#ffe8ac" stroke-width="3"/>'
        return svg(40 if heavy else 24,40 if heavy else 24,f'<g transform="scale({.4 if heavy else .24})">'+DEFS+fruit(50,50,34+tier*1.4,33+tier*1.6,tier>=4)+decor+p("M47 10q-12-12-22-6m23 7l10-7","none","#c5df9c",3)+'</g>')
    color=COLORS[role]
    art=f'<circle cx="12" cy="12" r="11" fill="{color}" opacity=".1"/><circle cx="12" cy="12" r="{6+frame}" fill="{color}" opacity=".27"/>'
    if role==0:
        art+=f'<circle cx="12" cy="12" r="{4+tier*.4}" fill="{["#9fc77f","#b4dd91","#cee7a2","#e5dda0","#e5e9ba","#fff1b8"][tier]}" stroke="#f2f5cb"/><ellipse cx="10" cy="10" rx="2" ry="1.2" fill="#fff9db"/>'
        if tier>=2:art+=p("M1 10h5M0 14h5","none","#c8e7a0",1.5)
        if tier>=3:art+='<circle cx="12" cy="12" r="9" fill="none" stroke="#e6dfa1" stroke-width=".8"/>'
        if tier==5:art+=p("M12 0v5m0 14v5M0 12h5m14 0h5","none","#fff5c4",1.1)
    else:
        for n in range(3+tier):
            x=12+math.cos(n*math.tau/(3+tier)+frame)*(5+tier*.5);y=12+math.sin(n*math.tau/(3+tier)+frame)*(5+tier*.5)
            art+=f'<circle cx="{x}" cy="{y}" r="2.5" fill="#e1c5ed" stroke="#f6e8ff" stroke-width=".5"/>'
        art+=p("M8 12q4-9 8 0-3 6-8 0Z","#c3a2df","#fff1ff",.8)
        if tier>=4:art+='<ellipse cx="12" cy="12" rx="10" ry="6" fill="none" stroke="#ead1ff" stroke-width=".8"/>'
    return svg(24,24,art)


def cloud(tier: int, frame: int) -> str:
    art='<circle cx="65" cy="65" r="57" fill="#9c7fc0" opacity=".12"/><circle cx="65" cy="65" r="50" fill="none" stroke="#c6a5e5" stroke-dasharray="5 6" opacity=".6"/>'
    for n in range(15):
        a=n*2.4+frame*.2;r=12+n%5*9
        x=65+math.cos(a)*r;y=65+math.sin(a)*r
        art+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{4+n%4*2}" fill="#bfa0d5" opacity=".2"/><circle cx="{x:.2f}" cy="{y-3:.2f}" r="2" fill="#e4cef2" opacity=".8"/>'
    return svg(130,130,art)


def burst(role: int, tier: int, frame: int) -> str:
    r=8+frame*8;alpha=max(0,1-frame/10);color=COLORS[role]
    art=f'<circle cx="100" cy="100" r="{r}" fill="{color}" opacity="{alpha*.1}"/><circle cx="100" cy="100" r="{r}" fill="none" stroke="{color}" stroke-width="{3*alpha}"/>'
    for n in range(12):
        a=n*math.pi/6;x=100+math.cos(a)*r*.8;y=100+math.sin(a)*r*.8
        if role==2:
            art+=p(f"M{x} {y}l6 3-5 8-4-5Z","#d99b88" if tier!=4 else "#c2e8e9","#7eab81",1, f'opacity="{alpha}"')
        else:
            art+=f'<circle cx="{x}" cy="{y}" r="{3+role}" fill="{color}" opacity="{alpha}"/>'
    return svg(200,200,art)


def extend() -> None:
    directory=ROOT/"assets/sprites/Actor";data=json.loads((directory/"index.json").read_text())
    # Old costume aliases remain for old previews; gameplay uses the new profession names.
    extra=[]
    for role in range(3):
        for tier in range(6):
            for player in [1,2]:
                for d,name in enumerate(["up","right","down","left"]):
                    for frame in range(6):
                        extra.append((f"hero-{role}-{tier}-p{player}-{name}-{frame}",48,52,hero(role,tier,player,d,frame)))
            for frame in range(2):
                extra.append((f"role-shot-{role}-{tier}-{frame}",24,24,shot(role,tier,frame)))
                if role==2:
                    extra.append((f"role-heavy-{tier}-{frame}",40,40,shot(role,tier,frame,True)))
            for frame in range(4):
                if role==1:extra.append((f"role-cloud-{tier}-{frame}",130,130,cloud(tier,frame)))
            for frame in range(10):
                extra.append((f"role-burst-{role}-{tier}-{frame}",200,200,burst(role,tier,frame)))
    for name,w,h,content in extra:
        (directory/f"{name}.svg").write_text(content,encoding="utf-8")
        data["costumes"].append({"name":name,"path":name+".svg","x":w/2,"y":h/2,"imageWidth":w,"imageHeight":h,"bitmapResolution":1,"faceRight":0})
    write_json("assets/sprites/Actor/index.json",data)
