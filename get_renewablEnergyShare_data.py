# data from OWID
# dependent variable


import pandas as pd

url = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"

print("Downloading OWID energy data...")
df_owid = pd.read_csv(url)

# overlook similar names to be sure 100%
renewable_cols = [col for col in df_owid.columns if 'renewable' in col.lower()]
print("Available renewable columns in OWID:", renewable_cols)

# select exactly name
target_col = "renewables_share_energy" 
if target_col not in df_owid.columns:
    # if isn't select similar name
    target_col = renewable_cols[0] if renewable_cols else None
    
print(f"Using column for renewable share: {target_col}")

# OPEC+ countries (22 countries)
opec_plus_iso = [
    'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 
    'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
]

#f filter base on countries name, years
filtered_df = df_owid[
    df_owid["iso_code"].isin(opec_plus_iso) & 
    df_owid["year"].between(2000, 2023)
][["country", "iso_code", "year", target_col]]

# sort
filtered_df = filtered_df.sort_values(by=["iso_code", "year"]).reset_index(drop=True)

# rename cols same as data panel
filtered_df.rename(
    columns={
        "country": "Country_Name",
        "iso_code": "Economy",
        "year": "Year",
        target_col: "Renewable_Share_OWID",
    },
    inplace=True,
)

# saving
output_filename = "OPECPlus_Renewable_Share_OWID.xlsx"
filtered_df.to_excel(output_filename, index=False)

print(f"\nSuccessfully generated: {output_filename}")
print(f"Total observations: {len(filtered_df)} (Expected: 22 countries * 24 years = 528 rows)")
print(filtered_df.head(10))
