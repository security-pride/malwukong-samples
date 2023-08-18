# MalWuKong-Samples

The repository provides samples of malicious code poisoning in OSS supply chains detected by MalWuKong and related security communities. We are actively maintaining the list and hope to contribute to the understanding and mitigation of supply chain attacks.

# Environment
Use conda for environments creation and setup.
```bash
conda create -n <your_env_name> python=3.7

source activate

conda activate <your_env_name>

cd src

pip install -r requirements.txt
```


# To Run the Crawler

```bash
# PyPI Crawler
# To get pkgs within specified durations:
python src/pypi_crawler/multiprocess_downloader.py

# NPM Crawler
# To get all the npm pkg list:
python src/npm_crawler/crawler.py
# To update pkg list day by day:
python src/npm_crawler/updater.py
# To download the updated pkgs:
python src/npm_crawler/downloader.py

# Snyk Crawler(NPM)
# To get the npm malware list reported by Snyk
python src/snyk_crawler/snyk_crawler.py
# For cross-validation with local pkgs
python src/snyk_crawler/package_checker.py
```

# The Advisories that Tracks Malicious Pkgs

- [Snyk Database](https://security.snyk.io/vuln)

- [OSV Database](https://osv.dev/)

# Acknowledgement 

This repo  is credited to [all-the-package-names](https://github.com/nice-registry/all-the-package-names).
