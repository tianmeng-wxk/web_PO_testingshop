import pytest
#pytest.main(["-s","-vv","../../testingshop","--html=../config/report/pytest_report.html"])
#"--maxfail=1","-n=2"

#生成allure测试报告
pytest.main(['-s','-q','./test_cases.py','--alluredir','../config/report/xml'])
#命令行
#allure generate --clean ../config/report/xml/ -o ../config/report/allure_html