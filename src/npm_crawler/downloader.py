import datetime
import pandas as pd
from crawler import Crawler

if __name__ == '__main__':
    root_dir = "/root/js-malware-detection/datasets/all-the-package-names/"
    updated_file = root_dir + "/updated.csv"
    today = datetime.datetime.now()
    today_num = int(today.strftime('%m%d'))

    # download updated pkgs
    df = pd.read_csv(updated_file)
    for i in range(df.shape[0]):
        date = df.loc[i, 'date']
        pkg = df.loc[i, 'pkg']
        if date == today_num-1:
            crawler = Crawler(pkg)