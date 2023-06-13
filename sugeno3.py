import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fungsi keanggotaan untuk indikator nilai
indikator_nilai = ctrl.Antecedent(np.arange(2.4, 4.1, 0.1), 'indikator_nilai')
indikator_nilai['berprestasi'] = fuzz.trapmf(indikator_nilai.universe, [3.1, 3.1, 4.0, 4.0])
indikator_nilai['cukup'] = fuzz.trimf(indikator_nilai.universe, [2.5, 3.0, 3.0])
indikator_nilai['kurang'] = fuzz.trapmf(indikator_nilai.universe, [2.4, 2.4, 2.4, 3.0])

# Fungsi keanggotaan untuk indikator pengambilan sks
indikator_pengambilan_sks = ctrl.Antecedent(np.arange(15, 25, 1), 'indikator_pengambilan_sks')
indikator_pengambilan_sks['tinggi'] = fuzz.trapmf(indikator_pengambilan_sks.universe, [20, 20, 24, 24])
indikator_pengambilan_sks['sedang'] = fuzz.trimf(indikator_pengambilan_sks.universe, [16, 20, 24])
indikator_pengambilan_sks['rendah'] = fuzz.trapmf(indikator_pengambilan_sks.universe, [15, 15, 15, 20])

# Fungsi keanggotaan untuk semester saat ini
semester_saat_ini = ctrl.Antecedent(np.arange(1, 8, 1), 'semester_saat_ini')
semester_saat_ini['awal'] = fuzz.trapmf(semester_saat_ini.universe, [1, 1, 3, 3])
semester_saat_ini['tengah'] = fuzz.trimf(semester_saat_ini.universe, [4, 5, 6])
semester_saat_ini['akhir'] = fuzz.trapmf(semester_saat_ini.universe, [6, 7, 7, 7])

# Fungsi keanggotaan untuk kemungkinan lulus
kemungkinan_lulus = ctrl.Consequent(np.arange(0, 101, 1), 'kemungkinan_lulus')
kemungkinan_lulus['rendah'] = fuzz.trimf(kemungkinan_lulus.universe, [0, 0, 50])
kemungkinan_lulus['tinggi'] = fuzz.trimf(kemungkinan_lulus.universe, [50, 100, 100])

# Menentukan aturan fuzzy
rule1 = ctrl.Rule(indikator_nilai['berprestasi'] & indikator_pengambilan_sks['tinggi'] & semester_saat_ini['akhir'], kemungkinan_lulus['tinggi'])
rule2 = ctrl.Rule(indikator_nilai['cukup'] & indikator_pengambilan_sks['sedang'] & semester_saat_ini['tengah'], kemungkinan_lulus['tinggi'])
rule3 = ctrl.Rule(indikator_nilai['kurang'] & indikator_pengambilan_sks['rendah'] & semester_saat_ini['awal'], kemungkinan_lulus['rendah'])

# Membangun sistem inferensi fuzzy
fuzzy_system = ctrl.ControlSystem([rule1, rule2, rule3])
fuzzy_simulator = ctrl.ControlSystemSimulation(fuzzy_system)

# Contoh penggunaan fuzzy sugeno dengan data uji
nilai = 3.5
pengambilan_sks = 22
semester = 5

# Set nilai variabel input pada simulator fuzzy
fuzzy_simulator.input['indikator_nilai'] = nilai
fuzzy_simulator.input['indikator_pengambilan_sks'] = pengambilan_sks
fuzzy_simulator.input['semester_saat_ini'] = semester

# Melakukan perhitungan fuzzy
fuzzy_simulator.compute()

# Mendapatkan hasil output
hasil = fuzzy_simulator.output['kemungkinan_lulus']
print('Hasil:', hasil)
