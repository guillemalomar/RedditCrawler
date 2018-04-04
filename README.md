# RedditCrawler

*    Title: Reddit Crawler     
*    Author: Guillem Nicolau Alomar Sitjes      
*    Initial release: September 1st, 2017                     
*    Code version: 0.1                         
*    Availability: Public     

**Index**
* [Requirements](#requirements)
* [Documentation](#documentation)
    * [Project Structure](#project-structure)
    * [Explanation](#explanation)
* [Using the application](#using-the-application)
    * [Executing](#executing)
    * [Testing](#testing)
* [Decisions taken](#decisions-taken)

## Requirements

- Python 2.7 (not tested on python3, at least the prints should be removed) 
- lib xml (lxml): pip install lxml
- Web.py: pip install web.py
- Praw: pip install praw==3.6.0
- Unidecode: pip install unidecode

## Documentation

### Explanation

This project is all about obtaining data from Reddit, processing it, and showing it to the user. It presents a Client-Server architecture, featuring a RestAPI server, which is backed by a SQLite database.

### Project Structure

- Application Architecture

![alt text][logo]

[logo]: https://github.com/guillemnicolau/RedditCrawler/blob/master/documentation/ApplicationArchitecture.png?raw=true "Application Architecture"

- Files and Folders

![alt text][logo2]

[logo2]: https://github.com/guillemnicolau/RedditCrawler/blob/master/documentation/FoldersOrganization.png?raw=true "Folders and Files"


## Using the application

### First of all
- I recommend creating a virtualenv for this project. After creating it, you should run:
```
~/RedditCrawler$ pip install -r requirements.txt
```
Now all pip packages needed have been installed.

### Executing
- Running the server

First of all, the user should start by running the server. This is done this way:
```
~/RedditCrawler$ python src/rest_api/rest_api.py
```
If this has worked correctly, this should be the output:`
```
http://localhost:8080/
```
- Executing the client application

Now that the server is running, we can execute the application. This is done by typing this:
```
~/RedditCrawler$ python src/reddit_crawler.py
```
### Testing

Some tests have been added to the 'tests' folder. To run them, simply type from the main project folder:
```
nosetests tests
```

## Decisions taken

To do this project I followed some basic instructions, but the specific components and architecture had to be chosen by me.
This wasn't the first time I implemented a RESTful API (see https://github.com/guillemnicolau/SongsPlatform), and neither that I used a SQL database.

- Database

When choosing the database I decided to use SQLite3 after pondering between the mentioned one and MongoDB (those seemed to be the most mentioned on the web for small-scale projects). After seeing this post in StackOverflow about their comparison (https://stackoverflow.com/questions/9702643/mysql-vs-mongodb-1000-reads) I thought that in this case all inserts would be done once in a while, maybe once every 6 hours (Subreddit top pages don't change really often, it's not like tweeter, so with that periodicity would be enough to have an ~updated database). After thinking about this, and seeing that SQLite is faster than MongoDB for selects when the number of tables is not over +100, I decided to use SQLite3.

- Reddit library

About the library to retrieve data from Reddit, I chose PRAW. This was quite an easy decision. There are not many alternatives, and after doing some research I knew it had all functionalities that I needed.
Another possibility was to filter all data from the webpage myself, but after checking how it was structured, and knowing that I have close to no experience in web crawlers, for me it was clear that using PRAW was the best decision.

- Application Architecture

Another important decision was the location of the database. At first the architecture was quite different from the final one. The database was located independently from both the server and the client, and it could be accessed both from the server and the processing module. Although this probably would lead to a better performance, it was contrary to the philosophy of a RESTful API. So in the end I decided to only be able to access it through the server, as that's the logical way to design it. The crawlers module was also located in the client module at the beginning, but it makes more sense to be located in the server, as this way it can connect directly to the Subreddit webpage.

test: new_user@mail_service.com
