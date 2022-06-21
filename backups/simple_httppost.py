from requests_toolbelt import MultipartEncoder
import requests

m = MultipartEncoder(
    fields={'field0': 'value', 'field1': 'value',
            'field2': ('filename', open('file.py', 'rb'), 'text/plain')}
    )

r = requests.post('http://127.0.0.1:4433/', data=m,
                  headers={'Content-Type': m.content_type})

# def simple_httppost(url):
#     payload = (('username', 'test_app'), ('password', '000000'))
#     req = requests.post(url,data=payload)

# if __name__ == '__main__':
#     url = 'http://127.0.0.1:4433/'
#     simple_httppost(url)