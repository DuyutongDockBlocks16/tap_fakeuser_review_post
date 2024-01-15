const puppeteer = require('puppeteer');
const fs = require('fs');
const fspromises = require('fs').promises;

function sleep(delay) {
	return new Promise((resolve, reject) => {
		setTimeout(() => {
			try {
				resolve(1)
			} catch (e) {
				reject(0)
			}
		}, delay)
	})
}

function writeerremail(strerr){
   const fd = fs.openSync("./errlog/errlog.txt", "a+")
   fs.writeSync(fd, strerr, 'utf8');
   fs.writeSync(fd, "\n", 'utf8');

   fs.closeSync(fd);
}

(async () => {
  var {program} = require('commander');
  program.option('-i, --index_num <index>', '文件编号');
  program.parse(process.argv);
  var options = program.opts();
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0');

  await page.goto('https://www.taptap.com/');
  await sleep(2000)

  const cookies = await fs.readFileSync('./datajson/set_cookies_'+ options.index_num +'.json', 'utf8')
  const deserializedCookies = JSON.parse(cookies)
  await page.setCookie(...deserializedCookies)

  await page.goto('https://www.taptap.com/profile')
  await sleep(2000)

   const cookies2 = await page.cookies();
   await fspromises.writeFile('./datajson/cookies_taplogin_'+ options.index_num +'.json', JSON.stringify(cookies2, null, 2));

   await browser.close();
})();
