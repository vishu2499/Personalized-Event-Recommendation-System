# AMIGOS - Personalized Event Recommendation System

## A powerful recommendation system for suggesting events based on user's web browsing history and intra-website browsing patterns.

### Features of the project

- showing trending events
- Showing trending events by category
- Extracting keywords from Event's title and description using TF*IDF algorithm
- Calculating similarities between the events.
- Recommendation of events based on past intra-website search
- Recommendation of events based on intra-website browsing patterns
- Extracting user's web history using **history_extractor_extension** 
- Calculating similarities between user's web history and events and based on that provide recommendations.
- Recommending local events only.



### Following is the technology stack

<img alt="JavaScript" src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/> <img alt="HTML5" src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"/> <img alt="CSS3" src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"/> <img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/> <img alt="Bootstrap" src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"/> <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white"/> <img alt="SASS" src="https://img.shields.io/badge/SASS-hotpink.svg?style=for-the-badge&logo=SASS&logoColor=white"/> 





**Note**: Code is available on master branch

### How to run?

Download the project using below command

`Git clone https://github.com/vikramBhavsar/Event-Recommendation-System.git`

Change directory using: 

`cd Event-Recommendation-System`
Find out all the branches of the repo:

`git branch -a`

Checkout to the remote master branch using following command:

`git checkout remotes/origin/master`
The project needs **Django==3.0.7 (or above)** and **Python 3.5** and above. It is recommended that the user runs the project in a virtualenv. Check out the link below on [setting up virtualenv using python] (https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)

Following are list of dependencies that can be installed using **pip install** 

- `pip install pandas` - (for handling CV data)
- `pip install sklearn` - (for training and keyword extraction)
- `pip instal geopandas` - (for recommendation of local events)
- `pip install geopy` - (for recommendation of local events)
- `pip install folium` - (mostly not required)



Once all the dependencies are installed make sure the database is in correct state using following commands

`python manage.py makemigrations` and  `python manage.py migrate` 

The github repository contains pre-calculated similarity of events, keywords etc. If in case a new CSV is provided or to be used then few scripts are needed to run prior the execution of the project. These scripts calculate the similarities between events, extract keywords etc and fill in the models with those data. Following is the order in which scripts need to be run. Also make sure that the user is in virtualenv created using python.

- `python add_events_data_to_models_from_csv.py`
- `python add_categories_to_events.py` 
- `python add_keywords_to_events.py`
- `python add_similarity_to_events.py`

Once everything is setup, user can run the project using following command: `Python manage.py runserver <port-number>` Here port-number is optional 

For personalized Recommendation we need to install **History Extractor Extension** on google chrome browser. Chromium browser does not work with handling location. To install the google chrome extension follow the below steps:

- Open chromeClick on the 3 dots on top right hand side and open settings
- Open Extensions from the left hand menu.
- Activate developer mode option on top right side.
- Click on load Unpacked.
- Go to our **Event-Recommendation-System** folder and select the folder which is named **history_extractor_extension** The browser extension will successfully install itself.

## The project is now ready to run.
