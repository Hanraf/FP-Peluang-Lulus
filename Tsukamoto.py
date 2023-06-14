import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd

# Membaca data dari file Excel
data = pd.read_excel('nama_file.xlsx')

# Membuat variabel input
nilai_ip = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'Nilai IP')
total_sks = ctrl.Antecedent(np.arange(0, 151, 1), 'Total SKS')

# Membuat variabel output
kemungkinan_lulus = ctrl.Consequent(np.arange(0, 101, 1), 'Kemungkinan Lulus')

# Definisi fungsi keanggotaan untuk variabel input dan output
nilai_ip['rendah'] = fuzz.trapmf(nilai_ip.universe, [0, 0, 1.5, 2.5])
nilai_ip['sedang'] = fuzz.trimf(nilai_ip.universe, [1.5, 2.5, 3.5])
nilai_ip['tinggi'] = fuzz.trapmf(nilai_ip.universe, [2.5, 3.5, 4, 4])

total_sks['rendah'] = fuzz.trapmf(total_sks.universe, [0, 0, 50, 75])
total_sks['sedang'] = fuzz.trimf(total_sks.universe, [50, 75, 100])
total_sks['tinggi'] = fuzz.trapmf(total_sks.universe, [75, 100, 150, 150])

kemungkinan_lulus['rendah'] = fuzz.trapmf(kemungkinan_lulus.universe, [0, 0, 30, 50])
kemungkinan_lulus['sedang'] = fuzz.trimf(kemungkinan_lulus.universe, [30, 50, 70])
kemungkinan_lulus['tinggi'] = fuzz.trapmf(kemungkinan_lulus.universe, [50, 70, 100, 100])

# Membuat aturan fuzzy
rule1 = ctrl.Rule(nilai_ip['rendah'] | total_sks['rendah'], kemungkinan_lulus['rendah'])
rule2 = ctrl.Rule(nilai_ip['sedang'], kemungkinan_lulus['sedang'])
rule3 = ctrl.Rule(nilai_ip['tinggi'] & total_sks['tinggi'], kemungkinan_lulus['tinggi'])

# Membuat sistem kontrol fuzzy
kemungkinan_lulus_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
kemungkinan_lulus_estimasi = ctrl.ControlSystemSimulation(kemungkinan_lulus_ctrl)

# Memasukkan data dari dataset ke dalam sistem kontrol fuzzy
for index, row in data.iterrows():
    kemungkinan_lulus_estimasi.input['Nilai IP'] = row['Nilai IP']
    kemungkinan_lulus_estimasi.input['Total SKS'] = row['Total SKS']

    # Melakukan perhitungan
    kemungkinan_lulus_estimasi.compute()

    # Mendapatkan hasil output
    print("Kemungkinan Lulus:", kemungkinan_lulus_estimasi.output['Kemungkinan Lulus'])
