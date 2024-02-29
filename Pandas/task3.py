from numpy import mean
import pandas as pd

# Create a sample DataFrame
data = {
    "department": ["HR", "Engineering", "Engineering", "HR", "Sales"],
    'name' : ['siva','givi','sai','sala','AK',],
    "salary": [50000.0, 60000.0, 70000.0, 55000.0, 48000.0]
}

df = pd.DataFrame(data)

# Grouping and Aggregation Operations

# Group by department and calculate the total salary for each department
total_salary = df.groupby("department")["salary"].sum()

# Group by department and calculate the average salary for each department
average_salary = df.groupby("department")["salary"].mean()

# Group by department and calculate the minimum salary for each department
min_salary = df.groupby("department")["salary"].min()

# Group by department and calculate the maximum salary for each department
max_salary = df.groupby("department")["salary"].max()

# Group by department and calculate the number of employees in each department
employee_count = df.groupby("department")["name"].count()

# Custom Aggregation Functions

# Define a custom aggregate function to concatenate employee names
def concatenate_names(series):
    return ', '.join(series)

# Apply the custom aggregate function to get a comma-separated list of names per department
employee_names = df.groupby("department")["name"].agg(concatenate_names)

# Using Multiple Aggregation Functions

# Calculate multiple aggregations at once
agg_operations = df.groupby("department")["salary"].agg([sum, mean, min, max])

# Renaming Columns in the Result

# Rename columns in the result DataFrame
agg_operations = agg_operations.rename(columns={"sum": "Total Salary",
                                              "mean": "Average Salary",
                                              "min": "Minimum Salary",
                                              "max": "Maximum Salary"})

# Filtering Groups

# Filter groups based on a condition
high_salary_departments = df.groupby("department").filter(lambda group: group["salary"].mean() > 55000)

# Sorting the Result

# Sort the result by a specific column
sorted_result = total_salary.sort_values(ascending=False)

# Other Aggregations

# Calculate the median salary per department
median_salary = df.groupby("department")["salary"].median()

# Calculate the standard deviation of salary per department
std_dev_salary = df.groupby("department")["salary"].std()

# Calculate the variance of salary per department
variance_salary = df.groupby("department")["salary"].var()

# Find the top N earners in each department
top_earners = df.groupby("department").apply(lambda group: group.nlargest(2, 'salary'))

print("Total Salary Per Department:")
print(total_salary)
print('----------------------------------------------------------')

print("\nAverage Salary Per Department:")
print(average_salary)
print('----------------------------------------------------------')

print("\nMinimum Salary Per Department:")
print(min_salary)
print('----------------------------------------------------------')

print("\nMaximum Salary Per Department:")
print(max_salary)
print('----------------------------------------------------------')

print("\nNumber of Employees Per Department:")
print(employee_count)
print('----------------------------------------------------------')

print("\nEmployee Names Per Department:")
print(employee_names)
print('----------------------------------------------------------')

print("\nMultiple Aggregations:")
print(agg_operations)
print('----------------------------------------------------------')

print("\nHigh Salary Departments:")
print(high_salary_departments)
print('----------------------------------------------------------')

print("\nSorted Total Salary:")
print(sorted_result)
print('----------------------------------------------------------')

print("\nMedian Salary Per Department:")
print(median_salary)
print('----------------------------------------------------------')

print("\nStandard Deviation of Salary Per Department:")
print(std_dev_salary)
print('----------------------------------------------------------')

print("\nVariance of Salary Per Department:")
print(variance_salary)
print('----------------------------------------------------------')

print("\nTop Earners in Each Department:")
print(top_earners)
print('----------------------------------------------------------')

