import { execFile } from 'node:child_process';
import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const execFileAsync = promisify(execFile);

const root = process.cwd();
const inputHtml = process.argv[2] ?? 'poster.html';
const outputFolder = process.argv[3] ?? 'poster-pages';
const htmlPath = path.join(root, inputHtml);
const outputDir = path.join(root, outputFolder);
const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const tempPath = path.join(root, '.poster-export.html');

const pages = [
  ['cover', '01-cover.png'],
  ['map', '02-capability-map.png'],
  ['molecule', '03-small-molecule.png'],
  ['biomolecule', '04-biomolecule-design.png'],
  ['structure', '05-structure-pocket.png'],
  ['antibody', '06-antibody-engineering.png'],
  ['workflow', '07-workflow.png'],
  ['install', '08-install-invoke.png'],
];

const exportCss = (id) => `
<style id="poster-export-style">
  html, body { width: 1080px; height: 1528px; margin: 0; overflow: hidden; }
  .topbar, .print-note { display: none !important; }
  .poster-shell { padding: 0 !important; }
  .page { display: none !important; }
  #${id} {
    display: grid !important;
    width: 1080px !important;
    min-height: 1528px !important;
    height: 1528px !important;
    padding: 0 !important;
    align-items: stretch !important;
    break-after: auto !important;
  }
  #${id} .page-inner {
    width: 100% !important;
    min-height: 1528px !important;
    height: 1528px !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }
</style>`;

await mkdir(outputDir, { recursive: true });
const source = await readFile(htmlPath, 'utf8');

for (const [id, filename] of pages) {
  const html = source.replace('</head>', `${exportCss(id)}\n</head>`);
  await writeFile(tempPath, html, 'utf8');

  const outputPath = path.join(outputDir, filename);
  await execFileAsync(chromePath, [
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--no-first-run',
    '--no-default-browser-check',
    '--window-size=1080,1528',
    `--screenshot=${outputPath}`,
    pathToFileURL(tempPath).href,
  ], { timeout: 60000 });

  console.log(`wrote ${path.join(outputFolder, filename)}`);
}

await rm(tempPath, { force: true });