package main
import "testing"

func brainSetup() (int,int) {
 campaignSetup(1,true)
 base:=0;for i:=2;i<191;i++ {if entity[i]==5{base=i}else{entity[i]=0}}
 px[1]=-160;py[1]=100;px[191]=160;py[191]=100;shield=100000;shield2=100000
 waveSpawned=waveTarget
 enemy:=zombieAt(0,px[base],py[base]+23)
 return base,enemy
}
func TestBrainBarrierLastsExactlyThreeSeconds(t *testing.T) {
 base,enemy:=brainSetup()
 if hp[base]!=150||maxHP[base]!=150{t.Fatal("brain did not start protected")}
 x,y:=px[enemy],py[enemy]
 for frame:=1;frame<150;frame++ {
  updateGame()
  if hp[base]!=150-frame||entity[base]!=5||state!=0{t.Fatal("barrier timing",frame,hp[base])}
 }
 if px[enemy]!=x||py[enemy]!=y{t.Fatal("biting zombie wandered away")}
 updateGame();if hp[base]!=0||entity[base]!=5||state!=0{t.Fatal("last barrier tick destroyed brain")}
 updateGame();if entity[base]==5||state!=-1{t.Fatal("exposed brain survived contact")}
}
func TestInterruptedBitingPreservesBarrierDamage(t *testing.T) {
 base,enemy:=brainSetup()
 for frame:=0;frame<60;frame++{updateGame()}
 px[enemy]=0;py[enemy]=100
 for frame:=0;frame<30;frame++{updateGame()}
 if hp[base]!=90{t.Fatal("absent biter changed durability",hp[base])}
 px[enemy]=px[base];py[enemy]=py[base]+23
 for frame:=0;frame<89;frame++{updateGame()}
 if hp[base]!=1||state!=0{t.Fatal("resumed biting did not preserve damage")}
 updateGame();if hp[base]!=0||entity[base]!=5{t.Fatal("final bite")}
}
func TestSeveralBitersDoNotAccelerateBarrierLoss(t *testing.T) {
 for _,kind:=range []int{0,3}{
  base,enemy:=brainSetup();zombieType[enemy]=kind
  for n:=0;n<3;n++{i:=zombieAt(1,px[base]+float64(n),py[base]+23);summoned[i]=true}
  for frame:=0;frame<149;frame++{updateGame()}
  if hp[base]!=1||state!=0{t.Fatal("group bypassed three-second barrier",kind,hp[base])}
  updateGame();if hp[base]!=0||entity[base]!=5{t.Fatal("group final barrier tick",kind)}
 }
}
func TestBrainBarrierFreezesAndResetsAtStageStart(t *testing.T) {
 freshProgress();defer checkpointCleanup();base,_:=brainSetup();recordCheckpoint(1,0,0,true)
 for frame:=0;frame<50;frame++{updateGame()}
 paused=true;for frame:=0;frame<200;frame++{updateGame()}
 paused=false;state=6;for frame:=0;frame<200;frame++{updateGame()}
 if hp[base]!=100{t.Fatal("paused or menu barrier changed")}
 if !continueCheckpoint(){t.Fatal("resume checkpoint")}
 for i:=2;i<191;i++{if entity[i]==5&&hp[i]!=150{t.Fatal("resume did not restore barrier")}}
 restart();for i:=2;i<191;i++{if entity[i]==5&&hp[i]!=150{t.Fatal("retry did not restore barrier")}}
}
func TestFriendlyAttacksAndBossZonesDoNotHurtBrainBarrier(t *testing.T) {
 base,enemy:=brainSetup();entity[enemy]=0
 blast(px[base],py[base],999,150)
 for _,kind:=range []int{1,2,3}{i:=addHazard(kind,px[base],py[base]);age[i]=hazardWarmup[i];updateHazard(i)}
 playerClass=0;facing[1]=2;px[1]=px[base];py[1]=py[base]+40;fire(1)
 for frame:=0;frame<20;frame++{updateGame()}
 if hp[base]!=150||entity[base]!=5||state!=0{t.Fatal("non-bite damage bypassed barrier")}
}
