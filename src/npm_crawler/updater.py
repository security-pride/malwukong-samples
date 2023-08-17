import os
import csv
import json
import datetime
import subprocess
import pandas as pd
from crawler import Crawler

def get_all_the_package_names_today(root_dir, today_string):
    cmd = "wget -O {}/all-the-package-names-{}.json https://raw.githubusercontent.com/nice-registry/all-the-package-names/master/names.json".format(root_dir, today_string)
    subprocess.run(cmd, shell=True)

def calculate_increments(root_dir, today_string, yesterday_string):
    with open(root_dir+"/all-the-package-names-{}.json".format(yesterday_string), 'r') as fp:
        data = json.load(fp)
        yesterday_files = set(data)
    with open(root_dir+"/all-the-package-names-{}.json".format(today_string), 'r') as fp:
        data = json.load(fp)
        today_files = set(data)
    updated_pkgs = today_files.difference(yesterday_files)
    deleted_pkgs = yesterday_files.difference(today_files)
    return updated_pkgs, deleted_pkgs

def write_csv(filename, headers, data):
    if os.path.exists(filename):
        # 如果文件存在，读取表头
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames

        # 追加写入数据
        with open(filename, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            for row in data:
                writer.writerow(row)
    else:
        # 如果文件不存在，新建文件并写入表头和数据
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

def drop_csv_duplicates(filename, headers):
    df = pd.read_csv(filename)
    df.drop_duplicates(inplace=True)
    df.sort_values(by=headers, inplace=True)
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    root_dir = "/root/js-malware-detection/datasets/all-the-package-names/"
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    today_string = today.strftime("%m%d")
    yesterday_string = yesterday.strftime("%m%d")

    # today_string = '0629'
    # yesterday_string = '0627'
    get_all_the_package_names_today(root_dir, today_string)

    updated_pkgs, deleted_pkgs = calculate_increments(root_dir, today_string, yesterday_string)

    updated_data = []
    deleted_data = []
    for pkg in updated_pkgs:
        updated_data.append({
            "date": today_string,
            "pkg": pkg
        })
    for pkg in deleted_pkgs:
        deleted_data.append({
            "date": today_string,
            "pkg": pkg
        })

    updated_file = root_dir + "/updated.csv"
    deleted_file = root_dir + "deleted.csv"
    headers = ["date", "pkg"]

    write_csv(updated_file, headers, data=updated_data)
    drop_csv_duplicates(updated_file, headers)
    write_csv(deleted_file, headers, data=deleted_data)
    drop_csv_duplicates(deleted_file, headers)

    print("update success")

