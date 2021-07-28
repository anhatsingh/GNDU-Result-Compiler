import requests, time, threading, os, timeit, random
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def ini(wa, stop, fC):    
    sess=requests.Session()

    url = 'http://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx'
    d = { #data, to check result for
        "years": ['2020', '2021'],
        "month": ['5', '12'],
        "courseType": ['C'],
        "course": [''], #1703 for CSE
        "semester": [''], #17030x for x-th sem
        "rollNo": ['']
    }

    p = { #post data
        'DrpDwnYear': '2020',
        'DrpDwnMonth': '12',
        'DropDownCourseType': 'C',

        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwUKMTE0NjMzNTU5Ng9kFgICAw9kFgoCAQ8QDxYEHg5EYXRhVmFsdWVGaWVsZAUEY29kZR4NRGF0YVRleHRGaWVsZAUEbmFtZWQQFQwEWWVhcgQyMDExBDIwMTIEMjAxMwQyMDE0BDIwMTUEMjAxNgQyMDE3BDIwMTgEMjAxOQQyMDIwBDIwMjEVDAAEMjAxMQQyMDEyBDIwMTMEMjAxNAQyMDE1BDIwMTYEMjAxNwQyMDE4BDIwMTkEMjAyMAQyMDIxFCsDDGdnZ2dnZ2dnZ2dnZxYBAglkAgMPEA8WBB8BBQlNb250aG5hbWUfAAUEQ29kZWQQFQMFTW9udGgERGVjLgRNYXkuFQMAAjEyATUUKwMDZ2dnZGQCBQ8QDxYEHwEFC0NvdXJzZSBUeXBlHwAFCFR5cGVDb2RlZBAVAwtDb3Vyc2UgVHlwZQtQYXNzIENvdXJzZQpDQkVTIChOZXcpFQMAAVABQxQrAwNnZ2cWAQICZAIHDxAPFgYfAAUJQ2xhc3Njb2RlHwEFBWNuYW1lHgtfIURhdGFCb3VuZGdkEBWYARAtLVNlbGVjdCBDbGFzcy0tG0IuQS4gKEhvbnMuIFNjaG9vbCkgUHVuamFiaSxCLkEuIChIb25zLikgSm91cm5hbGlzbSAmIE1hc3MgQ29tbXVuaWNhdGlvbhxCLkEuIChIb25zLikgU29jaWFsIFNjaWVuY2VzHkIuQS4gTEwuQi4gKEZpdmUgWWVhcnMgQ291cnNlKSVCLlNjLiAoSG9ub3VycyBTY2hvb2wpIEh1bWFuIEdlbmV0aWNzHkIuU2MuIChIb25zLiBTY2hvb2wpIEVjb25vbWljcxlCLlNjLiAoSG9ucy4pIEFncmljdWx0dXJlFEIuU2MuIChIb25zLikgQm90YW55GUIuU2MuIChIb25zLikgTWF0aGVtYXRpY3MdQi5TYy4gKEhvbnMuU2Nob29sKSBDaGVtaXN0cnkdQi5TYy4oSG9ub3VycyBTY2hvb2wpIFBoeXNpY3MdQi5TYy4oTUVESUNBTCBMQUIgVEVDSE5PTE9HWSkbQi5UZWNoLiAoQ2l2aWwgRW5naW5lZXJpbmcpHkIuVGVjaC4gKENvbXB1dGVyIEVuZ2luZWVyaW5nKSJCLlRlY2guIChDb21wdXRlciBTY2llbmNlICYgRW5nZy4pK0IuVGVjaC4gKEVsZWN0cm9uaWNzICYgQ29tbXVuaWNhdGlvbiBFbmdnLiksQi5UZWNoLiAoRWxlY3Ryb25pY3MgJiBDb21wdXRlciBFbmdpbmVlcmluZykZQi5UZWNoLiAoRm9vZCBUZWNobm9sb2d5KSBCLlRlY2guIChNZWNoYW5pY2FsIEVuZ2luZWVyaW5nKSdCLlRFQ0guIChURVhUSUxFIFBST0NFU1NJTkcgVEVDSE5PTE9HWSkYQmFjaGVsb3Igb2YgQXJjaGl0ZWN0dXJlHEJhY2hlbG9yIG9mIENvbW1lcmNlIChIb25zLikaQmFjaGVsb3IgT2YgQ29tbWVyY2UgKE9ETCknQmFjaGVsb3IgT2YgQ29tcHV0ZXIgQXBwbGljYXRpb25zIChPREwpMkJhY2hlbG9yIG9mIEhvdGVsIE1hbmFnZW1lbnQgJiBDYXRlcmluZyBUZWNobm9sb2d5L0JhY2hlbG9yIE9mIExpYnJhcnkgJiBJbmZvcm1hdGlvbiBTY2VpbmNlIChPREwpM0JhY2hlbG9yIG9mIExpYnJhcnkgYW5kIEluZm9ybWF0aW9uIFNjaWVuY2UgKEhvbnMuKRRCYWNoZWxvciBvZiBQaGFybWFjeSdCYWNoZWxvciBvZiBQbGFubmluZyAoVXJiYW4gJiBSZWdpb25hbCknQmFjaGVsb3Igb2YgVG91cmlzbSAmIFRyYXZlbCBNYW5hZ2VtZW50LUNlcnRpZmljYXRlIGluIEVhcmx5IENoaWxkIENhcmUgYW5kIEVkdWNhdGlvbjNEaXBsb21hIENvdXJzZSBpbiBDb21wdXRlciBBcHBsaWNhdGlvbnMgKEZ1bGwgVGltZSkpRGlwbG9tYSBpbiBFYXJseSBDaGlsZCBDYXJlIGFuZCBFZHVjYXRpb24ZTEwuQiAoVGhyZWUgWWVhcnMgQ291cnNlKRdMTC5NLiAoT25lIFllYXIgQ291cnNlKRlNLkEuIChCdXNpbmVzcyBFY29ub21pY3MpGE0uQS4gKFNwb3J0cyBQc3ljaG9sb2d5KTJNLkEuIEludGVybmF0aW9uYWwgUmVsYXRpb25zIChTb3V0aCBBc2lhbiBTdHVkaWVzKSRNLkEuIEpvdXJuYWxpc20gJiBNYXNzIENvbW11bmljYXRpb24bTS5CLkEuIChGaW5hbmNpYWwgQW5hbHlzaXMpHU0uQi5BLiAoRmluYW5jaWFsIE1hbmFnZW1lbnQpI00uQi5BLiAoSFVNQU4gUkVTT1VSQ0UgREVWRUxPUE1FTlQpIk0uQi5BLiAoSFVNQU4gUkVTT1VSQ0UgTUFOQUdFTUVOVCkdTS5CLkEuIChNYXJrZXRpbmcgTWFuYWdlbWVudCkbTS5QLkEuIE11c2ljIChJbnN0cnVtZW50YWwpFE0uUC5BLiBNdXNpYyAoVm9jYWwpHU0uUC5ULiAoU3BvcnRzIFBoeXNpb3RoZXJhcHkpHU0uUGhpbC4gTXVzaWMgKFZvY2FsICYgSW5zdC4pGU0uUGhpbC4gUmVsaWdpb3VzIFN0dWRpZXMlTS5TYy4gKEV4Y2VyY2lzZSAmIFNwb3J0cyBQaHlzaW9sb2d5KRdNLlNjLiAoRm9vZCBUZWNobm9sb2d5KSBNLlNjLiAoSG9ub3VycyBTY2hvb2wpIENoZW1pc3RyeSVNLlNjLiAoSG9ub3VycyBTY2hvb2wpIEh1bWFuIEdlbmV0aWNzG00uU2MuIChIb25zKSBab29sb2d5IChGWUlDKR5NLlNjLiAoSG9ucy4gU2Nob29sKSBFY29ub21pY3McTS5TYy4gKEhvbnMuIFNjaG9vbCkgUGh5c2ljcxhNLlNjLiAoU3BvcnRzIE51dHJpdGlvbikpTS5TYy4gQXBwbGllZCBDaGVtaXN0cnkgKFBoYXJtYWNldXRpY2Fscyk6TS5TYy4gQmlvY2hlbWlzdHJ5IChTcGVjaWFsaXphdGlvbiBpbiBTcG9ydHMgQmlvY2hlbWlzdHJ5KRNNLlNjLiBCaW90ZWNobm9sb2d5DE0uU2MuIEJvdGFueQ9NLlNjLiBDaGVtaXN0cnkdTS5TYy4gQ2hlbWlzdHJ5IChGWUlDKSAoVVNIUykWTS5TYy4gQ2hlbWlzdHJ5IChVU0hTKRxNLlNjLiBFbnZpcm9ubWVudGFsIFNjaWVuY2VzFE0uU2MuIEh1bWFuIEdlbmV0aWNzIk0uU2MuIEh1bWFuIEdlbmV0aWNzIChGWUlDKSAoVVNIUykbTS5TYy4gSHVtYW4gR2VuZXRpY3MgKFVTSFMpEU0uU2MuIE1hdGhlbWF0aWNzH00uU2MuIE1hdGhlbWF0aWNzIChGWUlDKSAoVVNIUykSTS5TYy4gTWljcm9iaW9sb2d5Jk0uU2MuIE1vbGVjdWxhciBCaW9sb2d5ICYgQmlvY2hlbWlzdHJ5DU0uU2MuIFBoeXNpY3MbTS5TYy4gUGh5c2ljcyAoRllJQykgKFVTSFMpFE0uU2MuIFBoeXNpY3MgKFVTSFMpDU0uU2MuIFpvb2xvZ3kbTS5TYy4gWm9vbG9neSAoRllJQykgKFVTSFMpOE0uVGVjaC4gKENvbXB1dGVyIFNjaWVuY2UgJiBFbmdpbmVlcmluZykgVHdvIFllYXIgQ291cnNlNU0uVGVjaC4gKEVDRSopIFNwZWNpYWxpemF0aW9uIChDb21tdW5pY2F0aW9uIFN5c3RlbXMpOE0uVGVjaC4gKE1lY2hhdHJvbmljcyBFbmdpbmVlcmluZykgRHVhbCBEZWdyZWUgUHJvZ3JhbW1lJU1hc3RlciBpbiBQaHlzaW90aGVyYXB5IChPcnRob3BlZGljcyklTWFzdGVyIG9mIEFyY2hpdGVjdHVyZSAoVXJiYW4gRGVzaWduKRtNYXN0ZXIgb2YgQXJ0cyBpbiBFZHVjYXRpb24ZTWFzdGVyIG9mIEFydHMgaW4gRW5nbGlzaB9NYXN0ZXIgT2YgQXJ0cyBJbiBFbmdsaXNoIChPREwpF01hc3RlciBvZiBBcnRzIGluIEhpbmRpGU1hc3RlciBvZiBBcnRzIGluIEhpc3RvcnkcTWFzdGVyIG9mIEFydHMgaW4gUGhpbG9zb3BoeSNNYXN0ZXIgb2YgQXJ0cyBpbiBQb2xpdGljYWwgU2NpZW5jZSlNYXN0ZXIgT2YgQXJ0cyBJbiBQb2xpdGljYWwgU2NpZW5jZSAoT0RMKRxNYXN0ZXIgb2YgQXJ0cyBpbiBQc3ljaG9sb2d5GU1hc3RlciBvZiBBcnRzIGluIFB1bmphYmkjTWFzdGVyIG9mIEFydHMgaW4gUmVsaWdpb3VzIFN0dWRpZXMaTWFzdGVyIG9mIEFydHMgaW4gU2Fuc2tyaXQbTWFzdGVyIG9mIEFydHMgaW4gU29jaW9sb2d5IU1hc3RlciBvZiBCdXNpbmVzcyBBZG1pbmlzdHJhdGlvbitNYXN0ZXIgb2YgQnVzaW5lc3MgQWRtaW5pc3RyYXRpb24gKEZpbmFuY2UpKE1hc3RlciBvZiBCdXNpbmVzcyBBZG1pbmlzdHJhdGlvbiAoRllJQyknTWFzdGVyIE9mIEJ1c2luZXNzIEFkbWluaXN0cmF0aW9uIChPREwpEk1hc3RlciBvZiBDb21tZXJjZRlNQVNURVIgT0YgQ09NTUVSQ0UgKEZZSUMpJk1hc3RlciBvZiBDb21wdXRlciBBcHBsaWNhdGlvbnMgKEZZSUMpJU1hc3RlciBPZiBDb21wdXRlciBBcHBsaWNhdGlvbnMgKE9ETCklTWFzdGVyIG9mIENvbXB1dGVyIEFwcGxpY2F0aW9ucyAoVFlDKRNNYXN0ZXIgb2YgRWR1Y2F0aW9uJ01hc3RlciBvZiBMaWJyYXJ5ICYgSW5mb3JtYXRpb24gU2NpZW5jZRJNYXN0ZXIgb2YgUGhhcm1hY3kjTWFzdGVyIG9mIFBsYW5uaW5nIChJbmZyYXN0cnVjdHVyZSkeTWFzdGVyIG9mIFBsYW5uaW5nIChUcmFuc3BvcnQpGk1hc3RlciBvZiBQbGFubmluZyAoVXJiYW4pIk1hc3RlcnMgaW4gSG9zcGl0YWwgQWRtaW5pc3RyYXRpb24sUEcgRElQTE9NQSBJTiBCQU5LSU5HLCBJTlNVUkFOQ0UgQU5EIEZJTkFOQ0UwUG9zdCBHcmFkdWF0ZSBEaXBsb21hIGluIEFwcGxpZWQgTnV0cml0aW9uIChPREwpMlBvc3QgR3JhZHVhdGUgRGlwbG9tYSBpbiBCdXNpbmVzcyBNYW5hZ2VtZW50IChPREwpLlBvc3QgR3JhZHVhdGUgRGlwbG9tYSBJbiBDb21wdXRlciBBcHBsaWNhdGlvbnM0UG9zdCBHcmFkdWF0ZSBEaXBsb21hIEluIENvbXB1dGVyIEFwcGxpY2F0aW9ucyAoT0RMKTFQb3N0IEdyYWR1YXRlIERpcGxvbWEgaW4gR3VpZGFuY2UgYW5kIENvdW5zZWxsaW5nPlBvc3QgR3JhZHVhdGUgRGlwbG9tYSBpbiBKb3VybmFsaXNtICYgTWFzcyBDb21tdW5pY2F0aW9uIChPREwpMlBvc3QgR3JhZHVhdGUgRGlwbG9tYSBJbiBNZW50YWwgSGVhbHRoIENvdW5zZWxsaW5nLVByZSBQaC5kIENvdXJzZSBpbiBTcG9ydHMgU2NpZW5jZXMgJiBNZWRpY2luZSBQcmUgUGguRC4gQ291cnNlIGluIEFyY2hpdGVjdHVyZSFQcmUgUGguRC4gQ291cnNlIGluIEJpb3RlY2hub2xvZ3kaUHJlIFBoLkQuIENvdXJzZSBpbiBCb3RhbnkrUHJlIFBoLkQuIENvdXJzZSBpbiBCdXNpbmVzcyBBZG1pbmlzdHJhdGlvbh1QcmUgUGguRC4gQ291cnNlIGluIENoZW1pc3RyeRxQcmUgUGguRC4gQ291cnNlIGluIENvbW1lcmNlJFByZSBQaC5ELiBDb3Vyc2UgaW4gQ29tcHV0ZXIgU2NpZW5jZTRQcmUgUGguRC4gQ291cnNlIGluIENvbXB1dGVyIFNjaWVuY2UgYW5kIEVuZ2luZWVyaW5nHVByZSBQaC5ELiBDb3Vyc2UgaW4gRWNvbm9taWNzHVByZSBQaC5ELiBDb3Vyc2UgaW4gRWR1Y2F0aW9uMVByZSBQaC5ELiBDb3Vyc2UgaW4gRWxlY3Ryb25pY3MgYW5kIENvbW11bmljYXRpb24oUHJlIFBoLkQuIENvdXJzZSBpbiBFbnZpcm9ubWVudCBTY2llbmNlcyNQcmUgUGguRC4gQ291cnNlIGluIEZvb2QgVGVjaG5vbG9neRlQcmUgUGguRC4gQ291cnNlIGluIEhpbmRpG1ByZSBQaC5ELiBDb3Vyc2UgaW4gSGlzdG9yeSJQcmUgUGguRC4gQ291cnNlIGluIEh1bWFuIEdlbmV0aWNzMVByZSBQaC5ELiBDb3Vyc2UgSW4gTGlicmFyeSAmIEluZm9ybWF0aW9uIFNjaWVuY2UgUHJlIFBoLkQuIENvdXJzZSBpbiBNaWNyb2Jpb2xvZ3k0UHJlIFBoLkQuIENvdXJzZSBJbiBNb2xlY3VsYXIgQmlvbG9neSAmIEJpb2NoZW1pc3RyeTBQcmUgUGguRC4gQ291cnNlIGluIE11c2ljIChWb2NhbCAmIEluc3RydW1lbnRhbCk5UHJlIFBoLkQuIENvdXJzZSBpbiBQaGFybWFjZXV0aWNhbCBTY2llbmNlcywgMXN0IFNlbWVzdGVyJlByZSBQaC5ELiBDb3Vyc2UgaW4gUGh5c2ljYWwgRWR1Y2F0aW9uJVByZSBQaC5ELiBDb3Vyc2UgSW4gUGh5c2ljYWwgUGxhbm5pbmcbUHJlIFBoLkQuIENvdXJzZSBpbiBQaHlzaWNzJVByZSBQaC5ELiBDb3Vyc2UgaW4gUG9saXRpY2FsIFNjaWVuY2UeUHJlIFBoLkQuIENvdXJzZSBpbiBQc3ljaG9sb2d5G1ByZSBQaC5ELiBDb3Vyc2UgaW4gUHVuamFiaRxQcmUgUGguRC4gQ291cnNlIEluIFNhbnNrcml0I1ByZSBQaC5ELiBDb3Vyc2UgSW4gU29jaWFsIFNjaWVuY2VzHVByZSBQaC5ELiBDb3Vyc2UgSW4gU29jaW9sb2d5G1ByZSBQaC5ELiBDb3Vyc2UgaW4gWm9vbG9neRWYAQAEMTcxMgQxNzI4BDE3MTMEMTcxNAQxNzE1BDE3MTYEMTczMQQxNzI3BDE3MjAEMTcxNwQxNzE4BDE3MjIEMTcwMQQxNzAyBDE3MDMEMTcwNAQxNzMwBDE3MDUEMTcwNgQxNzIzBDE3MDcEMTcyNAQxOTA0BDE5MDMEMTcyNQQxOTAxBDE3MjEEMTcyNgQxNzE5BDE3MTAENTcwMgQ0NzAyBDQ3MDEEMTcxMQQyNzAxBDI3MDIEMjc1NwQyNzcyBDI3NjgEMjcwMwQyNzczBDI3NjMEMjc3NAQyNzA0BDI3MDUEMjcwNgQyNzU5BDI3MDkEMjcxMQQyNzU4BDI3MTMEMjcxNAQyNzE1BDI3NjUEMjcxNgQyNzE3BDI3NTYEMjcxOAQyNzc1BDI3MTkEMjcyMAQyNzIxBDI3NzAEMjc4MAQyNzIyBDI3MjMEMjc3OAQyNzc5BDI3MjQEMjc4MQQyNzI1BDI3MjYEMjcyNwQyNzcxBDI3NzYEMjcyOAQyNzgyBDI3MjkEMjczMAQyNzY5BDI3NjAEMjczNAQyNzM1BDI3MzYEMjkwNQQyNzM3BDI3MzgEMjczOQQyNzQwBDI5MDYEMjc0MQQyNzQyBDI3NDMEMjc0NAQyNzQ1BDI3NDYEMjc2NAQyNzQ3BDI5MDEEMjc0OQQyNzMxBDI3NTAEMjkwMgQyNzUxBDI3NTIEMjc1MwQyNzY2BDI3NjcEMjc3NwQyNzYxBDI3NjIEMzcwMgQzOTA1BDM5MDMEMzcwMwQzOTAyBDM3MDQEMzkwNAQzNzAxBDc3MjkENzcyMwQ3NzA0BDc3MDUENzcyNgQ3NzA4BDc3MDcENzcxMQQ3NzI3BDc3MzgENzcyNQQ3NzAxBDc3MTUENzcwOQQ3NzIxBDc3MTYENzcwMgQ3NzM5BDc3MDYENzczNQQ3NzIyBDc3MTkENzczNwQ3NzM2BDc3MTIENzczMAQ3NzE0BDc3MTcENzczNAQ3NzI4BDc3MzEENzcwMxQrA5gBZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAWZkAgkPEGRkFgBkZOMLSrEb6Aqo2c/xM2bKKOdHTeQzNnAsA/RnP+jdcDWI',
        '__VIEWSTATEGENERATOR': '72A7EE3D',
        
    }

    ffL = [] #first fetch list
    sfL = [] #second fetch list
    listOfPayloads = [] #list of all possible post data
    avgTimeL = [] #list of time taken for each compare
    waitTime = 2 #minutes
    t_id = "{}.{}".format(os.getpid(),threading.get_ident()) #process id
    global doFetch    

    fC.set("r", "pid", t_id)
    wa.sendMessage("Automation", "AUTOMATOR<br><br>*Result checker*<br>Yipeee! I am alive :P<br><br>Thread ID: " + str(t_id) + "<br>Wait Time: " + str(waitTime) + " minutes")        

    for y in d['years']:
        for m in d['month']:
            for cT in d['courseType']:
                    p['DrpDwnYear'] = y
                    p['DrpDwnMonth'] = m
                    p['DropDownCourseType'] = cT        
                    listOfPayloads.append(p) 
    
    def getAvg():
        sum = 0
        for i in avgTimeL:
            sum += i        
        return sum/len(avgTimeL)
    def waitHere(t):
        i = 0        
        while(i<=t):
            if(not stop()):
                i+=1
                fC.set("r", "timeRemaining", t-i)
                time.sleep(1)
            else:
                break        
    
    def fetch(num):
        global doFetch        
        try:
            if(num == 1):
                ffL.clear()
            elif(num == 2):
                sfL.clear()
            for i in listOfPayloads:            
                fetch = sess.post(url, data=i).text
                pH1 = BeautifulSoup(fetch, features="html.parser")
                op1 = pH1.body.find('select', attrs={'name':'DrpDwnCMaster'}).text.split("\n")
                final = {
                    "year": i["DrpDwnYear"],
                    "month": ("May" if m == '5' else "December"),
                    "courseType": "CBES (new)",
                    "courses": op1
                }
                if(num == 1):
                    ffL.append(final)
                elif(num == 2):
                    sfL.append(final)
            doFetch = False

        except Exception as e:
            try:                            
                wa.sendMessage("Automation", "AUTOMATOR<br><br>*Error occured while fetching:*<br>" + str(e))                                    
            except:
                print("error in fetching " + str(e))
            doFetch = True
           

    n = 0    
    while(True):        
        if(not stop()):                           
            start_time = timeit.default_timer()            
            #if(fC.get("r", "waitTime") != waitTime):
             #   avgTimeL.clear()
            waitTime = random.randint(7,15)
            fC.set("r", "waitTime", waitTime)

            doFetch = True            
            while(doFetch):                
                fetch(1)
                time.sleep(10)
                
            waitHere(waitTime*60)

            doFetch = True
            while(doFetch):                
                fetch(2)
                time.sleep(10)

            try:                
                for x in range(len(ffL)):                
                    changes = [i for i in ffL[x]["courses"] + sfL[x]["courses"] if i not in ffL[x]["courses"] or i not in sfL[x]["courses"]]

                    if(len(changes) > 0):                    
                        cStr = '<br>'.join(map(str, changes))
                        theStr = "Year: " + str(sfL[x]["year"]) + "<br>Month: " + sfL[x]["month"] + "<br>CourseType: CBES (new)<br><br>*Courses:*<br>" + cStr                
                        finalStr = "AUTOMATOR<br><br>*Change detected in results page*<br>" + theStr

                        try:                            
                            wa.sendMessage("Automation", finalStr)                                    
                        except:
                            msg = theStr.split("<br>")        
                            for i in msg:
                                print(i + "\n")
                
            except Exception as e:
                try:                            
                    wa.sendMessage("Automation", "AUTOMATOR<br><br>*Error in comparing results*<br>" + str(e))                                    
                except:
                    print("error in comparing results " + str(e))

            avgTimeL.append(timeit.default_timer() - start_time)                            
            n += 1
            fC.set("r", "avgTime", getAvg())            
            fC.set("r", "TimesChecked", n)
                        
        else:
            fC.set("r", "running", False)
            try:
                wa.sendMessage("Automation", "AUTOMATOR<br><br>*Result Checker KILLED*<br>Thread ("+str(t_id)+") stopped")
            except:
                print("Result Checker stopped<br>Thread ("+str(t_id)+") Killed")
            break