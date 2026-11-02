"""Check Markdown modules, portable links, media files and animation metadata."""
import re
from pathlib import Path
from urllib.parse import unquote

from PIL import Image
from project_paths import ROOT



def headings(source: str) -> set[str]:
    """Return the anchors used by the simple headings in these documents."""
    result = set()
    for title in re.findall(r"^#{1,6}\s+(.+)$", source, re.MULTILINE):
        title = re.sub(r"[`*_]", "", title).lower()
        result.add(re.sub(r"[^\w\-\s\u4e00-\u9fff]", "", title).replace(" ", "-"))
    return result


def verify() -> None:
    """Fail if any authored local link or GIF contract is broken."""
    readmes = [ROOT / "README.md", ROOT / "REAMD.md"]
    documents = readmes + list((ROOT / "docs").rglob("*.md")) + [ROOT/"tools/README.md",ROOT/"tests/README.md"]
    checked = 0
    for file in documents:
        source = file.read_text(encoding="utf-8-sig")
        text = re.sub(r"```[\s\S]*?```", "", source)
        for href in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            if href.startswith(("https://", "http://", "mailto:")):
                continue
            location, _, fragment = unquote(href).partition("#")
            target = (file.parent / location).resolve() if location else file
            assert target.exists(), f"Missing link in {file.name}: {href}"
            if fragment:
                assert fragment in headings(target.read_text(encoding="utf-8-sig")), f"Missing anchor: {href}"
            checked += 1
        if file in readmes:
            for title in ["版本说明", "背景介绍", "快速开始", "游戏规则", "玩法介绍", "代码说明"]:
                assert f"## {title}" in source
            assert source.count(".gif)") == 4
            assert "不是 XBuilder 在线实机录像" in source
        if file in readmes or file.name == "GAMEPLAY.md":
            assert not re.search(r"(?:全部|所有)\s*(?:20|二十)?\s*关卡?[^。\n]{0,8}(?:均可|都可|可以)直接选择",source), f"Outdated unlocked-stage rule in {file.name}"
            assert "M 返回选关" not in source and "M选关" not in source, f"Outdated home shortcut in {file.name}"
    assert (ROOT / "README.md").read_bytes() == (ROOT / "REAMD.md").read_bytes()
    for name, frames, duration in [("boss-poses.gif", 28, 140), ("boss-warnings.gif", 50, 100)]:
        with Image.open(ROOT / "docs/media" / name) as animation:
            assert animation.is_animated and animation.n_frames == frames
            assert animation.size == (800, 260) and animation.info["loop"] == 0
            total = 0
            for frame in range(animation.n_frames):
                animation.seek(frame)
                total += animation.info["duration"]
            assert total == frames*duration
    for file in (ROOT / "docs/media").glob("*.png"):
        with Image.open(file) as image:
            image.verify()
    for name,count,size in [("animated-home.gif",36,(720,540)),("profession-evolution.gif",6,(1080,660))]:
        with Image.open(ROOT/"docs/media"/name) as animation:
            assert animation.is_animated and animation.n_frames==count and animation.size==size
    print(f"Checked {len(documents)} Markdown files, {checked} local links, 4 animated GIFs and all PNGs.")


if __name__ == "__main__":
    verify()
