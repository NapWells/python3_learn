import random
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from urllib import request
from http import cookiejar


def make_cookie(name, value,domain,path):
    return cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path=path,
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )



def do_crawler(username, password):
    user_agent = r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
    login_page = r'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true'
    user_info_page = "https://www.alimama.com/getLogInfo.htm?callback=__jp0"
    firefoxOptions = webdriver.FirefoxOptions()
    # firefoxOptions.set_headless(True)
    firefoxOptions.add_argument('--user-agent' + user_agent)
    firefoxOptions.add_argument('--proxy-server=http://localhost:8888')
    driverPath = '/Users/lhy/geckodriver'
    driver = webdriver.Firefox(options=firefoxOptions, executable_path=driverPath)
    try:
        driverWait = WebDriverWait(driver=driver, timeout=16)
        driver.get(login_page)
        driver.maximize_window()
        driver.find_element_by_id('J_Quick2Static').click()
        usernameElement = driver.find_element_by_id('TPL_username_1')
        for i in username:
            usernameElement.send_keys(i)
            time.sleep(random.random())
        # passwordElement = driver.find_element_by_id('TPL_password_1')
        # for i in password:
        #     passwordElement.send_keys(i)
        #     time.sleep(random.random())


        reslideTime = 0
        while True:
            passwordElement = driver.find_element_by_id('TPL_password_1')
            passwordElement.clear()
            for i in password:
                passwordElement.send_keys(i)
                time.sleep(random.random())


            if '哎呀，出错了，点击' in driver.page_source:
                print('滑块验证错误')
                driver.find_element_by_css_selector("a[href='javascript:noCaptcha.reset(1)']").click()

            result = driver.find_element_by_id("nc_1_imgCaptcha").get_attribute("style")
            slideText = driver.find_element_by_css_selector("#nc_1__scale_text > span").text

            if result.strip() == '':
                print("不需要滑块")

            if '验证通过' in slideText:
                print("滑块验证通过")

            elif reslideTime == 16:
                print("登陆失败,滑块验证16次未通过")
                return

            elif '请按住滑块，拖动到最右边' in slideText:
                sliderElement = driver.find_element_by_id("nc_1_n1z")
                ActionChains(driver).drag_and_drop_by_offset(sliderElement,440, 0).perform()
                time.sleep(1)
                continue

            driver.find_element_by_id('J_SubmitStatic').click()

            time.sleep(random.random())
            isLogin = False
            errorMessage = ''
            try:
                errorMessage = driver.find_element_by_css_selector('#J_Message > p').text
            except Exception as e:
                isLogin = True

            if errorMessage.strip() == '':
                print('登陆成功，即将获取用户资料')
                break
            else:
                print('登陆失败，{}'.format(errorMessage))


        cj = cookiejar.CookieJar()
        wedriverCookies = driver.get_cookies()
        for webdriverCookie in wedriverCookies:
            cj.set_cookie(make_cookie(webdriverCookie['name'],webdriverCookie['value'],webdriverCookie["domain"],webdriverCookie['path']))
        driver.quit()


        headers = {'user_agent' :user_agent,
                   'accept': r'*/*',
                   'referer': r'https://www.alimama.com/index.htm',
                   'accept-language':'zh-cn'}

        req = request.Request(url=user_info_page,headers=headers)

        cookie_support = request.HTTPCookieProcessor(cj)
        opener = request.build_opener(cookie_support)
        resp = opener.open(req)
        html = resp.read()
        print(html.decode('utf-8'))

    except Exception as e:
        raise (e)
    finally:
        driver.quit()

if __name__ == '__main__':
    do_crawler('18xxxxxxxx', '88***')
