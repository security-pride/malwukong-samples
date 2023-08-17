import os
import sqlite3
import datetime
import tarfile
import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account
from pandas import Timestamp
from pypi_simple import PyPISimple
import pandas_gbq
import numpy as np
import subprocess
import json
import datetime
import tarfile
import requests
from bs4 import BeautifulSoup
import pickle
import signal

def get_download_url(package_name, package_version):
    try:
        with PyPISimple(endpoint="https://pypi.tuna.tsinghua.edu.cn/simple/") as client:
            requests_page = client.get_project_page(package_name)
            package_list = requests_page.packages
            package_list = [i for i in package_list if i.package_type=='sdist']
            for package in package_list:
                if package.version == package_version:
                    url = package.url
                    return url
    except:
        pass
    try:
        with PyPISimple() as client: # endpoint="https://pypi.tuna.tsinghua.edu.cn/simple/"
            requests_page = client.get_project_page(package_name)
            package_list = requests_page.packages
            package_list = [i for i in package_list if i.package_type=='sdist']
            for package in package_list:
                if package.version == package_version:
                    url = package.url
                    return url
            header = {'user-agent': 'Mozilla/5.0'} 
            req = requests.get('https://pypi.org/project/{}/{}/#files'.format(package_name,package_version), headers = header)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            for item in soup.select('div[class="card file__card"] a'):
                detail_url = item.get('href')
                if '.tar.gz' in detail_url:
                    url = detail_url
                    return url
    except:
        print(f"Can't find {package_name}=={package_version}")

def get_datestamp(date):
   return datetime.datetime.strptime(date.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S").timestamp()

def get_big_query_info():
    ## Replace with your own credentials and project information.
    credentials = service_account.Credentials.from_service_account_info(
        {
            ## Replace with your own credentials.
        })

    sql = """
    SELECT name, version, upload_time
    FROM `bigquery-public-data.pypi.distribution_metadata` 
    WHERE upload_time BETWEEN '2023-xx-xx 0:0:0 UTC' and '2023-xx-xx 23:59:59 UTC' 
    """
    res_df = pandas_gbq.read_gbq(sql, project_id='xxxx', credentials=credentials)
    res_array = np.array(res_df)
    res_list = res_array.tolist()
    return sorted(res_list,key=lambda date:get_datestamp(date[2]))
