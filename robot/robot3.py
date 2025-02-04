import tkinter as tk
import pygame
from PIL import Image, ImageTk
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/robot')
def show_robot_interface():
    return render_template('robot_interface.html')

# Inicializar Pygame Mixer
pygame.mixer.init()

# Función para reproducir audio
def play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

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

        # Frame para la palabra inicial
        self.initial_word_frame = tk.Frame(self.main_frame)
        self.initial_word_frame.pack(pady=(20, 0))

        # Mostrar la palabra "matemáticas" en negro al inicio
        self.display_initial_word()

        # Frame para las visualizaciones
        self.visualization_frame = tk.Frame(self.main_frame)
        self.visualization_frame.pack(pady=(20, 50))  # Ajusta el espacio inferior para el GIF

        # Variables para controlar la animación del GIF
        self.gif_running = False
        self.gif_index = 0
        self.gif_frames = []  # Lista para almacenar los frames del GIF

        # Cargar el GIF y los fotogramas
        self.load_gif_frames()

        # Mostrar el GIF en un widget Label
        self.gif_label = tk.Label(self.main_frame)
        self.gif_label.pack(side=tk.BOTTOM, pady=(0, 10))  # Alinea el GIF en la parte inferior y agrega espacio

        # Iniciar la reproducción del audio y el GIF al inicio
        self.play_audio_and_start_gif()

        # Botones para navegar
        self.button_prev = tk.Button(self.main_frame, text="Paso Anterior", command=self.prev_step)
        self.button_next = tk.Button(self.main_frame, text="Siguiente Paso", command=self.next_step)

        self.button_prev.place(relx=0, rely=0.5, anchor=tk.W, x=20)
        self.button_next.place(relx=1, rely=0.5, anchor=tk.E, x=-20)

        # Verificar el estado del audio y actualizar el GIF continuamente
        self.check_audio()
        self.update_gif()

    def load_gif_frames(self):
        gif_path = "robot.gif"
        self.gif_image = Image.open(gif_path)
        try:
            while True:
                self.gif_image.seek(len(self.gif_frames))
                frame = self.gif_image.copy()
                self.gif_frames.append(ImageTk.PhotoImage(frame))
        except EOFError:
            pass

    def load_next_frame(self):
        if self.gif_running:
            self.gif_index += 1
            if self.gif_index >= len(self.gif_frames):
                self.gif_index = 0

            self.gif_label.config(image=self.gif_frames[self.gif_index])
            self.gif_label.image = self.gif_frames[self.gif_index]

            self.after(100, self.load_next_frame)

    def play_audio_and_start_gif(self):
        # Reproducir el audio del primer paso
        play_audio(self.steps[self.current_step][1])

        # Mostrar el primer fotograma del GIF
        if self.gif_frames:
            self.gif_label.config(image=self.gif_frames[self.gif_index])
            self.gif_label.image = self.gif_frames[self.gif_index]
            self.gif_running = True
            self.load_next_frame()

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step()

    def update_step(self):
        # Detener la animación del GIF si se cambia de paso
        self.gif_running = False

        # Actualizar el texto y reproducir el audio
        self.label_text.config(text=self.steps[self.current_step][0])
        play_audio(self.steps[self.current_step][1])

        # Reiniciar el GIF al cambiar de paso
        self.gif_index = 0  # Reiniciar el índice del GIF para cargar desde el primer fotograma
        self.play_audio_and_start_gif()  # Iniciar el audio y el GIF

        # Mostrar todas las visualizaciones hasta el paso actual
        self.display_visualization()

    def display_initial_word(self):
        # Mostrar la palabra en la ventana inicialmente en negro
        self.word_canvas = tk.Canvas(self.initial_word_frame, width=700, height=50)
        self.word_canvas.pack()
        word = "matemáticas"
        x = 50
        for letter in word:
            self.word_canvas.create_text(x, 25, text=letter, font=("Arial", 20))
            x += 30

    def highlight_repeated_letters(self):
        # Destacar las letras repetidas con diferentes colores
        word = "matemáticas"
        colors = {'m': 'green', 'a': 'red', 't': 'blue', 'e': 'purple', 'i': 'orange', 'c': 'yellow', 's': 'pink'}
        highlight_canvas = tk.Canvas(self.visualization_frame, width=700, height=50)
        highlight_canvas.pack()
        x = 50
        for letter in word:
            color = colors.get(letter, 'black')
            highlight_canvas.create_text(x, 25, text=letter, font=("Arial", 20), fill=color)
            x += 30

    def display_visualization(self):
        # Limpiar las visualizaciones anteriores
        for widget in self.visualization_frame.winfo_children():
            widget.destroy()

        # Mostrar todas las visualizaciones hasta el paso actual
        for i in range(1, self.current_step + 1):
            if i == 1:
                self.highlight_repeated_letters()
            elif i == 2:
                self.display_formula()
            elif i == 3:
                self.display_factorial_total()
            elif i == 4:
                self.display_factorial_repetitions()
            elif i == 5:
                self.display_division_fraction()
            elif i == 6:
                self.display_result()

    def display_formula(self):
        # Mostrar la fórmula en la ventana
        formula_label = tk.Label(self.visualization_frame, text="n! / (n1! * n2! * ...)", font=("Arial", 20))
        formula_label.pack()

    def display_factorial_total(self):
        # Mostrar el factorial total en la ventana
        factorial_label = tk.Label(self.visualization_frame, text="11! = 39916800", font=("Arial", 20))
        factorial_label.pack()

    def display_factorial_repetitions(self):
        # Mostrar el factorial de las repeticiones en la ventana
        factorial_repetitions_label = tk.Label(self.visualization_frame, text="3! * 2! * 2! = 24", font=("Arial", 20))
        factorial_repetitions_label.pack()

    def display_division_fraction(self):
        # Mostrar la fracción de la división en la ventana
        division_label = tk.Label(self.visualization_frame, text="39916800 / 24", font=("Arial", 20))
        division_label.pack()

    def display_result(self):
        # Calcular y mostrar el resultado
        result = 39916800 / 24
        result_label = tk.Label(self.visualization_frame, text=f"Resultado: {result} palabras posibles que se pueden formar con las letras de 'matemáticas'.", font=("Arial", 20))
        result_label.pack()

    def check_audio(self):
        if not pygame.mixer.music.get_busy():
            self.gif_running = False  # Detener el GIF si el audio no está reproduciéndose
        self.after(100, self.check_audio)  # Verificar el estado del audio cada 100 ms

    def update_gif(self):
        if self.gif_running:
            self.load_next_frame()  # Cargar el siguiente fotograma del GIF si está en ejecución
        self.after(100, self.update_gif)  # Actualizar el GIF cada 100 milisegundos

# Instanciar y ejecutar la aplicación
if __name__ == "__main__":
    app = PermutationExplainer()
    app.mainloop()
