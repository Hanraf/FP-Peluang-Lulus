import numpy as np
from sklearn.model_selection import train_test_split

# Fungsi keanggotaan untuk indikator nilai
def nilai(x):
    if x >= 3.1 and x <= 4.0:
        return 1.0
    elif x >= 2.5 and x <= 3.0:
        return 0.5
    elif x <= 2.4:
        return 0.0

# Fungsi keanggotaan untuk indikator pengambilan SKS
def sks(x):
    if x >= 20 and x <= 24:
        return 1.0
    elif x >= 16 and x < 20:
        return 0.5
    elif x <= 15:
        return 0.0

# Fungsi keanggotaan untuk indikator semester
def semester(x):
    if x >= 1 and x <= 3:
        return 1.0
    elif x >= 4 and x <= 6:
        return 0.5
    elif x > 6:
        return 0.0

# Fungsi inferensi menggunakan metode Sugeno
def sugeno_inference(nilai_input, sks_input, semester_input):
    rules = {
        'Tepat waktu': max(min(nilai_input, sks_input, semester_input), 0.5),
        'Tidak tepat waktu': max(min(nilai_input, sks_input, 1 - semester_input), 0.5)
    }

    return rules

# Fungsi defuzzifikasi menggunakan metode weighted average
def defuzzification(rules):
    numerator = 0.0
    denominator = 0.0

    for key, value in rules.items():
        if key == 'Tepat waktu':
            numerator += value * 100
        elif key == 'Tidak tepat waktu':
            numerator += value * 0
        denominator += value

    if denominator != 0:
        return numerator / denominator
    else:
        return 0

# Fungsi untuk menghitung tingkat akurasi
def compute_accuracy(predicted, actual):
    return np.sum(predicted == actual) / len(actual)

# Generate dataset
np.random.seed(42)
nilai_dataset = np.random.uniform(2.0, 4.1, size=1000)
sks_dataset = np.random.randint(10, 25, size=1000)
semester_dataset = np.random.randint(1, 10, size=1000)
lulus_dataset = []

# Membangun dataset lulus berdasarkan indikator-indikator
for i in range(len(nilai_dataset)):
    nilai_input = nilai(nilai_dataset[i])
    sks_input = sks(sks_dataset[i])
    semester_input = semester(semester_dataset[i])
    
    inference_result = sugeno_inference(nilai_input, sks_input, semester_input)
    defuzzified_value = defuzzification(inference_result)
    
    if defuzzified_value >= 50:
        lulus_dataset.append(1)  # Lulus
    else:
        lulus_dataset.append(0)  # Tidak lulus

lulus_dataset = np.array(lulus_dataset)

# Split dataset menjadi training set dan test set
nilai_train, nilai_test, lulus_train, lulus_test = train_test_split(nilai_dataset, lulus_dataset, test_size=0.2, random_state=42)
sks_train, sks_test, _, _ = train_test_split(sks_dataset, lulus_dataset, test_size=0.2, random_state=42)
semester_train, semester_test, _, _ = train_test_split(semester_dataset, lulus_dataset, test_size=0.2, random_state=42)

# Melakukan prediksi pada dataset uji
predictions = []
for i in range(len(nilai_test)):
    nilai_input = nilai(nilai_test[i])
    sks_input = sks(sks_test[i])
    semester_input = semester(semester_test[i])
    
    inference_result = sugeno_inference(nilai_input, sks_input, semester_input)
    defuzzified_value = defuzzification(inference_result)
    
    if defuzzified_value >= 50:
        predictions.append(1)  # Lulus
    else:
        predictions.append(0)  # Tidak lulus

predictions = np.array(predictions)

# Menghitung tingkat akurasi dari dataset uji
accuracy = compute_accuracy(predictions, lulus_test)
print("Tingkat akurasi: {:.2f}%".format(accuracy * 100))
