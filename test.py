import requests
proxies = {'http': 'http://172.16.0.95:9100', 'https': 'http://172.16.0.95:9100'}

# Should print your real ip
response = requests.get('http://jsonip.com')
print (response.json())

# Should print an ip from tor network
response = requests.get('http://jsonip.com', proxies=proxies)
print (response.json())

# Should print another ip from tor network
response = requests.get('http://jsonip.com', proxies=proxies)
print (response.json())

# Should print another ip from tor network
response = requests.get('http://jsonip.com', proxies=proxies)
print (response.json())

# Should print another ip from tor network
response = requests.get('http://jsonip.com', proxies=proxies)
print (response.json())