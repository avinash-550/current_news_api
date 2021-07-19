# Current_news_api
An api to fetch current new articles from across varied news sources. It uses mongodb for storing and retrieving data from news sources(indian) parsed through rss feed.


# Entry points

1. **sources**: This simply returns list of all sources with their category in the database. Use these while making 'source' param of 'allnews' entry point.
URI - http://viwarriornewsapi.herokuapp.com/sources

REQUEST - GET

Ex.
```javascript
{
    "sources": [
        {
            "name": "dna",
            "category": "all"
        }, ...
        
```

2. **users**: This entry point is used to register your email address. Upon first time, it adds user to the database and returns back attributes. On subsequent calls with same email, it checks for password and returns user details directly from database. Use this to know your 'dev_key' if forgot. Users require 'dev_key' for accessing news from 'allnews' entry point.

URI - http://viwarriornewsapi.herokuapp.com/users

PARAMS -
Field | Description| Required
------|------------|---------
email | user's email| Yes 
pwd | password|   Yes

REQUEST - POST

RESPONSE - 
Field | Description
------|------------
email | email of user
left_calls | left api calls for allnews entry point(refreshes everyday)
before_time | the time after which 'left_calls' will become 100 again
dev_key | secret developer key for the user

Ex. https://viwarriornewsapi.herokuapp.com/users?email=viwarrior&pwd=viwarrior
```javascript
{
    "email": "viwarrior",
    "left_calls": 96,
    "before_time": "2021-07-19 12:13:35.469000",
    "dev_key": "20210718121335507036"
}
```
3. **allnews**: This entry point is from where news can be accessed. You must have a 'dev_key' to access news(read 2nd entry point). Returns news from low_date to up_date(format - YYYY-MM-DD hh:mm:ss). Date is valid even if only YYYY-MM-DD specified. If nothing is given for low_date and up_date then news from last 3 hours is returned.

URI - http://viwarriornewsapi.herokuapp.com/allnews

PARAMS - 
Field | Description| Required | default
------|------------|----------|--------
dev_key|developer key| Yes | -
source|comma separated list of sources|No|all sources
category|comma separated list of categories|No|'all'
keywords| comma separated keywords to match news|No|not considered
low_date|the lower range on date|No| current time -3 hours
up_date| upper bound on date | No| current time


REQEST - GET

RESPONSE - "news" object
Field | Description
------|------------
pub_date | publication date
title | title of the news
description | news description
summary | short summary of the news
url| news url
image | image url in news article
content| whole text of article
source| news source(agency)
category| category of news(all, business, sports, entertainment etc.)
keywords| list of keywords



Ex.
```javascript
"news": [
        {
            "pub_date": "2021-07-18 01:16:05",
            "title": "With Krishna surging, Jurala lifts five gates",
            "url": "https://www.deccanchronicle.com/nation/in-other-news/180721/with-krishna-surging-jurala-lifts-five-gates.html",
            "description": "MAHABUBNAGAR: Priyadarshini Jurala, the first project of Telangana state on Krishna River, has opened five of its crest gates on Saturday after it started receiving 59,438 cusecs of water",
            "summary": "MAHABUBNAGAR: Priyadarshini Jurala, the first project of Telangana state on Krishna River, has opened five of its crest gates on Saturday after it started receiving 59,438 cusecs of water.\nThe project is releasing 33,908 cusecs of water after using it for generating power.\nOn the same day last year, Jurala had, however, received 89,129 cusecs of water and released 86,826 cusecs of it.\nSince June 1, when the water year began, Jurala has received total of 39.25 tmc of water, with a flood cushion of 1.19 tmc.\nAlamatti Dam in Karnataka upstream of Jurala is receiving 53,502 cusecs and is releasing 42,264 cusecs.",
            "image": "https://s3.ap-southeast-1.amazonaws.com/images.deccanchronicle.com/dc-Cover-9p7sib989iv43l5ik363fav9b7-20210702010115.Medi.jpeg",
            "content": "MAHABUBNAGAR: Priyadarshini Jurala, the first project of Telangana state on Krishna River, has opened five of its crest gates on Saturday after it started receiving 59,438 cusecs of water.\n\nThe project is releasing 33,908 cusecs of water after using it for generating power. 624 cusecs of water is being let out into its canals.\n\nOn the same day last year, Jurala had, however, received 89,129 cusecs of water and released 86,826 cusecs of it. The project has a gross capacity of just 9.66 tmc. The current reservoir level of 1,053.08 feet is just a little short of its total storage capacity of 1,045 feet at FRL. Since June 1, when the water year began, Jurala has received total of 39.25 tmc of water, with a flood cushion of 1.19 tmc.\n\nAn engineer at the project site said that they are not holding any water and releasing inflows continuously.\n\nOn the other hand, Srisaialam Reservoir has received average inflows of 26,045 cusecs during the past 24 hours. The reservoir has only 34.10 tmc of water against its total storage capacity of 215.80 tmc.\n\nAlamatti Dam in Karnataka upstream of Jurala is receiving 53,502 cusecs and is releasing 42,264 cusecs. Narayanpur is getting 45,629 cusecs and allowing 40,608 cusecs to flow out.",
            "source": "deccanchronicle",
            "category": "all",
            "keywords": [
                "total",
                "tmc",
                "reservoir",
                "cusecs",
                "surging",
                "capacity",
                "releasing",
                "project",
                "received",
                "water",
                "lifts",
                "krishna",
                "jurala",
                "gates"
            ]
        }, ...
```

@author - [Avinash](https://github.com/Viwarrior)
