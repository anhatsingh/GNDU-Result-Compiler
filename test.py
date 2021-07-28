import time, traceback
from seleniumManager.manager import Manager
from selenium.webdriver.support.ui import Select
from sheets_api_v3 import googleAPI

startRoll = 17022000300
totalStu = 51
p = { #post data
        'DrpDwnYear': '2020',
        'DrpDwnMonth': '12',
        'DropDownCourseType': 'C',
        'DrpDwnCMaster': '1702', #change course here
        'DrpDwnCdetail': '170201',    #change semester here
    }

url = 'http://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
#url2 = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx'

si = Manager(r'chromedriver.exe')
d, k = si.driver(), si.getKeys()

def fetchMarks(RollNo):
    for i in p:
        Select(d.find_element_by_id(i)).select_by_value(p[i])
        time.sleep(2)

    d.find_element_by_id("textboxRno").send_keys(RollNo)
    time.sleep(1)
    d.find_element_by_id('buttonShowResult').click()
    time.sleep(3)

    theGeneralData = {
        'rollNo' : '',
        'regnNo' : '',
        'name' : '',
        'supply': ''
    }

    subjects = {
        'mech' : {'credits' : '', 'grade' : '', 'gradePoint': ''},
        'egd' : {'credits' : '', 'grade' : '', 'gradePoint': ''},
        'phy' : {'credits' : '', 'grade' : '', 'gradePoint': ''},
        'math' : {'credits' : '', 'grade' : '', 'gradePoint': ''},
        'mater' : {'credits' : '', 'grade' : '', 'gradePoint': ''},
        'pbi' : {'credits' : '', 'grade' : '', 'gradePoint': ''},
        'drug' : {'credits' : '', 'grade' : '', 'gradePoint': ''}
    }

    totals = {
        'gradpoint' : '',
        'credsReg' : '',
        'credsEar' : '',
        'SGPA' : '',
        'CGPA' : '',
    }
    
    theGeneralData['rollNo']    = (d.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[4]/td[1]").text).replace('Roll No. ', '')
    theGeneralData['regnNo']    = (d.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[4]/td[2]").text).replace('Registration No. ', '')
    theGeneralData['name']      = d.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[5]/td[1]/b[1]").text
    theGeneralData['supply']    = d.find_element_by_xpath("//*[@id='form1']/center/table[1]/tbody/tr[5]/td[2]/b[1]").text
    

    ini_row = 2
    ini_col = 6
    for i in subjects:
        subjects[i]["credits"]      = d.find_element_by_xpath("//*[@id='GridPrintNetResult']/tbody/tr["+ str(ini_row) +"]/td["+ str(ini_col) +"]").text
        subjects[i]["grade"]        = d.find_element_by_xpath("//*[@id='GridPrintNetResult']/tbody/tr["+ str(ini_row) +"]/td["+ str(ini_col + 1) +"]").text
        subjects[i]["gradePoint"]   = d.find_element_by_xpath("//*[@id='GridPrintNetResult']/tbody/tr["+ str(ini_row) +"]/td["+ str(ini_col + 2) +"]").text
        ini_row += 1
    
    totals['gradpoint'] = d.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[1]/td[4]/b").text
    totals['credsReg']  = d.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[1]/td[2]/centre/b").text
    totals['credsEar']  = d.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[2]/td[2]/centre/b").text
    totals['SGPA']      = d.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[3]/td[2]/centre/b").text
    totals['CGPA']      = d.find_element_by_xpath("//*[@id='form1']/center/table[2]/tbody/tr[4]/td[2]/centre/b").text

    return theGeneralData, subjects, totals

def uploadToGoogle(sData):
    api = googleAPI("")    
    api.connectToGoogle()
    api.setSheet(api.createSpreadsheet("Result_1 Sem_C Section"))    

    finData = [
        ["Roll No.", "Name", "Registration Number", "Supply", "", "Mechanics", "", "", "EGD", "", "", "Physics", "", "", "Maths", "", "", "Material", "", "", "Punjabi", "", "", "Drug Abuse", "", "Grade Point Total", "Credits Earned", "Total Credits", "SGPA", "CGPA"],
        ["", "", "", "", "Credits", "Grade", "Grade Point", "Credits", "Grade", "Grade Point", "Credits", "Grade", "Grade Point", "Credits", "Grade", "Grade Point", "Credits", "Grade", "Grade Point", "Credits", "Grade", "Grade Point", "Credits", "Grade", "Grade Point", "", "", "", "", ""]
    ]
    finData.extend(sData)
    cellsAffected = api.updateSheet("Sheet1!A1:AD"+ str(len(finData)), finData)

finalData = []
errorRoll = []
firstRoll = startRoll
for a in range(1, totalStu + 1):
    try:
        print("Getting " + str(firstRoll + a))
        d.get(url)
        time.sleep(2)
        g,s,t = fetchMarks(firstRoll + a)
        stu = [
            g["rollNo"], g["name"], g["regnNo"], g["supply"],

            s["mech"]["credits"], s["mech"]["grade"], s["mech"]["gradePoint"],
            s["egd"]["credits"], s["egd"]["grade"], s["egd"]["gradePoint"],
            s["phy"]["credits"], s["phy"]["grade"], s["phy"]["gradePoint"],
            s["math"]["credits"], s["math"]["grade"], s["math"]["gradePoint"],
            s["mater"]["credits"], s["mater"]["grade"], s["mater"]["gradePoint"],
            s["pbi"]["credits"], s["pbi"]["grade"], s["pbi"]["gradePoint"],
            s["drug"]["credits"], s["drug"]["grade"], s["drug"]["gradePoint"],

            t["gradpoint"], t["credsEar"], t["credsReg"], t["SGPA"], t["CGPA"]
            ]
        finalData.append(stu)        

    except Exception as e:                    
        print(traceback.format_exc())
        errorRoll.append(firstRoll + a)
        finalData.append([firstRoll + a, "N/A"])

uploadToGoogle(finalData)
print("Errors: ")
print(errorRoll)
print("Done")
d.close()