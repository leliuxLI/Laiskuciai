from time import sleep
import urllib.request

while True:
    urllib.request.urlopen('http://127.0.0.1:8000/send/')
    sleep(60)
