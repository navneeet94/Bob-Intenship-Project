import pandas as pd
sheet_id = "10jrohsRw0zgByMIAgyVJT8vkmKTNg_ut"
sheet_name = "Sheet1"
sales_target_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
sales_person_target = pd.read_csv(sales_target_url)
print(sales_person_target)