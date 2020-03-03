import requests
from bs4 import BeautifulSoup as soup
import newspaper
from newspaper import urls
from validator_collection import validators, checkers
import re

errorLog = open("errorLog.txt","r+")
errorLog.truncate(0)
errorLog = open("errorLog.txt", "a+")
errorLog.write("hello")
