import os
from tkinter import *
from tkinter import filedialog
from PIL import Image

def select_folder():
    folder_path = filedialog.askdirectory()
    entry_path.delete(0, END)
    entry_path.insert(END, folder_path)

def process_images():
    source_folder = entry_path.get()
    image_size = int(entry_size.get())

    success_message.set("Przetwarzanie zdjęć w toku...")

    for filename in os.listdir(source_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(source_folder, filename)
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    x_slices = width // image_size
                    y_slices = height // image_size
                    for y in range(y_slices):
                        for x in range(x_slices):
                            box = (x * image_size, y * image_size, (x + 1) * image_size, (y + 1) * image_size)
                            cropped_img = img.crop(box)
                            category_folder = os.path.join(source_folder, filename[:-4])
                            if not os.path.exists(category_folder):
                                os.makedirs(category_folder)
                            cropped_img.save(os.path.join(category_folder, f"{x}_{y}.png"))
                success_message.set("Przetwarzanie zdjęć zakończone pomyślnie.")
            except Exception as e:
                success_message.set(f"Błąd przetwarzania {image_path}: {e}")

# Tworzenie interfejsu użytkownika
root = Tk()
root.title("Texture Image Cutter")
root.geometry('1000x200')

label_path = Label(root, text="Wybierz folder z obrazami (.png):")
label_path.grid(row=0, column=0, padx=10, pady=5)

entry_path = Entry(root, width=50)
entry_path.grid(row=0, column=1, padx=10, pady=5)

button_browse = Button(root, text="Przeglądaj", command=select_folder)
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_size = Label(root, text="Podaj rozmiar fragmentu w pikselach (np. wpisz '128', w celu uzyskania rozmiaru 128x128):")
label_size.grid(row=1, column=0, padx=10, pady=5)

entry_size = Entry(root, width=10)
entry_size.grid(row=1, column=1, padx=10, pady=5)

button_process = Button(root, text="Przetwórz obrazy", command=process_images)
button_process.grid(row=1, column=2, padx=5, pady=5)

success_message = StringVar()
success_label = Label(root, textvariable=success_message)
success_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

root.mainloop()

