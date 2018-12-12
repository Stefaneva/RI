class Query:
    def __init__(self, description, urls):
        self.description = description
        self.urls = urls

    def __repr__(self):
        return self.description + ' ' + ', '.join("{!s}={!r}".format(key, val) for (key, val) in self.urls.items())


class Url:
    def __init__(self, url, title, headers, body_hits):
        self.url = url
        self.title = title
        self.headers = headers
        self.body_hits = body_hits

    # def __repr__(self):
    #     return self.url + ' ' + self.title + ', '.join("{!s}={!r}".format(key, val) for (key, val) in self.headers.items()) + ', '.join("{!s}={!r}".format(key, val) for (key, val) in self.body_hits.items())

    def __repr__(self):
        return self.url


class Header:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text


class BodyHits:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text
