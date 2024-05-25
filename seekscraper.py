import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import requests
import json
from bs4 import BeautifulSoup
# import pandas as pd
from datetime import datetime
from json import JSONDecoder
from json import JSONEncoder
from openpyxl import Workbook, load_workbook
import argparse
import pandas as pd
from itertools import groupby
from operator import itemgetter
from datetime import datetime, timedelta

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

def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)
    for i in range(2, len(e) - 1, 2):
        de += chr(int(e[i:i + 2], 16) ^ k)
    return de



def parse(urls):
    # urls = []
    alldata = []
    for idx, url in enumerate(urls):
        response = requests.get(url, cookies=cookies, headers=getheaders)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        print(idx, url)
        # breakpoint()
        jb_title = soup.find("h1", {"data-automation":"job-detail-title"}).text
        jb_subtitile = soup.find("span", {"data-automation":"advertiser-name"}).text
        # elems =  soup.find_all("span", class_="y735df0 _1iz8dgs4y _1iz8dgsr")
        # breakpoint()
        # jb_address = elems[0].text
        # jb_jobcat = elems[1].text
        jb_address = soup.find("span", {"data-automation":"job-detail-location"}).text
        jb_jobtype = soup.find('span', {'data-automation':'job-detail-work-type'}).text
        jb_jobcat = soup.find('span', {'data-automation':'job-detail-classifications'}).text

        
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

def savedata(alldata):
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


def main():
    parser = argparse.ArgumentParser(description="SEEK Scraper")
    parser.add_argument('-start', '--start', type=str,help="Start number")
    parser.add_argument('-end', '--end', type=str,help="End number")

    args = parser.parse_args()
    if args.start == None or args.end == None:
        print('use: python seekscraper.py -start <start_index> -end <end_index>')
        exit()
    with open("fileresult/urls.json", "r") as jsdata:
        ids = json.load(jsdata)
    urls = ["https://www.seek.com.au/job/"+id for idx, id in enumerate(ids) if idx >= int(args.start)-1 and idx < int(args.end)]

    alldata = parse(urls)
    print(alldata)
    
if __name__ == '__main__':
    main()