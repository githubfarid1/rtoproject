import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
from itertools import groupby
from operator import itemgetter
import json

def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)
    for i in range(2, len(e) - 1, 2):
        de += chr(int(e[i:i + 2], 16) ^ k)
    return de


getheaders = {
    'authority': 'www.seek.com.au',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,id;q=0.8',
    'cache-control': 'max-age=0',
    'referer': 'https://www.upwork.com/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
}
response = requests.get('https://www.seek.com.au', headers=getheaders)
cookies_dict = response.cookies.get_dict()
cookies = cookies_dict
# breakpoint()
subclass = [6124,6125,6126,6127,6128,6129,6130,6132,6133,6134,6135,6136,6131,6137,6138,6139]
alldata = []
page = 0
urls = []
maxcount = 550
for cl in subclass:
    params = {
        'subclassification': cl, 
    }
    response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    # breakpoint()
    try:
        if "," in soup.find('span', {"data-automation":"totalJobsCount"}).text:
            jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text.replace(",",""))
        else:
            jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text)
    except:
        jobcount = 0

    worktype = [242,243,244,245]
    if jobcount > maxcount:
        for wt in worktype:
            params = {
                'subclassification': cl,
                'worktype': wt, 
            }
            response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            try:
                if "," in soup.find('span', {"data-automation":"totalJobsCount"}).text:
                    jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text.replace(",",""))
                else:
                    jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text)
            except:
                jobcount = 0
            salaryrange = ['0-30000', '30000-40000', '40000-50000', '50000-60000', '60000-70000', '70000-80000', '80000-100000', '100000-120000', '120000-150000', '150000-200000', '200000-250000', '250000-350000', '350000-']
            if jobcount > maxcount:
                for sal in salaryrange:
                    params = {
                        'subclassification': cl,
                        'worktype': wt,
                        'salaryrange': sal 
                    }
                    
                    response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
                    html = response.content
                    soup = BeautifulSoup(html, "html.parser")
                    try:
                        if "," in soup.find('span', {"data-automation":"totalJobsCount"}).text:
                            jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text.replace(",",""))
                        else:
                            jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text)
                    except:
                        jobcount = 0

                    if jobcount > maxcount:

                        #---
                        daterange = 7
                        params = {
                            'subclassification': cl,
                            'worktype': wt,
                            'salaryrange': sal,
                            'daterange': daterange 
                        }
                        
                        response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
                        html = response.content
                        soup = BeautifulSoup(html, "html.parser")
                        try:
                            if "," in soup.find('span', {"data-automation":"totalJobsCount"}).text:
                                jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text.replace(",",""))
                            else:
                                jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text)
                        except:
                            jobcount = 0

                        if jobcount > maxcount:
                            print(jobcount, 'out')
                        # else:
                        print(jobcount, 'subclassification', cl, 'worktype', wt, "salary", sal, "daterange", daterange)
                        # breakpoint()
                        page = 0
                        while True:
                            page += 1
                            params = {
                                'page': page,
                                'subclassification': cl, 
                                'worktype': wt,
                                'salaryrange': sal,
                                'daterange': daterange 
                            }
                            response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
                            html = response.content
                            soup = BeautifulSoup(html, "html.parser")
            
                            print("pagex", page)

                            trs = soup.find_all("article", class_='y735df0')
                            print(len(trs))
                            if len(trs) == 0:
                                break    
                            # dlist = []
                            
                            for tr in trs:
                                atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                                atl =  atl.split('?')[0].replace("/job/","")
                                joblink = atl
                                urls.append(joblink)

                        #---


                    else:
                        print(jobcount, 'subclassification', cl, 'worktype', wt, "salary", sal)
                        # breakpoint()
                        page = 0
                        while True:
                            page += 1
                            params = {
                                'page': page,
                                'subclassification': cl, 
                                'worktype': wt,
                                'salaryrange': sal 
                            }
                            response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
                            html = response.content
                            soup = BeautifulSoup(html, "html.parser")
             
                            print("pagex", page)

                            trs = soup.find_all("article", class_='y735df0')
                            print(len(trs))
                            if len(trs) == 0:
                                break    
                            # dlist = []
                            
                            for tr in trs:
                                atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                                atl =  atl.split('?')[0].replace("/job/","")
                                joblink = atl
                                urls.append(joblink)


            else:
                print(jobcount, 'subclassification', cl, 'worktype', wt)
                page = 0
                while True:
                    page += 1
                    params = {
                        'page': page,
                        'subclassification': cl, 
                        'worktype': wt, 
                    }
                    response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
                    html = response.content
                    soup = BeautifulSoup(html, "html.parser")

                    print("page", page)

                    trs = soup.find_all("article", class_='y735df0')
                    if len(trs) == 0:
                        break    
                    # dlist = []
                    
                    for tr in trs:
                        atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                        atl =  atl.split('?')[0].replace("/job/","")
                        joblink = atl
                        urls.append(joblink)

    else:
        print(jobcount, 'subclassification', cl)
        page = 0
        while True:
            page += 1
            params = {
                'page': page,
                'subclassification': cl, 
            }
            response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
            print("page", page)
            html = response.content
            soup = BeautifulSoup(html, "html.parser")

            trs = soup.find_all("article", class_='y735df0')
            if len(trs) == 0:
                break    
            # dlist = []
            
            for tr in trs:
                atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                atl =  atl.split('?')[0].replace("/job/","")
                joblink = atl
                urls.append(joblink)
        
