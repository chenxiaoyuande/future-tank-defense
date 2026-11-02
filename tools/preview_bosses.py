from project_paths import PREVIEW_DIR, FRONT_FRAMES, prepare_outputs
prepare_outputs()
"""Create an outlined contact sheet from the exact boss costumes used in the game."""
from art_utils import ROOT, svg
from boss_art import boss_art
from campaign_art import BOSSES


def build_preview() -> None:
    """Show enlarged art and three actual-size animation poses for each theme."""
    colors = ["#b5e493", "#a5eaff", "#ffbb7b", "#d8bcff"]
    details = ["藤甲 / 木纹 / 生命法杖", "晶冠 / 冰晶 / 分层长裙", "岩甲 / 熔核 / 裂隙与利爪", "线圈 / 导电装甲 / 电弧"]
    art = '<rect width="960" height="416" fill="#102734"/>'
    for theme in range(4):
        x = theme*240+5
        art += f'<g transform="translate({x} 5)">'
        art += '<rect width="230" height="406" rx="12" fill="#1d3542" stroke="#46616b"/>'
        art += f'<text x="115" y="29" text-anchor="middle" font-size="17" fill="{colors[theme]}">{BOSSES[theme]}</text>'
        art += f'<text x="115" y="48" text-anchor="middle" font-size="10" fill="#acc5c8">{details[theme]}</text>'
        art += f'<g transform="translate(25 56) scale(2.5)">{boss_art(theme)}</g>'
        art += '<path d="M12 258h206" stroke="#46616b"/>'
        art += '<text x="115" y="278" text-anchor="middle" font-size="10" fill="#acc5c8">游戏原尺寸 / 动画状态</text>'
        for index, (pose, label) in enumerate([("idle", "待机"), ("cast", "施法"), ("rage", "狂暴")]):
            left = 4+index*75
            art += f'<g transform="translate({left} 289)">{boss_art(theme,pose,1)}</g>'
            art += f'<text x="{left+36}" y="387" text-anchor="middle" font-size="11" fill="{colors[theme]}">{label}</text>'
        art += '</g>'
    (PREVIEW_DIR / "preview-boss-detail.svg").write_text(svg(960, 416, art), encoding="utf-8")


if __name__ == "__main__":
    build_preview()
