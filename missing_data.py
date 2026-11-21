import pandas as pd

# run final output panel
df = pd.read_excel('OPECPlus_Full_Panel_Data_Clean.xlsx')

print('=== تعداد داده‌های مفقود در Renewable_Share به تفکیک کشور ===')
print(df[df['Renewable_Share'].isnull()]['Economy'].value_counts())

print('\n=== تعداد داده‌های مفقود در Renewable_Share به تفکیک سال ===')
print(df[df['Renewable_Share'].isnull()]['Year'].value_counts().sort_index())