urlsset = set(urls)
urls = list(urlsset)
print("Found urls:", len(urls))

with open("seekjson4.json", "w") as f:
    json.dump(urls, f)

sys.exit()    
for idx, url in enumerate(urls):
    response = requests.get(url, cookies=cookies, headers=getheaders)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    print(idx, url)
    # breakpoint()
    jb_title = soup.find("h1", {"data-automation":"job-detail-title"}).text
    jb_subtitile = soup.find("span", {"data-automation":"advertiser-name"}).text
    elems =  soup.find_all("span", class_="y735df0 _1iz8dgs4y _1iz8dgsr")
    # breakpoint()
    jb_address = elems[0].text
    jb_jobcat = elems[1].text
    jb_jobtype = soup.find('span', {'data-automation':'job-detail-work-type'}).text
    
    try:
        jb_salary = elems[3].text
    except:
        jb_salary = ""
    
    try:
        loc = jb_address.split(",")[0].strip()
    except:
        loc = ""

    try:
        area = jb_address.split(",")[1].strip()
    except:
        area = ""

    jobdetail = soup.find("div", {"data-automation":"jobAdDetails"})
    emaillist = []
    phonelist = []
    emailstr = ''
    phonestr = ''

    try:
        findcontacts = jobdetail.find_all("span", class_="__cf_email__")
        for fc in findcontacts:
            emaillist.append(decodeEmail(fc.get('data-cfemail')).lower())

    except:
        pass
    if len(emaillist) != 0:
        for ei,email in enumerate(emaillist):
            if email[-3:] == 'for':
                email = email[:-3]
            emaillist[ei] = email
        emailset = set(emaillist)
        emailstr = ', '.join(emailset)


    try:
        findcontacts = soup.find_all("a", {"data-contact-match":"true"})
        for fc in findcontacts:
            if "tel:" in fc.get("href"):
                phonelist.append(fc.get("href").replace("tel:","").strip())
    except:
        pass

    if len(phonelist) != 0:
        for pi, phone in enumerate(phonelist):
            phone = phone.replace(" ","").replace("(","").replace(")","")
            if phone[0] == '0':
                phone = phone[1:]
            if phone[0] != '+':
                phone = "+61" + phone
            phonelist[pi] = phone    
        phoneset = set(phonelist)
        phonestr = ', '.join(phoneset)


    posteddate = ""
    current_date = datetime.today().date()
    for tr  in soup.find_all("div", class_="y735df0 _1iz8dgs6y"):
        try:
            if "Posted" in tr.find('span').text and "ago" in tr.find('span').text:
                postedat = tr.find('span').text.replace("Posted", "").replace("ago", "")
                if "h" in postedat or "m " in postedat:
                    posteddate = current_date.strftime("%d/%m/%Y")
                if "d" in postedat:
                    posteddate = (current_date - timedelta(days=int(postedat.replace("d","")))).strftime("%d/%m/%Y")
                if "mo" in postedat:
                    posteddate = (current_date - timedelta(days=int(postedat.replace("mo","")*30 ))).strftime("%d/%m/%Y")

                break
        except:
            pass

    jobbrief = [f'Job Title: {jb_title}', f'Job Company: {jb_subtitile}', f'Job Location: {jb_address}', f'Job Category: {jb_jobcat}', f'Job Type: {jb_jobtype}', f'Job Posted Date: {posteddate}']
    jobbriefstr = "\n".join(jobbrief)

    # seekstr =  url.replace('https://www.seek.com.au/job/','')
    # joblink = f"https://www.seek.com.au{atl}"
    try:
        jobCategory =  jb_jobcat.split("(")[1][:-1].strip()
    except:
        jobCategory = ""
    try:
        jobSubCategory = jb_jobcat.split("(")[0].strip()
    except:
        jobSubCategory = ""
    joblink =  url
    seekstr =  joblink.replace('https://www.seek.com.au/job/','')
    # joblink = f"https://www.seek.com.au{atl}"

    mdict = {
        "COMPANY ID VALUES": "",
        "companyName": jb_subtitile,
        "CONTACT ID VALUES": "",
        "Email": emailstr, 
        "Phone": phonestr,
        "Recruitment Lead Chase Contact":"",
        "Job Recruiter":"",
        "Lead Source (via import)": "Seek",
        "LatestJobAdTitle": "",# ok
        "Latest jobType": "",# ok
        "Latest jobCompany": "",# ok
        "Latest Job Ad Posted Date":"", #ok
        "JobAdTitle": jb_title,
        "jobType": jb_jobtype,
        "jobCompany": jb_subtitile,
        "JobAdPosted": posteddate,# ok
        # "jobBriefText": jobbriefstr,#
        # "Job Full Description":jobdetail.text,
        "Price": jb_salary,
        "jobAdLocation": loc,
        "jobAdArea": area,
        "jobCategory": jobCategory ,
        "jobSubCategory": jobSubCategory,
        "Seek#":seekstr,
        "joburl": joblink,
    }
    alldata.append(mdict)

