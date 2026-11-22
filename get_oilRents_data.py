import pandas as pd
import requests
import time


opec_plus_iso = [
    'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 
    'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
]

# WDI: Oil rents (% of GDP)
indicator_code = "NY.GDP.PETR.RT.ZS"

all_data = []

print("Fetching Oil Rents data from World Bank WDI API for 22 countries...")

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount("https://", adapter)
session.mount("http://", adapter)

for iso in opec_plus_iso:
    url = f"http://api.worldbank.org/v2/country/{iso}/indicator/{indicator_code}?date=2000:2023&format=json"
    
    success = False
    for attempt in range(3):
        try:
            response = session.get(url, timeout=30)
            data = response.json()
            
            if len(data) > 1 and data[1]:
                for entry in data[1]:
                    year = int(entry['date'])
                    value = entry['value']
                    country_name = entry['country']['value']
                    
                    all_data.append({
                        "Country_Name": country_name,
                        "Economy": iso,
                        "Year": year,
                        "Oil_Rents_GDP": value
                    })
            success = True
            print(f"Successfully fetched: {iso}")
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {iso}: {e}")
            time.sleep(2)
            
    if not success:
        print(f"WARNING: Could not fetch data for {iso}")

# saving
df_oil = pd.DataFrame(all_data)

if not df_oil.empty:
    df_oil = df_oil.sort_values(by=["Economy", "Year"]).reset_index(drop=True)
    output_filename = "OPECPlus_Oil_Rents_WDI.xlsx"
    df_oil.to_excel(output_filename, index=False)
    print(f"\nSuccessfully generated and saved: {output_filename}")
else:
    print("\nERROR: DataFrame is empty. Check connection.")
