package main
import("testing";"strings")

func professionSetup() {
 freshProgress();campaignSetup(1,true)
 for i:=2;i<191;i++{entity[i]=0}
 px[1]=-130;py[1]=0;px[191]=-130;py[191]=-70;facing[1]=1;facing[191]=1
 playerClass=0;playerClass2=0;routeTiers=[3]int{};evolution=0
}
func professionCleanup(){checkpointCleanup();playerClass=0;playerClass2=0;routeTiers=[3]int{};labClass=0}
func TestThreeClassesHaveDifferentWeapons(t *testing.T){
 professionSetup();defer professionCleanup()
 fire(1);if count(6)!=1||classShotDelay(1)!=14{t.Fatal("base pea")}
 evolution=2;fire(1);if count(6)!=3||classShotDelay(1)!=8{t.Fatal("gatling pea")}
 for i:=2;i<191;i++{entity[i]=0};playerClass=1;fire(1)
 if count(6)!=1||classShotDelay(1)!=22{t.Fatal("mushroom shot")}
 for i:=2;i<191;i++{if entity[i]==6 && (projectileClass[i]!=1||pierceRemaining[i]!=1){t.Fatal("missing spore pierce")}}
 for i:=2;i<191;i++{entity[i]=0};playerClass=2;fire(1)
 if count(6)!=0||count(18)!=1||classShotDelay(1)!=38{t.Fatal("melon is not a lob")}
}
func TestMushroomPiercesWithoutRepeatingDamage(t *testing.T){
 professionSetup();defer professionCleanup();playerClass=1
 a:=zombieAt(0,-78,0);b:=zombieAt(0,-40,0);fire(1)
 // Freeze enemies while checking the actual collision loop.
 for i:=0;i<15;i++{dashWindup[a]=100;dashWindup[b]=100;updateGame()}
 if hp[a]!=4||hp[b]!=4{t.Fatal("pierce must damage each enemy once",hp[a],hp[b])}
 if lives!=3||lives2!=3{t.Fatal("friendly fire")}
}
func TestCloudTicksAndMelonUltimateAreDistinct(t *testing.T){
 professionSetup();defer professionCleanup();playerClass=1
 enemy:=zombieAt(0,-70,0);hp[enemy]=30;maxHP[enemy]=30
 if !castUltimate()||count(17)!=1||count(9)!=0||ultimateCooldown!=300{t.Fatal("spore ultimate")}
 for i:=2;i<191;i++{if entity[i]==17{for tick:=1;tick<=150;tick++{age[i]=tick;updateSporeCloud(i)}}}
 if hp[enemy]!=24||count(17)!=0{t.Fatal("cloud tick lifetime",hp[enemy])}
 playerClass=2;ultimateCooldown=0
 if !castUltimate()||count(18)!=1||ultimateCooldown!=350{t.Fatal("melon ultimate")}
 for i:=2;i<191;i++{if entity[i]==18 && (!rocket[i]||projectileDamage[i]!=8){t.Fatal("heavy melon snapshot")}}
}
func TestOverlappingSporeTargetsAreNotHitTwice(t *testing.T){
 professionSetup();defer professionCleanup();playerClass=1;routeTiers[1]=5
 a:=zombieAt(0,-87,0);b:=zombieAt(0,-86,0);hp[a]=100;hp[b]=100;maxHP[a]=100;maxHP[b]=100
 fire(1)
 for n:=0;n<7;n++{dashWindup[a]=100;dashWindup[b]=100;updateGame()}
 if hp[a]!=94||hp[b]!=94{t.Fatal("two spores must each hit a clustered target once",hp[a],hp[b])}
}
func TestMelonLobDelayedSplashAndFreeze(t *testing.T){
 professionSetup();defer professionCleanup();playerClass=2;routeTiers[2]=4
 enemy:=zombieAt(0,-10,0);other:=zombieAt(0,10,0);hp[enemy]=20;hp[other]=20
 addEntity(4,-75,0,0);fire(1);slot:=0
 for i:=2;i<191;i++{if entity[i]==18{slot=i}}
 if slot==0||landingX[slot]!=-10{t.Fatal("targeting")}
 routeTiers[2]=0
 for tick:=1;tick<30;tick++{age[slot]=tick;updateMelon(slot)}
 if hp[enemy]!=20||hp[other]!=20{t.Fatal("airborne damage")}
 age[slot]=30;updateMelon(slot)
 if hp[enemy]!=15||hp[other]!=15||chillTicks[enemy]!=80||chillTicks[other]!=80{t.Fatal("splash/freeze snapshot",hp[enemy],hp[other])}
 if count(18)!=0||count(10)!=1{t.Fatal("impact transition")}
}
func TestCoopIndependentClassTierAndCooldown(t *testing.T){
 professionSetup();defer professionCleanup();playerClass=1;playerClass2=2;routeTiers[1]=3;routeTiers[2]=4
 keys=map[int]bool{KeySpace:true,KeyJ:true,KeyE:true,KeyK:true};updateGame()
 if count(6)!=2||count(18)!=2||count(17)!=1||count(9)!=0{t.Fatal("co-op weapon types")}
 if ultimateCooldown!=255||ultimateCooldown2!=270||shotDelay!=19||shotDelay2!=26{t.Fatal("co-op cooldowns",ultimateCooldown,ultimateCooldown2,shotDelay,shotDelay2)}
}
func TestThreeRoutesPurchaseAndTG3Reload(t *testing.T){
 professionSetup();defer professionCleanup();awardCoins(5000);state=4
 for role:=0;role<3;role++{labClass=role;if !buyEvolution(){t.Fatal("route purchase",role)}}
 labClass=1;buyEvolution();playerClass=1;playerClass2=2;clearedLevel=3;recordCheckpoint(4,900,9,true)
 if evolution!=1||routeTiers[1]!=2||routeTiers[2]!=1||coins!=4450{t.Fatal("independent cost",coins)}
 profileLoaded=false;loadProfile()
 if !strings.HasPrefix(savedProgress,"TG3|")||evolution!=1||routeTiers[1]!=2||routeTiers[2]!=1||coins!=4450||checkpointClass!=1||checkpointClass2!=2{t.Fatal("TG3 roster not saved")}
 if !continueCheckpoint()||playerClass!=1||playerClass2!=2||level!=4{t.Fatal("roster checkpoint resume")}
 before:=savedProgress
 for _,bad:=range []string{encodeRosterSave(100,1,200,1,0,0,false,0,0,5,0,0,0),encodeRosterSave(0,0,0,1,0,0,false,0,0,0,0,3,0),before+"x"}{if importProfile(bad)||savedProgress!=before{t.Fatal("invalid roster accepted")}}
}
func TestOldSaveRetainsWalletAndPeaRoute(t *testing.T){
 professionSetup();defer professionCleanup()
 for _,code:=range []string{profileCode(600,2,950),encodeSaveValues(600,2,950,1,0,0,false,0,1)}{
 if !importProfile(code)||coins!=600||evolution!=2||routeTiers[1]!=0||routeTiers[2]!=0||playerClass!=0{t.Fatal("old save migration")}
 }
}
func TestHomeStageClassFlowAndLocks(t *testing.T){
 professionSetup();defer professionCleanup();state=6;selectedLevel=18;uiAction(0)
 if state!=1||selectedLevel!=1||unlockedLevel()!=1{t.Fatal("start must begin at stage one")}
 selectedLevel=2;openClassSelect();if state!=1||evolveNotice!=9{t.Fatal("locked stage opened")}
 pendingClass=2;startWithClasses();if state!=1{t.Fatal("locked stage started")}
 manualCheckpoint();if checkpointLevel!=0{t.Fatal("locked checkpoint saved")}
 selectedLevel=1;openClassSelect();chooseClass(1);uiAction(4);chooseClass(2);uiAction(5)
 if state!=0||level!=1||playerClass!=1||playerClass2!=2||checkpointClass!=1{t.Fatal("class confirmation")}
 stageKills=waveTarget;updateGame();if unlockedLevel()!=2||clearedLevel!=1||checkpointLevel!=2{t.Fatal("stage did not unlock next")}
 profileLoaded=false;loadProfile();if unlockedLevel()!=2||!canStartStage(2)||canStartStage(3){t.Fatal("unlock reload")}
}
func TestLegacyCheckpointCannotBypassLock(t *testing.T){
 professionSetup();defer professionCleanup()
 if !importProfile(encodeSaveValues(500,0,500,17,5000,50,true,2,0)){t.Fatal("legacy import")}
 if checkpointLevel!=3||checkpointScore!=0||checkpointKills!=0||unlockedLevel()!=3{t.Fatal("legacy checkpoint bypass")}
 if !continueCheckpoint()||level!=3{t.Fatal("legacy resume")}
}
func TestHomeSettingsAndMenuDoNotRunCombat(t *testing.T){
 professionSetup();defer professionCleanup();state=6;before:=ticks;uiAction(2)
 if state!=8{t.Fatal("settings entry")};uiAction(1);if language!=1||saveStatus!=1{t.Fatal("settings persist")};uiAction(2)
 if state!=6{t.Fatal("settings return")};uiAction(3);if state!=4{t.Fatal("lab entry")};uiAction(2);if labClass!=2{t.Fatal("lab tabs")};uiAction(4)
 if state!=6{t.Fatal("lab back")};uiAction(1);if state!=5{t.Fatal("load entry")};uiAction(3)
 for _,menu:=range []int{1,4,5,6,7,8}{state=menu;updateGame();if ticks!=before{t.Fatal("menu advanced combat",menu)}}
 playerClass=2;ultimateCooldown=350;if ultimateBar()!=0{t.Fatal("negative cooldown bar")}
}
