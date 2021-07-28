import requests, sys, time, timeit, traceback
from seleniumManager.manager import Manager
from sheets_api_v5 import GoogleAPI
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

class misc:
    def __init__(self):
        pass

    def get_view_state(self, gndu_url_form, data_to_send):
        try:
            selenium_instance = Manager(r'chromedriver.exe')
            driver = selenium_instance.driver()
            driver.get(gndu_url_form)
            time.sleep(3)
            for i in data_to_send:
                Select(driver.find_element_by_id(i)).select_by_value(data_to_send[i])
                time.sleep(2)
            
            view_state_string = driver.find_element_by_id("__view_state").get_attribute("value")
            driver.close()
            return view_state_string
        except Exception as e:
            print(e)
            sys.exit("could not get view_state, please try again")

    def upload_to_google_sheets(self, data_to_upload, google_sheet_title, subjects, old_sheet_id = False):
        try:            
            if(not old_sheet_id):
                api = GoogleAPI("")
                api.connect_to_google()
                api.setSheet(api.create_spreadsheet(google_sheet_title))
                sheet_title = "Sheet1"
            else:
                api = GoogleAPI(old_sheet_id, google_sheet_title)
                api.connect_to_google()
                api.setGid(api.add_sheet(google_sheet_title))
                sheet_title = google_sheet_title

            row1 = ["Roll No.", "Name", "Registration Number", "Supply", "SGPA", "CGPA"]
            row2 = ["", "", "", "", "", ""]
            for i in subjects:
                row1.extend(["", i, ""])
                row2.extend(["Credits", "Grade", "Grade Point"])
            row1.extend(["Grade Point Total", "Credits Earned", "Total Credits"])
            row2.extend(["", "", ""])

            final_data_to_upload = [
                row1,
                row2,
            ]
            final_data_to_upload.extend(data_to_upload)
            api.update_sheet("'"+sheet_title+"'!A1:" + api.get_column_letter(len(row1) - 1) + str(len(final_data_to_upload)), final_data_to_upload)
            return True
        except:
            return False

class worker:
    def __init__(self, thread, subjects, data_to_send, view_state, count_roll):
        self.thread = thread
        self.subjects = subjects
        self.data_to_send = data_to_send
        self.view_state = view_state
        self.count_roll = count_roll

    def startTheWork(self, roll_nums):
        final_data_of_thread = []
        roll_num_not_found = []        
        for a in roll_nums:            
            try:                
                #print("Thread " + str(self.thread) + ", Getting " + str(a))

                headers = {
                    "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
                }
                sess = requests.session()
                sess.headers.update(headers)

                general,subject_data, totals = self.get_marks_single(a, sess)

                stu = [general["rollNo"], general["name"], general["regnNo"], general["supply"], totals["SGPA"], totals["CGPA"]]
                for i in subject_data:
                    stu.append(subject_data[i]["credits"])
                    stu.append(subject_data[i]["grade"])
                    stu.append(subject_data[i]["gradePoint"])
                stu.extend([totals["gradpoint"], totals["credsEar"], totals["credsReg"]])

                final_data_of_thread.append(stu)                

            except Exception as e:                    
                #print(traceback.format_exc())
                #print("Unable to fetch " + str(a))
                roll_num_not_found.append(a)
                final_data_of_thread.append([a, "N/A"])
            
            self.count_roll()
                
        return [self.thread, final_data_of_thread, roll_num_not_found]

    def get_marks_single(self, roll_num, session):
        data = {
                'textboxRno': roll_num,
                'buttonShowResult': 'Submit',

                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__view_state': self.view_state,
                '__view_stateGENERATOR': '72A7EE3D',
        }

        new_data_to_send = self.data_to_send | data
        response = session.post('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx', data=new_data_to_send)
        response = session.get('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx')

        soup = BeautifulSoup(response.text, features="lxml")
        b = soup.select('#form1')[0]
        table2 = b.find_all("table")[1]
        table3 = b.find_all("table")[2]

        tab2_tr = table2.find_all("tr")
        tab3_tr = table3.find_all("tr")

        general_data = {}

        general_data['rollNo'] = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(1) > td:nth-child(1) > b:nth-child(1)')[0].getText()
        general_data['regnNo'] = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)')[0].getText()
        general_data['name']   = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > b:nth-child(2)')[0].getText()
        general_data['supply'] = soup.select('#form1 > center > table > span:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > b:nth-child(1)')[0].getText()

        totals = {}
        totals['credsReg'] = tab3_tr[0].find_all("td")[1].find_all("b")[0].text
        totals['gradpoint']  = tab3_tr[0].find_all("td")[3].find_all("b")[0].text
        totals['credsEar']  = tab3_tr[1].find_all("td")[1].find_all("b")[0].text
        totals['SGPA']      = tab3_tr[2].find_all("td")[1].find_all("b")[0].text
        totals['CGPA']      = tab3_tr[3].find_all("td")[1].find_all("b")[0].text
        
        subject_data = {}
        for i in self.subjects:
            subject_data[i] = {'credits' : '', 'grade' : '', 'gradePoint': ''}  
            
        a = 0
        for i in subject_data:
            subject_data[i]["credits"]      = tab2_tr[a+1].find_all("td")[5].getText().strip()
            subject_data[i]["grade"]        = tab2_tr[a+1].find_all("td")[6].getText().strip()
            subject_data[i]["gradePoint"]   = tab2_tr[a+1].find_all("td")[7].getText().strip()
            a += 1

        return general_data, subject_data, totals