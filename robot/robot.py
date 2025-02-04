import tkinter as tk
import pygame
from PIL import Image, ImageTk

# Inicializar Pygame Mixer
pygame.mixer.init()

# Función para reproducir audio
def play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Clase de la aplicación para explicar permutaciones con repeticiones
class PermutationExplainer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Explicación de Permutaciones con Repeticiones")
        self.geometry("800x700")  # Aumenta la altura para dejar espacio para el GIF en la parte inferior

        # Lista de pasos con texto y archivos de audio
        self.steps = [
            ("Enunciado del problema: calcular el número de palabras que se pueden formar con las letras de 'matemáticas'", "audio1.mp3"),
            ("Paso 1: Identificar las letras y sus repeticiones", "audio2.mp3"),
            ("Paso 2: Aplicar la fórmula de permutaciones con repeticiones (n!/n1!*n2!*...)", "audio3.mp3"),
            ("Paso 3: Calcular el factorial del número total de letras", "audio4.mp3"),
            ("Paso 4: Calcular el factorial de cada conjunto de letras repetidas", "audio5.mp3"),
            ("Paso 5: Dividir el factorial total por los factoriales de las repeticiones", "audio6.mp3"),
            ("Conclusión: El número de palabras posibles es...", "audio7.mp3")
        ]
        self.current_step = 0

        # Frame principal
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Texto para mostrar el paso
        self.label_text = tk.Label(self.main_frame, text=self.steps[self.current_step][0], wraplength=700)
        self.label_text.pack(pady=20)

        # Frame para las visualizaciones
        self.visualization_frame = tk.Frame(self.main_frame)
        self.visualization_frame.pack(pady=(20, 50))  # Ajusta el espacio inferior para el GIF

        # Cargar el GIF
        gif_path = "robot.gif"
        self.gif_image = Image.open(gif_path)
        self.gif_index = 0  # Índice para rastrear los fotogramas del GIF

        # Mostrar el GIF en un widget Label
        self.gif_label = tk.Label(self.main_frame)
        self.gif_label.pack(side=tk.BOTTOM, pady=(0, 10))  # Alinea el GIF en la parte inferior y agrega espacio

        # Reproducir el audio del primer paso
        play_audio(self.steps[self.current_step][1])

        # Botones para navegar
        self.button_prev = tk.Button(self.main_frame, text="Paso Anterior", command=self.prev_step)
        self.button_next = tk.Button(self.main_frame, text="Siguiente Paso", command=self.next_step)

        self.button_prev.place(relx=0, rely=0.5, anchor=tk.W, x=20)
        self.button_next.place(relx=1, rely=0.5, anchor=tk.E, x=-20)

        # Mostrar la palabra "matemáticas" en el primer paso
        self.display_word("matemáticas")

        # Actualizar el GIF continuamente
        self.update_gif()

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step()

    def update_step(self):
        # Eliminar el canvas actual si existe
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()

        # Actualizar el texto y reproducir el audio
        self.label_text.config(text=self.steps[self.current_step][0])
        play_audio(self.steps[self.current_step][1])

        # Mostrar las visualizaciones correspondientes a cada paso
        if self.current_step == 0:
            self.display_word("matemáticas")
        elif self.current_step == 1:
            self.highlight_repeated_letters()
        elif self.current_step == 2:
            self.display_formula()
        elif self.current_step == 3:
            self.display_factorial_total()
        elif self.current_step == 4:
            self.display_factorial_repetitions()
        elif self.current_step == 5:
            self.display_division_fraction()
        elif self.current_step == 6:
            self.display_result()

    def display_word(self, word):
        # Muestra la palabra en la ventana
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        x = 50
        for letter in word:
            self.current_canvas.create_text(x, 25, text=letter, font=("Arial", 20))
            x += 30

    def highlight_repeated_letters(self):
        # Destaca las letras repetidas con diferentes colores
        word = "matemáticas"
        colors = {'m': 'green', 'a': 'red', 't': 'blue', 'e': 'purple', 'i': 'orange', 'c': 'yellow', 's': 'pink'}
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        x = 50
        for letter in word:
            color = colors.get(letter, 'black')
            self.current_canvas.create_text(x, 25, text=letter, font=("Arial", 20), fill=color)
            x += 30

    def display_formula(self):
        # Muestra la fórmula en la ventana
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        formula_text = "n! / (n1! * n2! * ...)"
        self.current_canvas.create_text(350, 25, text=formula_text, font=("Arial", 20))

    def display_factorial_total(self):
        # Muestra el factorial total en la ventana
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        factorial_text = "11! = 39916800"
        self.current_canvas.create_text(350, 25, text=factorial_text, font=("Arial", 20))

    def display_factorial_repetitions(self):
        # Muestra el factorial de las repeticiones en la ventana
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        factorial_text = "3! * 2! * 2! = 24"
        self.current_canvas.create_text(350, 25, text=factorial_text, font=("Arial", 20))

    def display_division_fraction(self):
        # Muestra la fracción de la división en la ventana
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        fraction_text = "39916800 / 24"
        self.current_canvas.create_text(350, 25, text=fraction_text, font=("Arial", 20))

    def display_result(self):
        # Calcula y muestra el resultado de la división en la ventana
        result = 39916800 / 24
        self.current_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        self.current_canvas.pack()
        result_text = f"Resultado: {result}"
        self.current_canvas.create_text(350, 25, text=result_text, font=("Arial", 20))

    def load_next_frame(self):
        try:
            # Obtener el siguiente fotograma del GIF
            self.gif_image.seek(self.gif_index)
            frame = self.gif_image.copy()
            self.gif_index += 1

            # Convertir el fotograma en un objeto de imagen de Tkinter y mostrarlo
            self.gif_tk = ImageTk.PhotoImage(frame)
            self.gif_label.config(image=self.gif_tk)
            self.gif_label.image = self.gif_tk

            # Programar la carga del siguiente fotograma
            self.after(100, self.load_next_frame)
        except EOFError:
            # Reiniciar la animación si llegamos al final del GIF
            self.gif_index = 0
            self.load_next_frame()

    def update_gif(self):
        # Actualizar el GIF continuamente
        self.load_next_frame()

# Ejecutar la aplicación
if __name__ == "__main__":
    app = PermutationExplainer()
    app.mainloop()
