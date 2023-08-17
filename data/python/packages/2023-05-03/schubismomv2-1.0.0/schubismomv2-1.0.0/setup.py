from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = "pypiuser583"
LONG_DESCRIPTION = "pypiuser583"

# Setting up
setup(
    name="schubismomv2",
    version=VERSION,
    author="SuSB0t",
    author_email="nick.faltermeier@gmx.de",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)