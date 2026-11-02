package main
import ("testing";"syscall/js")

func mockBrowser(source string) {js.Global().Call("eval",source)}
func TestWasmStorageReloadAndEvolution(t *testing.T) {
 mockBrowser(`globalThis.testProgress=new Map();globalThis.localStorage={getItem:k=>testProgress.has(k)?testProgress.get(k):null,setItem:(k,v)=>testProgress.set(k,String(v))};`)
 profileLoaded=false;loadProfile();awardCoins(900);state=4;buyEvolution();buyEvolution()
 if coins!=550||evolution!=2||profileDirty {t.Fatal("web save failed")}
 clearedLevel=8;recordCheckpoint(9,2100,21,true);language=1;languageDirty=true;profileDirty=true;persistProfile()
 profileLoaded=false;coins=0;lifetimeCoins=0;evolution=0;loadProfile()
 if coins!=550||lifetimeCoins!=900||evolution!=2 {t.Fatal("web reload lost progress")}
 if checkpointLevel!=9||checkpointScore!=2100||checkpointKills!=21||!checkpointCoop||language!=1 {t.Fatal("web reload lost checkpoint or language")}
}
func TestWasmDeniedStorageAndReadbackFailure(t *testing.T) {
 mockBrowser(`Object.defineProperty(globalThis,'localStorage',{configurable:true,get(){throw new Error('denied')}});`)
 if _,ok:=storageRead();ok||storageWrite("data") {t.Fatal("denied access not caught")}
 mockBrowser(`Object.defineProperty(globalThis,'localStorage',{configurable:true,writable:true,value:{getItem:()=>null,setItem:()=>{}}});`)
 if storageWrite("data") {t.Fatal("readback failure accepted")}
 mockBrowser(`globalThis.localStorage={getItem:()=>{throw new Error('read blocked')},setItem:()=>{throw new Error('quota')}};`)
 if _,ok:=storageRead();ok||storageWrite("data") {t.Fatal("quota/read errors not caught")}
}
func TestWasmBackupRestoreDialogs(t *testing.T) {
 mockBrowser(`globalThis.prompt=(message,value)=>{globalThis.lastBackup=value;return 'TG1|550|2|900|90861'};`)
 backupProgress("backup-check");if js.Global().Get("lastBackup").String()!="backup-check" {t.Fatal("backup not exposed")}
 if restoreProgress()=="" {t.Fatal("restore text missing")}
 mockBrowser(`globalThis.prompt=()=>null;`);if restoreProgress()!="" {t.Fatal("cancel changed save")}
 mockBrowser(`globalThis.prompt=()=>{throw new Error('blocked')};`);if restoreProgress()!=""||evolveNotice!=5 {t.Fatal("dialog failure not caught")}
}
func TestWasmTG3ClassesRoutesAndLockedProgress(t *testing.T) {
 mockBrowser(`Object.defineProperty(globalThis,'localStorage',{configurable:true,writable:true,value:{getItem:k=>globalThis.rosterData??null,setItem:(k,v)=>globalThis.rosterData=String(v)}});globalThis.rosterData=null;`)
 profileLoaded=false;loadProfile();awardCoins(2000);state=4
 for role:=0;role<3;role++ {labClass=role;buyEvolution()}
 labClass=1;buyEvolution();playerClass=1;playerClass2=2;clearedLevel=1;recordCheckpoint(2,800,8,true)
 profileLoaded=false;routeTiers=[3]int{};playerClass=0;playerClass2=0;loadProfile()
 if coins!=1450||evolution!=1||routeTiers[1]!=2||routeTiers[2]!=1||unlockedLevel()!=2||canStartStage(3){t.Fatal("TG3 browser reload changed routes or unlocks")}
 if !continueCheckpoint()||level!=2||playerClass!=1||playerClass2!=2||!twoPlayers{t.Fatal("TG3 co-op checkpoint")}
}
