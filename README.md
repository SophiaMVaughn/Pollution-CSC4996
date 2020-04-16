# P.E.A.T.


## Introduction

Pollution Events Aggregation Tool (aka P.E.A.T.) was developed under the direction of Professor Nic DePaula as a group senior capstone given at Wayne State University. Using crawling and scraping of Michigan news sites, the back end collects and filters news articles that are likely to contain a pollution or contamination event, then uses NLP techniques to locate the data of interest. This information is stored in a database, then displayed on the PEAT site.



## Motivation

The motive for developing this tool was to create a resource for residents, politicians and scientists in the state of Michigan to view the aggregated data of pollution events or trends with details and the articles that those details were retrieved from. A tool of this range, detail and type does not exist as of 2020, so the areas of application were unprecedented and fascinating to implement.



## Tech and approaches used

spaCy, regular expressions, POS tagging, [BERT-NER](https://github.com/kamalkraj/BERT-NER), [newspaper](https://github.com/codelucas/newspaper), [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), Bootstrap, CSS, Flask, Google Maps API, HTML



## How to use/application of code

This application is self-contained and fully-functional. There are 2 separate components that are invoked by the 2 core python files, the back end (by main.py) and the front end (by app.py). The main.py must be run first to populate the shared database. After this, app.py can be run to view this data in a meaningful way with the map and table view of this data aggregated in the locations found in the articles.

If you want this application to be self-updating consistently (seeks out recently published articles on the news sites), utilize cron jobs to invoke the main.py, which will rerun the crawling and scraping without your manual interaction with the command line. This will automatically update the database with new articles without removing the old articles.



## INSTALLATION

**NOTE: if you do not have python 3.6.8, some versions may be incompatible. It is highly recommended that you attempt this application with 3.6.8 for the best results. Follow the link below to get the installer.**

Download python 3.6.8 from https://www.python.org/downloads/release/python-368/
(windows -> https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)

Install and add to PATH in environment variables

**Once python 3.6.8 is installed:**

Download out_base from https://drive.google.com/open?id=10GeUFUaEetQvhnKR488n4Tjmho0Rljp0 (download whole file)

Unzip file after download

Move **out_base** folder to the git repository directory (the same level as main.py)


**Use the following commands to install all of the needed modules for both the front end and back end to run as expected.**
```bash
pip3 install mongoengine
pip3 install newspaper3k
pip3 install tqdm
pip3 install -U spacy
python3 -m spacy download en_core_web_sm
python3 -m pip3 install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip3 install pytorch_transformers
pip3 install flask
pip3 install flask_pymongo
pip3 install flask_googlemaps
pip3 install flask_bootstrap
pip3 install googlemaps
```




## Running after installation

**NOTE: the way this application works, for the front end to be of any use, you must run the backend first to populate the database shared between the backend and front end.**

### Running the back end

```bash
python3 main.py
```

After this finishes running, run the following command to start the front end locally.

### Running the front end after running the back end

```bash
python3 app.py
```

Connect to the PEAT site by opening a supported browser (chrome or edge) and navigating to http://127.0.0.1:5000/ while this command is still running in the command line. If the backend successfully found any articles, the map and table pages should reflect that information.



## Credits

[BERT-NER](https://github.com/kamalkraj/BERT-NER)

[newspaper](https://github.com/codelucas/newspaper)

Professor Nic DePaula of WSU



## License

No license. Feel free to use this code as you see fit.
