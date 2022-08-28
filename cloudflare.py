import ast
import CloudFlare
import click

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
    print(filters)
    rules = cf.zones.firewall.rules.get(zone_id)
    for item_data in data:
        print(item_data)
        if filters == []:
            try:
                filter_id = cf.zones.filters.post(zone_id, data=[{
                    "paused": False,
                    "expression": item_data["filter"]
                }])[0]["id"]
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                print(e)
        for item_filter in filters:
            print(item_filter)
            if item_data["filter"] != item_filter["expression"]:
                print("Создаем фильтр " + item_data["filter"])
                print(type(item_data["filter"]))
                try:
                    filter_id = cf.zones.filters.post(zone_id, data=[{
                                                            "paused": False,
                                                            "expression": item_data["filter"]
                                                        }])[0]["id"]
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    print(e)
            else:
                print("Фильтр " + item_data["filter"] + " уже есть!")
                filter_id = item_filter["id"]
        if rules == []:
            try:
                cf.zones.firewall.rules.post(
                    zone_id, data=[{"action": item_data["action"],
                                    "priority": item_data["priority"],
                                    "paused": item_data["paused"],
                                    "description": item_data["name"],
                                    "filter":
                                        {
                                            "id": filter_id,
                                            "paused": item_data["paused"],
                                        }}]
                )
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                print(e)
        for item_rule in rules:
            if item_data["name"] != item_rule["description"]:
                try:
                    cf.zones.firewall.rules.post(
                        zone_id, data=[{"action": item_data["action"],
                                        "priority": item_data["priority"],
                                        "paused": item_data["paused"],
                                        "description": item_data["name"],
                                        "filter":
                                            {
                                                "id": filter_id,
                                                "paused": item_data["paused"],
                                            }}]
                    )
                except CloudFlare.exceptions.CloudFlareAPIError as e:
                    print(e)


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
         "priority": 1, "paused": False},
        {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)", "priority": 2, "paused": False},
        {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3, "paused": False}
    ]

#create_dns(cf, create_zone(cf, '777-777.org'), dns)
#create_firewallrules(cf, create_zone(cf, '777-777.org'), firewall_rules)


@click.command()
@click.option(
    '--api_key', '-a',
    help='Апи токен доступа CF(НЕ Global API Key, а индивидуально созданный)',
)
@click.option(
    '--file', '-f',
    help='файл для парсинга значений для добавления',
)

@click.option(
    '--jenkins', '-j',
    help='Если скрипт запускается с Jenkins',
)


def main(api_key, file, jenkins):
    """
    Данная программа предназначена для автоматизации работы с CloudFlare

    """


    firewall_rules = [
        {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
         "priority": 1, "paused": False},
        {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)", "priority": 2,
         "paused": False},
        {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3,
         "paused": False}
    ]
    try:
        api_key
    except NameError:
        api_key = None

    try:
        file
    except NameError:
        file = None

    try:
        jenkins
    except NameError:
        jenkins = None


    if not(api_key == None):
        TOKEN = api_key

    #if file != None:
     #   file_pars(file)

    if jenkins != None:
        jenkins = ast.literal_eval(jenkins)
        dns = {"name": "@", "type": "A", "proxied": True}
        print(jenkins["mongol"])
        if jenkins["mongol"] == False:
            firewall_rules = [
                {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
                 "priority": 1, "paused": False},
                {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)",
                 "priority": 2,
                 "paused": False},
                {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3,
                 "paused": False}
            ]
        elif jenkins["mongol"] == True:
            firewall_rules = [
                {"name": "Block DDoS UserAgent", "action": "block", "filter": "(http.user_agent contains \"Python\")",
                 "priority": 1, "paused": False},
                {"name": "Allow Enterra list", "action": "allow", "filter": "(ip.src in $white_list_enterra)",
                 "priority": 2,
                 "paused": False},
                {"name": "Block ne MN", "action": "block", "filter": "(ip.geoip.country ne \"MN\")", "priority": 3,
                 "paused": True}
            ]

        zone_id = create_zone(cf, jenkins["zone"])
        dns["content"] = jenkins["ipaddress"]
        create_dns(cf, zone_id, dns)
        create_firewallrules(cf, zone_id, firewall_rules)

if __name__ == "__main__":
    main()