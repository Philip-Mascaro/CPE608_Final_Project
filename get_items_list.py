#Philip Mascaro


import pandas as pd



#load data
bakery_data = pd.read_csv("archive/bakery_sales_revised.csv")

#get all column headers
column_headers = bakery_data.columns.tolist()

#remove duplicate rows
bakery_data = bakery_data.drop_duplicates(subset=column_headers, keep="first")

#get the lists of unique items, unique period_day options, and unique weekday_weekend options
item_options = sorted(list(set(bakery_data['Item'].tolist())))

print("ID\tItem")
print()
for i in range(len(item_options)):
    print(str(i+1)+"\t"+str(item_options[i]))