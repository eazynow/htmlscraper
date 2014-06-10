# HTMLScraper

HTMLScraper is a python library used to scrape data from html web pages.

## Installation
The scraper requires requests to run. It was developed using Python 2.7.5.

## Usage
To use the scraper you need to tell it what to scrape and what to look for. The scraping works by setting up _listeners_.

Each listener listens for a piece of data. That data could be an individual string of a repeating set of data. Below is the structure of a listener:

    {
        "key": "",
        "path": "",
        "listento": "",
        "attribute": "",
        "default": "",
        "class"
    }

* key defines the name to use in the output json that is produced.
* path is where to find the tag in the html. The path should be separated by spaces, for example "html body div input". Partial paths can also be used, for example "div div span span"
* listento defines when to listen. Options are _start_ and _data_. _start_ is used when looking for the opening tag via the path, for example to get an attribute of it. _data_ is used to get the data just after the tag in the path, for example a label.
* attribute is the attribute to get if listening to a start event
* class is an optional filter on the class that the tag should be
* default is an optional attribute. If not set then it will be an empty string. If set to [] then it will be an empty list. When set to [], it will collect all instances of the listener into a list


## Meta
Written by Erol Ziya
Released under MIT License
