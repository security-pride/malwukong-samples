from setuptools import setup, find_packages
from glob import glob

setup(
    name="prismstudio",
    version="1.1.1",
    description="Python Extension for PrismStudio",
    author="Prism39",
    author_email="jmp@prism39.com",
    url="https://www.prism39.com",
    packages=find_packages(),
    platforms="nt",
    python_requires=">=3.8",
    data_files=[("pyarmor_trasnfor", glob("prism/pytransform/*"))],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        "pandas==1.4.1",
        "pytest==7.1.1",
        "mypy==0.941",
        "pyarrow==8.0.0",
        "multivolumefile==0.2.3",
        "urllib3==1.26.9",
        "tqdm==4.64.0",
        "orjson==3.7.3",
        "ipywidgets==7.7.1",
        "requests==2.26.0",
        "pyarmor==7.6.1",
        "setuptools==58.1.0",
        "wheel==0.37.1",
        "twine==4.0.1",
        "pydantic==1.10.2",
        "pyzmq==24.0.1"
    ],
    include_package_data=True
)