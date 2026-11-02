// Render exported, outlined SVG assets without relying on installed fonts.
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require('./project_paths.cjs').sharpRuntime();
(async () => {
  const tasks = JSON.parse(await fs.readFile(path.join(require('./project_paths.cjs').previews, 'front-preview-manifest.json'), 'utf8'));
  for (const item of tasks) {
    const local = value => process.platform === 'win32' ? value.replace(/^\/mnt\/([a-z])\//, (_,drive)=>drive.toUpperCase()+':/') : value;
    const source = local(item.source);
    const output = local(item.output);
    await sharp(source).resize(item.width, item.height).png().toFile(output);
  }
  const {root,previews} = require('./project_paths.cjs');
  await sharp(path.join(previews,'preview-brain.svg')).png().toFile(path.join(root,'docs/media/brain-barrier.png'));
  console.log(`Rendered ${tasks.length} front end and evolution frames.`);
})().catch(error => { console.error(error); process.exitCode = 1; });
