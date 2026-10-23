"""Power-up art, called by the project's main asset builder."""

def generate(svg, text, star, defs):
    frames=[]; effects=[]; panels=[]
    colors=['#f2ce91','#f39c9f','#8fd8dc','#ffb37b']
    for kind in range(4):
        for f in range(2):
            c=colors[kind]
            s=defs+f'<ellipse cx="20" cy="37" rx="16" ry="4" fill="{c}" opacity=".14"/><ellipse cx="20" cy="37" rx="14" ry="3" fill="none" stroke="{c}" stroke-width=".8"/><circle cx="20" cy="20" r="{16+f}" fill="{c}" opacity=".07"/>'
            if kind==0:
                s+='<path d="M8 11Q20 1 32 11v13Q29 32 20 36Q9 32 8 24Z" fill="#73543e" stroke="#e1b580" stroke-width="1.2"/><path d="M11 12Q20 5 29 12v11Q27 29 20 32Q13 29 11 23Z" fill="url(#gold)"/><path d="M20 10v19m-5-14l-2 6 4 5m8-11l2 7-4 5" stroke="#a3754e" stroke-width="1.4" fill="none"/><ellipse cx="16" cy="19" rx="1.5" ry="2" fill="#523e3c"/><ellipse cx="24" cy="19" rx="1.5" ry="2" fill="#523e3c"/>'
            if kind==1:
                s+='<path d="M13 19Q12 5 23 5Q29 10 29 20" stroke="#82bb78" stroke-width="2" fill="none"/><path d="M22 5q5-7 11-2-5 5-11 2" fill="#a9d58c"/><circle cx="12" cy="25" r="9" fill="#d66e80" stroke="#7e4e63"/><circle cx="28" cy="25" r="9" fill="#f18d92" stroke="#7e4e63"/><path d="M7 21l4-2m13 2l4-2" stroke="#ffe0c2" stroke-width="2" stroke-linecap="round"/><path d="M24 8l5-6" stroke="#f6c79e"/>'
                s+=star(30,2,3+f,'#ffe5a1')
            if kind==2:
                s+='<path d="M15 19l-2 14q7 5 14 0l-2-14" fill="#efe6c6" stroke="#6a9d9e"/><path d="M3 21Q4 3 20 3Q36 3 37 21Q20 27 3 21Z" fill="#6ebcc1" stroke="#3d7789" stroke-width="1.2"/><circle cx="13" cy="12" r="3.4" fill="#d5f3d0"/><circle cx="27" cy="14" r="4" fill="#d5f3d0"/><circle cx="20" cy="7" r="2" fill="#e2f7d7"/><path d="M10 31l-7 3m26-2l8 2" stroke="#91e7d8" stroke-width="1.2"/>'
            if kind==3:
                s+='<path d="M21 12Q31 9 32 20Q30 33 8 35Q21 29 18 20Q14 16 21 12Z" fill="#ec846e" stroke="#a44c5b" stroke-width="1.2"/><path d="M23 12q-4-9 4-10" fill="none" stroke="#9dc67d" stroke-width="3"/><path d="M19 12l7-3 5 6-8 1Z" fill="#81ad72"/><path d="M25 18q5 7-5 12" fill="none" stroke="#ffe1a0" stroke-width="1.4"/><path d="M7 26Q-1 17 9 10Q5 19 13 22Z" fill="#ffc67e" opacity=".7"/>'
            s+=star(5,7,2,'#ffebba',.8)+star(35,31,1.5,'#e7f3c7')
            frames.append((f'pickup-{kind}-{f}',40,42,svg(40,42,s)))
    for f in range(2):
        s=f'<circle cx="10" cy="10" r="{9-f}" fill="#ffa470" opacity=".2"/><path d="M7 17Q-1 11 8 2Q7 8 13 5Q20 15 11 18Z" fill="#f2996d"/><circle cx="10" cy="11" r="4" fill="#ffe3a0"/>'
        frames.append((f'fire-seed-{f}',20,20,svg(20,20,s)))
        s='<path d="M0 10Q7 1 16 6L25 4l8 6-8 6-12-2Q5 20 0 10Z" fill="#f5a875" stroke="#ffd19b"/><path d="M15 9h14" stroke="#fff0b7" stroke-width="3"/><path d="M16 6l-5-4 10 4m-5 8l-5 4 10-4" fill="#a7d69b"/>'
        frames.append((f'fire-missile-{f}',36,20,svg(36,20,s)))
    for f in range(8):
        r=[12,30,52,76,94,100,100,100][f];opacity=1-f*.11
        s=f'<circle cx="110" cy="110" r="{r}" fill="#e9948d" opacity="{opacity*.15}"/><circle cx="110" cy="110" r="{r}" fill="none" stroke="#ffc49c" stroke-width="{4-f*.4}" opacity="{opacity}"/>'
        for n in range(8):
            import math
            a=n*math.pi/4+f*.15;x=110+math.cos(a)*r;y=110+math.sin(a)*r
            s+=star(x,y,6-f*.4,['#fbc9a3','#ef9caa'][n%2],opacity)
        frames.append((f'cherry-burst-{f}',220,220,svg(220,220,s)))
    effects.append(('fire-trail',48,20,svg(48,20,'<path d="M1 10L43 1v18Z" fill="#f59b76" opacity=".25"/><path d="M7 10l12-5-3 5 15-3-5 5 17-2" fill="#ffe6a4" opacity=".8"/>')))
    effects.append(('nut-shield',68,68,svg(68,68,'<path d="M9 11Q34-1 59 11v25Q54 55 34 64Q14 55 9 36Z" fill="#e8c68d" opacity=".12" stroke="#f1d79f" stroke-width="1.2"/><path d="M17 16Q34 7 51 16" stroke="#fff0c9" stroke-width="1.4" fill="none"/>'+star(12,27,3,'#ffedb4'))))
    effects.append(('speed-wake',74,36,svg(74,36,'<path d="M1 9h24M6 18h29M0 27h25" stroke="#a6efe5" stroke-width="1.7" opacity=".8"/><path d="M21 3Q37 18 21 33" stroke="#baf4dc" stroke-width="1" fill="none" opacity=".45"/>')))
    effects.append(('pepper-aura',62,62,svg(62,62,'<ellipse cx="31" cy="46" rx="25" ry="10" fill="#fa9a74" opacity=".12"/><path d="M9 42Q1 26 14 18Q8 32 19 37m31 5q12-17-2-26 7 15-6 21" fill="#fbb27e" opacity=".65"/>'+star(9,10,3,'#ffd4a0')+star(52,28,2,'#ffe3ad'))))
    def panel(name,label,color='#d8ebcb',width=144):
        s=f'<rect x="1" y="1" width="{width-2}" height="17" rx="7" fill="#213c43" opacity=".94" stroke="#8e9e7c" stroke-width=".6"/>'+text(width/2,13,label,9,color,'middle')
        panels.append((name,width,20,svg(width,20,s)))
    for charges in range(1,4):
        for sec in range(1,11): panel(f'shield-{charges}-{sec}',f'坚果盾 ×{charges} · {sec}秒','#f1d7a5')
    for sec in range(1,9):
        panel(f'speed-{sec}',f'蘑菇加速 +55% · {sec}秒','#b3e9df')
        panel(f'pepper-{sec}',f'辣椒增伤 +1 · {sec}秒','#ffd1aa')
    for kind,label in enumerate(['坚果盾！可抵挡三次伤害','樱桃炸弹！范围爆炸','蘑菇！移动速度提高','辣椒！火焰弹伤害提高']): panel(f'picked-{kind}',label,colors[kind],220)
    return frames,effects,panels
