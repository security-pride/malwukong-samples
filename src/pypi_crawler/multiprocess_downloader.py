from multiprocessing import Pool, Manager
import os
import sqlite3
from google.oauth2 import service_account
import pandas_gbq
import numpy as np
import subprocess
import json
import pickle
import signal

from pypi_query import get_download_url, get_big_query_info


def package_downloader(package_url, package_date):
    save_dir = '.../pypi-samples/{}/'.format(package_date)
    tmp_dir = '.../pypi-samples/{}/tmp/'.format(package_date)
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    package_path = save_dir+'/tmp/'+package_url.rsplit("/",1)[1]
    command = f"curl -L {package_url} -o {package_path}"
    if 'files.pythonhosted.org' in package_url:
        command = 'proxychains -q ' + command
    subprocess.run(command, shell=True)
    file = tarfile.open(package_path)
    file.extractall(path = save_dir)


def package_logger(key, value, result_queue):
    result_queue.put((key, value))


def big_query_info_analysis(arg):
    res_list, result_queue = arg
    for res in res_list:
        package_name = res[0]
        package_version = res[1]
        package_upload_time= res[2].strftime("%Y-%m-%d %H:%M:%S")
        package_date = package_upload_time.split(' ')[0]
        error = False
        try:
            download_url = get_download_url(package_name, package_version)
            package_downloader(download_url, package_date)
            package_logger((package_name, package_version), [package_name, package_version, download_url, package_upload_time, error], result_queue)
        except:
            error = True
            package_logger((package_name, package_version), [package_name, package_version, download_url, package_upload_time, error], result_queue)

def pool_processing(package_list):
    package_list_filtered = []
    for p in package_list:
        package_name = p[0]
        package_version = p[1]
        package_upload_time= p[2].strftime("%Y-%m-%d %H:%M:%S")
        package_date = package_upload_time.split(' ')[0]
        if os.path.exists(f"../pypi-samples/{package_date}/{package_name}-{package_version}"):
            print(f"Already exists: {package_name} == {package_version}")
            continue
        package_list_filtered.append(p)
    package_list = package_list_filtered

    log_path = '../log.pickle'
    processes = 16
    batch_size = (len(package_list) + processes - 1) // processes
    batched_package_names = [package_list[i:i+batch_size] for i in range(0, len(package_list), batch_size)]
    manager = Manager()
    result_queue=manager.Queue()

    results = {}
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            results = pickle.load(f)

    args =[]
    for p in batched_package_names:
        args.append((p, result_queue))

    with Pool(processes=processes, initializer=signal.signal, initargs=(signal.SIGINT, signal.SIG_IGN)) as pool:
        try:
            pool.map_async(big_query_info_analysis, args)
            while True:
                k,v = result_queue.get()
                results[k] = v
        finally:
            with open(log_path, "wb") as f:
                pickle.dump(results, f)
        print("Download finished!")


if __name__ == '__main__':
    
    package_list = get_big_query_info()
    pool_processing(package_list)
