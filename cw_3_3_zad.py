import os
import numpy as np
import pandas as pd
from tkinter import Tk, filedialog
from skimage import io, color
from skimage.util import img_as_ubyte
from skimage.feature import graycomatrix, graycoprops


def compute_texture_features(image, distances, angles):
    features = []
    if len(image.shape) == 3 and image.shape[2] == 4:  #Sprawdź, czy obraz ma kanał alfa (RGBA)
        image = image[:, :, :3]  #Ignoruj kanał alfa

    gray_image = color.rgb2gray(image)
    gray_image = img_as_ubyte(gray_image)  #Zmniejszenie głębi jasności do 8 bitów (256 poziomów)

    #Obliczenie macierzy zdarzeń dla każdej kombinacji odległości i kierunku
    for d in distances:
        for a in angles:
            glcm = graycomatrix(gray_image, distances=[d], angles=[a], levels=256, symmetric=True, normed=True)
            props = [graycoprops(glcm, prop)[0, 0] for prop in ['dissimilarity', 'correlation', 'contrast', 'energy', 'homogeneity', 'ASM']]
            features.extend(props)

    return features

def process_texture_samples():
    root = Tk()
    root.withdraw()  #Ukryj główne okno tkinter

    input_folder = filedialog.askdirectory()  # Wybierz folder za pomocą okna dialogowego

    if not input_folder:
        print("Nie wybrano folderu.")
        return

    output_file = os.path.join(input_folder, input_folder + "wynik.csv")

    data = []

    #Przetwarzanie każdego obrazu w folderze
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(input_folder, filename)
            image = io.imread(image_path)
            features = compute_texture_features(image, distances=[1, 3, 5],angles=[0, np.pi / 4, np.pi / 2, 3 * np.pi / 4])
            category = filename.split('_')[0]  # Kategoria tekstury to nazwa pliku przed pierwszym podkreśleniem
            data.append(features + [category])

    #Tworzenie ramki danych Pandas i zapis do pliku CSV
    columns = [f"{prop}_{d}_{a}" for d in [1, 3, 5] for a in [0, 45, 90, 135] for prop in ['dissimilarity', 'correlation', 'contrast', 'energy', 'homogeneity', 'ASM']] + ['category']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_file, index=False)

    print(f"Plik CSV został zapisany w folderze: {output_file}")

#Uruchomienie programu
process_texture_samples()
