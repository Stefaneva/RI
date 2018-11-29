class Query:
    def __init__(self, description, urls):
        self.description = description
        self.urls = urls


class Url:
    def __init__(self, url, title, headers, body_hits):
        self.url = url
        self.title = title
        self.headers = headers
        self.body_hits = body_hits


class Header:
    def __init__(self, text):
        self.text = text


class BodyHits:
    def __init__(self, text):
        self.text = text

