import os
import sys

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

TOKEN = 'cca03865f623bec447d23db4755789a9d544c'
EMAIL = 'hramovalexandr1988@yandex.ru'

def main():
    cf = CloudFlare.CloudFlare(EMAIL, TOKEN)
    zone_name = '777-777.org'
    #print(cf.zones.post(data={'jump_start': , 'name': "777-777.org"})) #Создание зоны
    #print(cf.zones.get()) # Просмотр
    #for i in cf.api_list(): print(i)
    #for i in cf.zones.dns_records.get('5e63190dbe5762c3ae072921a14d0811'):
    #    print(cf.zones.dns_records.delete('5e63190dbe5762c3ae072921a14d0811', i['id']))
    #print(cf.accounts())
    #print(cf.accounts.rules.lists('0260e75b414a8881dd19d936a2fe6e9d'))
    print(cf.zones.firewall.rules.delete('5e63190dbe5762c3ae072921a14d0811', '04cc5bef8f054c408df481b43ee94a73'))
if __name__ == '__main__':
    main()
