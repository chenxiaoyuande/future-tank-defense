"""Generate checkpoint-centre panels using the existing illustrated UI style."""
import json

from art_utils import ROOT, svg, write_json


def append(folder: str, name: str, width: int, height: int, content: str) -> None:
    directory = ROOT / "assets/sprites" / folder
    data = json.loads((directory / "index.json").read_text())
    (directory / f"{name}.svg").write_text(content, encoding="utf-8")
    data["costumes"].append({"name":name,"path":name+".svg","x":width/2,"y":height/2,"imageWidth":width,"imageHeight":height,"bitmapResolution":1})
    write_json(f"assets/sprites/{folder}/index.json",data)


def extend(text) -> None:
    for mode in [1,2]:
        for stage in range(21):
            art='<rect width="460" height="320" rx="16" fill="#122c38" stroke="#c9cc9d" stroke-width="2"/>'
            art+=text(20,30,"闯关存档中心",22)
            art+=text(20,49,"自动保存关卡进度 · O 手动存档 · N 继续游戏",10,"#b4cdbf")
            art+=text(20,80,f"继续关卡：第 {stage:02d} / 20 关" if stage else "尚无可继续存档，先开始一局",16,"#ffe3a1")
            art+=text(20,104,"最高通关：",12,"#b4cdbf")+text(145,104,"/ 20",12,"#b4cdbf")
            art+=text(20,126,("继续模式：单人" if mode==1 else "继续模式：双人合作") if stage else "开始任意关卡后自动建立存档。",12)
            art+=text(20,151,"继续从关卡起点恢复生命，敌人和道具重新生成。",11,"#b4cdbf")
            art+=text(20,176,"T 切换中文 / English · 自动保存语言选择",11,"#a8d9cf")
            art+=text(20,214,"持有金币：",12,"#ffe09a")
            art+=text(20,237,"累计收入：",12,"#b4c9bf")
            art+=text(230,312,"N 继续  O 存档  C 备份  V 恢复  M 返回  T 语言",11,"#ffe09a","middle")
            append("Notice",f"savepanel-{mode}-{stage}",460,320,svg(460,320,art))
    for n,label in [(7,"关卡存档已保存，可在选关界面按 N 继续"),(8,"尚无可继续存档，请先开始任意关卡")]:
        append("Wallet",f"notice-{n}",430,18,svg(430,18,text(215,13,label,11,"#ffe3a1","middle")))
    for n in range(1,9):
        source=(ROOT/f"assets/sprites/Wallet/notice-{n}.svg").read_text()
        source=source.replace('>','><rect width="430" height="18" rx="5" fill="#173443"/>',1)
        append("Wallet",f"notice-toast-{n}",430,18,source)
