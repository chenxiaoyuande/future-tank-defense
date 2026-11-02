package main
import "testing"

func freshProgress() {
 coins=0;lifetimeCoins=0;evolution=0;profileLoaded=false;profileDirty=false;profileDamaged=false
 savedProgress="";unavailable=false;saveStatus=0;evolveNotice=0;loadProfile()
}
func TestCoinsRewardExactlyOnceAndSurviveRestart(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 campaignSetup(1,false);i:=zombieAt(0,100,0);damageZombie(i,99);damageZombie(i,99)
 if coins!=15||lifetimeCoins!=15||saveStatus!=1 {t.Fatal("kill reward not saved exactly once")}
 restart();if coins!=15 {t.Fatal("restart erased wallet")}
 state=2;nextLevel();if coins!=15 {t.Fatal("next stage erased wallet")}
 profileLoaded=false;coins=0;lifetimeCoins=0;loadProfile();if coins!=15||lifetimeCoins!=15 {t.Fatal("reload lost wallet")}
}
func TestBossAndSummonRewards(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 campaignSetup(20,true);damageZombie(bossSlot,999)
 if coins!=250 {t.Fatal("final boss reward")}
 i:=zombieAt(1,100,0);summoned[i]=true;damageZombie(i,99)
 if coins!=252||stageKills!=0 {t.Fatal("summon reward or wave accounting")}
}
func TestFiveEvolutionPurchasesPersistAndMaxOut(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 awardCoins(3250);state=4
 for tier:=1;tier<=5;tier++ {
  if !buyEvolution()||evolution!=tier {t.Fatal("purchase",tier)}
  profileLoaded=false;loadProfile();state=4;if evolution!=tier {t.Fatal("tier did not persist")}
 }
 if coins!=0||lifetimeCoins!=3250||buyEvolution() {t.Fatal("cost or max tier")}
 restart();if evolution!=5||coins!=0 {t.Fatal("new run erased evolution")}
}
func TestEvolutionInsufficientAndCombatGuard(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 state=4;awardCoins(99);if buyEvolution()||coins!=99||evolution!=0 {t.Fatal("insufficient funds")}
 awardCoins(1000);state=0;if buyEvolution() {t.Fatal("combat purchase")}
 state=1;keys=map[int]bool{KeyB:true};evolutionDown=false;updateControls()
 if state!=4 {t.Fatal("outside evolution entry")}
 keys=map[int]bool{KeyU:true};buyDown=false;updateControls();updateControls()
 if evolution!=1||coins!=999 {t.Fatal("holding U repeated purchase")}
 keys=map[int]bool{KeyM:true};menuDown=false;updateControls();if state!=1 {t.Fatal("return from evolution")}
 state=2;evolutionDown=false;keys=map[int]bool{KeyB:true};updateControls()
 keys=map[int]bool{KeyM:true};menuDown=false;updateControls();if state!=2 {t.Fatal("lost stage clear state")}
}
func TestDamagedSaveImportAndFailure(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 for _,bad:=range []string{"broken","TG1|-1|0|0|0",profileCode(10,6,99),profileCode(0,5,1)} {
  savedProgress=bad;profileLoaded=false;loadProfile()
  if !profileDamaged||saveStatus!=3 {t.Fatal("accepted corrupt save")}
  awardCoins(10);if savedProgress!=bad {t.Fatal("overwrote corrupt save")}
 }
 valid:=profileCode(500,2,850)
 if !importProfile(valid)||coins!=500||evolution!=2||profileDamaged {t.Fatal("restore failed")}
 before:=savedProgress;if importProfile("invalid")||coins!=500||savedProgress!=before {t.Fatal("invalid restore changed progress")}
 unavailable=true;state=4;buyEvolution()
 if saveStatus!=2||!profileDirty {t.Fatal("storage failure falsely reported success")}
 unavailable=false;saveRetry=0;updateProfile();if profileDirty||saveStatus!=1 {t.Fatal("failed save not retried")}
}
func TestEvolutionProjectilesAndIndependentPepper(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 campaignSetup(1,true);for i:=2;i<191;i++ {entity[i]=0}
 evolution=5;pepperBuff2=50;fire(1);fire(191)
 first,second:=0,0
 for i:=2;i<191;i++ {if entity[i]==6 {if first==0{first=i}else{second=i}}}
 if projectileDamage[first]!=3||projectileDamage[second]!=4||projectileTier[first]!=5 {t.Fatal("evolution and pepper damage")}
 evolution=0;if projectileTier[first]!=5||projectileDamage[first]!=3 {t.Fatal("in-flight projectile mutated")}
 evolution=5;ultimateCooldown=0;castUltimate();if ultimateCooldown!=175 {t.Fatal("ultimate cooldown")}
}
func TestUnreadSaveCannotBeOverwrittenByTemporaryEarnings(t *testing.T) {
 freshProgress();defer func(){profileLoaded=false;evolution=0}()
 savedProgress=profileCode(500,2,850);unavailable=true;profileLoaded=false;loadProfile()
 awardCoins(15);state=4;if buyEvolution() {t.Fatal("purchase before old save was read")}
 before:=savedProgress
 if !profileReadPending||savedProgress!=before {t.Fatal("unread save was overwritten")}
 unavailable=false;saveRetry=0;updateProfile()
 if coins!=515||lifetimeCoins!=865||evolution!=2||profileReadPending||profileDirty {t.Fatal("pending rewards not merged with existing profile")}
}
