const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage(); await p.goto('file://' + __dirname + '/card.html');
  for (const k of process.argv.slice(2)) {
    const r = await p.evaluate(o => make(o), { src: 'card_' + k + '.png', bbox: [386, 821, 704, 992], color: '#2b6d47', bg: 'rgb(249,247,241)' });
    fs.writeFileSync(__dirname + '/card_' + k + '_new.png', Buffer.from(r.url.split(',')[1], 'base64'));
    console.log(k, Math.round(r.size)); }
  await b.close(); })();
