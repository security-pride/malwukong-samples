import json
import subprocess
import sqlite3
import requests
from datetime import datetime
from multiprocessing import Pool
from functools import partial


class Crawler():
    def __init__(self, package):
        self.package = package
        self.threshold = datetime.fromisoformat('2023-04-01T00:00:00.000')
        self.metadata = self.metadata_crawler()
        if self.metadata != None:
            self.created = datetime.fromisoformat(self.metadata['time']['modified'].replace('Z', ''))
            if self.created > self.threshold:
                self.package_downloader()
    
    def metadata_crawler(self):
        metaurl = 'https://registry.npmjs.org/' + self.package
        response = requests.get(metaurl)
        if response.status_code == 200:
            metadata = response.json()
            return metadata
        else:
            return None

    def package_downloader(self):
        save_dir = '/root/js-malware-detection/datasets/npm-latest-samples/tgz'
        command = f"npm pack {self.package} --pack-destination {save_dir}"
        subprocess.run(command, shell=True)


if __name__ == '__main__':
    # 初始化数据库连接
    conn = sqlite3.connect('npm_pkgs.db')
    cursor = conn.cursor()

    # 创建表（如果不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS package_list
                    (id INTEGER PRIMARY KEY, name TEXT UNIQUE, created TEXT)''')

    with open('/root/js-malware-detection/datasets/all-the-package-names-526.txt', 'r') as f:
        package_names = [line.strip() for line in f.readlines()]


    def processor(package_list):
        for i, package in enumerate(package_list):
            crawler = Crawler(package)
            cursor.execute("INSERT OR REPLACE INTO package_list (name, created) VALUES (?, ?)", (package, crawler.created.strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            
            # 打印进度
            if i % 1000 == 0:
                print(f"已完成{i}个包的查询")
    
    processes = 128
    batch_size = (len(package_names) + processes - 1) // processes
    batched_package_names = [package_names[i:i+batch_size] for i in range(0, len(package_names), batch_size)]
    
    with Pool(processes=processes) as pool:
        pool.map(processor, batched_package_names)

    cursor.close()
    conn.close()