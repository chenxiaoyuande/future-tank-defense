"""Create an editable XBuilder project with original vector artwork."""
import json
from functools import lru_cache
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


@lru_cache(maxsize=1)
def outline_font():
    return TTFont('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', fontNumber=0)


def outline_text(source):
    """Make SVG lettering independent of the game's SVG font renderer."""
    document = ET.fromstring(source)
    for parent in list(document.iter()):
        for node in list(parent):
            if node.tag != f"{{{SVG_NS}}}text":
                continue
            text = "".join(node.itertext())
            font = outline_font()
            cmap = font.getBestCmap()
            glyphs = font.getGlyphSet()
            size = float(node.get("font-size", "16"))
            scale = size / font["head"].unitsPerEm
            width = sum(font["hmtx"][cmap[ord(c)]][0] for c in text) * scale
            x, y = float(node.get("x", "0")), float(node.get("y", "0"))
            anchor = node.get("text-anchor", "start")
            if anchor == "middle":
                x -= width / 2
            elif anchor == "end":
                x -= width
            group = ET.Element(f"{{{SVG_NS}}}g", {"fill": node.get("fill", "black"), "aria-label": text})
            advance = 0
            for character in text:
                name = cmap[ord(character)]
                pen = SVGPathPen(glyphs)
                glyphs[name].draw(pen)
                commands = pen.getCommands()
                if commands:
                    ET.SubElement(group, f"{{{SVG_NS}}}path", {
                        "d": commands,
                        "transform": f"translate({x + advance * scale:.6f} {y:g}) scale({scale:.8f} {-scale:.8f})",
                    })
                advance += font["hmtx"][name][0]
            assert x >= 0 and x + width <= float(document.get("width")), f"Text exceeds image: {text}"
            index = list(parent).index(node)
            parent.remove(node)
            parent.insert(index, group)
    return ET.tostring(document, encoding="unicode")


def write_json(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def svg(width, height, body):
    source = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">{body}</svg>'
    return outline_text(source) if "<text" in body else source


