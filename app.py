#!/usr/bin/python3

# Imports
from flask import Flask, jsonify, request
import requests
import json
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()


def get_client_ip():
    """ a function that retrieve User Ip address"""
    if request.headers.get('X-Forwarded-For'):
        # 'X-Forwarded-For' can contain multiple IPs. The first one is the client IP.
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        return request.remote_addr


def get_location(ip):
    """ a function that retrieves Users ip address """
    access_token = os.getenv('IP_API_KEY')
    url = f"https://ipinfo.io/{ip}/json?token={access_token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        location = data.get('city', 'unknown location')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
        location = 'Unknown Location'
    return location

def get_temperature(location):
    """ a function that retrieves Users location temperature """
    api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temperature = data['current']['temp_c']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching temperature data: {e}")
        temperature = "Unknown"
    return temperature

    



@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'visitor')
    client_ip = get_client_ip()
    location = get_location(client_ip)
    temperature = get_temperature(location)
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    response_data = {
        "client_ip": client_ip,
        "greeting": greeting
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
