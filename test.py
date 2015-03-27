csv_text = """\
Title,Year,Director
North by Northwest,1959,Alfred Hitchcock
Notorious,1946,Alfred Hitchcock
The Philadelphia Story,1940,George Cukor
To Catch a Thief,1955,Alfred Hitchcock
His Girl Friday,1940,Howard Hawks
"""

import pandas as pd

df1 = pd.read_csv('sample.csv')
df1.columns = map(str.lower, df1.columns)
print(df1)

df2 = df1.groupby(['director', df1.index]).first()
df3 = df2.reset_index('director')
df4 = df3[['title', 'year', 'director']]
df5 = df4.sort_index()
print(df5)

print()
print(repr(df1.columns))
print(repr(df5.columns))
print()
print(df1.dtypes)
print(df5.dtypes)
print()
print(df1 == df5)
print()
print(df1.index == df5.index)
print()
print(df1.equals(df5))
