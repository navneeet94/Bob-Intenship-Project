# For Importing Files
import requests
import pandas as pd
import numpy as np

# For Getting access Tokken
refresh_token = '1000.53a093be4ff4de69d2200dc38e458f17.449fc0158f779c05a36b6c640d52dd28'
client_id = '1000.7DSQ5S0EEAFUSEYPP02PVKORLFIXMV'
client_secret = '9cac16f9675e298204f2e12e2659c7edf0e8f7140e'
access_response = requests.post(
    f"https://accounts.zoho.com/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token"
)
access_response = access_response.json()

access_token = access_response['access_token']
access_token
page_number = 1
ending_page_number = 50000000000000
pages_data = []
for i in range(page_number,(ending_page_number+1)):
    get_url="https://www.zohoapis.com/crm/v2/Leads?page="+str(i)
    response = requests.get(f'{get_url}',headers={'Authorization':f'Zoho-oauthtoken {access_token}'}
    )
    if response.status_code != 204:
        Combined_Response = response.json()
        pages_data.append(Combined_Response)
    else:
        break
    i+=1    

# For Getting Column Contain Which Kind Of Data Type
fixedDTcounter = 0
fixedDTcount = 0
data_type_containing = {"key":[],"type":[],"value":[]}
for typeChecker in pages_data:
    current_page  = pages_data[fixedDTcounter]['data']
    for i in current_page:       
        for j in i:
            data_type_containing["key"].append(j)
            data_type_containing["type"].append(type(i[j]))
            data_type_containing["value"].append(i[j])
        if fixedDTcount < 1:
            break
        fixedDTcount+=1
    if fixedDTcounter < 1:
        break
    fixedDTcounter += 1  

# Converting Other Type data to dict Type
counter = 0
count = 0

for current_page in pages_data:
    current_page  = pages_data[counter]['data']
    data_counter = 0
    for i in current_page:
        column_counter = 0
        for j in i:            
            data_type_counter = 0
            for k in data_type_containing:
                if (j == data_type_containing['key'][column_counter]):
                    if type(i[j]) != data_type_containing['type'][column_counter]:
                        if (data_type_containing['type'][column_counter] == dict):
                            chandeValType = {}
                            for l in data_type_containing['value'][column_counter]:
                                chandeValType[f"{l}"] = i[j]
                            pages_data[counter]['data'][data_counter][j] = chandeValType
                data_type_counter+=1 

                if data_type_counter < 2:
                    break

            column_counter+=1
        data_counter+=1

        count+=1
    counter += 1

dataset = {}
for current_page in pages_data:
    containing_data = current_page['data']
    containing_data_len = len(containing_data)
    for count in range(0,containing_data_len):
        check_data = containing_data[count]
        for i in check_data:
            col_type_data = type(check_data[i])
            if(col_type_data == dict):
                for j in check_data[i]:
                    keyname = i+"_"+j
                    if len(dataset) == 0 :
                        if (check_data[i][j] == None) or (check_data[i][j] == ''):
                            dataset[f"{keyname}"] = ['Blank']
                        else:
                            dataset[f"{keyname}"] = [check_data[i][j]]
                    elif keyname not in dataset:
                        if (check_data[i][j] == None) or (check_data[i][j] == ''):
                                dataset[f"{keyname}"] = ['Blank']
                        else:
                            dataset[f"{keyname}"] = [check_data[i][j]]
                    else:
                        if (check_data[i][j] == None) or (check_data[i][j] == ''):
                            dataset[f"{keyname}"].append('Blank')
                        else:
                            dataset[f"{keyname}"].append(check_data[i][j])
            else:
                single_keyname = i
                if len(dataset) == 0 :
                    if (check_data[i] == None) or (check_data[i] == ''):
                        dataset[f"{single_keyname}"] = ['Blank']
                    else:
                        dataset[f"{single_keyname}"] = check_data[i]
                elif single_keyname not in dataset:
                    if (check_data[i] == None) or (check_data[i] == ''):
                        dataset[f"{single_keyname}"] = ['Blank']
                    else:
                        dataset[f"{single_keyname}"] = [check_data[i]]
                else:
                    if (check_data[i] == None) or (check_data[i] == ''):
                        dataset[f"{single_keyname}"].append('Blank')
                    else:
                        dataset[f"{single_keyname}"].append(check_data[i])

df = pd.DataFrame(dataset)
df

Leads_DF = df.applymap(lambda x: str(x).replace('[]','Blank'))
Leads_DF


def firstNameget(name):
    if name == 'HDD US':
        return 'HDD US'
    else:
        return str(name).split()[0]

Leads_DF['Creator Name'] = Leads_DF['Owner_name'].apply(lambda x: firstNameget(x))
print(Leads_DF)