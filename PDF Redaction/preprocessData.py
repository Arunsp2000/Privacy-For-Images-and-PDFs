import pandas as pd
from redaction import Redaction

input_csv_path = 'validation.csv'
df = pd.read_csv(input_csv_path)

red = Redaction(useAsApi=1)
def morph(value):
    try:
        value = red.replacePiiWithRegex(value)
        value = red.replacePiiWithSpacy(value)
    except:
        return ""  
    return value


df['fakeText'] = df['article'].apply(morph)


result_df = df[['article', 'fakeText']]

output_csv_path = 'output.csv'
result_df.to_csv(output_csv_path, index=False)

print(f"New CSV file created: {output_csv_path}")
