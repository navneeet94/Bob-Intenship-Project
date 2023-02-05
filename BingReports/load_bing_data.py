import pandas as pd
from time import gmtime, strftime
Bing_Ads_data = pd.read_csv("C:/Users/Soul_Reaper_X/Desktop/BlackCoffer/Project___Bob_HDD/Git_files/Bob-Tanzola-Apps/BingReports/BingReport_2019.csv")
for t in range(2020,int(strftime("%Y", gmtime()))+1):
    temp_data = pd.read_csv(f"C:/Users/Soul_Reaper_X/Desktop/BlackCoffer/Project___Bob_HDD/Git_files/Bob-Tanzola-Apps/BingReports/BingReport_{t}.csv")
    Bing_Ads_data = pd.concat([Bing_Ads_data,temp_data],ignore_index=True)