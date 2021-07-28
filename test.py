import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
}

s = requests.session()
s.headers.update(headers)

s.get('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx')
data = {    
        'DrpDwnYear': '2020',
        'DrpDwnMonth': '12',
        'DropDownCourseType': 'C',
        'DrpDwnCMaster': '1702',
        'DrpDwnCdetail': '170201',
        'textboxRno': '17022000302',
        'buttonShowResult': 'Submit',

        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__view_state': '/wEPDwUKMTE0NjMzNTU5Ng9kFgICAw9kFgoCAQ8QDxYEHg5EYXRhVmFsdWVGaWVsZAUEY29kZR4NRGF0YVRleHRGaWVsZAUEbmFtZWQQFQwEWWVhcgQyMDExBDIwMTIEMjAxMwQyMDE0BDIwMTUEMjAxNgQyMDE3BDIwMTgEMjAxOQQyMDIwBDIwMjEVDAAEMjAxMQQyMDEyBDIwMTMEMjAxNAQyMDE1BDIwMTYEMjAxNwQyMDE4BDIwMTkEMjAyMAQyMDIxFCsDDGdnZ2dnZ2dnZ2dnZxYBAgpkAgMPEA8WBB8BBQlNb250aG5hbWUfAAUEQ29kZWQQFQMFTW9udGgERGVjLgRNYXkuFQMAAjEyATUUKwMDZ2dnZGQCBQ8QDxYEHwEFC0NvdXJzZSBUeXBlHwAFCFR5cGVDb2RlZBAVAwtDb3Vyc2UgVHlwZQtQYXNzIENvdXJzZQpDQkVTIChOZXcpFQMAAVABQxQrAwNnZ2cWAQICZAIHDxAPFgYfAAUJQ2xhc3Njb2RlHwEFBWNuYW1lHgtfIURhdGFCb3VuZGdkEBVeEC0tU2VsZWN0IENsYXNzLS0bQi5BLiAoSG9ucy4gU2Nob29sKSBQdW5qYWJpLEIuQS4gKEhvbnMuKSBKb3VybmFsaXNtICYgTWFzcyBDb21tdW5pY2F0aW9uM0IuU2MuIChDb21wdXRhdGlvbmFsIFN0YXRpc3RpY3MgYW5kIERhdGEgQW5hbHl0aWNzKSVCLlNjLiAoSG9ub3VycyBTY2hvb2wpIEh1bWFuIEdlbmV0aWNzHkIuU2MuIChIb25zLiBTY2hvb2wpIEVjb25vbWljcxlCLlNjLiAoSG9ucy4pIEFncmljdWx0dXJlFEIuU2MuIChIb25zLikgQm90YW55HUIuU2MuIChIb25zLlNjaG9vbCkgQ2hlbWlzdHJ5EkIuU2MuIE1pY3JvYmlvbG9neR5CLlRlY2guIChDb21wdXRlciBFbmdpbmVlcmluZykZQi5UZWNoLiAoRm9vZCBUZWNobm9sb2d5KSdCLlRFQ0guIChURVhUSUxFIFBST0NFU1NJTkcgVEVDSE5PTE9HWSkYQmFjaGVsb3Igb2YgQXJjaGl0ZWN0dXJlIkJhY2hlbG9yIG9mIENvbW1lcmNlIChIb25zLikoVVNIUykhQmFjaGVsb3IgT2YgQ29tcHV0ZXIgQXBwbGljYXRpb25zKUJhY2hlbG9yIE9mIExpYnJhcnkgJiBJbmZvcm1hdGlvbiBTY2llbmNlM0JhY2hlbG9yIG9mIExpYnJhcnkgYW5kIEluZm9ybWF0aW9uIFNjaWVuY2UgKEhvbnMuKSdCYWNoZWxvciBvZiBQbGFubmluZyAoVXJiYW4gJiBSZWdpb25hbCknQmFjaGVsb3Igb2YgVG91cmlzbSAmIFRyYXZlbCBNYW5hZ2VtZW50M0RpcGxvbWEgQ291cnNlIGluIENvbXB1dGVyIEFwcGxpY2F0aW9ucyAoRnVsbCBUaW1lKSZEaXBsb21hIGluIENvbXB1dGVyIEFwcGxpY2F0aW9ucyAoT0RMKRlNLkEuIChCdXNpbmVzcyBFY29ub21pY3MpGE0uQS4gKFNwb3J0cyBQc3ljaG9sb2d5KTJNLkEuIEludGVybmF0aW9uYWwgUmVsYXRpb25zIChTb3V0aCBBc2lhbiBTdHVkaWVzKSRNLkEuIEpvdXJuYWxpc20gJiBNYXNzIENvbW11bmljYXRpb24bTS5CLkEuIChGaW5hbmNpYWwgQW5hbHlzaXMpHU0uQi5BLiAoRmluYW5jaWFsIE1hbmFnZW1lbnQpI00uQi5BLiAoSFVNQU4gUkVTT1VSQ0UgREVWRUxPUE1FTlQpIk0uQi5BLiAoSFVNQU4gUkVTT1VSQ0UgTUFOQUdFTUVOVCkdTS5CLkEuIChNYXJrZXRpbmcgTWFuYWdlbWVudCkbTS5QLkEuIE11c2ljIChJbnN0cnVtZW50YWwpFE0uUC5BLiBNdXNpYyAoVm9jYWwpHU0uUC5ULiAoU3BvcnRzIFBoeXNpb3RoZXJhcHkpJU0uU2MuIChFeGNlcmNpc2UgJiBTcG9ydHMgUGh5c2lvbG9neSkXTS5TYy4gKEZvb2QgVGVjaG5vbG9neSkbTS5TYy4gKEhvbnMpIFpvb2xvZ3kgKEZZSUMpHk0uU2MuIChIb25zLiBTY2hvb2wpIEVjb25vbWljcxxNLlNjLiAoSG9ucy4gU2Nob29sKSBQaHlzaWNzG00uU2MuIChTcG9ydHMgQmlvbWVjaGFuaWNzKRhNLlNjLiAoU3BvcnRzIE51dHJpdGlvbikpTS5TYy4gQXBwbGllZCBDaGVtaXN0cnkgKFBoYXJtYWNldXRpY2Fscyk6TS5TYy4gQmlvY2hlbWlzdHJ5IChTcGVjaWFsaXphdGlvbiBpbiBTcG9ydHMgQmlvY2hlbWlzdHJ5KRNNLlNjLiBCaW90ZWNobm9sb2d5DE0uU2MuIEJvdGFueQ9NLlNjLiBDaGVtaXN0cnkWTS5TYy4gRWNvbm9taWNzIChVU0hTKRxNLlNjLiBFbnZpcm9ubWVudGFsIFNjaWVuY2VzFE0uU2MuIEh1bWFuIEdlbmV0aWNzIk0uU2MuIEh1bWFuIEdlbmV0aWNzIChGWUlDKSAoVVNIUykbTS5TYy4gSHVtYW4gR2VuZXRpY3MgKFVTSFMpEU0uU2MuIE1hdGhlbWF0aWNzH00uU2MuIE1hdGhlbWF0aWNzIChGWUlDKSAoVVNIUykSTS5TYy4gTWljcm9iaW9sb2d5Jk0uU2MuIE1vbGVjdWxhciBCaW9sb2d5ICYgQmlvY2hlbWlzdHJ5DU0uU2MuIFBoeXNpY3MUTS5TYy4gUGh5c2ljcyAoVVNIUykNTS5TYy4gWm9vbG9neRtNLlNjLiBab29sb2d5IChGWUlDKSAoVVNIUyk4TS5UZWNoLiAoQ29tcHV0ZXIgU2NpZW5jZSAmIEVuZ2luZWVyaW5nKSBUd28gWWVhciBDb3Vyc2U1TS5UZWNoLiAoRUNFKikgU3BlY2lhbGl6YXRpb24gKENvbW11bmljYXRpb24gU3lzdGVtcyklTWFzdGVyIGluIFBoeXNpb3RoZXJhcHkgKE9ydGhvcGVkaWNzKSVNYXN0ZXIgb2YgQXJjaGl0ZWN0dXJlIChVcmJhbiBEZXNpZ24pG01hc3RlciBvZiBBcnRzIGluIEVkdWNhdGlvbh9NYXN0ZXIgT2YgQXJ0cyBJbiBFbmdsaXNoIChPREwpF01hc3RlciBvZiBBcnRzIGluIEhpbmRpGU1hc3RlciBvZiBBcnRzIGluIEhpc3RvcnkjTWFzdGVyIG9mIEFydHMgaW4gUG9saXRpY2FsIFNjaWVuY2UcTWFzdGVyIG9mIEFydHMgaW4gUHN5Y2hvbG9neRlNYXN0ZXIgb2YgQXJ0cyBpbiBQdW5qYWJpI01hc3RlciBvZiBBcnRzIGluIFJlbGlnaW91cyBTdHVkaWVzGk1hc3RlciBvZiBBcnRzIGluIFNhbnNrcml0G01hc3RlciBvZiBBcnRzIGluIFNvY2lvbG9neSFNYXN0ZXIgb2YgQnVzaW5lc3MgQWRtaW5pc3RyYXRpb24rTWFzdGVyIG9mIEJ1c2luZXNzIEFkbWluaXN0cmF0aW9uIChGaW5hbmNlKShNYXN0ZXIgb2YgQnVzaW5lc3MgQWRtaW5pc3RyYXRpb24gKEZZSUMpJ01hc3RlciBPZiBCdXNpbmVzcyBBZG1pbmlzdHJhdGlvbiAoT0RMKRJNYXN0ZXIgb2YgQ29tbWVyY2UYTWFzdGVyIG9mIENvbW1lcmNlIChPREwpJU1hc3RlciBPZiBDb21wdXRlciBBcHBsaWNhdGlvbnMgKE9ETCklTWFzdGVyIG9mIENvbXB1dGVyIEFwcGxpY2F0aW9ucyAoVFlDKRNNYXN0ZXIgb2YgRWR1Y2F0aW9uJ01hc3RlciBvZiBMaWJyYXJ5ICYgSW5mb3JtYXRpb24gU2NpZW5jZSNNYXN0ZXIgb2YgUGxhbm5pbmcgKEluZnJhc3RydWN0dXJlKR5NYXN0ZXIgb2YgUGxhbm5pbmcgKFRyYW5zcG9ydCkaTWFzdGVyIG9mIFBsYW5uaW5nIChVcmJhbikiTWFzdGVycyBpbiBIb3NwaXRhbCBBZG1pbmlzdHJhdGlvbixQRyBESVBMT01BIElOIEJBTktJTkcsIElOU1VSQU5DRSBBTkQgRklOQU5DRTBQb3N0IEdyYWR1YXRlIERpcGxvbWEgaW4gQXBwbGllZCBOdXRyaXRpb24gKE9ETCkyUG9zdCBHcmFkdWF0ZSBEaXBsb21hIGluIEJ1c2luZXNzIE1hbmFnZW1lbnQgKE9ETCkuUG9zdCBHcmFkdWF0ZSBEaXBsb21hIEluIENvbXB1dGVyIEFwcGxpY2F0aW9uczRQb3N0IEdyYWR1YXRlIERpcGxvbWEgSW4gQ29tcHV0ZXIgQXBwbGljYXRpb25zIChPREwpPlBvc3QgR3JhZHVhdGUgRGlwbG9tYSBpbiBKb3VybmFsaXNtICYgTWFzcyBDb21tdW5pY2F0aW9uIChPREwpLlBvc3QgR3JhZHVhdGUgRGlwbG9tYSBpbiBOdXRyaXRpb24gYW5kIEZpdG5lc3MVXgAEMTcxMgQxNzI4BDE3MzMEMTcxNQQxNzE2BDE3MzEEMTcyNwQxNzE3BDE3MzIEMTcwMgQxNzA1BDE3MjMEMTcwNwQxNzM0BDE5MDMEMTkwMQQxNzIxBDE3MTkEMTcxMAQ0NzAyBDQ5MDIEMjcwMgQyNzU3BDI3NzIEMjc2OAQyNzAzBDI3NzMEMjc2MwQyNzc0BDI3MDQEMjcwNQQyNzA2BDI3NTkEMjc1OAQyNzEzBDI3NjUEMjcxNgQyNzE3BDI3ODUEMjc1NgQyNzE4BDI3NzUEMjcxOQQyNzIwBDI3MjEEMjc4OQQyNzIyBDI3MjMEMjc3OAQyNzc5BDI3MjQEMjc4MQQyNzI1BDI3MjYEMjcyNwQyNzc2BDI3MjgEMjc4MgQyNzI5BDI3MzAEMjc2MAQyNzM0BDI3MzUEMjkwNQQyNzM3BDI3MzgEMjc0MAQyNzQxBDI3NDIEMjc0MwQyNzQ0BDI3NDUEMjc0NgQyNzY0BDI3NDcEMjkwMQQyNzQ5BDI5MDcEMjkwMgQyNzUxBDI3NTIEMjc1MwQyNzY3BDI3NzcEMjc2MQQyNzYyBDM3MDIEMzkwNQQzOTAzBDM3MDMEMzkwMgQzOTA0BDM3MDYUKwNeZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZxYBAgpkAgkPEA8WBh8ABQljbGFzc2NvZGUfAQUFY25hbWUfAmdkEBUDEy0gIFNlbGVjdCBTZW1lc3Rlci0sQi5UZWNoLiAoQ29tcHV0ZXIgRW5naW5lZXJpbmcpLCAxc3QgU2VtZXN0ZXIsQi5UZWNoLiAoQ29tcHV0ZXIgRW5naW5lZXJpbmcpLCAzcmQgU2VtZXN0ZXIVAwAGMTcwMjAxBjE3MDIwMxQrAwNnZ2cWAWZkZNexsfMa+8Td4qnJ6GdEvWByMFdpnZnNSQ/F1DpBCUlp',
        '__view_stateGENERATOR': '72A7EE3D',
}


