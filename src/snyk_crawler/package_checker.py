import os
import json
import shutil
import pprint
import loguru
import pandas as pd

with open("/root/js-malware-detection/src/snyk_crawler/snyk_malware.json", "r") as fp:
    malware_dict = json.load(fp)

update_data = {}

root_dir = "/root/js-malware-detection/datasets/all-the-package-names/"
updated_file = root_dir + "/updated.csv"
df = pd.read_csv(updated_file)
package = df["pkg"].tolist()

for malware in malware_dict.keys():
    if malware in package:
        update_data[malware] = [malware_dict[malware], True]

pprint.pprint(update_data)

# tgz_dir = '/root/js-malware-detection/datasets/npm-latest-samples/tgz'
# dest_dir = '/root/js-malware-detection/datasets/snyk_malware/'

# for malware in update_data.keys():
#     try:
#         shutil.copy(os.path.join(tgz_dir, malware), dest_dir)
#     except Exception as e:
#         loguru.logger.error(e)


