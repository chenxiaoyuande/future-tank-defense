"""Draw layered, animated elemental bosses within the existing 72 by 76 footprint."""
import math

from art_utils import svg

POSES = [("idle", n) for n in range(4)] + [("cast", n) for n in range(2)] + [("hit", 0)] + [("rage", n) for n in range(4)]

DEFS = '''<defs>
<linearGradient id="wood" x1="0" y1="0" x2="1" y2=".7"><stop stop-color="#b0be7a"/><stop offset=".3" stop-color="#658770"/><stop offset=".7" stop-color="#315451"/><stop offset="1" stop-color="#183c42"/></linearGradient>
<linearGradient id="leaf" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#e1e8a4"/><stop offset=".45" stop-color="#8bb789"/><stop offset="1" stop-color="#315e55"/></linearGradient>
<linearGradient id="bark" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#a38e68"/><stop offset=".5" stop-color="#665e52"/><stop offset="1" stop-color="#303f40"/></linearGradient>
<linearGradient id="ice" x1="0" y1="0" x2="1" y2=".5"><stop stop-color="#f2fdff"/><stop offset=".28" stop-color="#a8dceb"/><stop offset=".58" stop-color="#578fac"/><stop offset="1" stop-color="#234960"/></linearGradient>
<linearGradient id="silk" x1="0" y1="0" x2="1" y2=".3"><stop stop-color="#203f62"/><stop offset=".4" stop-color="#658bad"/><stop offset=".55" stop-color="#a4c5d8"/><stop offset=".8" stop-color="#466e91"/><stop offset="1" stop-color="#233b58"/></linearGradient>
<linearGradient id="rock" x1=".1" y1="0" x2=".8" y2="1"><stop stop-color="#b39787"/><stop offset=".25" stop-color="#7e6a6d"/><stop offset=".65" stop-color="#443d50"/><stop offset="1" stop-color="#272d3c"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2=".6"><stop stop-color="#ede1d3"/><stop offset=".24" stop-color="#b6aec9"/><stop offset=".48" stop-color="#676d93"/><stop offset=".7" stop-color="#3f4569"/><stop offset="1" stop-color="#252f48"/></linearGradient>
<linearGradient id="gold" x2=".8" y2="1"><stop stop-color="#fff1bf"/><stop offset=".45" stop-color="#c4a675"/><stop offset="1" stop-color="#78665d"/></linearGradient>
<radialGradient id="life"><stop stop-color="#ffffd4"/><stop offset=".3" stop-color="#d5efa6"/><stop offset=".7" stop-color="#8dbd86"/><stop offset="1" stop-color="#375d57"/></radialGradient>
<radialGradient id="frost"><stop stop-color="#ffffff"/><stop offset=".25" stop-color="#d1f6ff"/><stop offset=".7" stop-color="#81c2dd"/><stop offset="1" stop-color="#375b84"/></radialGradient>
<radialGradient id="magma"><stop stop-color="#fffad1"/><stop offset=".3" stop-color="#ffd393"/><stop offset=".65" stop-color="#ef8d65"/><stop offset="1" stop-color="#963e4d"/></radialGradient>
<radialGradient id="storm"><stop stop-color="#ffffff"/><stop offset=".3" stop-color="#ead7ff"/><stop offset=".7" stop-color="#b29bdd"/><stop offset="1" stop-color="#5b538b"/></radialGradient>
</defs>'''


def path(d: str, fill: str, stroke: str = "#20343e", width: float = 1.6, extra: str = "") -> str:
    """Render a shape with the same dark contour as the original garden actors."""
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def gem(x: float, y: float, size: float, color: str = "#c5eaf5") -> str:
    """Draw a faceted jewel with separate lit and shaded planes."""
    return (
        path(f"M{x} {y-size}l{size*.65} {size}L{x} {y+size}l{-size*.65} {-size}Z", color, "#294655", .9)
        + path(f"M{x} {y-size}v{size*2}l{-size*.65} {-size}Z", "#ffffff", "none", 0, 'opacity=".3"')
        + path(f"M{x} {y-size}l{size*.65} {size}L{x} {y+size}", "none", "#ecfcff", .7)
    )


