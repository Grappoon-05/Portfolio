# hmi.py
# Tkinter graphical user interface for the operator
# Communicate with the FastAPI server (main.py) via HTTP requests

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import requests
import shutil
import os

# ── Parameters for the connexion to the server ──────────────────────────────────────
SERVER_URL = "http://localhost:5000/scan"


# ── Principal class of the window ────────────────────────────────────────
class IHM(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Read serial number")
        self.geometry("550x480")
        self.resizable(False, False)

        # Status variable
        self.path_image = None          # Local path of the selected image
        self.path_txt_server = None    # Path of the .txt file sent by the server
        self.is_circular = tk.BooleanVar(value=False)  # Case to check

        self._build_interface()

    # ── Construction of widgets ─────────────────────────────────────────────
    def _build_interface(self):

        # --- Block 1 : selection of the image ---
        image_frame = tk.LabelFrame(self, text="Image to analyse", padx=10, pady=8)
        image_frame.pack(fill="x", padx=15, pady=(15, 5))

        self.file_label = tk.Label(image_frame, text="No file selected",
                                      fg="grey", anchor="w")
        self.file_label.pack(side="left", expand=True, fill="x")

        browse_button = tk.Button(image_frame, text="Browse…",
                                  command=self._choose_image)
        browse_button.pack(side="right")

        # --- Block 2 : options ---
        options_frame = tk.LabelFrame(self, text="Options", padx=10, pady=8)
        options_frame.pack(fill="x", padx=15, pady=5)

        # Check box : circular text
        # Its value (True/False) is sent to the server in the file name
        # and read in main.py via the variable is_circular
        check_circular = tk.Checkbutton(
            options_frame,
            text="Is it circular ? (apply polar warp)",
            variable=self.is_circular
        )
        check_circular.pack(anchor="w")

        # --- Block 3 : run script button ---
        self.scan_button = tk.Button(self, text="▶  Scan",
                                  font=("Arial", 11, "bold"),
                                  bg="#2563eb", fg="white",
                                  activebackground="#1d4ed8",
                                  padx=12, pady=6,
                                  command=self._run_scan,
                                  state="disabled")   # désactivé tant qu'aucune image
        self.scan_button.pack(pady=10)

        # --- Block 4 : result text ---
        result_frame = tk.LabelFrame(self, text="Detected text", padx=10, pady=8)
        result_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Text box with a scroll bar, read-only
        self.text_zone = scrolledtext.ScrolledText(result_frame, height=8,
                                                     state="disabled",
                                                     wrap="word")
        self.text_zone.pack(fill="both", expand=True)

        # --- Block 5 : Download button for the .txt ---
        self.download_button = tk.Button(self, text="💾  Download file .txt",
                                         command=self._download_txt,
                                         state="disabled")  # activé après un scan réussi
        self.download_button.pack(pady=(0, 15))

    # ── Actions ─────────────────────────────────────────────────────────────

    def _choose_image(self):
        """Open a file explorer to select the image."""
        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("Tous", "*.*")]
        )
        if path:
            self.path_image = path
            # Affiche uniquement le nom du fichier (pas le chemin complet)
            self.file_label.config(text=os.path.basename(path), fg="black")
            self.scan_button.config(state="normal")   # on peut maintenant lancer

    def _run_scan(self):
        """Send the image to the server and retrieve the result."""
        if not self.path_image:
            messagebox.showwarning("Warning", "Please choose an image first")
            return

        self.scan_button.config(text="Analysing…", state="disabled")
        self.update()  # forces the interface to refresh whilst sending
        try:
            # Reading the image in binary format and sending it as multipart/form-data
            with open(self.path_image, "rb") as img:
                response = requests.post(
                    SERVER_URL,
                    files={"file": (os.path.basename(self.path_image), img, "image/jpeg")},
                    # On envoie aussi est_circulaire comme paramètre de formulaire
                    data={"is_circular": str(self.is_circular.get())}
                )

            response.raise_for_status()   # throws an exception if an HTTP error occurs
            data = response.json()

            # Displays the detected text in the results area
            text = data.get("detected_text", "(no text detected)")

            self._show_text(text)

            # Save the path to the .txt file for downloading
            self.path_txt_server = data.get("txt_file")
            self.download_button.config(state="normal")


        except requests.ConnectionError:
            messagebox.showerror("Error", "Impossible to join the server.\n"
                                           "Check is uvicorn is running.")
        except Exception as e:
            messagebox.showerror("Error", f"An error has occured :\n{e}")
        finally:
            # Resets the button to its original state in all cases
            self.scan_button.config(text="▶  Scan", state="normal")

    def _show_text(self, text):
        """Inserts the text into the display area (read-only)."""
        self.text_zone.config(state="normal")
        self.text_zone.delete("1.0", "end")
        self.text_zone.insert("end", text)
        self.text_zone.config(state="disabled")

    def _download_txt(self):
        """Prompts the user to save the .txt file locally."""
        if not self.path_txt_server or not os.path.exists(self.path_txt_server):
            messagebox.showwarning("Warning", "No file .txt disponible.")
            return

        # Opens a dialogue box to choose where to save
        destination = filedialog.asksaveasfilename(
            title="Save file .txt",
            defaultextension=".txt",
            initialfile="result.txt",
            filetypes=[("Text file", "*.txt")]
        )
        if destination:
            shutil.copy(self.path_txt_server, destination)
            messagebox.showinfo("Success", f"File saved :\n{destination}")


# ── Entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = IHM()
    app.mainloop()
