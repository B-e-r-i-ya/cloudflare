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
    #cf.zones.dns_records.get(zone_id)
    for item_data in data:
        print(type(item_data))
        try:
            cf.zones.dns_records.post(zone_id, data=item_data)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            print(e)
            break

def create_firewallrules(cf, zone_id, data):
    filters = cf.zones.filters(zone_id)
    rules = cf.zones.rules(zone_id)
    for item_data in data:
        for item_filter in filters:
            if item_data["filter"] != item_filter["result"]["expression"]:
                try:
                    cf.zones.filters.post(zone_id, data=[{
                                                            "paused": False,
                                                            "expression": item_data["filter"]
                                                        }])
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    print(e)
        for item_rule in rules:
            if item_data["name"] != item_rule["result"]["description"]:


cf = CloudFlare.CloudFlare(token=TOKEN)

#print(cf.zones())
#print(create_zone(cf, '777-777.org'))
#for i in cf.zones.filters('cf749561a3d6671ec8038a459445182d'):
    #print(i)
    #cf.zones.filters.delete('cf749561a3d6671ec8038a459445182d', i["id"])

#for i in cf.zones.dns_records('cf749561a3d6671ec8038a459445182d'):
#    print(i)
#    cf.zones.dns_records.delete('cf749561a3d6671ec8038a459445182d', i["id"])

#cf.zones.delete('cf749561a3d6671ec8038a459445182d')

dns = [{"name": "@", "type": "A", "content": "8.13.56.100", "proxied": True}]

firewall_rules = [
        {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
         "priority": 1},
        {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)", "priority": 2},
        {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3}
    ]

#create_dns(cf, create_zone(cf, '777-777.org'), dns)