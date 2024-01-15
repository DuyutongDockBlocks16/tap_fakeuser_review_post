const puppeteer = require('puppeteer');
const fs = require('fs');

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
  const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0');

  await page.goto('https://www.taptap.com/');
  await sleep(2000)

  const cookies = await fs.readFileSync('./datajson/set_cookies.json', 'utf8')
  const deserializedCookies = JSON.parse(cookies)
  await page.setCookie(...deserializedCookies)

  await page.goto('https://www.taptap.com/profile')
  await sleep(2000)
  await page.screenshot({ path: './img/example_profile.png' });
  await page.goto('https://www.taptap.com/user-certification/idcard');

  const userinfo = fs.readFileSync('./initdata/userinfo.json', 'utf8')
  const jsonuser = JSON.parse(userinfo)

  const searchinput = await page.$("#real-name");
  if(null == searchinput)
  {
     console.log("没有找到name控件，应该是已经设置过身份:" + jsonuser['email']);
     await writeerremail("没有找到name控件，应该是已经设置过身份:" + jsonuser['email'])
     await browser.close();
     return
  }
  await searchinput.focus();
  await page.keyboard.type(jsonuser['name']);

   const searchinput2 = await page.$("#idcard-number");
   if(null == searchinput2)
  {
     console.log("没有找到idcard控件");
     await browser.close();
     return
  }
   await searchinput2.focus();
   await page.keyboard.type(jsonuser['idcard']);

   const clickbtn = await page.$("#verify-submit");
   await clickbtn.click();

   await sleep(1000)

   await page.screenshot({ path: './img/example_card.png' });

   const realname = await page.$("#real-name");
   if(null == realname)
   {
      console.log("身份已经成功设置!" + jsonuser['email'])
      await writeerremail("身份已经成功设置!" + jsonuser['email'])
   }
   else
   {
      console.log("身份设置失败!" + jsonuser['email'])
      await writeerremail("身份设置失败!" + jsonuser['email'])
   }

   await browser.close();
})();
