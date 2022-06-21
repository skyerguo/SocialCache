import requests
def simple_httpget(url):
    res = requests.get(url=url)
    print(res.text)

if __name__ == '__main__':
    url = 'http://127.0.0.1:4433/'
    simple_httpget(url)