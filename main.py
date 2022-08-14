import requests
import json


class cf_class:
    TOKEN = ''
    EMAIL = ''

    def __init__(self, email, token):
        self.TOKEN = token
        self.EMAIL = email

    def request(self, urls, type):
        url = 'https://api.cloudflare.com/client/v4/' + urls
        payload = {}
        headers = {
            'X-Auth-Email': self.EMAIL,
            'X-Auth-Key': self.TOKEN,
            'content-type': 'application/json'
        }
        respose = requests.get(url, data=json.dumps(payload), headers=headers)
        return respose

    def create_site(self, name):
        url = 'https://api.cloudflare.com/client/v4/zones'
        payload = {"name":name,"account":{"id":"0260e75b414a8881dd19d936a2fe6e9d"},"jump_start":True,"type":"full"}
        headers = {
            'X-Auth-Email': self.EMAIL,
            'X-Auth-Key': self.TOKEN,
            'content-type': 'application/json'
        }
        respose = requests.post(url, data=json.dumps(payload), headers=headers)
        return respose

    def delete_site(self, id):
        url = 'https://api.cloudflare.com/client/v4/zones/'+id
        payload = {}
        headers = {
            'X-Auth-Email': self.EMAIL,
            'X-Auth-Key': self.TOKEN,
            'content-type': 'application/json'
        }
        respose = requests.delete(url, data=json.dumps(payload), headers=headers)
        return respose

cf = cf_class('hramovalexandr1988@yandex.ru', 'cca03865f623bec447d23db4755789a9d544c' )
#print(cf.delete_site('5e63190dbe5762c3ae072921a14d0811').json())
print(cf.create_site('777-777.org').json())