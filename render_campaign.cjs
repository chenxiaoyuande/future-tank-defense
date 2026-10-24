// Compose QA previews from actual assets and snapshots of the tested SPX logic.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('C:/Users/lijia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root = __dirname;
const directions = ['up', 'right', 'down', 'left'];
async function render(frame, level, menu = false) {
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
  for (const e of frame.Entities) {
    let name;
    if (e.Kind === 1) name = `${e.ID === 191 ? 'partner' : 'plant'}-${directions[e.Facing]}-0`;
    if (e.Kind === 2) name = e.Type === 3 ? 'boss' : `zombie-${e.Type}-${directions[e.Facing]}-0`;
    if (e.Kind === 3) name = 'hedge';
    if (e.Kind === 4) name = 'stone';
    if (e.Kind === 5) name = 'house';
    if (name) await put('Actor', name, e.X, e.Y);
  }
  await put('Frame', 'frame', 0, 0);
  if (!menu) {
    await put('Campaign', 'p1-3-0', -150, 130);
    await put('Campaign', 'p2-3-0', 150, 130);
    await put('Campaign', `stage-${level}-${3 + level * 3}`, 105, -155);
    await put('Campaign', 'boss-10', 0, 148);
  }
  if (menu) await put('Notice', `menu-2-${level}`, 0, 0);
  const backdrop = path.join(root, 'assets/painted-ground.png');
  const output = path.join(root, `preview-campaign-${menu ? 'menu' : level}.png`);
  await sharp(backdrop).resize(480, 360).composite(layers).png().toFile(output);
  console.log(output);
}
(async () => {
  const frames = JSON.parse(fs.readFileSync(path.join(root, 'campaign-frames.json')));
  for (let i = 0; i < frames.length; i++) await render(frames[i], i + 1);
  await render(frames[0], 1, true);
})().catch(error => { console.error(error); process.exit(1); });
