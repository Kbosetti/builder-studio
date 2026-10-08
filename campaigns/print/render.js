// Render print pieces: PNG at print resolution, plus PDF at the trim size when one is given.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: j.scale });
    await page.goto('file://' + j.html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(300);
    await page.screenshot({ path: j.png });
    if (j.pdf) await page.pdf({ path: j.pdf, width: j.pw, height: j.ph, printBackground: true, pageRanges: '1' });
    await page.close();
  }
  await browser.close();
})();
