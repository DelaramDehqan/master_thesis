# data from OWID

import pandas as pd



url = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

print("OWID excteracting data")
df_owid = pd.read_csv(url)

# OPEC+ countries
opec_plus_iso = [
  'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
   ]

# filter requested data base on year, name
filtered_df = df_owid[
    df_owid["iso_code"].isin(opec_plus_iso)
    & df_owid["year"].between(2000, 2023)
][["country", "iso_code", "year", "renewables_energy_share_pct"]]

# sorting
filtered_df = filtered_df.sort_values(by=["iso_code", "year"]).reset_index(
    drop=True
)

# rename to be same as main file
filtered_df.rename(
    columns={
        "country": "Country_Name",
        "iso_code": "Economy",
        "year": "Year",
        "renewables_energy_share_pct": "Renewable_Share_OWID",
    },
    inplace=True,
)

# saving
output_filename = "OPECPlus_Renewable_Share_OWID.xlsx"
filtered_df.to_excel(output_filename, index=False)

print(
    f"successfully operation: {output_filename}"
)
print(f"number of observation: {len(filtered_df)}")
print(filtered_df.head(10))
