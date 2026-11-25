import time
import pandas as pd
import requests
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

opec_plus_iso = [
    'ARE', 'AZE', 'BHR', 'BRN', 'COG', 'DZA', 'GAB', 'GNQ', 'IRN', 'IRQ', 
    'KAZ', 'KWT', 'LBY', 'MEX', 'MYS', 'NGA', 'OMN', 'RUS', 'SAU', 'SDN', 'SSD', 'VEN'
]

years = list(range(2000, 2024))

wgi_indicators = {
    "Rule_of_Law": "GOV_WGI_RL_EST",
    "Reg_Quality": "GOV_WGI_RQ_EST",
    "Gov_Effectiveness": "GOV_WGI_GE_EST",
    "Control_Corruption": "GOV_WGI_CC_EST",
    "Voice_Accountability": "GOV_WGI_VA_EST",
    "Pol_Stability": "GOV_WGI_PV_EST",
}

all_data = []
print("Fetching WGI indicators directly from World Bank API...")

for country in opec_plus_iso:
    for name, code in wgi_indicators.items():
        url = f"https://api.worldbank.org/v2/country/{country}/indicator/{code}?date=2000:2023&format=json&per_page=100"
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and data[1]:
                    for item in data[1]:
                        val = item.get("value")
                        yr = item.get("date")
                        if yr and int(yr) in years:
                            all_data.append(
                                {
                                    "Economy": country,
                                    "Year": int(yr),
                                    "Indicator": name,
                                    "Value": val,
                                }
                            )
            time.sleep(0.05)
        except Exception as e:
            print(f"Connection error for {country} - {name}: {e}")

if all_data:
    df_long = pd.DataFrame(all_data)
    panel_wgi = df_long.pivot_table(
        index=["Economy", "Year"], columns="Indicator", values="Value"
    ).reset_index()

    panel_wgi = panel_wgi.sort_values(by=["Economy", "Year"]).reset_index(drop=True)

    indicator_cols = list(wgi_indicators.keys())
    
    # report number of lost observation before remove
    print(f"Total panel rows before cleaning: {len(panel_wgi)}")
    
    # make standard PCL
    valid_mask = panel_wgi[indicator_cols].notnull().all(axis=1)
    X = panel_wgi.loc[valid_mask, indicator_cols]

    if not X.empty:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        pca = PCA(n_components=1)
        iqi_scores = pca.fit_transform(X_scaled)

        # make sure for bigger IQ (+)
        temp_df = pd.DataFrame(iqi_scores, index=X.index, columns=["IQI_Raw"])
        corr_check = pd.concat([X, temp_df], axis=1).corr()["IQI_Raw"][indicator_cols].mean()
        if corr_check < 0:
            iqi_scores = -iqi_scores

        print(f"PCA Explained Variance Ratio: {pca.explained_variance_ratio_[0]*100:.2f}%")

        panel_wgi["Institutional_Quality_Index"] = float("nan")
        panel_wgi.loc[valid_mask, "Institutional_Quality_Index"] = iqi_scores[:, 0]

    output_excel = "OPECPlus_WGI_IQI_2000_2023.xlsx"
    panel_wgi.to_excel(output_excel, index=False)
    print(f"Successfully saved: {output_excel}")
    print(panel_wgi.head(10))
else:
    print("Error: No data fetched from API.")
