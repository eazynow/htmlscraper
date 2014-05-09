import requests
from HTMLParser import HTMLParser


class HTMLScraper(HTMLParser):
    """
    HTMLScraper subclasses the python html parser and adds
    support to scrape the web directly.
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # the http status code
        self.status_code = None
        self.tagPath = []
        self.elemAttrs = {}
        self.scraped = {}
        self.listeners = []

    def scrape(self, url):
        r = requests.get(url)

        self.status_code = r.status_code

        if self.status_code == 200:
            self.__set_defaults(url)

            # now pass the html into HTMLParser
            self.feed(r.text)

    def __set_default(self, listener):
        self.scraped[listener["key"]] = listener["default"]

    def __set_defaults(self, url):
        self.scraped["url"] = url
        map(self.__set_default,
            filter(lambda l: l["key"] not in self.scraped, self.listeners))

    def __path_check(self, pathToCheck):
        pathList = pathToCheck.split()
        return self.tagPath[len(pathList)*-1:] == pathList

    def __attr_check(self, listener, attribs):
        for attrib in attribs:
            if attrib in listener:
                if attrib not in self.elemAttrs:
                    return False

                if isinstance(self.elemAttrs[attrib], list):
                    if listener[attrib] not in self.elemAttrs[attrib]:
                        return False
                elif self.elemAttrs[attrib] != listener[attrib]:
                    return False
        return True

    def __set_scraped_value(self, key, data):
        if isinstance(self.scraped[key], list):
            self.scraped[key].append(data)
        else:
            self.scraped[key] = data

    def __process_listener(self, listener, data=None):
        if not self.__path_check(listener["path"]):
            return

        if not self.__attr_check(listener, ["id", "class"]):
            return

        if "attribute" in listener and listener["attribute"] in self.elemAttrs:
            data = self.elemAttrs[listener["attribute"]]

        self.__set_scraped_value(listener["key"], data)

    def handle_starttag(self, tag, attrs):
        if tag != 'br':
            self.tagPath.append(tag)

            self.elemAttrs = dict(attrs)
            if 'class' in self.elemAttrs:
                self.elemAttrs["class"] = self.elemAttrs["class"].split()

            map(lambda x: self.__process_listener(x),
                filter(lambda l: l["listento"] == "start",
                       self.listeners))

    def handle_endtag(self, tag):
        if tag != 'br' and tag in self.tagPath:
            popped = self.tagPath.pop()

            while popped != tag:
                popped = self.tagPath.pop()

    def handle_data(self, data):
        map(lambda x: self.__process_listener(x, data),
            filter(lambda l: l["listento"] == "data",
                   self.listeners))
