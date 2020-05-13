from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


class SeleniumService(object):
    '''
    重新封装selenium
    '''

    def __init__(self) -> None:
        """
        初始化驱动，以及一些参数的调用
        """
        # 设置浏览器参数
        options = ChromeOptions()

        # 不加载图片, 提升速度
        # options.add_argument('blink-settings=imagesEnabled=false')

        # 以最高权限运行
        options.add_argument('--no-sandbox')

        # 设置开发者模式启动，该模式下webdriver属性为正常值
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        # options.add_argument('--headless')

        # 开启后提高浏览器访问性能
        options.add_argument('--disable-gpu')

        # 禁用浏览器弹窗
        prefs = {
            'profile.default_content_setting_values': {
                'notifications': 2
            },
        }
        options.add_experimental_option('prefs', prefs)

        # 设置手机模式
        WIDTH = 320
        HEIGHT = 640
        PIXEL_RATIO = 3.0
        UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'
        mobileEmulation = {
            'deviceMetrics': {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO},
            'userAgent': UA
        }
        options.add_experimental_option('mobileEmulation', mobileEmulation)

        # 设置页面无需加载完成，即可访问元素
        caps = DesiredCapabilities.CHROME
        caps["pageLoadStrategy"] = 'none'

        # 创建驱动
        self.driver = Chrome(chrome_options=options, desired_capabilities=caps)

        # 设置窗口最大化
        self.driver.maximize_window()

        # 绕过反爬验证
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })

    def open_url(self, url):
        """
        请求访问的页面
        :param url:
        :return: None
        """
        self.driver.get('about:blank')
        self.driver.get(url)
        return self

    def find_element_by_xpath(self, element: WebElement, xpath: str, timeout: int) -> WebElement:
        """
        element 通过Xpath查找元素目标
        :param element: Parent element
        :param xpath: 目标的xpath
        :param timeout: 超时时间
        :return: 目标元素
        """
        for i in range(timeout):
            try:
                self.scroll_bottom()
                self.scroll_top()
                if isinstance(element, WebElement):
                    ele: WebElement = element.find_element_by_xpath(xpath)
                else:
                    ele: WebElement = self.driver.find_element_by_xpath(xpath)
                return ele
            except:
                pass
            time.sleep(1)
        raise TimeoutError

    def find_element_list_by_xpath(self, element: WebElement, xpath: str, timeout: int) -> list:
        """
        element 通过Xpath查找元素目标
        :param ele: Parent element
        :param xpath: 目标的xpath
        :param timeout: 超时时间
        :return: 目标元素List
        """
        for i in range(timeout):
            try:
                self.scroll_bottom()
                self.scroll_top()
                if isinstance(element, WebElement):
                    element_list: list = element.find_elements_by_xpath(xpath)
                else:
                    element_list: list = self.driver.find_elements_by_xpath(xpath)
                if element_list.__len__() > 0:
                    return element_list
            except:
                pass
            time.sleep(1)
        raise TimeoutError

    def scroll_bottom(self):
        """
        滚动到最底端
        :return: None
        """
        js = 'var q=document.documentElement.scrollTop=100000'
        self.driver.execute_script(js)
        return self

    def scroll_top(self):
        """
        滚动到最顶端
        :return: None
        """
        js = 'var q=document.documentElement.scrollTop=0'
        self.driver.execute_script(js)
        return self

    def click(self, element: WebElement, timeout: int):
        """
        点击元素
        :param element: 点击的元素
        :param timeout: 超时时间
        :return: None
        """
        for i in range(timeout):
            try:
                element.click()
                return self
            except Exception:
                pass
            time.sleep(1)
        raise TimeoutError

    def send_key(self, element: WebElement, text: str, timeout: int):
        """
        对目标元素输入文本信息
        :param element: 目标元素
        :param text: 文本信息
        :param timeout:  超时时间
        :return: None
        """
        for i in range(timeout):
            try:
                element.clear()
                element.send_keys(text)
                return self
            except Exception:
                pass
            time.sleep(1)
        raise TimeoutError

    def close(self):
        if self.driver != None:
            self.driver.quit()
