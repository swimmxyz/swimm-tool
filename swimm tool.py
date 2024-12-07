import os
import yaml
import re
import customtkinter as ctk
from tkinter import messagebox

# ASCII Art do dodania na początek pliku
ascii_art = """██████╗ ██╗   ██╗    ███████╗██╗    ██╗██╗███╗   ███╗███╗   ███╗
██╔══██╗╚██╗ ██╔╝    ██╔════╝██║    ██║██║████╗ ████║████╗ ████║
██████╔╝ ╚████╔╝     ███████╗██║ █╗ ██║██║██╔████╔██║██╔████╔██║
██╔══██╗  ╚██╔╝      ╚════██║██║███╗██║██║██║╚██╔╝██║██║╚██╔╝██║
██████╔╝   ██║       ███████║╚███╔███╔╝██║██║ ╚═╝ ██║██║ ╚═╝ ██║
╚═════╝    ╚═╝       ╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝
"""

# === Funkcja do pobrania nazwy pliku ===
def get_output_file_name(prompt):
    dialog = ctk.CTkInputDialog(text=prompt, title="Wpisz nazwę - by Swimm")
    file_name = dialog.get_input()
    if not file_name:
        file_name = "output"  # Domyślna nazwa pliku
    return file_name + ".txt"

# === Funkcja dla opcji Userdata ===
def userdata():
    input_folder = "userdata"
    output_file_path = get_output_file_name("Wpisz nazwę (bez .txt):")

    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(ascii_art + "\n")

            for filename in os.listdir(input_folder):
                filepath = os.path.join(input_folder, filename)

                if os.path.isfile(filepath):
                    with open(filepath, 'r', encoding='utf-8') as file:
                        try:
                            data = yaml.safe_load(file)
                            nick = data.get('last-account-name')
                            ip_address = data.get('ip-address')

                            if nick and ip_address:
                                output_file.write(f"{nick}:{ip_address}\n")
                        except Exception as e:
                            print(f"Nie udało się przetworzyć pliku {filename}: {e}")

        with open(output_file_path, 'r', encoding='utf-8') as output_file:
            line_count = sum(1 for _ in output_file)

        messagebox.showinfo("Userdata - Wynik",
                            f"Zapisano w '{output_file_path}'.\nLiczba linii: {line_count}")

    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się przetworzyć plików: {e}")

# === Funkcja dla opcji Logs ===
def logs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_folder = os.path.join(script_dir, 'logs')
    output_file_path = os.path.join(script_dir, get_output_file_name("Wpisz nazwę (bez .txt):"))

    log_pattern = re.compile(r'\[.*\]:\s(?P<nick>[^\[]+)\[\/(?P<ip>[\d\.]+)')

    def display_line_count():
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r', encoding='utf-8') as file:
                line_count = sum(1 for _ in file)
            return line_count
        return 0

    nick_ip_pairs = {}
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    nick, ip = line.split(':')
                    nick_ip_pairs[nick] = ip

    if os.path.exists(logs_folder) and os.path.isdir(logs_folder):
        for filename in os.listdir(logs_folder):
            if filename.endswith(('.txt', '.log', '.md', '.cfg')):
                file_path = os.path.join(logs_folder, filename)
                with open(file_path, 'r', encoding='utf-8') as log_file:
                    for line in log_file:
                        match = log_pattern.search(line)
                        if match:
                            nick = match.group('nick').strip()
                            ip = match.group('ip').strip()
                            nick_ip_pairs[nick] = ip

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(ascii_art + "\n")

            for nick, ip in nick_ip_pairs.items():
                output_file.write(f"{nick}:{ip}\n")

    line_count = display_line_count()
    messagebox.showinfo("Logs - Wynik",
                        f"Plik: {os.path.basename(output_file_path)}\nLiczba linii: {line_count}")


# === Główne okno aplikacji ===
def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("swimm tool")

    # Ustawienie rozmiaru okna na 500x500
    root.geometry("500x500")

    header_label = ctk.CTkLabel(root, text="swimm tool", font=ctk.CTkFont(size=20, weight="bold"))
    header_label.pack(pady=20)

    userdata_button = ctk.CTkButton(root, text="Userdata", command=userdata, font=ctk.CTkFont(size=14))
    userdata_button.pack(pady=10)

    logs_button = ctk.CTkButton(root, text="Logs", command=logs, font=ctk.CTkFont(size=14))
    logs_button.pack(pady=10)

    root.mainloop()


# Start aplikacji
if __name__ == "__main__":
    main()
