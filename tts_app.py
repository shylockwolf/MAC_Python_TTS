import os
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import wave
import sys
from piper import PiperVoice

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piper TTS Generator")
        self.root.geometry("600x350")

        # Variables
        self.model_path = tk.StringVar()
        self.text_file_path = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.available_models = []

        # Initialize UI
        self.create_menu()
        self.create_widgets()
        
        # Load models on startup
        self.load_models()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Text File...", command=self.select_text_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Piper TTS Generator\nPowered by Piper TTS"))

    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        # Model Selection
        model_frame = tk.LabelFrame(main_frame, text="Model Configuration", padx=10, pady=10)
        model_frame.pack(fill="x", pady=(0, 10))

        tk.Label(model_frame, text="Select Voice:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.model_combobox = ttk.Combobox(model_frame, textvariable=self.model_path, width=50, state="readonly")
        self.model_combobox.grid(row=0, column=1, padx=5, sticky="ew")
        
        tk.Button(model_frame, text="Refresh", command=self.load_models).grid(row=0, column=2, padx=5)

        # File Selection
        file_frame = tk.LabelFrame(main_frame, text="Text File Selection", padx=10, pady=10)
        file_frame.pack(fill="x", pady=(0, 10))

        tk.Label(file_frame, text="Text File:").grid(row=0, column=0, sticky="w", padx=(0, 5))
        tk.Entry(file_frame, textvariable=self.text_file_path, width=40).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(file_frame, text="Browse...", command=self.select_text_file).grid(row=0, column=2, padx=5)

        # Generate Button
        tk.Button(main_frame, text="Generate Audio", command=self.generate_audio, bg="#4CAF50", fg="black", font=("Arial", 12, "bold"), height=2).pack(fill="x", pady=10)

        # Status Bar
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w", padx=5)
        status_bar.pack(side="bottom", fill="x")

        # Grid configuration
        model_frame.columnconfigure(1, weight=1)
        file_frame.columnconfigure(1, weight=1)

    def load_models(self):
        models_dir = os.path.join(os.getcwd(), "models")
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
        
        self.available_models = []
        try:
            for f in os.listdir(models_dir):
                if f.endswith(".onnx"):
                    full_path = os.path.join(models_dir, f)
                    self.available_models.append(full_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load models: {e}")

        if self.available_models:
            # Update combobox values to show filenames only, but store full path in logic if needed
            # Actually, let's just show filenames in the box
            display_names = [os.path.basename(m) for m in self.available_models]
            self.model_combobox['values'] = display_names
            if display_names:
                self.model_combobox.current(0) # Select first one
                self.model_path.set(display_names[0])
            self.status_var.set(f"Loaded {len(self.available_models)} models.")
        else:
            self.model_combobox['values'] = []
            self.status_var.set("No models found in ./models directory.")
            messagebox.showinfo("No Models", "No voice models found in the 'models' folder.\nPlease download a .onnx model and its .json config.")

    def select_text_file(self):
        filename = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filename:
            self.text_file_path.set(filename)

    def generate_audio(self):
        # model_path might just be the filename from combobox
        selected_model_name = self.model_path.get()
        if not selected_model_name:
             messagebox.showerror("Error", "Please select a voice model.")
             return

        # Find full path
        models_dir = os.path.join(os.getcwd(), "models")
        model_file = os.path.join(models_dir, selected_model_name)
        
        text_file = self.text_file_path.get()

        if not os.path.exists(model_file):
            # Fallback if user manually entered a path or something weird happened
            if os.path.exists(selected_model_name):
                model_file = selected_model_name
            else:
                messagebox.showerror("Error", f"Model file not found: {model_file}")
                return

        if not text_file or not os.path.exists(text_file):
            messagebox.showerror("Error", "Please select a valid text file.")
            return

        # Determine output filename
        base_name = os.path.splitext(text_file)[0]
        output_wav = f"{base_name}.wav"

        self.status_var.set("Loading model...")
        self.root.update()

        try:
            voice = PiperVoice.load(model_file)
            
            self.status_var.set("Reading text...")
            self.root.update()
            
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()

            self.status_var.set("Synthesizing audio...")
            self.root.update()

            # Synthesize
            with wave.open(output_wav, "wb") as wav_file:
                voice.synthesize_wav(text, wav_file)

            self.status_var.set(f"Done! Saved to {os.path.basename(output_wav)}")
            messagebox.showinfo("Success", f"Audio generated successfully:\n{output_wav}")

        except Exception as e:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", str(e))
            print(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()
