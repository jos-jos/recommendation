'''
'''
import re
import time
import requests,json
from datetime import datetime
from hyper.contrib import HTTP20Adapter
from bs4 import BeautifulSoup
from tqdm import tqdm, trange
import os
import sys

from config import *

os.environ['NO_PROXY'] = 'xiaoyuan.zhaopin.com'

url = IT_url
path_list = IT_path_list
save_path = "./it_data/it_data"

org_headers = {
        "authority": "xiaoyuan.zhaopin.com",
        "method": "GET",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "x-zp-client-id=aa7b2131-b3de-4dce-b0c7-7be5ab0c854a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217c6ad9278845f-0f1158fc4713748-5373e62-1327104-17c6ad9278916e%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217c6ad9278845f-0f1158fc4713748-5373e62-1327104-17c6ad9278916e%22%7D; at=bedc564d0a244eeda99921e3d2ef52b7; rt=5867bfaf23704190a35c4ce6379638d3; acw_tc=ac11000116339271063154950e00ca9009ae2995d0ec3b91ad9adf50ecbaa6",
        "referer": "https://xiaoyuan.zhaopin.com/search/jn=2&pg=5",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }

payload = {
        "caseName": "",
        "caseNo": "",
        "caseReason": "",
        "content": "",
        "courtName": "",
        "involvedAmtMax": "",
        "involvedAmtMin": "",
        "isExactlySearch": "",
        "judgeDateBegin": "",
        "judgeDateEnd": "",
        "pageSize": "20",
        "party": "xxx",
        "publishDateBegin": "",
        "publishDateEnd": "",
        "searchKey": ""
    }
data = json.dumps(payload)

def details(jobId):
    #headers = org_headers
    #headers["path"] = path_list[0]
    #sessions=requests.session()
    #sessions.mount('https://xiaoyuan.zhaopin.com', HTTP20Adapter())
    #res=sessions.get('https://xiaoyuan.zhaopin.com/api/job/detail?jobNumber=%s'%jobId,headers=headers,data=data)
    requests.packages.urllib3.disable_warnings()
    res = requests.get('https://xiaoyuan.zhaopin.com/api/job/detail?jobNumber=%s'%jobId, verify=False)
    soup = re.sub("\\<.*?\\>", "", str(BeautifulSoup(res.text, 'lxml')))
    text_dir =json.loads(soup)["data"]["data"]["data"]
    key_soup = ['Address', 'ApplyEndDate', 'ApplyStartDate', 'Benefits', 'BenefitsName', 'CityName', 'CompanyAccountNumber', 'CompanyId', 'CompanyLogoUrl', 'CompanyName', 'CompanyShortName', 'CountyName', 'CreatedBy', 'DateRefresh', 'Education', 'EducationRequired', 'ExpectPostQuantity', 'HeadCount', 'IsShowCompanyInfo', 'JobAccountNumber', 'JobCategory', 'JobCategoryName', 'JobDescription', 'JobId', 'JobNature', 'JobSubCategory', 'JobSubCategoryName', 'JobTag', 'JobTagName', 'JobTitle', 'LanguageRequired', 'MajorData', 'MaxSalary', 'MinSalary', 'NeedSchool', 'RootCompanyAccountNumber', 'RootCompanyId', 'RootCompanyName', 'RootCompanyShortName', 'SalaryMonths', 'Status', 'fromCompanyName']
    useful_key_soup = ['Education', 'JobCategoryName', 'JobDescription', 'JobSubCategoryName', 'JobTitle', 'MajorData', 'RootCompanyName', 'fromCompanyName']
    useful_result = {}
    for key in useful_key_soup:
        if isinstance(text_dir[key], list):
            useful_result[key] = "，".join(text_dir[key])
        elif isinstance(text_dir[key], str):
            useful_result[key] = text_dir[key]
        else:
            useful_result[key] = "None"

    return useful_result

