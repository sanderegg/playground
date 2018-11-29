import urllib.request
if urllib.request.urlopen("http://localhost:8888").status == 200:
    print(0)
else:
    print(1)