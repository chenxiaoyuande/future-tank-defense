"""Package generated assets with versioned filenames and a compatibility copy."""
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from release_info import ROOT, DIST_DIR, write_current_identity

EXTENSIONS = {'.spx','.svg','.json','.ttf','.txt','.png','.gif','.md','.py','.cjs','.sh','.mod','.sum'}


def pack():
    identity = write_current_identity()
    DIST_DIR.mkdir(parents=True,exist_ok=True)
    target = DIST_DIR / identity["packageName"]
    with NamedTemporaryFile(dir=DIST_DIR,suffix=".xbp.tmp",delete=False) as output:
        temporary = Path(output.name)
    try:
        with ZipFile(temporary,"w",ZIP_DEFLATED) as archive:
            for path in ROOT.rglob('*'):
                relative = path.relative_to(ROOT)
                if path.is_file() and not any(part.startswith('.') or part in {'node_modules','__pycache__'} for part in relative.parts) and path.name != 'front-preview-manifest.json' and path.suffix in EXTENSIONS and not path.name.startswith(('preview-','demo-','campaign-frames')):
                    archive.write(path,relative.as_posix())
        with ZipFile(temporary) as archive:
            if archive.testzip() is not None:
                raise ValueError("Package CRC check failed")
        temporary.replace(target)
        shutil.copyfile(target,ROOT.parent/identity["legacyPackageName"])
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return target


if __name__ == "__main__":
    print(pack())