def main_pe(useful_dirt, index):
    headers = org_headers
    headers["path"] = path_list[index]

    sessions=requests.session()
    sessions.mount('https://xiaoyuan.zhaopin.com', HTTP20Adapter())
    res=sessions.get(url[index],headers=headers,data=data)

    text = res.text.replace("[]", "null").replace(":,", ":0,")
    text_dir =json.loads(text)

    key_text = ['code', 'message', 'data']
    key_data = ['data', 'statusCode', 'statusDescription', 'taskId']
    key_data_data = ['attachments', 'count', 'filter', 'isApprovedInvestment', 'isEndPage', 'isVerification', 'list', 'method', 'methodGroup', 'modularState', 'nullException', 'purposeOptimize', 'typeSearch']
    key_data_data_list = ['applyType', 'chatWindow', 'cityDistrict', 'cityId', 'companyId', 'companyLogo', 'companyName', 'companyNumber', 'companyRootId', 'companyScaleTypeTagsNew', 'companySize', 'companyUrl', 'deliveryPath', 'distance', 'education', 'extensions', 'hasAppliedPosition', 'industryName', 'jobId', 'liveCard', 'matchInfo', 'menVipLevel', 'name', 'needMajor', 'number', 'positionCommercialLabel', 'positionHighlight', 'positionSourceType', 'positionSourceTypeUrl', 'positionURL', 'positionUrl', 'property', 'publishTime', 'recallSign', 'recruitNumber', 'rpoProxied', 'rpoProxy', 'salary60', 'salaryCount', 'salaryReal', 'skillLabel', 'staffCard', 'tagABC', 'tradingArea', 'welfareLabel', 'workCity', 'workType', 'workingExp']

    useful_name = "name"
    useful_key = ["cityId", "companyName", "companySize", "number", "education", "industryName", "positionURL", "property", "publishTime", "recruitNumber", "salary60", "salaryReal", "staffCard", "workCity", "workType"]

    for text in text_dir['data']['data']['list']:
        temp_index = 1
        temp = text[useful_name]
        while temp in useful_dirt.keys():
            temp = text[useful_name] + "-%d"%temp_index
            temp_index += 1
        useful_dirt[temp] = {}
        for key in useful_key:
            useful_dirt[temp][key] = text[key] 
        temp_useful_dirt = details(text["number"])
        #useful_dirt[temp][key] = temp_useful_dirt
        for key, value in temp_useful_dirt.items():
            useful_dirt[temp][key] = value

def dirt2csv(useful_dirt, file_name):
    useful_key = ["name", "companyName", "companySize", "education", "industryName", "positionURL", "property", "publishTime", "recruitNumber", "salary60", "salaryReal", "workCity", "workType", 'Education', 'JobCategoryName', 'JobDescription', 'JobSubCategoryName', 'JobTitle', 'MajorData', 'RootCompanyName', 'fromCompanyName']
    with open(file_name+".csv", "w", encoding="utf-8") as f:
        temp = ""
        for i in useful_key:
            temp += i + ","
        f.write(temp[0:-1])
        f.write("\n")
        for key, data in useful_dirt.items():
            temp = key + ","
            for i in useful_key[1:]:
                temp += str(data[i]) + ","
            f.write(temp[0:-1])
            f.write("\n")

def update_data():
    code_time = '%s' % time.strftime("%Y-%m-%d")
    os.makedirs(os.path.join(sys.path[0], "data"), exist_ok=True)
    file_name = os.path.join(os.path.join(sys.path[0], "data"), code_time)
    useful_dirt = {}
    for i in trange(len(url)):
        main_pe(useful_dirt, i)
    js = json.dumps(useful_dirt, indent=4, separators=(',', ':'), ensure_ascii=False)
    dirt2csv(useful_dirt, file_name)
    with open(file_name+".json", "w", encoding="utf-8") as f:
        f.write(js)


if __name__ == "__main__":
    update_data()