def summoner(frame: int, cast: bool, rage: bool) -> str:
    """Ancient hollow-tree face, layered leaf mantle, roots and living staff."""
    art = path("M43 69Q20 80 20 126l21 9 28-8 25 9 20-10Q115 80 96 65Z", "#284b49")
    for x, y in [(39, 126), (61, 130), (84, 130), (101, 126)]:
        art += path(f"M{x} {y-13}q-13 11-17 25l16-3 7-8 5 7 11 3q-4-16-12-24Z", "url(#bark)")
        art += path(f"M{x} {y-8}l-6 14m8-5l3 8", "none", "#b7a77e", 1)
    art += path("M47 70Q32 77 35 113l35 14 34-16-5-34-26-16Z", "url(#wood)", width=2)
    for side in [-1, 1]:
        # Every leaf has a centre vein and a bevel that remains visible at game scale.
        for n in range(4):
            x, y = 72+side*(22+n*3), 65+n*11
            art += path(f"M{x-side*13} {y-3}Q{x+side*18} {y-13} {x+side*13} {y+10}Q{x} {y+15} {x-side*13} {y-3}Z", "url(#leaf)")
            art += path(f"M{x-side*9} {y-2}l{side*18} 8", "none", "#d8e5a7", .9)
    art += path("M57 103l-7 11 10 8m27-18l9 9-11 10", "none", "#a3be88", 2)
    art += path("M45 77L32 93l8 14 12-10m48-21l16 14-8 16-13-9", "url(#bark)", width=2)
    # A crooked staff reads as a separate object rather than an extra limb.
    art += path("M24 129L21 59q-15-7-10-23l13-11 13 7-3 15-11 7", "none", "#314b45", 7)
    art += path("M24 128L21 59q-12-9-8-20l11-10 9 6-2 10-9 6", "none", "#b6b885", 3)
    art += path("M19 72l13-7-3 10-10 3m3 22l-12-7 5 13 9 2", "url(#leaf)", width=1)
    art += f'<circle cx="23" cy="41" r="{7+frame*.5}" fill="url(#life)"/>'
    art += path("M38 93l-13-5-5 8 8 8 12-3", "url(#wood)")
    # Asymmetric branching antlers and carved wooden face.
    art += path("M55 37L40 20l-2-12m4 15-13-3-6-9m25 18l6-15m35 22l16-17 1-13m-4 16l13-6 6-9m-28 22l-5-14", "none", "#273f40", 7)
    art += path("M55 36L40 20 38 8m4 15-13-3-6-9m25 18l6-15m35 22l16-17 1-13m-4 16l13-6 6-9m-28 22l-5-14", "none", "#c0bf8c", 3)
    art += path("M43 19q-12-19-18-9 3 12 18 9m63-3q8-15 17-10-2 11-17 10", "url(#leaf)")
    art += path("M54 31l17-9 19 10-3 29-15 13-17-13-5-17Z", "url(#bark)", width=2)
    art += path("M58 33l7 7-4 19m19-27l-4 11 8 12m-15 9l3-11-2-13", "none", "#c1b88c", 1.2)
    art += path("M53 42l15 4-3 8-9-2m33-10l-15 4 3 8 9-2", "#173b3e", "#739779", 1)
    art += path("M57 47l7 2m17-2l-5 2", "none", "#f3f8bb", 2.3)
    art += path("M64 60l8 3 9-4", "none", "#253c3b", 2)
    art += '<ellipse cx="72" cy="92" rx="12" ry="15" fill="#264a45" stroke="#b8c58c" stroke-width="2"/>'
    art += '<ellipse cx="72" cy="91" rx="8" ry="11" fill="url(#life)"/>'
    art += path("M72 82q-8 6-2 12 7 3 6-4-3-4-5 1", "none", "#355d4f", 1.8)
    if cast or rage:
        art += '<circle cx="23" cy="41" r="12" fill="none" stroke="#e2f5b2" stroke-dasharray="3 3"/>'
        art += path("M99 91q18-25 29-9-2 21-23 13m3-4l12-6", "url(#leaf)", "#cae9a7", 1.3)
    return art


