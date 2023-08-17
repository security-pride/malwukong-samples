import json
import requests
from bs4 import BeautifulSoup

baseurl = "https://security.snyk.io/vuln/npm/"

malware_dict = {}

for page in range(1,31):
    url = baseurl + str(page)
    # 发送HTTP GET请求
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tbody = soup.find("tbody")
        if tbody:
            tr_list = tbody.findAll("tr")
            for tr in tr_list:
                td_list = tr.findAll("td")
                assert(len(td_list) == 4)
                published = td_list[3].text.strip()
                a_list = tr.findAll("a")
                assert(len(a_list)==2)
                type = a_list[0].text.strip()
                package = a_list[1].text.strip()
                if type == "Malicious Package":
                    malware_dict[package] = published
        else:
            print("未找到tbody标签")
    else:
        print("请求失败")

with open("/root/js-malware-detection/src/snyk_crawler/snyk_malware.json", "w+") as fp:
    json.dump(malware_dict, fp, indent=4)
