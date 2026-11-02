"""Run the actual stage functions in a headless Go harness."""
from pathlib import Path
import re
from project_paths import ROOT as root, LOGIC_DIR, STORAGE_DIR, prepare_outputs
prepare_outputs()
destination=LOGIC_DIR
destination.mkdir(parents=True,exist_ok=True)
stage=(root/'main.spx').read_text().split('onStart =>')[0]
web_stage = stage
stage = stage.replace('import "syscall/js"', '')
stage = re.sub(r'// BEGIN_BROWSER_STORAGE[\s\S]*?// END_BROWSER_STORAGE', '', stage)
shim='''
const (KeyW=iota;KeyUp;KeyD;KeyRight;KeyS;KeyDown;KeyA;KeyLeft;KeySpace;KeyE;KeyJ;KeyK;KeyM;KeyEnter;Key1;Key2;Key3;KeyTab;KeyF;KeyG;KeyH;KeyL;KeyR;KeyP;KeyB;KeyU;KeyC;KeyV;KeyT;KeyN;KeyO)
var keys=map[int]bool{}
func keyPressed(k int) bool {return keys[k]}
var rng uint32=12345
func rand(a,b int) float64 {rng=1664525*rng+1013904223;return float64(a+int((rng>>16)%uint32(b-a)))}
'''
(destination/'logic.go').write_text('package main\n'+stage+shim)
(destination/'storage.go').write_text('''package main
var savedProgress string
var unavailable bool
func storageRead() (string,bool) {return savedProgress,!unavailable}
func storageWrite(raw string) bool {if unavailable{return false};savedProgress=raw;return true}
func backupProgress(raw string) {}
func restoreProgress() string {return ""}
''')
(destination/'go.mod').write_text('module survivalcheck\ngo 1.25.0\n')
import shutil
shutil.copyfile(root/'tests/logic_test.go.txt',destination/'logic_test.go')
shutil.copyfile(root/'tests/campaign_test.go.txt',destination/'campaign_test.go')
shutil.copyfile(root/'tests/progress_test.go.txt',destination/'progress_test.go')
shutil.copyfile(root/'tests/checkpoint_test.go.txt',destination/'checkpoint_test.go')
shutil.copyfile(root/'tests/profession_test.go.txt',destination/'profession_test.go')
shutil.copyfile(root/'tests/brain_test.go.txt',destination/'brain_test.go')
web_destination=STORAGE_DIR
web_destination.mkdir(parents=True,exist_ok=True)
(web_destination/'go.mod').write_text('module progresswebcheck\ngo 1.25.0\n')
(web_destination/'logic.go').write_text('package main\n'+web_stage+shim)
shutil.copyfile(root/'tests/progress_web_test.go.txt',web_destination/'storage_test.go')
