import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from itertools import groupby
from operator import itemgetter
import pandas as pd
import setting as s
import json
import argparse

def savedata(alldata, filename):
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
        # print(key)
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
    df.to_excel(s.RESFOLDER + os.path.sep + filename, index=False)

def main():
    parser = argparse.ArgumentParser(description="SEEK Scraper")
    parser.add_argument('-o', '--output', type=str,help="File output")

    args = parser.parse_args()
    if not args.output:
        print('use: python saveseekdata.py -o <filename>')
        exit()

    if args.output and args.output[-5:] != '.xlsx':
        print('use: python saveseekdata.py -o <filename>')
        exit()

    files = [f for f in os.listdir(s.RESFOLDER) if os.path.isfile(os.path.join(s.RESFOLDER, f))]
    
    jsonfiles = []
    for file in files:
        if "jsondata" in file:
            jsonfiles.append(file)
    alldata = []
    for file in jsonfiles:
        with open(s.RESFOLDER + os.path.sep + file, "r") as jsdata:
            data = json.load(jsdata)
            alldata.extend(data)

    savedata(alldata=alldata, filename=args.output)
    print("File saved in", s.RESFOLDER + os.path.sep + args.output, "Success")
    
if __name__ == '__main__':
    main()
