// Screenshot HTML files or URLs to JPG for an approval page.
// usage: node shoot.js jobs.json    jobs: [{"src": "path/or/https://...", "out": "shots/x.jpg", "width": 640, "height": 900, "full": true, "scale": 1.5}]
// Waits for every image, retries up to three times when one fails (sandbox proxies drop connections), ignores the
// sandbox's own TLS interception. Set NODE_PATH to the global node_modules that holds playwright.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const exe = fs.existsSync('/opt/pw-browsers/chromium') ? '/opt/pw-browsers/chromium' : undefined;
  const browser = await chromium.launch(exe ? { executablePath: exe } : {});
  for (const j of jobs) {
    const url = /^https?:/.test(j.src) ? j.src : 'file://' + path.resolve(j.src);
    let broken = [];
    for (let t = 0; t < (j.tries || 3); t++) {
      const ctx = await browser.newContext({ viewport: { width: j.width || 1280, height: j.height || 900 }, deviceScaleFactor: j.scale || 1.5, ignoreHTTPSErrors: true });
      const p = await ctx.newPage();
      await p.goto(url, { waitUntil: 'load', timeout: 60000 }).catch(() => {});
      await p.waitForFunction(() => [...document.images].every(i => i.complete), null, { timeout: 30000 }).catch(() => {});
      await p.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
      await p.waitForTimeout(j.wait || 500);
      broken = await p.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src.slice(0, 90)));
      fs.mkdirSync(path.dirname(j.out), { recursive: true });
      await p.screenshot({ path: j.out, fullPage: j.full !== false, type: 'jpeg', quality: j.quality || 72 });
      await ctx.close();
      if (!broken.length) break;
    }
    console.log(j.out, broken.length ? 'MISSING IMAGES ' + broken.join(' ') : 'ok');
  }
  await browser.close();
})();
