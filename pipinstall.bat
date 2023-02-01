@echo off

winget install --id Git.Git -e --source winget
pip install undetected-chromedriver
pip install datetime
pip install bs4
pip install lxml
pip install git+https://github.com/lukect/undetected-chromedriver.git selenium~=4.8.0


pause
exit