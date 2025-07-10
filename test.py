import pandas as pd

df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4, 5],
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Value': [100, 150, 200, 250, 300]
})

df2 = pd.DataFrame({
    'ID': [3, 5, 6, 7],
    'Name': ['Charlie', 'Eve', 'Frank', 'Grace'],
    'Value': [200, 300, 350, 400]
})

merged_df = pd.merge(df1, df2, on=['ID', 'Name', 'Value'], how='left', indicator=True)

df1_rows_not_in_df2 = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')

print(df1_rows_not_in_df2)