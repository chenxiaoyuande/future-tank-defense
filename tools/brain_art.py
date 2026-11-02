"""Draw the protected brain objective as native SVG costumes."""
import math
from art_utils import svg

DEFS='''<defs>
<radialGradient id="brain-pink" cx=".35" cy=".25" r=".9"><stop stop-color="#ffe0cf"/><stop offset=".45" stop-color="#eaa6a9"/><stop offset="1" stop-color="#9d657f"/></radialGradient>
<linearGradient id="brain-stem" x2=".7" y2="1"><stop stop-color="#f2c7b2"/><stop offset="1" stop-color="#9c7d91"/></linearGradient>
<radialGradient id="brain-aura"><stop stop-color="#a4f0dc" stop-opacity=".1"/><stop offset=".75" stop-color="#6cbfca" stop-opacity=".12"/><stop offset="1" stop-color="#b4f3e0" stop-opacity=".3"/></radialGradient>
</defs>'''


def brain(strength=10, frame=0):
    art=DEFS+'<ellipse cx="32" cy="48" rx="23" ry="3" fill="#102f38" opacity=".55"/><path d="M13 45q19 9 38 0l-4 5H17Z" fill="#45675f" stroke="#a6be91" stroke-width=".8"/>'
    if strength:
        color="#b5eadb" if strength>3 else "#f5ca9f"
        art+=f'<ellipse cx="32" cy="28" rx="28" ry="22" fill="url(#brain-aura)" stroke="{color}" stroke-width="1.2" opacity="{.75+frame*.05}"/>'
        art+='<path d="M10 26q3-12 16-15M12 21q4-6 10-8" fill="none" stroke="#edfff0" stroke-width="1.2" stroke-linecap="round" opacity=".8"/>'
        for n in range(6):
            a=n*math.pi/3+frame*.035;x=32+math.cos(a)*27;y=28+math.sin(a)*21
            art+=f'<path d="M{x-1:.2f} {y-2:.2f}l2 2-2 2-2-2Z" fill="{color}"/>'
    art+='<path d="M28 37q-1 5 3 9l5-1-2-9" fill="url(#brain-stem)" stroke="#8d6378" stroke-width="1"/>'
    art+='<path d="M31 18C27 12 19 14 18 19c-6 0-9 7-6 12-2 5 2 11 8 11 4 3 9 0 11-2 2 3 9 5 13 1 7 0 10-6 7-11 3-6 0-11-5-12-2-5-10-7-15 0Z" fill="url(#brain-pink)" stroke="#81566f" stroke-width="1.3"/>'
    art+='<path d="M31 19q-3 7 0 12-2 5 0 9M23 18q-6 0-5 6 5-4 8 0 3 4-3 6M15 28q-2 7 5 8-1 5 5 3M18 24q-2 4 2 6m5 3q-4-1-5 3M39 18q6-1 7 5-6-2-8 3 0 5 7 4M48 28q4 5-1 8-3 5-8 3m1-8q-7 1-4 6m7-12q6 1 4 5" fill="none" stroke="#a86b87" stroke-width="1.4" stroke-linecap="round"/>'
    art+='<path d="M20 18q4-3 7 0M15 26q-2 3 0 5m23-13q4-2 6 1m-8 17q1 3 4 3" fill="none" stroke="#ffe3d1" stroke-width="1.2" stroke-linecap="round"/>'
    if strength:
        color="#a4e1cc" if strength>3 else "#f0bb92"
        if strength<=6:
            art+='<path d="M49 10l-4 8 7 5-6 5m-1-10l-6 1M9 32l7-2-2 7 5 4" fill="none" stroke="#e5fff0" stroke-width=".8" opacity=".85"/>'
        if strength<=3:
            art+='<path d="M27 8l-3 7 4 4-6 7m6-7l8-4M53 32l-6 5 2 9" fill="none" stroke="#ffe2bc" stroke-width="1"/>'
        art+='<rect x="11" y="1" width="42" height="4" rx="2" fill="#173e47" stroke="#799f96" stroke-width=".5"/>'
        art+=f'<rect x="12" y="2" width="{40*strength/10}" height="2" rx="1" fill="{color}"/>'
    return svg(64,52,art)


def frames():
    costumes=[("house",64,52,brain())]  # Compatibility name for older preview scripts.
    costumes.extend((f"brain-open-{f}",64,52,brain(0,f)) for f in range(4))
    costumes.extend((f"brain-barrier-{strength}-{f}",64,52,brain(strength,f)) for strength in range(1,11) for f in range(4))
    return costumes
