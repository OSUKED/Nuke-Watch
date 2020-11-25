"""
Imports
"""
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup


"""
Functions
"""
def retrieve_all_power_station_data(nuke_statuses_url='https://www.edfenergy.com/energy/power-station/daily-statuses'):
    r = requests.get(nuke_statuses_url)
    soup = BeautifulSoup(r.content, features='lxml')

    power_station_soups = [
        node.parent.parent.parent 
        for node 
        in soup.findAll('h3', {'class': 'node-title'})
    ]

    all_power_station_data = list()

    for power_station_soup in power_station_soups:
        power_station_data = dict()
        power_station_data['name'] = power_station_soup.find('h3', {'class': 'node-title'}).text.strip()

        reactor_soups = power_station_soup.findAll('div', {'class': 'reactor'})
        power_station_data['reactors'] = list()

        for reactor_soup in reactor_soups:
            reactor_data = dict()
            reactor_data['name'] = reactor_soup.find('h3', {'class': 'field-name-field-reactor-name'}).text.strip()
            reactor_data['status'] = reactor_soup.find('span', {'class': 'status-text'}).text.strip()
            reactor_data['output_MW'] = int(reactor_soup.find('div', {'class': 'generation-amount'}).text.strip()[:-2])

            power_station_data['reactors'] += [reactor_data]

        all_power_station_data += [power_station_data]
        
    return all_power_station_data

def update_readme_time(readme_fp, 
                       splitter='Last updated: ', 
                       dt_format='%Y-%m-%d %H:%M'):
    
    with open(readme_fp, 'r') as readme:
        txt = readme.read()
    
    start, end = txt.split(splitter)
    old_date = end[:16]
    end = end.split(old_date)[1]
    new_date = pd.Timestamp.now().strftime(dt_format)
    
    new_txt = start + splitter + new_date + end
    
    with open(readme_fp, 'w') as readme:
        readme.write(new_txt)
        
    return
    
    
"""
Retrieval Process
"""
all_power_station_data = retrieve_all_power_station_data()

with open('data/all_power_station_data.json', 'w') as fp:
    json.dump(all_power_station_data, fp)
    
update_readme_time('README.md')