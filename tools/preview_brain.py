from project_paths import PREVIEW_DIR, FRONT_FRAMES, prepare_outputs
prepare_outputs()
"""Show three actual objective costumes for the documentation."""
from art_utils import ROOT, svg
from front_end_art import t
from preview_evolution import image

art='<rect width="960" height="330" rx="18" fill="#112f36"/>'+t(30,40,"守护脑子 · 三秒啃咬屏障",25,"#eedeb5",width=900)
for n,(costume,label,detail) in enumerate([
    ("brain-barrier-10-0","屏障完整","每关开始恢复满耐久"),
    ("brain-barrier-5-0","屏障受损","累计啃咬 1.5 秒"),
    ("brain-open-0","脑子暴露","屏障消失后，再接触即失败"),
]):
    x=20+n*315
    art+=f'<rect x="{x}" y="62" width="290" height="217" rx="14" fill="#1e4045" stroke="#668a7b"/>'
    art+=image("Brain",costume,x+74,81,2.2)
    art+=t(x+145,232,label,18,"#e8cbaa","middle",270)+t(x+145,259,detail,12,"#b7cebc","middle",270)
art+=t(480,310,"累计有效啃咬 3 秒拆除屏障 · 多只僵尸不加速 · 暂停不计时",13,"#b2cbb8","middle",900)
(PREVIEW_DIR/"preview-brain.svg").write_text(svg(960,330,art),encoding="utf-8")
