// Rasterize generated SVG animation frames using the project's existing Sharp runtime.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require('./project_paths.cjs').sharpRuntime();
const directory = require('./project_paths.cjs').docsFrames;
const localPath = source => source.replace('/mnt/e/', 'E:/');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(path.join(directory, 'manifest.json')));
  for (const job of jobs) {
    for (const source of job.frames) {
      const file = localPath(source);
      await sharp(file).png().toFile(file.replace(/\.svg$/, '.png'));
    }
    console.log(`Rendered ${job.frames.length} frames: ${job.name}`);
  }
})().catch(error => { console.error(error); process.exit(1); });