finaldata = []
for dl in alldata:
    if ', ' in dl['Email']:
        emails = dl['Email'].split(", ")
        for email in emails:
            cpl = dl.copy()
            cpl['Email'] = email
            finaldata.append(cpl)
        continue
    finaldata.append(dl)
# breakpoint()
emailgroup = []
sortedlist = sorted(finaldata, key=itemgetter('Email'))
for key, value in groupby(sortedlist, key=itemgetter('Email')):
    if key == '':
        continue
    print(key)
    sortedvalue = sorted(value, key=itemgetter('JobAdPosted'), reverse=True)
    for k in sortedvalue:
        mdict = {
            "key": key,
            "data": k
        }
        emailgroup.append(mdict)
        break
        # print(k)
# breakpoint()
for fi, data in enumerate(finaldata):
    if data['Email'] == '':
        continue
    # breakpoint()
    emailsearch = data['Email']
    femail = [item for item in emailgroup if item["key"] == emailsearch]
    # breakpoint()
    finaldata[fi]['LatestJobAdTitle'] = femail[0]['data']['JobAdTitle']
    finaldata[fi]['Latest jobType'] = femail[0]['data']['jobType']
    finaldata[fi]['Latest jobCompany'] = femail[0]['data']['jobCompany']
    finaldata[fi]['Latest Job Ad Posted Date'] = femail[0]['data']['JobAdPosted']

df = pd.DataFrame(finaldata)
df.to_excel("seekjob-with-filter.xlsx", index=False)

# sys.exit()
