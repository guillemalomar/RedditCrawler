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

![alt text][logo]

[logo]: https://raw.githubusercontent.com/guillemnicolau/RedditCrawler/master/documentation/ApplicationArchitecture.png "Application Architecture"

## Using the application

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

## Decisions taken
