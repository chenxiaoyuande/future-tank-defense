"""One command entry for building, documenting and checking the XBuilder project."""
import argparse
import os
from pathlib import Path
import runpy
import shutil
import subprocess

from project_paths import ROOT, LOGIC_DIR, STORAGE_DIR, prepare_outputs

TOOLS=Path(__file__).resolve().parent


def run(script):
    runpy.run_path(str(TOOLS/script),run_name="__main__")


def write_documents():
    run("write_profession_docs.py")
    run("write_versions.py")
    run("write_docs.py")


def test():
    run("verify_logic.py")
    preferred=Path.home()/".local/share/xbuilder-tools/go1.27.3/bin/go"
    executable=os.environ.get("GARDEN_GO") or (str(preferred) if preferred.exists() else shutil.which("go"))
    if not executable:raise RuntimeError("Go was not found; set GARDEN_GO to the Go executable")
    subprocess.run([executable,"test","-count=1","./..."],cwd=LOGIC_DIR,check=True)
    environment=os.environ.copy();environment.update(GOOS="js",GOARCH="wasm")
    node_dir=Path.home()/".local/share/xbuilder-tools/node-v24.11.1-linux-x64/bin"
    if node_dir.exists():environment["PATH"]=str(node_dir)+os.pathsep+environment.get("PATH","")
    go_root=subprocess.check_output([executable,"env","GOROOT"],text=True).strip()
    runner=str(Path(go_root)/"lib/wasm/go_js_wasm_exec")
    subprocess.run([executable,"test",f"-exec={runner}","-count=1","./..."],cwd=STORAGE_DIR,env=environment,check=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["build","test","compile","docs","preview","media","package","check","number-archives"])
    parser.add_argument("--releases",action="store_true",help="also audit all historical release archives when checking")
    args=parser.parse_args()
    prepare_outputs()
    if args.command=="build":write_documents();run("build_survival.py")
    elif args.command=="test":test()
    elif args.command=="compile":subprocess.run(["bash",str(TOOLS/"validate.sh")],cwd=ROOT,check=True)
    elif args.command=="docs":write_documents()
    elif args.command=="preview":run("preview_brain.py");run("preview_frontend.py")
    elif args.command=="media":run("encode_frontend_media.py")
    elif args.command=="package":run("package_project.py")
    elif args.command=="number-archives":run("number_archives.py")
    elif args.command=="check":
        run("verify_docs.py");run("verify_package.py")
        if args.releases:run("verify_releases.py")


if __name__=="__main__":
    main()
