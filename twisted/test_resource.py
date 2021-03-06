from twisted.web.resource import Resource

class Hello(Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return "Hello, world! I am test_resource located at {}.".format(request.postpath).encode("utf-8")

resource = Hello()