"""Read release identity from the shared version catalogue."""
import json
import re
from pathlib import Path

from project_paths import ROOT, DIST_DIR


def catalogue():
    data = json.loads((ROOT / "releases.json").read_text(encoding="utf-8"))
    versions = [item["version"] for item in data["releases"]]
    if len(versions) != len(set(versions)) or not all(re.fullmatch(r"\d+\.\d+\.\d+", version) for version in versions):
        raise ValueError("Release versions must be unique MAJOR.MINOR.PATCH values")
    if data["currentVersion"] not in versions:
        raise ValueError("currentVersion must identify a release")
    return data


def current_release():
    data = catalogue()
    return next(item for item in data["releases"] if item["version"] == data["currentVersion"])


def package_name(release=None):
    release = release or current_release()
    return f"暮光花园-v{release['version']}-{release['name']}.xbp"


def manifest(release=None):
    release = release or current_release()
    return {"version":release["version"], "name":release["name"], "displayName":f"暮光花园 v{release['version']} · {release['name']}", "packageName":package_name(release), "legacyPackageName":release["legacyFilename"]}


def write_current_identity():
    identity = manifest()
    (ROOT / "version.json").write_text(json.dumps(identity,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    path = ROOT / "builder-meta.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(version=identity["version"],displayName=identity["displayName"])
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return identity
