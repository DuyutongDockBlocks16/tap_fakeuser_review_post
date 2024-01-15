const puppeteer = require('puppeteer');
const fs = require('fs')
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

(async () => {
  var {program} = require('commander');
  program.option('-i, --index_num <index>', '文件编号');
  program.parse(process.argv);
  var options = program.opts();
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0');
  await page.goto('https://accounts.taptap.com/login?type=email');

  await sleep(1000)

  const searchinput = await page.$("input");
   if(null == searchinput)
  {
     console.log("没有找到input控件");
     await browser.close();
     return
  }
  await searchinput.focus();

  const userinfo = fs.readFileSync('./initdata/user_info_json/userinfo_'+ options.index_num +'.json', 'utf8')
  const jsonuser = JSON.parse(userinfo)
  await page.keyboard.type(jsonuser['email']);

  const checkbtn = await page.$(".check-terms__text");
  await checkbtn.click();

  const clickbtn = await page.$("button");
  await clickbtn.click();

  await sleep(2000)

  await page.screenshot({ path: './img/example.png' });

  const cookies = await page.cookies();
  await fspromises.writeFile('./datajson/codecookies_'+ options.index_num +'.json', JSON.stringify(cookies, null, 2));

  await browser.close();
})();
