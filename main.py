import pandas as pd
import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)

rapid_apikey = os.environ.get('RAPIDAPI_API_KEY')

def get_lat_lng(pincode):
    """
    Fetch latitude and longitude for a given pincode.
    """
    
    url = f"https://india-pincode-with-latitude-and-longitude.p.rapidapi.com/api/v1/pincode/{pincode}"
    headers = {
        'X-RapidAPI-Key': rapid_apikey,
        'X-RapidAPI-Host': "india-pincode-with-latitude-and-longitude.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = data[0]['lat']
            lng = data[0]['lng']
            return lat, lng
    except Exception as e:
        logging.error(f"Error fetching data for pincode {pincode}: {e}")
    return None, None

def add_lat_lng_to_dataframe(df):
    """
    Add latitude and longitude columns to the DataFrame.
    """
    
    df['Latitude'], df['Longitude'] = zip(*df['pincode'].apply(get_lat_lng))
    return df

if __name__ == "__main__":
    try:
        # Replace with path to csv file
        df = pd.read_csv("PATH TO CSV")
        df = add_lat_lng_to_dataframe(df)
        df.to_csv('updated_excel_file.csv', index=False)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
