import requests
from bs4 import BeautifulSoup as soup
import newspaper
from newspaper import urls
from validator_collection import validators, checkers
import re
from tqdm import tqdm
import time
from colorama import Fore

colors = Fore.__dict__





