from PIL import Image
import requests,logging,time
import yaml,xlrd,smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from Chaojiying_Python.chaojiying import Chaojiying_Client
#第三方接口识别验证码方法一
def ivercode(driver):
    driver.save_screenshot("../vercode_img/page.png")
    vcode = driver.find_element_by_xpath("//*[@id='verify_code_img']")
    loc = vcode.location
    size = vcode.size
    left = loc['x']
    top = loc['y']
    right = (loc['x'] + size['width'])
    button = (loc['y'] + size['height'])
    page_pic = Image.open("../vercode_img/page.png")
    v_code_pic = page_pic.crop((left, top, right, button))
    v_code_pic.save("../vercode_img/vercode.png")
    chaojiying = Chaojiying_Client('qq121292679', 'a546245426', '904603')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('../vercode_img/vercode.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    res = chaojiying.PostPic(im, 1902)
    vercode = res['pic_str']
    return vercode

#第三方接口识别验证码方法二
def ivercode2(driver):
    ele = driver.find_element_by_xpath("//*[@id='verify_code_img']")
    ele.screenshot("../vercode_img/verify.png")
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }
    data = {
        'user': 'wuqingfqng',
        'pass2': '6e8ebd2e301f3d5331e1e230ff3f3ca5',#密碼：wuqing&fqng
        "softid": "904357",
        "codetype": "1902"
    }
    userfile = open("../vercode_img/verify.png", "rb").read()
    userfile = {"userfile": ("../vercode_img/verify.png", userfile)}
    res = requests.post("http://upload.chaojiying.net/Upload/Processing.php",data=data, files=userfile, headers=headers)
    res = res.json()
    vercode = res["pic_str"]
    return vercode


def read_yaml(file_path):
    file = open(file_path, encoding='utf-8')
    testdata = yaml.load(file, Loader=yaml.FullLoader)  # 或者yaml.full_load()
    return testdata



class ReadExcel:
    def __init__(self, excel_path, sheet_name):
        self.workbook = xlrd.open_workbook(excel_path)
        self.worksheet = self.workbook.sheet_by_name(sheet_name)
        self.rownum = self.worksheet.nrows
        self.colnum = self.worksheet.ncols

    def dict_data(self):
        if self.rownum <= 1:
             print("表格行数小于等于1，不能进行自动化")
        else:
             list = []
             self.headers = self.worksheet.row_values(0)
             #self.headers = self.worksheet.row_values(0)
             #j = 1#从1开始
             for i in range(1, self.rownum):
                 s = {}
                 values = self.worksheet.row_values(i)

                 for x in range(self.colnum):
                    s[self.headers[x]] = values[x]
                 list.append(s)
                 #j += 1
             return list


class Logger:
    def log(self):

        logger=logging.getLogger("logger")
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            sh = logging.StreamHandler()
            fh=logging.FileHandler(filename="../config/log/{}_log".format(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())),encoding="utf-8")
            formator=logging.Formatter(fmt="%(asctime)s %(filename)s %(levelname)s %(msg)s", datefmt="%Y-%m-%d %X")
            sh.setFormatter(formator)
            fh.setFormatter(formator)
            logger.addHandler(fh)
            logger.addHandler(sh)
        return logger



def browser_type(type):
    type=type.upper()
    if type == "CHR":
        driver = webdriver.Chrome()
    elif type == "IE":
        driver = webdriver.Ie()
    elif type == "FF":
        driver = webdriver.Firefox()
    return driver


def send_mail(email_path):
    with open(email_path, 'rb') as f:
        content = f.read()
    host = "smtp.qq.com"
    port = 587
    sender = "3394788013@qq.com"
    password = "lizceyidpekpdbhd"
    receiver = "tianmeng_wxk@163.com"
    message = MIMEText(content, "HTML", "UTF-8")
    message["Subject"] = "shopxo商城web自动化测试"
    message["From"] = sender
    message["To"] = receiver
    try:
        smtp = smtplib.SMTP(host, port)
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, message.as_string())
        Logger().log().info("发送邮件成功")
    except smtplib.SMTPException as e:
        Logger().log().info("发送邮件失败，失败信息：{}".format(e))







