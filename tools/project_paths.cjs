const path = require('node:path');
const root = path.resolve(__dirname, '..');
const previews = path.join(root, '.build', 'previews');
function sharpRuntime() {
  if (process.env.GARDEN_SHARP_MODULE) return require(process.env.GARDEN_SHARP_MODULE);
  try { return require('sharp'); }
  catch { return require('C:/Users/lijia/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'); }
}
module.exports = {root, previews, snapshots:path.join(root,'.build','snapshots'), frontFrames:path.join(previews,'front'), docsFrames:path.join(previews,'boss-frames'), sharpRuntime};
