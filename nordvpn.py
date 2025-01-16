#!/usr/bin/env python3
import requests
import argparse
import subprocess
import os
import time

servers_cache = []

def servers_api(s:requests.Session = None, update:bool = False) -> dict:
    if not s:
        s = requests.Session()
    if not servers_cache or update:
        r = s.get("https://api.nordvpn.com/v1/servers",params={"limit":"999999"})
        servers_cache.clear()
        servers_cache.extend(r.json())
    return servers_cache

def get_countries(s:requests.Session = None) -> list[str]:
    scache = servers_api(s)
    countries = []
    for server in scache:
        country = server['locations'][0]['country']['name']
        if not country in countries:
            countries.append(country)
    countries.sort()
    return countries

def get_servers(s:requests.Session = None) -> list[str]:
    scache = servers_api(s)
    servers = []
    for server in scache:
        servers.append(server['name'])
    servers.sort()
    return servers

def get_ip() -> str:
    while True:
        try:
            r = requests.get("https://ifconfig.co/json")
            return r.json()
        except:
            pass

def connect(auto:bool = False, server:str = None, country:str = None):
    cwd = os.getcwd()
    before_ip = get_ip()
    print("Current IP:",before_ip['ip'],before_ip['country'])
    if auto:
        subprocess.Popen(['nordvpn.exe','-c'], shell=True, cwd=cwd)
    elif server:
        subprocess.Popen(['nordvpn.exe','-c','-n',server], shell=True, cwd=cwd)
    elif country:
        subprocess.Popen(['nordvpn.exe','-c','-g',country], shell=True, cwd=cwd)
    print("Connecting..", end="")
    new_ip = get_ip()
    while new_ip['ip'] == before_ip['ip']:
        time.sleep(1)
        print(".", end="")
        new_ip = get_ip()
    print(" Connected!")
    print("New IP:",new_ip['ip'],new_ip['country'])

def disconnect() -> subprocess.Popen:
    cwd = os.getcwd()
    before_ip = get_ip()
    print("Current IP:",before_ip['ip'],before_ip['country'])
    print("Disconnecting..", end="")
    subprocess.Popen(['nordvpn.exe','--disconnect'], shell=True, cwd=cwd)
    new_ip = get_ip()
    while new_ip['ip'] == before_ip['ip']:
        time.sleep(1)
        print(".", end="")
        new_ip = get_ip()
    print("Disconnected!")
    print("New IP:",new_ip['ip'],new_ip['country'])

if __name__ == "__main__":
    s = requests.Session()
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--auto", action='store_true')
    g.add_argument("--country", type=str)
    g.add_argument("--server", type=str)
    g.add_argument("--disconnect", action='store_true')
    args = parser.parse_args()
    if args.auto:
        connect(auto=True)
    elif args.server:
        servers = get_servers(s)
        if not args.server in servers:
            raise argparse.ArgumentTypeError(f"Server not in list! Example: {servers[0]}")
        connect(server=args.server)
    elif args.country:
        countries = get_countries(s)
        country = args.country.lower().capitalize()
        if not country in countries:
            raise argparse.ArgumentTypeError(f"Country not in list! Available countries: {', '.join(countries)}")
        connect(country=country)
    elif args.disconnect:
        disconnect()
