import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.decomposition import PCA
from tkinter import filedialog, Tk


def select_csv_files():
    root = Tk()
    root.withdraw()  # Ukrycie głównego okna
    file_paths = filedialog.askopenfilenames(title="Wybierz pliki CSV", filetypes=[("Pliki CSV", "*.csv")])
    return file_paths


# Wybór plików CSV z okna dialogowego
csv_file_paths = select_csv_files()

# Inicjalizacja pustej macierzy do przechowywania połączonych macierzy pomyłek
combined_cm = None

for csv_file_path in csv_file_paths:
    if csv_file_path:
        # Wczytanie danych z pliku CSV
        data = pd.read_csv(csv_file_path, header=0, sep=',')  # Dodanie parametru header=0

        # Podział danych na cechy (X) i etykiety (y)
        X = data.drop(columns=['category'])
        y = data['category']

        # Dzielenie danych na część treningowy i testowy
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Inicjalizacja i trenowanie klasyfikatora SVM
        classifier = SVC(kernel='linear')
        classifier.fit(X_train, y_train)

        # Predykcja na zbiorze testowym
        y_pred = classifier.predict(X_test)

        # Obliczenie macierzy pomyłek
        labels = np.unique(y)  # Pobranie unikalnych etykiet
        cm = confusion_matrix(y_test, y_pred, labels=labels, normalize='true')

        # Dodanie macierzy pomyłek do połączonej macierzy
        if combined_cm is None:
            combined_cm = cm
        else:
            combined_cm += cm

# Utworzenie wykresu dla połączonej macierzy pomyłek
disp = ConfusionMatrixDisplay(confusion_matrix=combined_cm, display_labels= ['gras', 'laminat', 'tynk'])
disp.plot(cmap=plt.cm.Blues)
plt.show()

