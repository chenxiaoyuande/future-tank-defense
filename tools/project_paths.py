"""Canonical workspace paths for development tools."""
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
WORKSPACE=ROOT
DIST_DIR=ROOT/"dist"
BUILD_DIR=ROOT/".build"
PREVIEW_DIR=BUILD_DIR/"previews"
SNAPSHOT_DIR=BUILD_DIR/"snapshots"
FRONT_FRAMES=PREVIEW_DIR/"front"
DOC_FRAMES=PREVIEW_DIR/"boss-frames"
LOGIC_DIR=BUILD_DIR/"logic"
STORAGE_DIR=BUILD_DIR/"storage"

__all__=["ROOT","WORKSPACE","DIST_DIR","BUILD_DIR","PREVIEW_DIR","SNAPSHOT_DIR","FRONT_FRAMES","DOC_FRAMES","LOGIC_DIR","STORAGE_DIR","prepare_outputs"]


def prepare_outputs():
    for directory in [DIST_DIR,PREVIEW_DIR,SNAPSHOT_DIR,FRONT_FRAMES,DOC_FRAMES,LOGIC_DIR,STORAGE_DIR]:
        directory.mkdir(parents=True,exist_ok=True)
