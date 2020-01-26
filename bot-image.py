import json
import pickle
import random
import ssl
import urllib.request

# Disable ssl check
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Enable proxy
# proxy = 'http://<user>:<pass>@157.245.123.27:8888'
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

poolPost = 5
posts = []

with urllib.request.urlopen("https://www.reddit.com/r/ProgrammerHumor/top/.json?count=5", context=ctx) as url:
    data = json.loads(url.read().decode())

for jsonPost in data['data']['children']:
    if jsonPost['data']['url'].startswith('https://i.redd.it/'):
        post = (jsonPost['data']['url'], jsonPost['data']['title'], jsonPost['data']['permalink'])
        posts.append(post)

try:
    with open("history-image.bin", "rb") as f:
        historyPosts = pickle.load(f)
except FileNotFoundError:
    historyPosts = []

found = False
i = 0
selectedPost = {}
while not found and i < poolPost:
    selectedPost = posts[random.randrange(len(posts))]
    for historyPost in historyPosts:
        if selectedPost[0] == historyPost[0]:
            found = True
    i = i + 1

print(selectedPost)

historyPosts.append(selectedPost)
with open("history-image.bin", "wb") as f:
    pickle.dump(historyPosts, f)

message = {}
message['channel'] = "yolo"
message['text'] = "[{}](https://old.reddit.com{}) \n {} )".format(selectedPost[1], selectedPost[2], selectedPost[0])

req = urllib.request.Request("mattermsoturl", data=json.dumps(message).encode("utf8"),
                             headers={'content-type': 'application/json'})
response = urllib.request.urlopen(req)
