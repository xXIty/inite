from djproxy.views import HttpProxy

class WikiProxy(HttpProxy):
    #base_url = 'http://localhost:8081'
    base_url = 'http://localhost:8000'

class MoodleProxy(HttpProxy):
    #base_url = 'http://localhost:8081'
    base_url = 'http://localhost:8000'


class KhanProxy(HttpProxy):
    #base_url = 'http://localhost:8081'
    base_url = 'http://localhost:8000'