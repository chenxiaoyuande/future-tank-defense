"""Verify release identities, compatibility copies and the current title screen."""
from hashlib import sha256
import json
from zipfile import ZipFile
from release_info import DIST_DIR, ROOT, catalogue, current_release, manifest, package_name


def verify():
    data=catalogue()
    compatibility_owners={release["legacyFilename"]:release["version"] for release in data["releases"]}
    current=current_release()
    compatibility_owners[current["legacyFilename"]]=current["version"]
    for release in data["releases"]:
        path=DIST_DIR/package_name(release)
        with ZipFile(path) as archive:
            assert archive.testzip() is None
            assert json.loads(archive.read("version.json"))==manifest(release),path.name
            metadata=json.loads(archive.read("builder-meta.json"))
            assert metadata["version"]==release["version"] and f"v{release['version']}" in metadata["displayName"],path.name
            assert f"v{release['version']}" in archive.read("README.md").decode("utf-8-sig"),path.name
        legacy=ROOT/release["legacyFilename"]
        if compatibility_owners[release["legacyFilename"]]==release["version"]:
            assert sha256(path.read_bytes()).digest()==sha256(legacy.read_bytes()).digest(),legacy.name
    assert json.loads((ROOT/"version.json").read_text())==manifest()
    for suffix in ["","-en"]:
        assert f"v{current['version']}" in (ROOT/f"assets/sprites/Notice/home{suffix}.svg").read_text(),suffix
    print(f"Verified {len(data['releases'])} numbered releases, metadata, compatibility copies and v{current['version']} title screens.")


if __name__=="__main__":
    verify()
