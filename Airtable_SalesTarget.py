import os
import pandas as pd
import numpy as np
import requests
from datetime import datetime

BASE_ID = "appKAJE1ZTvFZnxJ4"
TOKEN_NAME = "Orders Summary"
API_KEY = "key9tcxlWbfKeps7M"

global offset
offset = '0'
raw_data = []

while True :
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TOKEN_NAME}"
    querystring = {
        "view":"All Orders List",
        "api_key":f"{API_KEY}",
        "offset": offset}

    try :
        response= requests.get(url, params=querystring)
        response_Table = response.json()
        records = list(response_Table['records'])
        raw_data.append(records)
        #print(records[0]['id'] , len(records))
    
        try : 
            offset = response_Table['offset']
            #print(offset)
            
        except Exception as ex:
            #print(ex , offset)
            break
    
    except error as e:
        print(e)


all_data = [d['fields'] for data in raw_data for d in data]

final_cols = []
for d,data in enumerate(all_data):
    for col in data:
        if type(all_data[d][col])==list:
            if len(all_data[d][col]) > 1:
                for i,_ in enumerate(all_data[d][col]):
                    if i==0:
                        idx = col
                    else:
                        idx = col+"_"+str(i)
                    if idx not in final_cols:
                        final_cols.append(idx)
            else:
                if col not in final_cols:
                        final_cols.append(col)
        else:    
            if col not in final_cols:
                final_cols.append(col)

final_data = pd.DataFrame(columns = final_cols, index = [i for i in range(len(all_data))])

for d,data in enumerate(all_data):
    for col in data:
        if type(all_data[d][col])==list:
            if len(all_data[d][col]) > 1:
                for i,_ in enumerate(all_data[d][col]):
                    if i==0:
                        idx = col
                    else:
                        idx = col+"_"+str(i)
                    final_data[idx][d] = all_data[d][col][i]
            else:
                final_data[col][d] = all_data[d][col][0]
        elif type(all_data[d][col]) not in [list,int,str,float]:
            final_data[col][d] = np.nan
            #print(type(all_data[d][col]))
        else:    
            final_data[col][d] = all_data[d][col]

all_data = pd.DataFrame(all_data)
final_data['Products_Count'] = [len(p) if type(p)==list else 0 for p in all_data['Products']]

sheet_id = "1d2Qi4qaRi0Edb2IA-4S_IorOvfgTFk3V2O5cGcLsaU4"
sheet_name = "Sheet1"
sales_target_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
sales_person_target = pd.read_csv(sales_target_url)

def dateChecker(entry):
    if str(entry) != "nan":
        return datetime.strptime(entry,"%Y-%m-%d")
    else:
        return None

final_data['Order Date'] = final_data['Order Date'].apply(lambda x : dateChecker(x))
final_data['Process Date'] = final_data['Process Date'].apply(lambda x : dateChecker(x))

final_data['Getting Year'] = final_data['Order Date'].apply(lambda x: x.year).replace(np.nan,0).apply(lambda y: int(y))
final_data['Getting Quarter'] = final_data['Order Date'].apply(lambda x: x.quarter).replace(np.nan,0).apply(lambda y: int(y))
final_data['Getting Month'] = final_data['Order Date'].apply(lambda x: x.month).replace(np.nan,0).apply(lambda y: int(y))
final_data['Getting Day'] = final_data['Order Date'].apply(lambda x: x.day).replace(np.nan,0).apply(lambda y: int(y))

final_data['P.Getting Year'] = final_data['Process Date'].apply(lambda x: x.year).replace(np.nan,0).apply(lambda y: int(y)).replace(0,None)
final_data['P.Getting Quarter'] = final_data['Process Date'].apply(lambda x: x.quarter).replace(np.nan,0).apply(lambda y: int(y)).replace(0,None)
final_data['P.Getting Month'] = final_data['Process Date'].apply(lambda x: x.month).replace(np.nan,0).apply(lambda y: int(y)).replace(0,None)
final_data['P.Getting Day'] = final_data['Process Date'].apply(lambda x: x.day).replace(np.nan,0).apply(lambda y: int(y)).replace(0,None)

final_data["Target Amount"] = [0 for _ in range(len(final_data))]
for air in range(len(final_data)):
    for target in range(len(sales_person_target)):
        if final_data["Division"][air] == sales_person_target["Division"][target] and final_data["Sales Person"][air] == sales_person_target["Sales Rep"][target] and final_data["Getting Year"][air] == sales_person_target["Year"][target] and final_data["Getting Quarter"][air] == sales_person_target["Quarter"][target] and final_data["Getting Month"][air] == sales_person_target["Month"][target]:
            final_data["Target Amount"][air] = sales_person_target["Target"][target]

print(final_data)