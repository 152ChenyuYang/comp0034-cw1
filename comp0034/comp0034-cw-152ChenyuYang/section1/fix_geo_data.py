import pandas as pd
import os

# **Get the path to the `geo_locations.csv` file**
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
geo_path = os.path.join(BASE_DIR, "geo_locations.csv")

# **Reading CSV**
df_geo = pd.read_csv(geo_path)

# **Make sure `latitude` and `longitude` are numeric types**
df_geo["latitude"] = pd.to_numeric(df_geo["latitude"], errors="coerce")


df_geo["longitude"] = pd.to_numeric(df_geo["longitude"], errors="coerce")

# **Manually correct wrong coordinates**
corrections = {
    "E09000030": (51.5155, -0.0724),  # Tower Hamlets
    "E12000008": (51.2723, -0.5196),  # South East
    "E12000009": (51.4545, -2.5879),  # South West
    "E09000029": (51.3618, -0.1934),  # Sutton
    "E92000001": (51.509865, -0.118092),  # England
}

# **APPLYING FIXES**
for area_code, (lat, lon) in corrections.items():
    df_geo.loc[df_geo["area_code"] == area_code, ["latitude", "longitude"]] = lat, lon


# **Save the corrected file**
df_geo.to_csv(geo_path, index=False)
print(f" The corrected geographic data has been saved to: {geo_path}")
