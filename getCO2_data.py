import os
import pandas as pd
import requests


url = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
local_csv = "owid_energy_data_local.csv"


if not os.path.exists(local_csv):
    print("downloading pure data from OWID github...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=5)
    session.mount("https://", adapter)

    response = session.get(url, headers=headers, stream=True, timeout=60)
    response.raise_for_status()

    with open(local_csv, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("successfully downloaded")
else:
    print("OWID is exist")

# filtering all data to get opec+ data
df_owid = pd.read_csv(local_csv)

opec_plus_iso = [
  'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
  ]

# get data from 2000-2023
df_co2 = df_owid[
    df_owid["iso_code"].isin(opec_plus_iso) & df_owid["year"].between(2000, 2023)
][
    [
        "country",
        "iso_code",
        "year",
        "co2",
        "co2_per_capita",
        "consumption_co2_per_capita",
    ]
]

# rename values to be same as main file for merging
df_co2.rename(
    columns={
        "country": "Country_Name",
        "iso_code": "Economy",
        "year": "Year",
        "co2": "Total_CO2_OWID",
        "co2_per_capita": "CO2_Per_Capita_OWID",
        "consumption_co2_per_capita": "Consumption_CO2_Per_Capita_OWID",
    },
    inplace=True,
)

df_co2 = df_co2.sort_values(by=["Economy", "Year"]).reset_index(drop=True)

# saving final co2 file
output_filename = "OPECPlus_CO2_Data_OWID.xlsx"
df_co2.to_excel(output_filename, index=False)
print(
    f"successfully extract {output_filename}"
)
print(df_co2.head(10))