r = s.post('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULT.aspx', data=data)
r = s.get('https://collegeadmissions.gndu.ac.in/studentArea/GNDUEXAMRESULTDISPLAY.aspx')
#form1 > center > table:nth-child(3) > tbody > tr:nth-child(5) > td:nth-child(1) > b:nth-child(2)
with open("response.html", "w") as f:        
    f.write(r.text)

# name = '#form1 > center > table > span:nth-child(3) > tr:nth-child(2) > td:nth-child(1) > b:nth-child(2)'
# rollno = '#form1 > center > table > span:nth-child(3) > tr:nth-child(1) > td:nth-child(1) > b:nth-child(1)'
# regnNo = '#form1 > center > table > span:nth-child(3) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)'
# supply = '#form1 > center > table > span:nth-child(3) > tr:nth-child(2) > td:nth-child(2) > b:nth-child(1)'

soup = BeautifulSoup(r.text, features="lxml")
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
totals['credReg'] = tab3_tr[0].find_all("td")[1].find_all("b")[0].text
totals['gradpoint']  = tab3_tr[0].find_all("td")[3].find_all("b")[0].text
totals['credsEar']  = tab3_tr[1].find_all("td")[1].find_all("b")[0].text
totals['SGPA']      = tab3_tr[2].find_all("td")[1].find_all("b")[0].text
totals['CGPA']      = tab3_tr[3].find_all("td")[1].find_all("b")[0].text

subjects = ["Mechanics", "EGD", "Physics", "Maths", "Material", "Punjabi", "Drug Abuse"]
subject_data = {}
for i in subjects:
    subject_data[i] = {'credits' : '', 'grade' : '', 'gradePoint': ''}  
      
a = 0
for i in subject_data:
    subject_data[i]["credits"]      = tab2_tr[a+1].find_all("td")[5].getText().strip()
    subject_data[i]["grade"]        = tab2_tr[a+1].find_all("td")[6].getText().strip()
    subject_data[i]["gradePoint"]   = tab2_tr[a+1].find_all("td")[7].getText().strip()
    a += 1