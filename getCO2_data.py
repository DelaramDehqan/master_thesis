import os
import pandas as pd
import requests

url = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
local_csv = "owid_energy_data_local.csv"

# download file correctly
if os.path.exists(local_csv):
    os.remove(local_csv)

print("Downloading fresh OWID energy dataset (this may take a few seconds)...")
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers, stream=True, timeout=120)
response.raise_for_status()

with open(local_csv, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
print("Successfully downloaded.")

# review cols
df_owid = pd.read_csv(local_csv)
print("Available columns in OWID containing 'co2':")
print([c for c in df_owid.columns if 'co2' in c])

opec_plus_iso = [
    'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 
    'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
]

# extract data 
df_co2 = df_owid[
    df_owid["iso_code"].isin(opec_plus_iso) & df_owid["year"].between(2000, 2023)
].copy()

# select requested data from OWID
target_cols = ["country", "iso_code", "year", "co2", "co2_per_capita"]
if "consumption_co2_per_capita" in df_owid.columns:
    target_cols.append("consumption_co2_per_capita")

df_co2 = df_co2[target_cols]

# rename for merge
rename_dict = {
    "country": "Country_Name",
    "iso_code": "Economy",
    "year": "Year",
    "co2": "Total_CO2_OWID",
    "co2_per_capita": "CO2_Per_Capita_OWID"
}
if "consumption_co2_per_capita" in df_co2.columns:
    rename_dict["consumption_co2_per_capita"] = "Consumption_CO2_Per_Capita_OWID"

df_co2.rename(columns=rename_dict, inplace=True)
df_co2 = df_co2.sort_values(by=["Economy", "Year"]).reset_index(drop=True)

output_filename = "OPECPlus_CO2_Data_OWID.xlsx"
df_co2.to_excel(output_filename, index=False)
print(f"Successfully extracted and saved {output_filename}")
print(df_co2.head(10))
