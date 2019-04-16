import time
import requests
from collections import deque

q = deque( maxlen=256 )
q.append( 10 )
q.append( 20 )
q.append( 30 )
# deque([ 10, 20, 30 ])

q.append( 40 )
# deque([ 20, 30, 40 ])

stream_url = 'https://virta.radiodiodi.fi/mp3'
r = requests.get(stream_url, stream=True)
start = time.time()
print("hello")
with open('streamN.mp3', 'wb') as f:
    for block in r.iter_content(1024):
        q.append(block)
        f.write(block)
        end = time.time()
        if(end - start > 5):
            break

with open('streamQ.mp3', 'wb') as f:
    for block in q:
        f.write(block)