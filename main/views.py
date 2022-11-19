from django.shortcuts import render
import subprocess
import json
import re
import requests
# Create your views here.



IP_PATTERN = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

def get_terminal_line(line, line_num):
    if line_num == 0:
        line_type = "input"
    else:
        line_type = "output"
    return json.dumps({"type": line_type, "msg": line})

def get_ip_from_line(line, line_num):
    if line_num != 0:
        ip = IP_PATTERN.search(line)
        if ip:
            return ip[0]
        return None
    else:
        return None
def trace(request):
    if request.method == 'POST':
        website = request.POST
        website = website['host']
        hop_list = []
        i_list = []
        line_list = []
#         command = ["tracert", "-h", "30", website]
#         command = ["traceroute", "-I", "--max-hop=30", website]
        command = ["traceroute", website]
        with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as process:
            for i, line in enumerate(process.stdout):
                ip = get_ip_from_line(line, i)
                terminal_line = get_terminal_line(line, i)
                if ip:
                    print(ip)
                    print(terminal_line)
                    token = "761eab6307df4b"
                    ip_geolocation_data = requests.get(f"https://ipinfo.io/{ip}?token={token}").json()
                    hop_list.append(ip_geolocation_data)
                    geo_loc_msg = json.dumps({"type": "geo", "msg": ip_geolocation_data})
                    i_list.append(geo_loc_msg)
                    line_list.append(terminal_line)
    

    # my_list = json.dumps(i_list)
    # dataDictionary = {
    #     'hello': 'World',
    #     'geeks': 'forgeeks',
    #     'ABC': 123,
    #     456: 'abc',
    #     14000605: 1,
    #     'list': ['geeks', 4, 'geeks'],
    #     'dictionary': {'you': 'can', 'send': 'anything', 3: 1}
    # }
    # # dump data
    # dataJSON = json.dumps(dataDictionary)
    # test = {
    #     "type": "geo",
    #  "msg": {"ip": "142.250.71.36", "hostname": "maa03s35-in-f4.1e100.net", "city": "Chennai", "region": "Tamil Nadu", "country": "IN", "loc": "13.0878,80.2785", "org": "AS15169 Google LLC", "postal": "600001", "timezone": "Asia/Kolkata"}

    
    
        data = json.dumps(hop_list)

        context = {
            'i_list' : i_list,
            'line_list' : line_list,
            'data' : data
        }

        return render(request, 'main/index.html', context)
    
    else :
        return render(request, 'main/index.html')
