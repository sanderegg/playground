from twisted.web import server, resource, static, script
from twisted.internet import reactor, endpoints
from twisted.web.resource import Resource
import time
import test_resource

class Hello(Resource):
    # isLeaf = True
    # def getChild(self, name, request):
    #     if name == '':
    #         return self
    #     return Resource.getChild(self, name, request)
    def render_GET(self, request):
        print(request.uri)
        return "Hello, world! I am located at {}.".format(request.postpath).encode("utf-8")

class ClockPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>" + time.ctime().encode('utf-8'))

class Bob(Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)
    def render_GET(self, request):
        print(request.uri)
        return "Hello, world! I am Bob {}.".format(request.postpath).encode("utf-8")


root = Resource()# static.File("www/", ignoredExts=(".rpy",))

files = static.File("www/", ignoredExts=(".rpy",))
# files.processors = {'.rpy': script.ResourceScript}
root.putChild(b"files", files)
# root.putChild('fred', Hello())
# root.putChild('bob', Hello())

root.putChild(b'bob', Bob())
root.putChild(b"clock", ClockPage())
site = server.Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(site)
reactor.run()
