// Composite previews from actual project assets and tested logic snapshots.
const fs=require('node:fs'),path=require('node:path');
const sharp=require('C:/Users/lijia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root=__dirname,cache=new Map(),directions=['up','right','down','left'];
async function asset(folder,name){
 const key=folder+'/'+name;
 if(!cache.has(key)) {
  const image=sharp(path.join(root,'assets/sprites',folder,name+'.svg')),m=await image.metadata();
  cache.set(key,{w:m.width,h:m.height,png:await image.resize(m.width*2,m.height*2).png().toBuffer()});
 }
 return cache.get(key);
}
async function render(frame){
 const layers=[];
 async function put(folder,name,x,y,scale=1,angle=0){
  const a=await asset(folder,name);let img=sharp(a.png);
  if(scale!==1) img=img.resize(Math.max(1,Math.round(a.w*2*scale)),Math.max(1,Math.round(a.h*2*scale)));
  if(angle) img=img.rotate(angle,{background:'#00000000'});
  let {data,info}=await img.png().toBuffer({resolveWithObject:true});
  const left=Math.round((240+x)*2-info.width/2),top=Math.round((180-y)*2-info.height/2);
  const cx=Math.max(0,-left),cy=Math.max(0,-top),w=Math.min(info.width-cx,960-Math.max(0,left)),h=Math.min(info.height-cy,720-Math.max(0,top));
  if(w<=0||h<=0)return;
  if(cx||cy||w!==info.width||h!==info.height)data=await sharp(data).extract({left:cx,top:cy,width:w,height:h}).png().toBuffer();
  layers.push({input:data,left:Math.max(0,left),top:Math.max(0,top)});
 }
 const tick=frame.Tick,hero=frame.Entities.find(e=>e.ID===1);
 for(let i=0;i<12;i++) await put('Atmosphere','firefly',(i*83)%420-210+Math.sin((tick+i*23)*.018)*9,(i*47)%260-130+Math.cos((tick+i*31)*.014)*6);
 for(const e of frame.Entities.filter(e=>[6,7,9].includes(e.Kind)).slice(0,10)){
  const angle=-Math.atan2(e.VY,e.VX)*180/Math.PI;
  await put('Atmosphere',e.Fire?'fire-trail':e.Kind===9?'mega-trail':e.Kind===6?(e.Rocket?'missile-trail':'seed-trail'):'spore-trail',e.X-e.VX*10,e.Y-e.VY*10,1,angle);
 }
 for(const e of frame.Entities.filter(e=>e.Kind===2&&e.Type===2&&(e.Windup>0||e.Dash>0))){
  const dist=e.Windup>0?36:-36;await put('Atmosphere',e.Windup>0?'dash-warning':'dash-trail',e.X+[0,1,0,-1][e.Facing]*dist,e.Y+[1,0,-1,0][e.Facing]*dist,1,e.Facing*90-90);
 }
 if(hero) {
  await put('Atmosphere',`aura-${Math.floor(tick/4)%4}`,hero.X,hero.Y-12,.78);
  if(frame.Nut) await put('Atmosphere','nut-shield',hero.X,hero.Y);
  if(frame.Speed) await put('Atmosphere','speed-wake',hero.X,hero.Y,1,hero.Facing*90-90);
  if(frame.Pepper) await put('Atmosphere','pepper-aura',hero.X,hero.Y);
 }
 for(const e of [...frame.Entities].sort((a,b)=>b.Y-a.Y)){
  let name,angle=0;
  if(e.Kind===1)name=`plant-${directions[e.Facing]}-${Math.floor(tick/5)%4}`;
  if(e.Kind===2)name=`zombie-${e.Type}-${directions[e.Facing]}-${e.Windup>0?6:e.Dash>0?7:Math.floor(e.Age/5)%4}`;
  if(e.Kind===3)name='hedge';if(e.Kind===4)name='stone';if(e.Kind===5)name='house';
  if(e.Kind===6){name=`${e.Fire?(e.Rocket?'fire-missile':'fire-seed'):(e.Rocket?'missile':'seed')}-${tick%2}`;if(e.Rocket)angle=-Math.atan2(e.VY,e.VX)*180/Math.PI;}
  if(e.Kind===7)name=`spore-${tick%2}`;if(e.Kind===8)name=`pop-${Math.min(6,Math.floor(e.Age/2))}`;
  if(e.Kind===9){name=`mega-${Math.floor(e.Age/2)%4}`;angle=e.Facing*90-90;}
  if(e.Kind===10)name=`burst-${Math.min(9,Math.floor(e.Age/3))}`;
  if(e.Kind===11)name=`grow-${Math.min(4,Math.floor(e.Growth/10))}`;
  if(e.Kind===12&&e.Age<30)name=`death-${Math.floor(e.Age/5)}`;
  if(e.Kind===13)name=`portal-${Math.floor(e.Age/4)%5}`;
  if(e.Kind===14)name=`pickup-${e.PickupType}-${Math.floor(tick/6)%2}`;
  if(e.Kind===15)name=`cherry-burst-${Math.min(7,Math.floor(e.Age/4))}`;
  if(name)await put('Actor',name,e.X,e.Y,1,angle);
 }
 for(const e of frame.Entities.filter(e=>e.Kind===2))await put('Health',`hp-${e.Type}-${e.HP}`,e.X,e.Y+26);
 await put('Frame','frame',0,0);
 await put('Atmosphere',frame.Weapon?'weapon-ready':`weapon-${Math.min(2,frame.Kills)}`,0,126);
 await put('Atmosphere',`cooldown-${10-Math.ceil(frame.Cooldown/25)}`,-112,-155);
 await put('Ability',frame.Cooldown?'wait-'+Math.ceil(frame.Cooldown/50):'ready-lit',112,-155);
 const score=String(frame.Score%100000).padStart(5,'0'),kills=String(frame.Kills%1000).padStart(3,'0');
 for(let n=0;n<5;n++)await put('Hud','d'+score[n],-170+n*10,148);
 await put('Hud','d'+frame.Lives,-35,148);
 for(let n=0;n<3;n++)await put('Hud','d'+kills[n],112+n*10,148);
 if(frame.Nut)await put('Buff','shield-3-'+Math.ceil(frame.Nut/50),-148,-135);
 if(frame.Speed)await put('Buff','speed-'+Math.ceil(frame.Speed/50),0,-135);
 if(frame.Pepper)await put('Buff','pepper-'+Math.ceil(frame.Pepper/50),148,-135);
 return sharp(path.join(root,'assets/painted-ground.png')).resize(960,720).composite(layers).png().toBuffer();
}
async function detailSheet(){
 const layers=[];
 async function place(folder,name,x,y,scale){const a=await asset(folder,name);layers.push({input:await sharp(a.png).resize(Math.round(a.w*scale),Math.round(a.h*scale)).png().toBuffer(),left:x,top:y});}
 for(let k=0;k<3;k++) {
  await place('Actor',`zombie-${k}-down-${k===2?6:0}`,100+k*265,35,3);
  await place('Health',`hp-${k}-${[5,1,3][k]}`,100+k*265,15,3);
 }
 for(let k=0;k<4;k++)await place('Actor',`pickup-${k}-0`,100+k*200,205,2.2);
 for(let f=0;f<5;f++)await place('Actor',`grow-${f}`,100+f*155,345,2.2);
 return sharp({create:{width:960,height:450,channels:4,background:'#203e45'}}).composite(layers).png().toBuffer();
}
(async()=>{
 const frames=JSON.parse(fs.readFileSync(path.join(root,'demo-frames.json'),'utf8'));
 for(let n=0;n<frames.length;n++)fs.writeFileSync(path.join(root,`preview-survival-${n}.png`),await render(frames[n]));
 fs.copyFileSync(path.join(root,'preview-survival-2.png'),path.join(root,'../暮光花园-僵尸道具版预览.png'));
 fs.writeFileSync(path.join(root,'preview-models.png'),await detailSheet());
 console.log(`Rendered ${frames.length} scenes and character/pickup/regrowth detail sheet.`);
})().catch(e=>{console.error(e);process.exitCode=1;});