def frost_queen(frame: int, cast: bool, rage: bool) -> str:
    """Tall crowned queen with an articulated gown, ice pauldrons and sceptre."""
    sway = [0, 2, 0, -2][frame % 4]
    art = path(f"M44 66Q18 92 {23+sway} 135l21-3 27 12 27-12 24 3Q119 92 99 65Z", "#29465e", "#8db8cf", 1.3)
    art += path("M52 70L35 134l36 9 37-10-18-63Z", "url(#silk)", width=2)
    for x in [46, 60, 83, 97]:
        art += path(f"M{x} 90l{(72-x)*.4} 46", "none", "#b1d4e3", 1)
    art += path("M35 134l10-6 13 11 14-10 14 10 12-11 10 5", "none", "#e1f8fa", 2)
    art += path("M49 65l22-8 23 8 1 25-24 15-22-15Z", "url(#ice)", width=1.8)
    art += path("M51 76l20 10 22-10m-36 18l14-8 17 8", "none", "#e4f8ff", 1.4)
    for x in [50, 94]:
        art += gem(x, 99, 5)
    for x, flip in [(39, -1), (105, 1)]:
        art += path(f"M{x} 59l{flip*16} -8 {flip*6} 23 {-flip*16} 13 {-flip*8} -15Z", "url(#ice)", width=1.6)
        art += path(f"M{x} 59l{flip*6} 25 {flip*16} -10", "none", "#daf8ff", 1)
        art += path(f"M{x+flip*6} 85l{flip*4} 18 {-flip*9} 6 {-flip*5} -20", "url(#silk)")
    art += path("M42 103l-12 2-5-6 2-6 15 3m62 7l12 2 4-7-2-6-13 4", "url(#ice)")
    art += path("M119 128L120 47", "none", "#234258", 5)
    art += path("M119 127L120 47", "none", "#d9f7ff", 2)
    art += gem(120, 37, 15)
    art += path("M106 42l14 8 14-8", "none", "#9dd8eb", 2)
    # A pale face under a crown of individually faceted ice shards.
    art += path("M54 29l16-10 18 10 6 29-10 14-12-8-13 8-10-14Z", "url(#silk)", width=1.8)
    art += path("M57 35l14-7 15 7-2 20-13 10-13-10Z", "#c8dce4", "#537b98", 1)
    art += path("M57 40l10 3m17-3l-10 3", "none", "#274a6c", 2)
    art += path("M60 45h6m11 0h5", "none", "#f7ffff", 1.7)
    art += path("M71 43l-2 8h5m-9 5l6 2 7-2", "none", "#6c8da1", 1)
    art += path("M51 34l-5-18 14 7L71 5l12 18 14-7-5 18-21 7Z", "url(#ice)", "#d6f7ff", 1.7)
    for x, y, size in [(53, 20, 9), (64, 18, 10), (73, 12, 11), (83, 19, 10), (92, 21, 8)]:
        art += gem(x, y, size)
    art += gem(71, 81, 9)
    for x, y, size in [(17, 64, 8), (132, 79, 7), (20, 116, 5)]:
        art += gem(x, y+frame%2*2, size)
    if cast or rage:
        art += '<ellipse cx="120" cy="37" rx="19" ry="7" fill="none" stroke="#d0f5ff" stroke-width="1.3"/>'
        art += path("M14 90l18-8m-13 15l11-6m94-28l12 7", "none", "#d8f8ff", 1.2)
    return art


