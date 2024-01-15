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

(async () => {
  var {program} = require('commander');
  program.option('-i, --index_num <index>', '文件编号');
  program.parse(process.argv);
  var options = program.opts();
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0');

  await page.goto('https://email.163.com');
  await sleep(2000);

  const userinfo = fs.readFileSync('./initdata/user_info_json/userinfo_'+ options.index_num +'.json', 'utf8');
  const jsonuser = JSON.parse(userinfo);

  const frames = await page.frames();
  var frame = null;
  for( var i of frames)
  {
      if(await i.title() ==='URS组件')
      {
         frame = i;
      }
  }

  const inputfirst = await frame.$("[ name=\"email\"]");
  if(null == inputfirst)
  {
     console.log("没有找到emailadress控件:" + jsonuser['email']);
     await browser.close();
     return
  }
  await inputfirst.focus();

  var emailadress = jsonuser['email'];
  const n = emailadress.indexOf("@");
  const email = emailadress.substring(0, n);
  await page.keyboard.type(email);

  const inputsecond = await frame.$("[name=\"password\"]");
  if(null == inputsecond)
  {
     console.log("没有找到emailpass控件" );
     await browser.close();
     return
  }
  await inputsecond.focus();
  await page.keyboard.type(jsonuser['password']);

  const clickbtn = await frame.$("#dologin");
  if(null == clickbtn)
  {
     console.log("没有找到clickbtn控件" );
     await browser.close();
     return
  }
  await clickbtn.click();

  await sleep(2000);

  await page.screenshot({ path: './img/emailinput.png' });

  const cookies = await page.cookies();
  await fspromises.writeFile('./datajson/cookies_email_'+ options.index_num +'.json', JSON.stringify(cookies, null, 2));

  await browser.close();
})();