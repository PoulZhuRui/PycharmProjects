import os
import unittest
from commonfile.Log import MyLog as Log
import readConfig as readconfig
from HTMLTestRunner import HTMLTestRunner
from commonfile.configEmail import MyEmail

local_readconfig = readconfig.ReadCaonfig()


class ALLTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = local_readconfig.get_email("on_off")
        self.caseListFile = os.path.join(readconfig.absolute_path, "caselist.txt")
        print(self.caseListFile)
        self.caseFile = os.path.join(readconfig.absolute_path, "testcase\\user")

        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != "" and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
                print(self.caseList)
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print(case_name + ".py")
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + ".py", top_level_dir= None)
            print(discover)
            suite_module.append(discover)
            print(suite_module)
        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()
            if suit is not None:
                logger.info("___________test start_______________")
                fp = open(resultPath, "wb")
                runner = HTMLTestRunner(stream = fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("_____________________test_ end__________________")
            fp.close()

            if on_off == "on":
                self.email.send_email()
            elif on_off == "off":
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = ALLTest()
    obj.run()