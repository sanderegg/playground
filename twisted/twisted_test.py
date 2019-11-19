from twisted.web import server, resource, static, script
from twisted.internet import reactor, endpoints

import test_resource

class Simple(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>".encode('utf-8')

root = static.File("www/", ignoredExts=(".rpy",))
root.processors = {'.rpy': script.ResourceScript}
root.putChild('fred', test_resource.Hello())
root.putChild('bob', test_resource.Hello())
site = server.Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(site)
reactor.run()