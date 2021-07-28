import threading, math, queue, timeit
from main_processor import misc as func
from main_processor import worker

# ============================================ Data is here, change things here =================

"""
roll_numbers_to_find: list<int>    --- Add custom roll numbers to crawl here
year: int                       --- year of Result to find
month: int                      --- month of Result to find
course_code: int                 --- 1703 for CSE (A and B Section), 1702 for CE (C Section)
semester: int                   --- semester number to find the result for
initial_roll_number: int                    --- (First Roll Number of class) - 1
total_students: int                   --- Total Number of students in class, set 0 if using custom
                                    roll numbers, can use in addition to custom roll too
subjects: list<str>       --- List of Subjects of the semester, Put them in order of
                                    the table given in Results Page of GNDU.

google_sheet_title: str                         --- Google Sheets Title, where everything will be
                                            uploaded to.
existing_sheet_id: str/Bool    --- Google Sheets Unique Identifier of a sheet, if
                                            to upload in an existing sheet, else set to
                                            False to create a new Google Sheet

gndu_url_form: str                    --- URL of the GNDU page where we fill the form to get
                                    the result.
gndu_url_display: str                 --- URL of the GNDU page where the result is displayed
                                    after filling the form and clicking on submit button

size_of_thread: int                  --- The Maximum number of Roll number each thread can
                                    process, the smaller, the faster.
"""

roll_numbers_to_find = []

year = 2020
month = 12
course_code = 1703
semester = 1
initial_roll_number = 17032000300
total_students  = 116
subjects = ["Mechanics", "EGD", "Physics", "Maths", "Material", "Punjabi", "Drug Abuse"]

google_sheet_title = "Section A"
existing_sheet_id = ''

gndu_url_form = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
gndu_url_display = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx'

size_of_thread = 2 # If you want to restrict by max_threads, uncomment the 2 lines below, and comment this one
#max_threads = math.ceil(len(roll_numbers_to_find) / 2)
#size_of_thread = math.ceil(len(roll_numbers_to_find) / max_threads)

# ============================================ Do Not touch anything after this line =============

for i in range(1,total_students+1):
    roll_numbers_to_find.append(initial_roll_number+i)

data_to_send = { #post data
     'DrpDwnyear': str(year),
     'DrpDwnmonth': str(month),
     'DropDownCourseType': 'C',
     'DrpDwnCMaster': str(course_code), #change course here
     'DrpDwnCdetail': str(semester) + '0' + str(course_code),    #change semester here
}

misc_functions = func()
view_state = misc_functions.get_view_state(gndu_url_form, data_to_send)

start_time = timeit.default_timer()
number_of_threads = math.ceil(len(roll_numbers_to_find) / size_of_thread)
threads = {}
que = queue.Queue()
count_of_roll_done = 0

def do_count_roll():
    global count_of_roll_done
    count_of_roll_done += 1
    print(str(count_of_roll_done) + "/" + str(total_students) + " Done")

for i in range(number_of_threads):
    w = worker(i, subjects, data_to_send, view_state, lambda: do_count_roll())
    rollForThisThread = [roll_numbers_to_find[(i*size_of_thread) + a] if (((i*size_of_thread) + a) < len(roll_numbers_to_find)) else None for a in range(size_of_thread)]    
    threads[i] = threading.Thread(target=lambda q, arg1: q.put(w.startTheWork(arg1)), args=(que, [a for a in rollForThisThread if a!= None]))    
    threads[i].start()    
    
for i in range(number_of_threads):
    threads[i].join()


data_from_threads = []
roll_num_not_found = []
while not que.empty():
    result = que.get()
    data_from_threads.extend(result[1])
    roll_num_not_found.extend(result[2])

misc_functions.upload_to_google_sheets(data_from_threads, google_sheet_title, subjects, existing_sheet_id)

total_time = timeit.default_timer() - start_time
print("Time taken: " + str(total_time) + "s")
print("Errors: ", roll_num_not_found)
