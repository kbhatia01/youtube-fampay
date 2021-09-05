<h1>Setup</h1>
To set up this project follow below steps:

* Clone repository
* enter keys in .env file
* replace spring-gift-270312-95978d74290d.json with your google service json file
* run command `docker-compose build`
* again run ` docker-compose up -d`

<h1>How to call the API:</h1>

**Base url:** localhost:8000/youtube/

Everything is in get request format

to seach anything in title/description pass query parameter
seach=**something**

for example:
http://localhost:8000/youtube/?search=Brazil

and to sort the data pass additional query parameter `sort_by`


http://localhost:8000/youtube/?search=Brazil&sort_by=-publishedAt

sort_by can take values like `'publishedAt', 'title', '-publishedAt', '-title'`


anything apart form given values passed in sort_by will be considered as sort by publishedAt as default
