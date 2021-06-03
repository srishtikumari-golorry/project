import pandas as pd

data = pd.read_csv("C:/Users/Satpal/Desktop/Project/2018_Accounts_Receivable.csv")
order = pd.read_csv("C:/Users/Satpal/Desktop/Project/2018 Order Data.csv")
placement = pd.read_csv("C:/Users/Satpal/Desktop/Project/2018 Placement Data.csv")

def count(placement,order):
    print("No. of Placements : {}".format(len(placement["ID"].unique())))
    print("Total No. of orders : {}".format(len(order["ID"].unique())))
    print("No. of orders on the placement data sheet : {}".format(len(placement["Order ID"].unique())))
print(count(placement,order))
# No of unique orders on the placement data is 1398 while on order data it is 1957
# There is a difference of 559 orders
print(order["Fulfilled"].value_counts())
print(order["Status"].value_counts())
df=order[order["Status"]=="Cancelled"]
l1 = placement["Order ID"].unique()
l2 = df["ID"].unique()
count =0
n=0
list = []
for l in l2:
    if l in l1:
        count = count+1
        list.append(l)
    else:
        n=n+1
print(count)
print(n)
print(list)

#Adding origin identifier and destination identifier columns to placement data using order data

merged_df=placement.merge(order.loc[:,["ID","Origin Identifier","Destination Identifier"]],how='left',left_on='Order ID',right_on='ID')
print(merged_df.head())
merged_df.drop(["ID_y"],axis=1,inplace=True)
print(merged_df.shape)
#merged_df.to_csv("merged.csv")
df_1=merged_df.loc[:,["ID_x","Origin Identifier","Destination Identifier"]]
df_1.rename(columns={"ID_x":"Placement ID"},inplace=True)
df_2 = data.loc[:,["Placement ID","Origin","Destination"]]
df_2.rename(columns={"Origin":"Origin Identifier","Destination":"Destination Identifier"},inplace=True)
print(df_1)
print(df_2)
print(df_1.equals(df_2))
print(df_1.info(),df_2.info())

# There are nan values in merged dataframe because there in one record which is in placement data sheet but not in order data
l1 = placement["Order ID"].unique()
l2 = order["ID"].unique()
count =0
n=0
list = []
for l in l1:
    if l in l2:
        count = count+1
    else:
        n=n+1
        list.append(l)
        
print(count)
print(n)
print("Order ID which is not in Order data: {}".format(list))

# Calculating Fulfillment rate
dataset = pd.merge(placement.loc[:,["Order ID","Weight"]],order.loc[:,["ID","Requested Weight"]],how="left",left_on='Order ID',right_on='ID',suffixes=("",""))
print(dataset.info())
dataset.dropna(axis=0,inplace=True)
dataset=pd.DataFrame(dataset.groupby("Order ID").agg({"Weight":'sum',"Requested Weight":'mean'}))
dataset["Fulfillment_rate"]=dataset["Weight"]/dataset["Requested Weight"]
print(dataset)

#We can put order info on a placement spreadsheet, but not possible for me to put placement info on an order spreadsheet
#This is because to fulfill one order we require multiple truck based on the weight of
#the product to be delivered. So, One order Id can have various Placement IDs 
#and in order data sheet we only have unique order IDs 
#so we can't use put placement info into order data



