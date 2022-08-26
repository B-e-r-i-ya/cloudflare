import CloudFlare

TOKEN = 'wgKC7ELJaC8t6c6DkOttyQEr0bBZV5IQ1Cy8wKtd'

def create_zone(cf, zone_name):
    zone_id = ''
    zone_info = cf.zones.get()

    for item_zone_info in zone_info:
        if zone_name == item_zone_info["name"]:
            zone_id = item_zone_info["id"]
    if zone_id == '':
        try:
            zone_id = (cf.zones.post(data={'jump_start': False, 'name': zone_name})["id"])
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            print(e)

    return zone_id

def create_dns(cf, zone_id, data):
    cf.zones.dns_records.get(cf, zone_id)


cf = CloudFlare.CloudFlare(token=TOKEN)

#print(cf.zones())
#print(create_zone(cf, '777-777.org'))
