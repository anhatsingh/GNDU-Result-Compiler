import threading, math, main, queue, timeit
from seleniumManager.manager import Manager
from sheets_api_v3 import googleAPI

start_time = timeit.default_timer()

max_threads = 15 #do not go over 15 for your PC's sake
sheetTitle = "Result_1 Sem_C Section_v2"
rollNumberToCrawl = [] # add custom roll numbers to crawl here

iniRoll = 17022000300 # if roll is a continuous series, give start roll here
totalStu  = 51 # total number of students to crawl
for i in range(1,totalStu+1):
    rollNumberToCrawl.append(iniRoll+i)

postData = { #post data
        'DrpDwnYear': '2020',
        'DrpDwnMonth': '12',
        'DropDownCourseType': 'C',
        'DrpDwnCMaster': '1702', #change course here
        'DrpDwnCdetail': '170201',    #change semester here
    }

listOfSubjects = ["Mechanics", "EGD", "Physics", "Maths", "Material", "Punjabi", "Drug Abuse"] # Put this in order of the result page table


# ============================================ Do Not touch anything after this line =============================================================== #
blockSize = math.ceil(len(rollNumberToCrawl) / max_threads) # number of roll numbers each thread will process

def uploadToGoogle(sData):
    api = googleAPI("")    
    api.connectToGoogle()
    api.setSheet(api.createSpreadsheet(sheetTitle))    

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
    cellsAffected = api.updateSheet("Sheet1!A1:" + api.getLetter(len(row1) - 1) + str(len(finData)), finData)

numOfBlocks = math.ceil(len(rollNumberToCrawl) / blockSize)
threads = {}
que = queue.Queue()

for i in range(numOfBlocks):
    threads[i] = {
        "thread": "",
        "rollToCrawl" : []
    }    
    
    # make the list of "blocksized" roll numbers to look through
    for a in range(blockSize):
        index = (i*blockSize) + a
        if(index < len(rollNumberToCrawl)):        
            threads[i]["rollToCrawl"].append(rollNumberToCrawl[index])

    si = Manager(r'chromedriver.exe')
    d = si.driver()
    w = main.worker(i, d, postData, listOfSubjects)

    
    threads[i]["thread"] = threading.Thread(target=lambda q, arg1: q.put(w.startTheWork(arg1)), args=(que, threads[i]["rollToCrawl"]))
    threads[i]["thread"].start()    
    
for i in range(numOfBlocks):
    threads[i]["thread"].join()


compiledData = []
errorData = []
while not que.empty():
    result = que.get()
    compiledData.extend(result[1])
    errorData.extend(result[2])

total_time = timeit.default_timer() - start_time
print("Time taken: " + str(total_time) + "s")
uploadToGoogle(compiledData)
print("Errors: ")
print(errorData)