import time, traceback, timeit
from selenium.webdriver.support.ui import Select

url = 'http://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
#url2 = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx'

class worker:
    def __init__(self, thread, d, p, subs):
        self.thread = thread        
        self.driver = d
        self.post = p
        self.subjects = subs

    def startTheWork(self, rollToCrawl):        
        finalData = []
        errorRoll = []
        avgTime = 0
        for a in rollToCrawl:
            start_time = timeit.default_timer()
            try:
                print("Thread " + str(self.thread) + ", Getting " + str(a) + ", Avg Time = " + str(avgTime) + "s")
                self.driver.get(url)
                time.sleep(2)
                g,s,t = self.fetchMarks(a)

                stu = [g["rollNo"], g["name"], g["regnNo"], g["supply"], t["SGPA"], t["CGPA"]]
                for i in s:
                    stu.append(s[i]["credits"])
                    stu.append(s[i]["grade"])
                    stu.append(s[i]["gradePoint"])
                stu.extend([t["gradpoint"], t["credsEar"], t["credsReg"]])

                finalData.append(stu)        

            except Exception as e:                    
                #print(traceback.format_exc())
                print("Unable to fetch " + str(a))
                errorRoll.append(a)
                finalData.append([a, "N/A"])
            avgTime = (avgTime + (timeit.default_timer() - start_time))/2
            
                
        self.driver.close()
        return [self.thread, finalData, errorRoll]        

    def fetchMarks(self, RollNo):
        for i in self.post:
            Select(self.driver.find_element_by_id(i)).select_by_value(self.post[i])
            time.sleep(2)

        self.driver.find_element_by_id("textboxRno").send_keys(RollNo)
        time.sleep(1)
        self.driver.find_element_by_id('buttonShowResult').click()
        time.sleep(3)

        theGeneralData = {
            'rollNo' : '',
            'regnNo' : '',
            'name' : '',
            'supply': ''
        }

        subjectData = {}
        for i in self.subjects:
            subjectData[i] = {'credits' : '', 'grade' : '', 'gradePoint': ''}        

        totals = {
            'gradpoint' : '',
            'credsReg' : '',
            'credsEar' : '',
            'SGPA' : '',
            'CGPA' : '',
        }
        
        theGeneralData['rollNo']    = (self.driver.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[4]/td[1]").text).replace('Roll No. ', '')
        theGeneralData['regnNo']    = (self.driver.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[4]/td[2]").text).replace('Registration No. ', '')
        theGeneralData['name']      = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[5]/td[1]/b[1]").text
        theGeneralData['supply']    = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[5]/td[2]/b[1]").text
        

        ini_row = 2
        ini_col = 6
        for i in subjectData:
            subjectData[i]["credits"]      = self.driver.find_element_by_xpath("//*[@id='GridPrintNetResult']/tbody/tr["+ str(ini_row) +"]/td["+ str(ini_col) +"]").text
            subjectData[i]["grade"]        = self.driver.find_element_by_xpath("//*[@id='GridPrintNetResult']/tbody/tr["+ str(ini_row) +"]/td["+ str(ini_col + 1) +"]").text
            subjectData[i]["gradePoint"]   = self.driver.find_element_by_xpath("//*[@id='GridPrintNetResult']/tbody/tr["+ str(ini_row) +"]/td["+ str(ini_col + 2) +"]").text
            ini_row += 1
        
        totals['gradpoint'] = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[1]/td[4]/b").text
        totals['credsReg']  = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[1]/td[2]/centre/b").text
        totals['credsEar']  = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[2]/td[2]/centre/b").text
        totals['SGPA']      = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[3]/td[2]/centre/b").text
        totals['CGPA']      = self.driver.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[4]/td[2]/centre/b").text

        return theGeneralData, subjectData, totals