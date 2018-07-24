import pandas as pd
import os
writer = pd.ExcelWriter('DTM.xlsx', engine='xlsxwriter')

for file in os.listdir(r"C:\Users\212616592\Projects\webtoons_crawler\DTM"):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(r"C:\Users\212616592\Projects\webtoons_crawler\DTM", file))
        print(os.path.join(r"C:\Users\212616592\Projects\webtoons_crawler\DTM", file))
        df.to_excel(writer, sheet_name=file)
writer.save()