def lava_beast(frame: int, cast: bool, rage: bool) -> str:
    """Broad basalt creature with craggy plates, glowing seams and heavy claws."""
    art = path("M44 110l-13 28 24 4 14-15 11 15 27-4-10-28Z", "#392f3c", width=2.8)
    for x in [35, 84]:
        art += path(f"M{x} 125l18-3 10 18-5 5-30-2Z", "url(#rock)", width=2)
        for n in range(3):
            art += path(f"M{x+n*8} 137l-2 7 7-1", "#d6b694", "#483b44", .8)
    art += path("M30 46l25-16 34 1 26 18 10 38-20 32-34 13-35-15L19 85Z", "#ec9867", "#2c2a37", 3)
    # Plate seams reveal a real hot interior, rather than painted lines on a flat body.
    plates = [
        "M30 47l23-11 12 18-18 22-22-9Z", "M69 36l20 1 23 15-8 23-29-17Z",
        "M24 72l21 8 7 20-17 12-14-28Z", "M109 78l13 7-17 29-17-15 5-15Z",
        "M50 103l19 8-1 17-30-13Z", "M74 111l15-7 13 13-29 10Z",
    ]
    for d in plates:
        art += path(d, "url(#rock)", "#392f40", 1.8)
    art += path("M32 48l17-7 9 10m21-9l10 1 16 11M29 78l10 6m62 9l12-10", "none", "#c0a08b", 1.2)
    for x, side in [(20, -1), (124, 1)]:
        art += path(f"M{x} 63l{side*11} -4 {side*7} 20 {-side*6} 13 {-side*20} -6Z", "url(#rock)", width=2.2)
        art += path(f"M{x+side*5} 87l{side*10} 7 {-side*2} 26 {-side*17} 7 {-side*13} -16 {side*5} -15Z", "url(#rock)", width=2)
        art += path(f"M{x+side*5} 94l{-side*6} 11 {side*10} 9", "none", "#ffc08a", 2)
        for n in range(3):
            xx = x-side*(n*5+1)
            art += path(f"M{xx} 119l{-side*2} 10 {side*6} -5", "#d1b699", "#4c3b43", .9)
    art += path("M46 46Q22 38 26 16l16 16 10-18 8 28m26 0l9-28 10 18 14-16q6 22-21 32", "url(#rock)", width=2)
    art += path("M27 18l10 16-2 5m77-20l-10 16 3 5", "none", "#e7b687", 1.5)
    art += path("M49 36l22-8 23 10 4 23-10 17-17 7-19-10-9-17Z", "url(#rock)", width=2.3)
    art += path("M48 45l20 6-7 7-13-2m45-11l-19 6 6 7 14-2", "#3c2c3c", "#ba7a61", 1)
    art += path("M51 51l10 2m22 0l9-3", "none", "#ffe2a5", 2.5)
    art += path("M55 66l8-4 9 5 11-4 6 3-9 9-14-1Z", "#332638", "#c98b68", 1)
    for x in [61, 70, 79]:
        art += path(f"M{x} 66l3 6 3-7", "#edca99", "none", 0)
    art += '<circle cx="71" cy="92" r="16" fill="#73384a" stroke="#d0926a" stroke-width="2"/>'
    art += f'<circle cx="71" cy="92" r="{12+frame%2}" fill="url(#magma)"/>'
    art += path("M74 79q-2 9 5 11 8 10-6 15-16-1-12-12l7 5q-4-8 6-19Z", "#ffedb5", "#f6bc80", .8)
    if cast or rage:
        for x, y in [(17, 36), (124, 45), (43, 16), (103, 107)]:
            art += path(f"M{x} {y+7}q-8-5 1-15-2 8 4 6 5 8-5 9Z", "url(#magma)", "#ffcc8c", .8)
        art += path("M48 84l-10 9 5 12m53-23l9 12-5 12", "none", "#ffd69d", 1.7)
    return art


