#!/usr/bin/env node
/**
 * render-mp4.js
 * Headless Chrome → WebM (MediaRecorder) → MP4 (FFmpeg).
 *
 * Usage:
 *   node scripts/render/render-mp4.js [URL] [SECONDS] [OUTPUT]
 *
 * Defaults:
 *   URL     = http://localhost:4173/concepts/_example-sports-tech/artifact.html
 *   SECONDS = 16.5  (full 3-stage loop)
 *   OUTPUT  = concepts/_example-sports-tech/loop.mp4
 *
 * Requires:
 *   • localhost preview server running (python3 http.server on :4173)
 *   • Google Chrome installed at /Applications/Google Chrome.app
 *   • Node ≥ 20
 */

import puppeteer from 'puppeteer-core';
import ffmpegPath from 'ffmpeg-static';
import { spawn } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const URL_ARG  = process.argv[2] || 'http://localhost:4173/concepts/_example-sports-tech/artifact.html';
const SECONDS  = parseFloat(process.argv[3] || '16.5');
const OUT_PATH = resolve(process.argv[4] || 'concepts/_example-sports-tech/loop.mp4');

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

console.log(`▸ url:      ${URL_ARG}`);
console.log(`▸ seconds:  ${SECONDS}`);
console.log(`▸ output:   ${OUT_PATH}`);
console.log(`▸ chrome:   ${CHROME}`);
console.log(`▸ ffmpeg:   ${ffmpegPath}`);

await mkdir(dirname(OUT_PATH), { recursive: true });

const HEADLESS = process.env.HEADLESS !== 'false';   // default headless; set HEADLESS=false to see the window
console.log(`▸ launching Chrome (headless=${HEADLESS})…`);
const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: HEADLESS,
  defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 },
  args: [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    // macOS native WebGL via ANGLE on Metal — only path that gives real
    // hardware WebGL in headless Chrome on this platform
    '--use-gl=angle',
    '--use-angle=metal',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    '--autoplay-policy=no-user-gesture-required',
  ],
});

const page = await browser.newPage();
page.on('console',  m => console.log(`  [page]    ${m.text()}`));
page.on('pageerror', e => console.log(`  [pageerr] ${e.message}`));

console.log('▸ navigating…');
await page.goto(URL_ARG, { waitUntil: 'networkidle2', timeout: 30_000 });

// Give the master canvas + assets a moment to load
console.log('▸ warming up (3s for assets)…');
await new Promise(r => setTimeout(r, 3000));

console.log(`▸ recording ${SECONDS}s of loop…`);
// Default protocol message size limits at ~250 MB; we keep blobs under that
// by using FileReader (browser-native, handles large blobs without stack overflow).
const blobBytes = await page.evaluate(async (sec) => {
  if (typeof window.captureLoop !== 'function') {
    throw new Error('window.captureLoop is not exposed by the page');
  }
  const blob = await window.captureLoop(sec);
  return await new Promise((res, rej) => {
    const r = new FileReader();
    r.onload  = () => res(r.result.split(',')[1]);   // strip 'data:video/webm;base64,'
    r.onerror = rej;
    r.readAsDataURL(blob);
  });
}, SECONDS);

await browser.close();

const webm = Buffer.from(blobBytes, 'base64');
const webmPath = OUT_PATH.replace(/\.mp4$/, '.webm');
await writeFile(webmPath, webm);
console.log(`▸ wrote webm: ${webmPath} (${(webm.length / 1024 / 1024).toFixed(1)} MB)`);

console.log('▸ converting webm → mp4 via ffmpeg…');
await new Promise((res, rej) => {
  const proc = spawn(ffmpegPath, [
    '-y',
    '-i', webmPath,
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',         // PowerPoint / QuickTime compat
    '-crf', '18',                   // visually lossless-ish
    '-preset', 'medium',
    '-movflags', '+faststart',      // streaming-friendly mp4
    OUT_PATH,
  ], { stdio: ['ignore', 'inherit', 'inherit'] });
  proc.on('exit', code => code === 0 ? res() : rej(new Error(`ffmpeg exit ${code}`)));
});

console.log(`✓ done → ${OUT_PATH}`);
