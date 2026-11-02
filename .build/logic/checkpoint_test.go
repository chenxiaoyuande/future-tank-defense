package main
import ("testing";"strings")

func checkpointCleanup() {profileLoaded=false;evolution=0;language=0;keys=map[int]bool{}}
func TestSaveMigrationAndCheckpointValidation(t *testing.T) {
 freshProgress();defer checkpointCleanup()
 savedProgress=profileCode(600,1,700);profileLoaded=false;loadProfile()
 if coins!=600||evolution!=1||checkpointLevel!=0||language!=0 {t.Fatal("TG1 migration")}
 persistProfile();if !strings.HasPrefix(savedProgress,"TG3|") {t.Fatal("old save not migrated on write")}
 code:=encodeSaveValues(500,2,850,12,3000,35,true,11,1)
 if !importProfile(code)||checkpointLevel!=12||checkpointScore!=3000||checkpointKills!=35||!checkpointCoop||language!=1||clearedLevel!=11 {t.Fatal("full import")}
 before:=savedProgress
 for _,bad:=range []string{code+"x",encodeSaveValues(500,2,850,21,0,0,false,0,0),encodeSaveValues(500,2,850,0,1,0,false,0,0),encodeSaveValues(500,2,850,1,0,0,false,0,2)} {
  if importProfile(bad)||savedProgress!=before||checkpointLevel!=12 {t.Fatal("invalid checkpoint changed save")}
 }
}
func TestCheckpointRestartsStageWithEntryProgress(t *testing.T) {
 freshProgress();defer checkpointCleanup()
 campaignSetup(7,true);clearedLevel=6;score=3000;kills=30;runEntryScore=score;runEntryKills=kills
 recordCheckpoint(7,score,kills,true);score+=500;kills+=5;lives=1;lives2=0
 manualCheckpoint();profileLoaded=false;loadProfile();state=5
 if !continueCheckpoint()||level!=7||!twoPlayers||score!=3000||kills!=30||lives!=3||lives2!=3||weaponLevel!=1||stageKills!=0||state!=0 {t.Fatal("resume was not a stage-start checkpoint")}
 if count(6)!=0||count(7)!=0||count(9)!=0 {t.Fatal("old projectiles survived resume")}
}
func TestStageClearSavesNextStageAndFinalCheckpoint(t *testing.T) {
 freshProgress();defer checkpointCleanup()
 campaignSetup(4,true);score=1000;kills=10;stageKills=waveTarget;updateGame()
 if state!=2||checkpointLevel!=5||checkpointScore!=1000||clearedLevel!=4 {t.Fatal("clear did not save next stage")}
 profileLoaded=false;loadProfile();state=1
 if !continueCheckpoint()||level!=5||!bossStarted {t.Fatal("could not continue into boss stage")}
 campaignSetup(20,true);runEntryScore=9000;runEntryKills=90;score=9000;kills=90;damageZombie(bossSlot,999);updateGame()
 if state!=3||checkpointLevel!=20||clearedLevel!=20||checkpointScore!=9000 {t.Fatal("final save points outside campaign")}
}
func TestLanguageAndSaveCentreInput(t *testing.T) {
 freshProgress();defer checkpointCleanup()
 campaignSetup(1,false);state=1;languageDown=false;keys=map[int]bool{KeyT:true};updateControls();updateControls()
 if language!=1||langSuffix()!="-en"||tr("中","EN")!="EN" {t.Fatal("language edge or text")}
 profileLoaded=false;loadProfile();if language!=1 {t.Fatal("language preference not persisted")}
 keys=map[int]bool{};updateControls();keys=map[int]bool{KeyS:true};savePanelDown=false;updateControls()
 if state!=5||saveReturnState!=1 {t.Fatal("save centre entry")}
 selectedLevel=8;clearedLevel=7;twoPlayers=true;keys=map[int]bool{KeyO:true};saveDown=false;updateControls()
 if checkpointLevel!=8||!checkpointCoop||evolveNotice!=7 {t.Fatal("manual selection save")}
 keys=map[int]bool{KeyN:true};continueDown=false;updateControls();if state!=0||level!=8||!twoPlayers {t.Fatal("resume key")}
}
func TestPendingReadKeepsNewLanguageAndCheckpoint(t *testing.T) {
 freshProgress();defer checkpointCleanup()
 savedProgress=encodeSaveValues(300,1,400,12,2000,20,true,11,0)
 unavailable=true;profileLoaded=false;loadProfile();language=1;languageDirty=true
 recordCheckpoint(3,0,0,false);awardCoins(10)
 unavailable=false;saveRetry=0;updateProfile()
 if language!=1||checkpointLevel!=3||clearedLevel!=11||coins!=310||evolution!=1||profileDirty {t.Fatal("delayed merge discarded active preference or progress")}
}
