"""Generate the version index and canonical links from releases.json."""
from release_info import ROOT, catalogue, package_name


def write():
    data=catalogue()
    lines=["# 版本与下载","","[返回项目说明](../README.md) · [详细更新记录](CHANGELOG.md)","",
           f"当前版本为 **v{data['currentVersion']}**。版本号按现有六份项目包的功能迭代顺序补充；没有独立留存包的中间修改归入对应版本，不额外编造历史包或发布日期。","",
           "| 版本 | 项目包 | 主要内容 |","| --- | --- | --- |"]
    for release in reversed(data["releases"]):
        label="（当前）" if release["version"]==data["currentVersion"] else ""
        lines.append(f"| v{release['version']}{label} | [{release['name']}](../../dist/{package_name(release)}) | {release['summary']} |")
    lines.extend(["","## 版本规则","",
                  "使用 `主版本.功能版本.修订版本`：主版本用于不兼容的大改，功能版本用于新增功能，修订版本用于修复和小调整。当前 v1.5.0 包含三职业、首页优化、接触伤害，以及脑子与三秒屏障。下一次修复可使用 v1.5.1，下一轮新功能可使用 v1.6.0。","",
                  "## 文件与存档","",
                  "文件名、XBuilder 项目名、首页页脚及包内 `version.json` 标识当前版本。未带版本号的旧文件名保留为兼容副本；下载和分发优先使用表格中的带版本号文件。历史包只补版本身份与 README 提示，游戏脚本和素材保持各自原版本。","",
                  "游戏版本号与 TG1 / TG2 / TG3 存档格式相互独立。补版本号不会清空金币、进化或关卡进度，也不会修改浏览器存储键。历史包的玩法与存档支持范围以其自身说明为准。","",
                  "## 后续发布","",
                  "1. 在 `releases.json` 追加版本记录，并修改 `currentVersion`；保留已有版本记录和带版本号的归档包。",
                  "2. 更新功能说明与 CHANGELOG，运行文档生成器。",
                  "3. 重建资源以更新首页版本文字，生成预览，再打包并执行版本、文档和资源检查。",
                  "","构建入口与命令见 [开发指南](DEVELOPMENT.md)。"])
    (ROOT/"docs/VERSIONS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


if __name__=="__main__":
    write()
