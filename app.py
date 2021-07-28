import threading, math, queue, timeit
from main_processor import misc as func
from main_processor import worker

# ============================================ Data is here, change things here =================

"""
ROLL_NUMS_TO_FIND: list<int>    --- Add custom roll numbers to crawl here
YEAR: int                       --- YEAR of Result to find
MONTH: int                      --- MONTH of Result to find
COURSE_CODE: int                 --- 1703 for CSE (A and B Section), 1702 for CE (C Section)
SEMESTER: int                   --- SEMESTER number to find the result for
INITIAL_ROLL_NUM: int                    --- (First Roll Number of class) - 1
TOTAL_STUDENTS: int                   --- Total Number of students in class, set 0 if using custom
                                    roll numbers, can use in addition to custom roll too
SUBJECTS: list<str>       --- List of Subjects of the SEMESTER, Put them in order of
                                    the table given in Results Page of GNDU.

GOOGLE_SHEETS_TITLE: str                         --- Google Sheets Title, where everything will be
                                            uploaded to.
EXISTING_SHEET_ID: str/Bool    --- Google Sheets Unique Identifier of a sheet, if
                                            to upload in an existing sheet, else set to
                                            False to create a new Google Sheet

GNDU_URL_FORM: str                    --- URL of the GNDU page where we fill the form to get
                                    the result.
GNDU_FORM_DISPLAY: str                 --- URL of the GNDU page where the result is displayed
                                    after filling the form and clicking on submit button

SIZE_OF_THREAD: int                  --- The Maximum number of Roll number each thread can
                                    process, the smaller, the faster.
"""

ROLL_NUMS_TO_FIND = []

YEAR = 2020
MONTH = 12
COURSE_CODE = 1703
SEMESTER = 1
INITIAL_ROLL_NUM = 17032000300
TOTAL_STUDENTS  = 116
SUBJECTS = ["Mechanics", "EGD", "Physics", "Maths", "Material", "Punjabi", "Drug Abuse"]

GOOGLE_SHEETS_TITLE = "Section A"
EXISTING_SHEET_ID = ''

GNDU_URL_FORM = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
GNDU_FORM_DISPLAY = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx'

SIZE_OF_THREAD = 2 # If you want to restrict by max_threads, uncomment the 2 lines below,
                   # and comment this one
#max_threads = math.ceil(len(ROLL_NUMS_TO_FIND) / 2)
#SIZE_OF_THREAD = math.ceil(len(ROLL_NUMS_TO_FIND) / max_threads)

# ============================================ Do Not touch anything after this line =============

for each_stundent in range(1,TOTAL_STUDENTS+1):
    ROLL_NUMS_TO_FIND.append(INITIAL_ROLL_NUM+each_stundent)

data_to_send = { #post data
     'DrpDwnyear': str(YEAR),
     'DrpDwnmonth': str(MONTH),
     'DropDownCourseType': 'C',
     'DrpDwnCMaster': str(COURSE_CODE), #change course here
     'DrpDwnCdetail': str(SEMESTER) + '0' + str(COURSE_CODE),    #change SEMESTER here
}

misc_functions = func()
view_state = misc_functions.get_view_state(GNDU_URL_FORM, data_to_send)

start_time = timeit.default_timer()
number_of_threads = math.ceil(len(ROLL_NUMS_TO_FIND) / SIZE_OF_THREAD)
threads = {}
que = queue.Queue()
count_of_roll_done = 0

def do_count_roll():
    global count_of_roll_done
    count_of_roll_done += 1
    print(str(count_of_roll_done) + "/" + str(TOTAL_STUDENTS) + " Done")

for thread_num in range(number_of_threads):
    job_doer = worker(thread_num, SUBJECTS, data_to_send, view_state, lambda: do_count_roll())
    roll_nums_for_this_thread = [
        ROLL_NUMS_TO_FIND[(thread_num*SIZE_OF_THREAD) + a] 
            if (((thread_num*SIZE_OF_THREAD) + a) < len(ROLL_NUMS_TO_FIND)) 
            else None 
            for a in range(SIZE_OF_THREAD)
        ]    
    threads[thread_num] = threading.Thread(
        target=lambda q,
        arg1: q.put(job_doer.startTheWork(arg1)),
        args=(que, [a for a in roll_nums_for_this_thread if a!= None])
        )    
    threads[thread_num].start()    
    
for thread_num in range(number_of_threads):
    threads[thread_num].join()


data_from_threads = []
roll_num_not_found = []
while not que.empty():
    result = que.get()
    data_from_threads.extend(result[1])
    roll_num_not_found.extend(result[2])

misc_functions.upload_to_google_sheets(data_from_threads, GOOGLE_SHEETS_TITLE, SUBJECTS, EXISTING_SHEET_ID)

total_time = timeit.default_timer() - start_time
print("Time taken: " + str(total_time) + "s")
print("Errors: ", roll_num_not_found)
