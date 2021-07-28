# ============================================ Data is here, change things here =============================================================== #

"""
rollNumberToCrawl: list<int>    --- Add custom roll numbers to crawl here
Year: int                       --- Year of Result to find
Month: int                      --- Month of Result to find
CourseCode: int                 --- 1703 for CSE (A and B Section), 1702 for CE (C Section)
Semester: int                   --- Semester number to find the result for
iniRoll: int                    --- (First Roll Number of class) - 1
totalStu: int                   --- Total Number of students in class, set 0 if using custom roll numbers, can use in addition to custom roll too
listOfSubjects: list<str>       --- List of Subjects of the Semester, Put them in order of the table given in Results Page of GNDU.

sheetTitle: str                         --- Google Sheets Title, where everything will be uploaded to.
addIntoExistingSheetWithID: str/Bool    --- Google Sheets Unique Identifier of a sheet, if to upload in an existing sheet, else set to False to create a new Google Sheet

formUrl: str                    --- URL of the GNDU page where we fill the form to get the result.
displayUrl: str                 --- URL of the GNDU page where the result is displayed after filling the form and clicking on submit button

blockSize: int                  --- The Maximum number of Roll number each thread can process, the smaller, the faster.
"""

rollNumberToCrawl = []

Year = 2020
Month = 12
CourseCode = 1703
Semester = 1
iniRoll = 17032000300
totalStu  = 116
listOfSubjects = ["Mechanics", "EGD", "Physics", "Maths", "Material", "Punjabi", "Drug Abuse"]

sheetTitle = "Section A"
addIntoExistingSheetWithID = ''

formUrl = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
displayUrl = 'https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx'

blockSize = 2 # If you want to restrict by max_threads, uncomment the 2 lines below, and comment this one
#max_threads = math.ceil(len(rollNumberToCrawl) / 2)
#blockSize = math.ceil(len(rollNumberToCrawl) / max_threads)

# ============================================ Do Not touch anything after this line =============================================================== #

import threading, math, queue, timeit
from main_processor import misc as func
from main_processor import worker


for i in range(1,totalStu+1):
    rollNumberToCrawl.append(iniRoll+i)

postData = { #post data
     'DrpDwnYear': str(Year),
     'DrpDwnMonth': str(Month),
     'DropDownCourseType': 'C',
     'DrpDwnCMaster': str(CourseCode), #change course here
     'DrpDwnCdetail': str(Semester) + '0' + str(CourseCode),    #change semester here
}

f = func()
viewState = f.getViewState(formUrl, postData)

start_time = timeit.default_timer()
numOfBlocks = math.ceil(len(rollNumberToCrawl) / blockSize)
threads = {}
que = queue.Queue()
numOfRollDone = 0

def doCount():
    global numOfRollDone
    numOfRollDone += 1
    print(str(numOfRollDone) + "/" + str(totalStu) + " Done")

for i in range(numOfBlocks):
    w = worker(i, listOfSubjects, postData, viewState, lambda: doCount())
    rollForThisThread = [rollNumberToCrawl[(i*blockSize) + a] if (((i*blockSize) + a) < len(rollNumberToCrawl)) else None for a in range(blockSize)]    
    threads[i] = threading.Thread(target=lambda q, arg1: q.put(w.startTheWork(arg1)), args=(que, [a for a in rollForThisThread if a!= None]))    
    threads[i].start()    
    
for i in range(numOfBlocks):
    threads[i].join()


compiledData = []
errorData = []
while not que.empty():
    result = que.get()
    compiledData.extend(result[1])
    errorData.extend(result[2])

f.uploadToGoogle(compiledData, sheetTitle, listOfSubjects, addIntoExistingSheetWithID)

total_time = timeit.default_timer() - start_time
print("Time taken: " + str(total_time) + "s")
print("Errors: ", errorData)
