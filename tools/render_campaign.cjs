// Compose QA previews from actual assets and snapshots of the tested SPX logic.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('./project_paths.cjs').sharpRuntime();
const {root,previews,snapshots} = require('./project_paths.cjs');
const directions = ['up', 'right', 'down', 'left'];
async function render(data, menu = false) {
  const level = data.Level, theme = data.Theme, frame = data.Snapshot;
  const layers = [];
  async function put(folder, name, x, y) {
    const directory = path.join(root, 'assets/sprites', folder);
    const config = JSON.parse(fs.readFileSync(path.join(directory, 'index.json')));
    const costume = config.costumes.find(item => item.name === name);
    if (!costume) throw new Error(`Unknown costume: ${folder}/${name}`);
    const input = path.join(directory, costume.path);
    const meta = await sharp(input).metadata();
    const left = Math.round(240 + x - meta.width / 2);
    const top = Math.round(180 - y - meta.height / 2);
    if (left < 0 || top < 0 || left + meta.width > 480 || top + meta.height > 360) return;
    layers.push({input: await sharp(input).png().toBuffer(), left, top});
  }
  await put('Scene', 'scene-' + level, 0, 0);
  for (const zone of data.Zones) await put('Actor', `zone-${zone.Kind}-warn-0`, zone.X, zone.Y);
  for (const e of frame.Entities) {
    let name;
    if (e.Kind === 1) name = `hero-0-0-p${e.ID === 191 ? '2' : '1'}-${directions[e.Facing]}-0`;
    if (e.Kind === 2) name = e.Type === 3 ? `boss-${theme}` : `zombie-${e.Type}-${directions[e.Facing]}-0`;
    if (e.Kind === 3) name = 'hedge';
    if (e.Kind === 4) name = 'stone';
    if (e.Kind === 13) name = 'portal-0';
    if (name) await put('Actor', name, e.X, e.Y);
  }
  for (const e of frame.Entities) if (e.Kind === 5) await put('Brain', 'brain-barrier-10-0', e.X, e.Y);
  await put('Frame', 'frame', 0, 0);
  if (!menu) {
    await put('Campaign', 'p1-3-0', -150, 130);
    await put('Campaign', 'p2-3-0', 150, 130);
    await put('Campaign', `stage-${level}-${frame.Kills}`, 105, -155);
    if (data.Boss) {
      await put('Campaign', `boss-${theme}-10`, 0, 148);
      await put('Campaign', `warning-${theme}`, 0, 50);
    }
  }
  if (menu) await put('Notice', `menu-2-${level}`, 0, 0);
  await put('Wallet', 'coin-label-1', menu ? 96 : -48, menu ? 148 : 130);
  for (let n = 0; n < 7; n++) await put('Wallet', 'coin-0', (menu ? 125 : -19)+n*10, menu ? 148 : 130);
  const backdrop = path.join(root, 'assets/painted-ground.png');
  const output = path.join(previews, `preview-20-${menu ? 'menu' : level}.png`);
  await sharp(backdrop).resize(480, 360).composite(layers).png().toFile(output);
  console.log(output);
}
(async () => {
  const frames = JSON.parse(fs.readFileSync(path.join(snapshots, 'campaign-frames.json')));
  for (const frame of frames) await render(frame);
  await render(frames[19], true);
  const bossImages = [];
  for (const level of [5, 10, 15, 20]) {
    bossImages.push({input: path.join(previews, `preview-20-${level}.png`), left: ((level/5-1)%2)*480, top: Math.floor((level/5-1)/2)*360});
  }
  await sharp({create:{width:960,height:720,channels:4,background:'#122c38'}}).composite(bossImages).png().toFile(path.join(previews,'preview-20-bosses.png'));
})().catch(error => { console.error(error); process.exit(1); });
