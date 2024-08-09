import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
from itertools import groupby
from operator import itemgetter
import json
import setting as s

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
subclass = s.SUBCLASSIFICATIONS
alldata = []
page = 0
urls = []
maxcount = 550
print("Get URLs started", end="...")
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
    # breakpoint()
    worktype = [242,243,244,245]
    if jobcount > maxcount:
        for wt in worktype:
            print(".", end="", flush=True)
            params = {
                'subclassification': cl,
                'worktype': wt, 
            }
            response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
            html = response.content
            # breakpoint()
            soup = BeautifulSoup(html, "html.parser")
            try:
                if "," in soup.find('span', {"data-automation":"totalJobsCount"}).text:
                    jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text.replace(",",""))
                else:
                    jobcount = int(soup.find('span', {"data-automation":"totalJobsCount"}).text)
            except:
                jobcount = 0
            salaryrange = ['0-30000', '30000-40000', '40000-50000', '50000-60000', '60000-70000', '70000-80000', '80000-100000', '100000-120000', '120000-150000', '150000-200000', '200000-250000', '250000-350000', '350000-']
            # salaryrange = ['0-', '30000-', '40000-', '50000-', '60000-', '70000-', '80000-', '100000-', '120000-', '150000-', '200000-', '250000-', '350000-']

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
                        # breakpoint()
                        print(".", end="", flush=True)

                        # if jobcount > maxcount: ##
                            # print(jobcount, 'out') ##
                        # else:
                        # print(jobcount, 'subclassification', cl, 'worktype', wt, "salary", sal, "daterange", daterange) ##
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
                            print(".", end="", flush=True)

                            # print("page", page) ##
                            
                            trs = soup.find_all("article", class_='_4603vi0')
                            # print(len(trs)) ##
                            # breakpoint()
                            print(".", end="", flush=True)

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
                        # print(jobcount, 'subclassification', cl, 'worktype', wt, "salary", sal) ##
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
             
                            # print("page", page) ##
                            print(".", end="", flush=True)
                            trs = soup.find_all("article", class_='_4603vi0')
                            # print(len(trs)) ##
                            if len(trs) == 0:
                                break    
                            # dlist = []
                            
                            for tr in trs:
                                atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                                atl =  atl.split('?')[0].replace("/job/","")
                                joblink = atl
                                urls.append(joblink)


            else:
                # print(jobcount, 'subclassification', cl, 'worktype', wt) ##
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

                    # print("page", page) ##
                    print(".", end="", flush=True)
                    trs = soup.find_all("article", class_='_4603vi0')
                    if len(trs) == 0:
                        break    
                    # dlist = []
                    
                    for tr in trs:
                        atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                        atl =  atl.split('?')[0].replace("/job/","")
                        joblink = atl
                        urls.append(joblink)

    else:
        # print(jobcount, 'subclassification', cl) ##
        page = 0
        while True:
            page += 1
            params = {
                'page': page,
                'subclassification': cl, 
            }
            response = requests.get('https://www.seek.com.au/jobs-in-education-training', params=params, cookies=cookies, headers=getheaders)
            # print("page", page) ##
            print(".", end="", flush=True)

            html = response.content
            soup = BeautifulSoup(html, "html.parser")

            trs = soup.find_all("article", class_='_4603vi0')
            if len(trs) == 0:
                break    
            # dlist = []
            
            for tr in trs:
                atl = tr.find("a", {"data-automation":"job-list-view-job-link"}).get('href')
                atl =  atl.split('?')[0].replace("/job/","")
                joblink = atl
                urls.append(joblink)
        
urlsset = set(urls)
urlsunique = list(urlsset)
print("Found urls:", len(urls), len(urlsunique))

with open(s.RESFOLDER + os.path.sep + "urls.json", "w") as f:
    json.dump(urlsunique, f)
