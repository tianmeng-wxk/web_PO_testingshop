from HTMLTestRunner import HTMLTestRunner
import unittest,os,time
from test_case.test_cases import TestCase
from datetime import datetime
from common.common import send_mail


# path = curPath+"../../test_case"
# discover = unittest.defaultTestLoader.discover(start_dir=path, pattern="read_*.py")#在path目录下运行以read开头的文件,运行discover

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    report_path = "../config/report/"
    #report_file = report_path+"{}_html_report.html".format(time.strftime("%Y_%m_%d %H-%M-%S",time.localtime()))
    time = datetime.now()
    now = time.strftime('%Y-%m-%d  %H-%M-%S')
    report_file = report_path + now + "_html_report.html"
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    else:
        pass

    with open(report_file, 'wb')as file:
        runner = HTMLTestRunner(stream=file, verbosity=2, title="特斯汀商城web测试", description="特斯汀商城web测试")
        runner.run(suite)

    send_mail(report_file)
if __name__ == '__main__':
    suite()