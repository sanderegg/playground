from twisted.web.resource import Resource

class MyResource(Resource):
    def render_GET(self, request):
        return "<html>Hello, I'm a rpy script!</html>".encode('utf-8')

resource = MyResource()