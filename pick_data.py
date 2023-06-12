import pandas as pd
import os

# Membutuhkan pandas, openpyxl

# Membaca file Excel
data = pd.read_excel(os.path.join(os.path.dirname(__file__),'data_lulus.xlsx'))

# Melihat struktur data
print(data.head())

# Memperoleh kolom yang diperlukan
total_sks = data['Total SKS']
nilai_ip = data['Nilai IP']
semester = data['Semester']
kemungkinan_lulus = data['Kemungkinan Lulus']