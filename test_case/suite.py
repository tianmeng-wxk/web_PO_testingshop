from HTMLTestRunner import HTMLTestRunner
import unittest,os,time
from test_case.test_cases import TestCase
#curPath = os.path.abspath(os.path.dirname(__file__))

# path = curPath+"../../test_case"
# discover = unittest.defaultTestLoader.discover(start_dir=path, pattern="read_*.py")#在path目录下运行以read开头的文件,运行discover

suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
report_path = "../config/report/"
report_file = report_path+"{}_html_report.html".format(time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime()))
if not os.path.exists(report_path):
    os.mkdir(report_path)
else:
    pass

with open(report_file, 'wb')as file:
    runner = HTMLTestRunner(stream=file, title="特斯汀商城測試報告", description="特斯汀商城web测试")
    runner.run(suite)