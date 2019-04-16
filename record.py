import time
import requests


stream_url = 'https://virta.radiodiodi.fi/ogg'
r = requests.get(stream_url, stream=True)
start = time.time()
print("hello")
with open('stream.mp3', 'wb') as f:
    for block in r.iter_content(1024):
        f.write(block)
        end = time.time()
        if(end - start > 5):
            break
