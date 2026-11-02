from project_paths import DOC_FRAMES, PREVIEW_DIR
"""Prepare README animation frames from the shipped SVG costumes, without gameplay edits."""
import json
import shutil

from art_utils import ROOT, svg
from campaign_art import BOSSES, ACCENTS

OUTPUT = DOC_FRAMES
MEDIA = ROOT / "docs/media"
ACTORS = ROOT / "assets/sprites/Actor"


def label(x: float, y: float, value: str, size: int = 12, color: str = "#c4d7d1") -> str:
    """Centre an outlined label independently of the viewer's installed fonts."""
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle" fill="{color}">{value}</text>'


def costume(name: str, x: float, y: float, scale: float = 1) -> str:
    """Embed the exact SVG referenced by the Actor sprite index."""
    index = json.loads((ACTORS / "index.json").read_text(encoding="utf-8"))
    item = next(c for c in index["costumes"] if c["name"] == name)
    source = (ACTORS / item["path"]).read_text(encoding="utf-8")
    return f'<g transform="translate({x} {y}) scale({scale})">{source}</g>'


def panel(theme: int) -> str:
    """Draw the shared card for one elemental boss."""
    return (
        f'<rect x="{theme*200+4}" y="4" width="192" height="252" rx="12" fill="#203b46" stroke="#55716d"/>'
        + label(theme*200+100, 30, BOSSES[theme], 15, ACCENTS[theme])
    )


def build() -> None:
    """Write SVG frames and a conversion manifest for Sharp and Pillow."""
    OUTPUT.mkdir(parents=True, exist_ok=True)
    MEDIA.mkdir(parents=True, exist_ok=True)
    copies = {
        "preview-boss-detail.png": "boss-detail.png",
        "preview-20-menu.png": "level-select.png",
        "preview-20-bosses.png": "four-bosses.png",
        "preview-20-1.png": "coop-garden.png",
        "preview-20-20.png": "thunder-arena.png",
        "preview-evolution-lineup.png": "evolution-lineup.png",
        "preview-evolution-shop.png": "evolution-shop.png",
        "preview-bilingual.png": "bilingual-save.png",
    }
    for source, target in copies.items():
        shutil.copyfile(PREVIEW_DIR / source, MEDIA / target)
    jobs = []
    frames = []
    sequence = [("idle", "待机", 8), ("cast", "施法", 8), ("hit", "受击", 2), ("rage", "狂暴", 10)]
    tick = 0
    for pose, title, count in sequence:
        for n in range(count):
            body = '<rect width="800" height="260" fill="#122c38"/>'
            for theme in range(4):
                frame = n % (2 if pose == "cast" else 1 if pose == "hit" else 4)
                body += panel(theme)
                body += costume(f"boss-{theme}-{pose}-{frame}", theme*200+35, 45, 1.8)
                body += label(theme*200+100, 210, title, 15, ACCENTS[theme])
                body += label(theme*200+100, 235, "实际造型帧 / 素材演示", 10)
            target = OUTPUT / f"boss-{tick:03}.svg"
            target.write_text(svg(800, 260, body), encoding="utf-8")
            frames.append(str(target))
            tick += 1
    jobs.append({"name": "boss-poses.gif", "duration": 140, "frames": frames})
    frames = []
    warmups = [1.5, 1.5, 1.2, 1.7]
    durations = [3.5, 3, 2, .32]
    for n in range(50):
        time = n / 10
        body = '<rect width="800" height="260" fill="#122c38"/>'
        for theme in range(4):
            x = theme*200
            active = warmups[theme] <= time < warmups[theme]+durations[theme]
            warning = time < warmups[theme]
            body += panel(theme)
            body += costume(f"boss-{theme}-cast-{n%2}", x+79, 40, .6)
            if warning or active:
                if theme == 0 and active:
                    body += costume("zombie-1-down-0", x+58, 118, .9)
                    body += costume("zombie-1-down-2", x+105, 118, .9)
                else:
                    body += costume(f"zone-{theme}-{'warn' if warning else 'active'}-{n%2}", x+60, 95)
            move = min(56, max(0, (time-.65)*70))
            if theme != 0:
                body += costume("plant-left-0", x+81-move, 114, .9)
            state = "预警中" if warning else ["援军现身", "冰区减速", "火焰生效", "落雷瞬间"][theme] if active else "区域结束"
            body += label(x+100, 205, state, 14, ACCENTS[theme])
            body += label(x+100, 228, f"预警 {warmups[theme]:g} 秒", 11)
            body += label(x+100, 246, "规则时序示意 / 非实机录像", 9)
        target = OUTPUT / f"warning-{n:03}.svg"
        target.write_text(svg(800, 260, body), encoding="utf-8")
        frames.append(str(target))
    jobs.append({"name": "boss-warnings.gif", "duration": 100, "frames": frames})
    (OUTPUT / "manifest.json").write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
    print(OUTPUT / "manifest.json")


if __name__ == "__main__":
    build()
