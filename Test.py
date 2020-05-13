from service.SeleniumService import SeleniumService
import time
if __name__ == '__main__':
    username = '18701312110'
    password = 'fcj1314.'
    # 加载服务
    ss = SeleniumService()
    # 打开浏览器登录
    ss.open_url('https://login.m.taobao.com/login.htm')
    # 获取登录信息
    username_ele = ss.find_element_by_xpath(None, "//input[@name='fm-login-id']", 30)
    password_ele = ss.find_element_by_xpath(None, "//input[@name='fm-login-password']", 30)
    login_btn_ele = ss.find_element_by_xpath(None, "//button[contains(text(),'登录')]", 30)
    # 开始操作
    ss.send_key(username_ele, username, 10)
    ss.send_key(password_ele, password, 10)
    ss.click(login_btn_ele, 10)

    time.time(3600)
    ss.close()
