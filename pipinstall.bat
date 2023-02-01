@echo off

winget install --id Git.Git -e --source winget
pip install undetected-chromedriver
pip install datetime
pip install bs4
pip install lxml

pause
exit