def thunder_judge(frame: int, cast: bool, rage: bool) -> str:
    """Armoured sentinel with coils, segmented joints, circuitry and a reactor."""
    art = path("M42 68l-13 62 22 7 21-15 23 15 20-8-12-62Z", "#34334f", "#8d82a3", 1.2)
    for x in [46, 81]:
        art += path(f"M{x} 108l19-1-1 23 6 13-28-1-1-9Z", "url(#metal)", width=2)
        art += path(f"M{x+2} 114l13 1-2 13-10 3Z", "#3b4362", "#a3a0bf", 1)
        art += path(f"M{x} 136h19m-13-5l3 4", "none", "#d7c5e8", 1.2)
    art += path("M49 59l22-10 26 12 9 33-17 21H55L38 94Z", "url(#metal)", width=2)
    art += path("M50 66l20 8 24-8-4 16-18 7-20-8Z", "#4a506f", "#e2d2e5", 1)
    art += path("M55 103l16 4 18-4m-36-7l-8-4m50 4l7-4", "none", "#e2c4f2", 1.6)
    for x, side in [(38, -1), (105, 1)]:
        art += path(f"M{x} 56l{side*17} -1 {side*8} 16 {-side*14} 15 {-side*15} -7Z", "url(#metal)", width=2)
        art += path(f"M{x+side*17} 60l{-side*15} 1 {-side*9} 14", "none", "#efdfed", 1)
        art += path(f"M{x+side*9} 82l{side*3} 22 {-side*12} 10 {-side*9} -12 {side*4} -20Z", "#41486a", "#bdabc9", 1.7)
        art += path(f"M{x+side*7} 87l{-side*10} 4m{side*11} 2l{-side*11} 4m{side*11} 2l{-side*11} 4", "none", "#d3bedc", 1.3)
        art += path(f"M{x+side*9} 110l{-side*3} 11 {-side*15} -3 {-side*2} -12", "url(#metal)", width=1.5)
    for x in [20, 124]:
        art += path(f"M{x} 73V25", "none", "#34394f", 5)
        art += path(f"M{x} 72V25", "none", "#c2afd7", 1.8)
        art += f'<ellipse cx="{x}" cy="26" rx="7" ry="3" fill="url(#metal)" stroke="#dec6e9"/>'
        art += f'<circle cx="{x}" cy="20" r="4" fill="url(#storm)"/>'
        for y in [38, 44, 50, 56, 62]:
            art += f'<ellipse cx="{x}" cy="{y}" rx="5" ry="2" fill="none" stroke="#c5b4d8" stroke-width="1.3"/>'
    art += path("M53 19l18-9 20 10-2 32-17 12-18-12Z", "url(#metal)", width=2)
    art += path("M56 20l15 9 17-9-4 19-12 6-13-6Z", "#2a334e", "#d2bce0", 1)
    art += path("M59 33l10 3m7 0l9-3", "none", "#f6e9ff", 2)
    art += path("M60 44l12 5 12-5-4 10-8 5-9-5Z", "#4f5877", "#c5aecb", 1)
    art += path("M69 18l5-16 6 18-7 8Z", "url(#gold)", "#e9d2df", 1)
    art += '<circle cx="72" cy="92" r="14" fill="#292c4b" stroke="#bca3cf" stroke-width="2"/>'
    art += '<circle cx="72" cy="92" r="10" fill="url(#storm)"/>'
    art += path("M75 80L65 94h8l-3 12 12-18h-9Z", "#fcf4ff", "#716391", 1)
    for x, side in [(50, -1), (94, 1)]:
        art += path(f"M{x} 83h{side*8}v12h{side*5}", "none", "#cfb8ed", 1)
        for y in [81, 103]:
            art += f'<circle cx="{x}" cy="{y}" r="1.5" fill="#e4ceef"/>'
    if cast or rage:
        offset = frame % 2*3
        art += path(f"M20 20l15 {8+offset} 10-9 10 11m69-10l-14 {10-offset}-9-9-11 12", "none", "#ece1ff", 2)
        art += path("M16 76l-8 9 7 9-8 10m121-28l8 9-7 9 8 10", "none", "#dac4fa", 1.5)
    return art


def boss_art(theme: int, pose: str = "idle", frame: int = 0) -> str:
    """Return one detailed sprite without altering its anchor or collision footprint."""
    painters = [summoner, frost_queen, lava_beast, thunder_judge]
    accent = ["#d1e6a0", "#c4eeff", "#ffb989", "#d9c1ff"][theme]
    pulse = [0, 1, 0, -1][frame % 4]
    cast, rage = pose == "cast", pose == "rage"
    art = DEFS + '<g transform="scale(.5)">'
    art += '<ellipse cx="72" cy="144" rx="61" ry="7" fill="#102735" opacity=".52"/>'
    art += f'<ellipse cx="72" cy="144" rx="{45+pulse}" ry="4" fill="{accent}" opacity=".12"/>'
    if cast or rage:
        art += f'<ellipse cx="72" cy="137" rx="54" ry="10" fill="none" stroke="{accent}" opacity=".45" stroke-width="1.4" stroke-dasharray="4 6"/>'
    art += f'<g transform="translate(0 {pulse*.65 if pose != "hit" else 0})">'
    art += painters[theme](frame, cast, rage)
    # Small elemental motes move around the shoulders, inside the original sprite bounds.
    for n in range(4):
        angle = (n*91+frame*24)*math.pi/180
        x, y = 72+57*math.cos(angle), 69+43*math.sin(angle)
        art += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{1.5 if n%2 else 2}" fill="{accent}" opacity=".75"/>'
    if pose == "hit":
        art += path("M47 58l12-14m-8 35l22-27m-4 42l24-28", "none", "#fff6dd", 3, 'opacity=".85"')
    art += '</g></g>'
    return svg(72, 76, art)
