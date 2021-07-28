import requests, sys, time, timeit, traceback
from seleniumManager.manager import Manager
from sheets_api_v5 import googleAPI
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

class misc:
    def __init__(self):
        pass

    def getViewState(self, formUrl, postData):
        try:
            si = Manager(r'chromedriver.exe')
            d = si.driver()
            d.get(formUrl)
            time.sleep(3)
            for i in postData:
                Select(d.find_element_by_id(i)).select_by_value(postData[i])
                time.sleep(2)
            
            vs = d.find_element_by_id("__VIEWSTATE").get_attribute("value")
            d.close()
            return vs  
        except Exception as e:
            print(e)
            sys.exit("could not get ViewState, please try again")

    def uploadToGoogle(self, sData, sheetTitle, listOfSubjects, oldSheet = False):
        try:            
            if(not oldSheet):
                api = googleAPI("")
                api.connectToGoogle()
                api.setSheet(api.createSpreadsheet(sheetTitle))
                sName = "Sheet1"
            else:
                api = googleAPI(oldSheet, sheetTitle)
                api.connectToGoogle()
                api.setGid(api.add_sheet(sheetTitle))
                sName = sheetTitle

            row1 = ["Roll No.", "Name", "Registration Number", "Supply", "SGPA", "CGPA"]
            row2 = ["", "", "", "", "", ""]
            for i in listOfSubjects:
                row1.extend(["", i, ""])
                row2.extend(["Credits", "Grade", "Grade Point"])
            row1.extend(["Grade Point Total", "Credits Earned", "Total Credits"])
            row2.extend(["", "", ""])

            finData = [
                row1,
                row2,
            ]
            finData.extend(sData)
            api.updateSheet("'"+sName+"'!A1:" + api.getLetter(len(row1) - 1) + str(len(finData)), finData)
            return True
        except:
            return False

class worker:
    def __init__(self, thread, subjects, postData, viewState, doCount):
        self.thread = thread
        self.subjects = subjects
        self.postData = postData
        self.viewState = viewState
        self.doCount = doCount

    def startTheWork(self, rollToCrawl):
        finalData = []
        errorRoll = []        
        for a in rollToCrawl:            
            try:                
                #print("Thread " + str(self.thread) + ", Getting " + str(a))

                headers = {
                    "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                }
                sess = requests.session()
                sess.headers.update(headers)

                g,s,t = self.fetchMarks(a, sess)

                stu = [g["rollNo"], g["name"], g["regnNo"], g["supply"], t["SGPA"], t["CGPA"]]
                for i in s:
                    stu.append(s[i]["credits"])
                    stu.append(s[i]["grade"])
                    stu.append(s[i]["gradePoint"])
                stu.extend([t["gradpoint"], t["credsEar"], t["credsReg"]])

                finalData.append(stu)                

            except Exception as e:                    
                #print(traceback.format_exc())
                #print("Unable to fetch " + str(a))
                errorRoll.append(a)
                finalData.append([a, "N/A"])
            
            self.doCount()
                
        return [self.thread, finalData, errorRoll]

    def fetchMarks(self, RollNo, session):
        data = {
                'textboxRno': RollNo,
                'buttonShowResult': 'Submit',

                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': self.viewState,
                '__VIEWSTATEGENERATOR': '72A7EE3D',
        }

        newData = self.postData | data
        r = session.post('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx', data=newData)
        r = session.get('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx')

        soup = BeautifulSoup(r.text, features="lxml")
        b = soup.select('#form1')[0]
        table2 = b.find_all("table")[1]
        table3 = b.find_all("table")[2]

        tab2_tr = table2.find_all("tr")
        tab3_tr = table3.find_all("tr")

        theGeneralData = {}

        theGeneralData['rollNo'] = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(1) > td:nth-child(1) > b:nth-child(1)')[0].getText()
        theGeneralData['regnNo'] = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)')[0].getText()
        theGeneralData['name']   = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > b:nth-child(2)')[0].getText()
        theGeneralData['supply'] = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > b:nth-child(1)')[0].getText()

        totals = {}
        totals['credsReg'] = tab3_tr[0].find_all("td")[1].find_all("b")[0].text
        totals['gradpoint']  = tab3_tr[0].find_all("td")[3].find_all("b")[0].text
        totals['credsEar']  = tab3_tr[1].find_all("td")[1].find_all("b")[0].text
        totals['SGPA']      = tab3_tr[2].find_all("td")[1].find_all("b")[0].text
        totals['CGPA']      = tab3_tr[3].find_all("td")[1].find_all("b")[0].text
        
        subjectData = {}
        for i in self.subjects:
            subjectData[i] = {'credits' : '', 'grade' : '', 'gradePoint': ''}  
            
        a = 0
        for i in subjectData:
            subjectData[i]["credits"]      = tab2_tr[a+1].find_all("td")[5].getText().strip()
            subjectData[i]["grade"]        = tab2_tr[a+1].find_all("td")[6].getText().strip()
            subjectData[i]["gradePoint"]   = tab2_tr[a+1].find_all("td")[7].getText().strip()
            a += 1

        return theGeneralData, subjectData, totals