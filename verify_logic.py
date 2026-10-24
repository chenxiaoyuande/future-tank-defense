"""Run the actual stage functions in a headless Go harness."""
from pathlib import Path
root=Path(__file__).resolve().parent
destination=root.parent/'.xbuilder-setup/survival-logic'
destination.mkdir(parents=True,exist_ok=True)
stage=(root/'main.spx').read_text().split('onStart =>')[0]
shim='''
const (KeyW=iota;KeyUp;KeyD;KeyRight;KeyS;KeyDown;KeyA;KeyLeft;KeySpace;KeyE;KeyJ;KeyK;KeyM;KeyEnter;Key1;Key2;KeyF;KeyG;KeyH;KeyR;KeyP)
var keys=map[int]bool{}
func keyPressed(k int) bool {return keys[k]}
var rng uint32=12345
func rand(a,b int) float64 {rng=1664525*rng+1013904223;return float64(a+int((rng>>16)%uint32(b-a)))}
'''
(destination/'logic.go').write_text('package main\n'+stage+shim)
(destination/'go.mod').write_text('module survivalcheck\ngo 1.25.0\n')
import shutil
shutil.copyfile(root/'logic_test.go.txt',destination/'logic_test.go')
shutil.copyfile(root/'campaign_test.go.txt',destination/'campaign_test.go')
