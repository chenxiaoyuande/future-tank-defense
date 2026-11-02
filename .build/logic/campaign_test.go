package main
import ("testing";"encoding/json";"os")
func campaignSetup(levelNumber int, coop bool) {
 selectedLevel=levelNumber;twoPlayers=coop;restart();keys=map[int]bool{}
}
func TestAllZombiesUseContactInsteadOfProjectiles(t *testing.T) {
 for stage:=1;stage<=20;stage++ {
  campaignSetup(stage,true)
  enemies:=[]int{}
  if bossStarted {enemies=append(enemies,bossSlot)} else {
   for _,i:=range zombieSlots {entity[i]=2;enemies=append(enemies,i)}
  }
  for tick:=1;tick<=1000;tick++ {
   for _,i:=range enemies {
    px[i]=0;py[i]=75;age[i]=tick;fire(i);updateZombie(i)
   }
   if count(6)!=0||count(7)!=0||count(9)!=0||count(18)!=0 {t.Fatal("enemy created a projectile",stage,tick)}
  }
 }
}
func TestZombieContactHurtsBothPlayersAndRespectsShields(t *testing.T) {
 for kind:=0;kind<4;kind++ {
  campaignSetup(1,true);for i:=2;i<191;i++ {entity[i]=0}
  px[1]=-8;py[1]=0;px[191]=8;py[191]=0;shield=0;shield2=0
  i:=zombieAt(0,0,0);zombieType[i]=kind;age[i]=1;updateZombie(i)
  if lives!=2||lives2!=2 {t.Fatal("contact missed a player",kind,lives,lives2)}
  px[1]=-8;py[1]=0;px[191]=8;py[191]=0;updateZombie(i)
  if lives!=2||lives2!=2 {t.Fatal("respawn protection ignored",kind)}
  shield=0;shieldBuff=500;shieldCharges=3;updateZombie(i)
  if lives!=2||shieldCharges!=2 {t.Fatal("contact ignored nut shield",kind)}
  updateZombie(i);if shieldCharges!=2 {t.Fatal("continuous overlap consumed shield repeatedly",kind)}
 }
}
func TestZombieAndBossContactCanDestroyExposedBrain(t *testing.T) {
 for _,kind:=range []int{0,3} {
  campaignSetup(1,true);for i:=2;i<191;i++ {entity[i]=0}
  px[1]=-140;py[1]=-100;px[191]=140;py[191]=-100
  base:=addEntity(5,0,0,0);hp[base]=0;i:=zombieAt(0,0,26);zombieType[i]=kind;facing[i]=0;age[i]=1
  if kind==3 {py[i]=35}
  updateGame();if entity[base]!=5||state!=0 {t.Fatal("brain damaged outside contact range",kind)}
  py[i]=23;if kind==3 {py[i]=32};updateGame()
  if entity[base]==5||state!=-1||count(8)==0 {t.Fatal("exposed brain contact did not end stage",kind)}
 }
}
func TestContactDamageStopsDuringPauseAndMenus(t *testing.T) {
 campaignSetup(1,false);for i:=2;i<191;i++ {entity[i]=0}
 px[1]=0;py[1]=0;shield=0;zombieAt(0,23,0)
 paused=true;updateGame();if lives!=3 {t.Fatal("paused contact damage")}
 paused=false;state=6;updateGame();if lives!=3 {t.Fatal("menu contact damage")}
 state=0;updateGame();if lives!=2 {t.Fatal("contact did not resume")}
}
func TestCooperativeControlsAndSkills(t *testing.T) {
 campaignSetup(1,true)
 px[1]=-100;py[1]=-60;px[191]=100;py[191]=-60
 for i:=2;i<191;i++ {entity[i]=0}
 keys[KeyW]=true;keys[KeyRight]=true;keys[KeySpace]=true;keys[KeyJ]=true;keys[KeyE]=true;keys[KeyK]=true
 updateGame()
 if py[1]!=-57.3 || px[191]!=102.7 || facing[1]!=0 || facing[191]!=1 {t.Fatal("controls coupled")}
 if shotDelay!=14 || shotDelay2!=14 || ultimateCooldown!=250 || ultimateCooldown2!=250 {t.Fatal("independent weapons failed")}
 if count(6)!=2 || count(9)!=2 {t.Fatal("both players must fire")}
 for n:=0;n<260;n++ {updateGame()}
 if ultimateCooldown!=0 || ultimateCooldown2!=0 {t.Fatal("holding skill must not repeat")}
}
func TestCooperativeLivesAndPickups(t *testing.T) {
 campaignSetup(1,true);shield=0;shield2=0
 collectSecondPickup(pickupAt(0,100,0));collectSecondPickup(pickupAt(2,100,0));collectSecondPickup(pickupAt(3,100,0))
 if shieldCharges2!=3 || speedBuff2!=400 || pepperBuff2!=400 || shieldBuff!=0 || speedBuff!=0 || pepperBuff!=0 {t.Fatal("pickups leaked to partner")}
 hitSecondPlayer();if shieldCharges2!=2 || lives2!=3 {t.Fatal("partner shield failed")}
 for n:=0;n<3;n++ {shield=0;hitPlayer()}
 if entity[1]!=0 || state!=0 || entity[191]!=1 {t.Fatal("one death ended cooperation")}
 shieldBuff2=0;for n:=0;n<3;n++ {shield2=0;hitSecondPlayer()}
 if state!=-1 {t.Fatal("both deaths must end game")}
}
func TestRespawnAvoidsPartnerAndObstacles(t *testing.T) {
 campaignSetup(1,true);px[191]=-48;py[191]=-120;shield=0
 hitPlayer()
 if blocked(px[1],py[1],1) {t.Fatal("respawn trapped player against partner or obstacle")}
}
func TestCampaignFiniteWavesAndBossProgression(t *testing.T) {
 for _,coop:=range []bool{false,true} {for n:=1;n<=20;n++ {
  campaignSetup(n,coop);shield=100000;shield2=100000
  if bossStarted!=(n%5==0) {t.Fatal("boss must appear only every fifth stage",n)}
  if n%5==0 {
   wantHP:=24+(n-1)/5*12;if coop {wantHP+=16}
   if zombieType[bossSlot]!=3 || hp[bossSlot]!=wantHP || waveTarget!=0 {t.Fatal("boss scaling or unexpected wave",n)}
   damageZombie(bossSlot,999);updateGame()
  } else {
   for tick:=0;tick<3000 && state==0;tick++ {
    for i:=2;i<191;i++ {if entity[i]==2 {damageZombie(i,99)};if entity[i]==7 {entity[i]=0}}
    updateGame()
   }
   if stageKills!=waveTarget || waveSpawned!=waveTarget || bossStarted {t.Fatal("regular wave failed",n,stageKills,waveSpawned,state)}
  }
  want:=2;if n==20 {want=3};if state!=want {t.Fatal("stage clear or victory failed",n,state)}
  if n<20 {old:=score;oldKills:=kills;nextLevel();if level!=n+1 || lives!=3 || lives2!=3 || score!=old || kills!=oldKills || (kills>=3 && weaponLevel!=1) {t.Fatal("next stage progression",n)}}
 }}
}
func TestTwentyDistinctTraversableMaps(t *testing.T) {
 seen:=map[string]bool{}
 for n:=1;n<=20;n++ {
  signature:="";ground:=0
  for row:=0;row<11;row++ {for col:=0;col<19;col++ {k:=mapTile(n,col,row);signature+=string(rune('0'+k));if k==0 {ground++}}}
  if seen[signature] {t.Fatal("repeated map",n)};seen[signature]=true
  reachable:=map[[2]int]bool{{0,0}:true};queue:=[][2]int{{0,0}}
  for len(queue)>0 {
   p:=queue[0];queue=queue[1:]
   for _,d:=range [][2]int{{1,0},{-1,0},{0,1},{0,-1}} {
    q:=[2]int{p[0]+d[0],p[1]+d[1]}
    if q[0]>=0&&q[0]<19&&q[1]>=0&&q[1]<11&&mapTile(n,q[0],q[1])==0&&!reachable[q] {reachable[q]=true;queue=append(queue,q)}
   }
  }
  if len(reachable)!=ground {t.Fatal("isolated ground",n,len(reachable),ground)}
  campaignSetup(n,true)
  if blocked(px[1],py[1],1)||blocked(px[191],py[191],191) {t.Fatal("blocked player start",n)}
  if n%5!=0 {for _,i:=range zombieSlots {if entity[i]!=13||blocked(px[i],py[i],i) {t.Fatal("unsafe initial enemy",n)}}}
 }
}
func TestBossTelegraphAndEnrage(t *testing.T) {
 for theme:=0;theme<4;theme++ {
  campaignSetup((theme+1)*5,true);i:=bossSlot
  updateBoss(i);normal:=count(16);period:=dashCooldown[i]
  if normal==0 || dashWindup[i]<=0 {t.Fatal("missing theme warning",theme)}
  for j:=2;j<191;j++ {if entity[j]==16 {if hazardKind[j]!=theme||age[j]>=hazardWarmup[j] {t.Fatal("wrong hazard or missing warning")};entity[j]=0}}
  hp[i]=maxHP[i]/2;dashCooldown[i]=0;updateBoss(i)
  if count(16)<=normal||dashCooldown[i]>=period {t.Fatal("enrage did not escalate",theme)}
 }
}
func TestCampaignMenuPauseAndRestart(t *testing.T) {
 campaignSetup(1,false);state=1;menuDown=false;confirmDown=false;clearedLevel=10
 keys[Key2]=true;keys[KeyH]=true;updateControls()
 if !twoPlayers || selectedLevel!=11 || state!=1 {t.Fatal("selection failed")}
 keys[KeyEnter]=true;updateControls();if state!=7 {t.Fatal("class selection not opened")}
 keys=map[int]bool{};updateControls();keys[KeyEnter]=true;updateControls();if level!=11 || state!=0 || entity[191]!=1 {t.Fatal("start failed")}
 paused=true;before:=ticks;cool:=ultimateCooldown2;updateGame()
 if ticks!=before || ultimateCooldown2!=cool {t.Fatal("pause advanced")}
 paused=false;keys=map[int]bool{KeyM:true};updateControls();before=ticks;updateGame()
 if state!=6 || ticks!=before {t.Fatal("home did not stop combat")}
}
func TestCooperativeFriendlyFire(t *testing.T) {
 campaignSetup(1,true)
 for i:=2;i<191;i++ {entity[i]=0}
 px[1]=-100;py[1]=0;px[191]=0;py[191]=0;shield2=0
 base:=addEntity(5,50,0,0)
 bullet:=addEntity(6,-20,0,1);velx[bullet]=1;vely[bullet]=0
 for n:=0;n<15;n++ {updateGame()}
 if lives2!=3 || entity[base]!=5 || state!=0 {t.Fatal("friendly fire")}
 zombieAt(0,px[191]-23,py[191]);updateGame();if lives2!=2 {t.Fatal("enemy contact did not hit second player")}
}
func TestCampaignPreviewSnapshots(t *testing.T) {
 frames:=[]map[string]any{};catalog:=[]map[string]any{}
 for n:=1;n<=20;n++ {
  campaignSetup(n,true);ticks=30;shield=0;shield2=0
  rows:=[]string{}
  for row:=2;row<=9;row++ {line:="";for col:=0;col<19;col++ {line+=string(rune('0'+mapTile(n,col,row)))};rows=append(rows,line)}
  catalog=append(catalog,map[string]any{"level":n,"theme":bossTheme,"target":waveTarget,"boss":bossStarted,"rows":rows})
  px[1]=-96;py[1]=-60;px[191]=96;py[191]=-60
  if bossStarted {planBossAttack(bossSlot)}
  zones:=[]map[string]any{}
  for j:=2;j<191;j++ {if entity[j]==16 {zones=append(zones,map[string]any{"Kind":hazardKind[j],"X":px[j],"Y":py[j],"Warmup":hazardWarmup[j]})}}
  frames=append(frames,map[string]any{"Level":n,"Theme":bossTheme,"Target":waveTarget,"Boss":bossStarted,"Snapshot":snapshot("四境远征"),"Zones":zones})
 }
 data,_:=json.MarshalIndent(frames,"","  ")
 if err:=os.WriteFile(previewFile("campaign-frames.json"),data,0644);err!=nil {t.Fatal(err)}
 data,_=json.MarshalIndent(catalog,"","  ")
 if err:=os.WriteFile("../../data/level-catalog.json",data,0644);err!=nil {t.Fatal(err)}
}
func TestElementWarningDamageAndIceSlow(t *testing.T) {
 for _,kind:=range []int{2,3} {
  campaignSetup(15,true);for i:=2;i<191;i++ {entity[i]=0}
  px[1]=0;py[1]=0;px[191]=100;py[191]=0;shield=0;shield2=0
  i:=addHazard(kind,0,0)
  for n:=0;n<hazardWarmup[i];n++ {age[i]=n;updateHazard(i);if lives!=3 {t.Fatal("warning caused damage",kind)}}
  age[i]=hazardWarmup[i];updateHazard(i)
  if lives!=2||lives2!=3 {t.Fatal("zone damage or escape failed",kind)}
  age[i]=hazardWarmup[i]+hazardDuration[i];updateHazard(i);if entity[i]!=0 {t.Fatal("zone did not expire")}
 }
 campaignSetup(10,true);for i:=2;i<191;i++ {entity[i]=0};px[1]=0;py[1]=0;px[191]=100;py[191]=0
 i:=addHazard(1,0,0);age[i]=hazardWarmup[i]-1;if onIce(1) {t.Fatal("warning slowed player")}
 age[i]++;if !onIce(1)||onIce(191) {t.Fatal("ice bounds")}
 keys[KeyW]=true;updateGame();if py[1]!=1.35||lives!=3 {t.Fatal("ice must halve speed without damage")}
}
func TestSummonCapsKillAccountingAndCleanup(t *testing.T) {
 campaignSetup(5,true);boss:=bossSlot
 for n:=0;n<10;n++ {
  planBossAttack(boss)
  for j:=2;j<191;j++ {if entity[j]==16 {age[j]=hazardWarmup[j];updateHazard(j)}}
 }
 if minionCount()>4||minionCount()==0 {t.Fatal("summon cap",minionCount())}
 for j:=2;j<191;j++ {if summoned[j] {damageZombie(j,999)}}
 if stageKills!=0||bossDefeated {t.Fatal("minion counted as stage/boss")}
 damageZombie(boss,999);updateGame()
 if state!=2||count(16)!=0||minionCount()!=0 {t.Fatal("boss cleanup")}
}
func TestHazardsFreezeAndReset(t *testing.T) {
 campaignSetup(20,true);i:=addHazard(3,0,0);paused=true;cool:=dashCooldown[bossSlot]
 for n:=0;n<100;n++ {updateGame()};if age[i]!=0||dashCooldown[bossSlot]!=cool {t.Fatal("paused hazard advanced")}
 restart();if count(16)!=0||minionCount()!=0 {t.Fatal("restart left hazards")}
}
func TestHazardsHitBothPlayersRespectShieldsAndThunderOnlyStrikesOnce(t *testing.T) {
 for _,kind:=range []int{2,3} {
  campaignSetup(20,true);for j:=2;j<191;j++ {entity[j]=0}
  px[1]=-8;py[1]=0;px[191]=8;py[191]=0;shield=0;shield2=0
  shieldBuff=500;shieldCharges=3
  i:=addHazard(kind,0,0);age[i]=hazardWarmup[i];updateHazard(i)
  if shieldCharges!=2||lives!=3||lives2!=2 {t.Fatal("hazard must hit both players and respect pickup shield",kind)}
  if kind==3 {
   shield=0;shield2=0;age[i]++;updateHazard(i)
   if shieldCharges!=2||lives2!=2 {t.Fatal("thunder repeatedly damaged after impact")}
  }
 }
}
func TestDifficultyAndAllTwentyMenuSelections(t *testing.T) {
 previous:=0
 for n:=1;n<=20;n++ {
  campaignSetup(n,false)
  if n%5!=0 {if waveTarget<=previous {t.Fatal("enemy quota not increasing")};previous=waveTarget}
 }
 campaignSetup(1,false);state=1;selectedLevel=1;menuDirection=0;confirmDown=false;clearedLevel=19
 for n:=2;n<=20;n++ {
  keys=map[int]bool{KeyRight:true};updateControls()
  if selectedLevel!=n {t.Fatal("cannot select all 20 stages",n)}
  updateControls();if selectedLevel!=n {t.Fatal("held input skipped a stage")}
  keys=map[int]bool{};updateControls()
 }
 keys=map[int]bool{KeyEnter:true};updateControls()
 if state!=7 {t.Fatal("missing class selection")}
 keys=map[int]bool{};updateControls();keys[KeyEnter]=true;updateControls()
 if level!=20||!bossStarted||bossTheme!=3 {t.Fatal("final boss selection failed")}
}
