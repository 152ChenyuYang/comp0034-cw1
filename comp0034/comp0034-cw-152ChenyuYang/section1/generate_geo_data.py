from geopy.geocoders import Nominatim
import sqlite3
import pandas as pd
import os
import time  # Avoid API restrictions

# **Initialize Geocoder**
geolocator = Nominatim(user_agent="geo_locator")

# **Get the database path**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(
    BASE_DIR, "..", "data0035", "coursework1", "database", "local_authority_housing.db"
)

# **Connect to the database and read all region names**
conn = sqlite3.connect(db_path)


df = pd.read_sql("SELECT area_code, area_name FROM Area", conn)  #  Reading `area_name`
conn.close()


# **Get longitude and latitude**
def get_lat_lon(area_name):
    try:
        location = geolocator.geocode(area_name + ", UK")  # Limited to the UK
        if location:
            return location.latitude, location.longitude
        return None, None
    except:
        return None, None


# **Traverse `area_name` and query the longitude and latitude**
df["latitude"], df["longitude"] = zip(*df["area_name"].apply(get_lat_lon))
time.sleep(1)  # Avoid API restrictions

# **Save to CSV**
geo_path = os.path.join(BASE_DIR, "geo_locations.csv")
df.to_csv(geo_path, index=False)
print("The latitude and longitude data has been saved to:", geo_path)
