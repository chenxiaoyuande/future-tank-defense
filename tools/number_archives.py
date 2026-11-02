"""Assign versions to existing historical packages without changing their gameplay."""
import json
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from release_info import ROOT, DIST_DIR, catalogue, current_release, manifest, package_name


def number_archives():
    DIST_DIR.mkdir(parents=True,exist_ok=True)
    current = current_release()["version"]
    for release in catalogue()["releases"]:
        if release["version"] == current:
            continue
        legacy = ROOT.parent / release["legacyFilename"]
        target = DIST_DIR / package_name(release)
        source = target if target.exists() else legacy
        identity = manifest(release)
        with NamedTemporaryFile(dir=DIST_DIR,suffix=".xbp.tmp",delete=False) as output:
            temporary = Path(output.name)
        try:
            with ZipFile(source) as previous, ZipFile(temporary,"w",ZIP_DEFLATED) as updated:
                names = set(previous.namelist())
                metadata = json.loads(previous.read("builder-meta.json"))
                if metadata.get("version") not in {None,release["version"]}:
                    raise ValueError(f"{source.name} belongs to another release; locate the correct historical archive")
                metadata.update(version=release["version"],displayName=identity["displayName"])
                replacements = {"builder-meta.json":json.dumps(metadata,ensure_ascii=False,indent=2)+"\n", "version.json":json.dumps(identity,ensure_ascii=False,indent=2)+"\n"}
                for name in ["README.md","REAMD.md"]:
                    text = previous.read(name).decode("utf-8-sig") if name in names else f"# 暮光花园 · {release['name']}\n"
                    marker = f"> 版本：**v{release['version']} · {release['name']}**"
                    if marker not in text:
                        text = text.replace("\n","\n\n"+marker+"。历史包补充编号，游戏逻辑与素材保留原版本。\n",1)
                    replacements[name] = text
                for entry in previous.infolist():
                    if entry.filename not in replacements:
                        updated.writestr(entry,previous.read(entry.filename))
                for name,text in replacements.items():
                    updated.writestr(name,text)
            with ZipFile(source) as previous, ZipFile(temporary) as updated:
                assert updated.testzip() is None
                for name in previous.namelist():
                    if name not in replacements:
                        assert previous.read(name) == updated.read(name), name
            temporary.replace(target)
            if release["legacyFilename"] != current_release()["legacyFilename"]:
                shutil.copyfile(target,legacy)
            print(f"v{release['version']} · {release['name']}")
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise


if __name__ == "__main__":
    number_archives()
