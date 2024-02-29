import pandas as pd

data ={
    'Name' : ['siva','givi','sai','sala','AK',],
    'Age' :[24,21,21,23,22,],
    'Salary':[10000,22000,22000,20000,35000],
    'City': ['New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Miami']
}
df = pd.DataFrame(data)
# selecting column
column = df[['Name','Age']]
print(column)
print("--------------------")

# filltering  rows
fillter = df[df['Age']>=21]
print(fillter)

print('---------------------')
# add new column
df['Experience'] = [4, 6, 8, 5, 3]
print(df)
print('------------------')
# modify the data
df.loc[df['Name']== 'siva','Salary']= 20000
print(df) 
print('----------------------')

# sorting
sorted_df = df.sort_values(by='Salary', ascending=False)
print("\nSorted DataFrame (by Salary):")
print(sorted_df)
print('-------------------------')

# grouping and aggregation
grouped = df.groupby('City')
result = grouped['Salary'].mean()
print("\nGrouped and Aggregated DataFrame (Mean Salary by City):")
print(result)
print('-------------------------')
# summary
summary = df.describe()
print("\nSummary Statistics:")
print(summary)

df.to_csv('create data.csv',index= False)