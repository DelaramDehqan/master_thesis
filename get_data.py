# data from WBD API

import pandas as pd
import wbgapi as wb

# countries
countries = [
    'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
    ]

# control, independed variables
indicators = {
    'FDI_Net': 'BX.KLT.DINV.WD.GD.ZS',
    'CO2_Emissions': 'EN.ATM.CO2E.PC',         
    'Trade_Openness': 'NE.TRD.GNFS.ZS',
    'GDP_per_Capita': 'NY.GDP.PCAP.CD',
    'Internet_Users': 'IT.NET.USER.ZS',
    # 'Renewable_Share': 'EG.FEC.RNEW.ZS',       
    'Oil_Rents': 'EG.EAS.OIL.GD.ZS'            
}

years = range(2000, 2024)

print("start processing...")

dfs = []

for name, code in indicators.items():
    print(f"receiving values {name} ({code})...")
    try:
        # receive dataFrame for all countries
        df_ind = wb.data.DataFrame(code, economy=countries, time=years, numericTimeKeys=True, skipAggs=True)
        
        # years = col, countries name= index
        df_ind = df_ind.reset_index()
        
        # convert long to wide(col to row)
        year_cols = [col for col in df_ind.columns if str(col).isdigit()]
        df_long = pd.melt(df_ind, id_vars=['economy'], value_vars=year_cols, var_name='Year', value_name=name)
        
        df_long.rename(columns={'economy': 'Economy'}, inplace=True)
        df_long['Year'] = df_long['Year'].astype(int)
        
        dfs.append(df_long)
    except Exception as e:
        print(f"receiving error: {name}: {e}")

if dfs:
    # merge all index base of year, name
    df_final = dfs[0]
    for next_df in dfs[1:]:
        df_final = pd.merge(df_final, next_df, on=['Economy', 'Year'], how='outer')

    # final sorting
    df_final = df_final.sort_values(by=['Economy', 'Year']).reset_index(drop=True)

    # final saving
    filename = "OPECPlus_Full_Panel_Data_Clean.xlsx"
    df_final.to_excel(filename, index=False)

    print(f"\n operation is successful")
    print(f"rows number: {len(df_final)}")
    print(f"saved final file path: {filename}")
    print("\n overview values")
    print(df_final.head(10))
else:
    print("anything to find")
