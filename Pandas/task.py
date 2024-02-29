import pandas as pd

data ={
    'Name' : ['siva','givi','givi','sala','AK',],
    'Age' :[24,'21','21',23,None,],
    'Salary':['10,000','22,000','22,000','20,000','35,000']
}
df = pd.DataFrame(data)
print(df)
print('-------------------')

# Data Cleaning Operations
#Replace Only For Specified Columns
df['Age'].fillna(22,inplace= True)
print(df)
print('---------------------')

# removing duplicates
df.dropna(inplace= True)
print(df)
print("--------------------")



#Removing Duplicates
df.drop_duplicates(inplace= True) 
print(df)
print('---------------------')

#  Renaming Columns
df.rename(columns={'Name': 'Full Name'}, inplace=True)

print(df)
print('---------------------')

df.to_csv('cleaned_data.csv', index=False)
 

