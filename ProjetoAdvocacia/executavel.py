import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def start_flask_app():
    try:

        # Inicie o script app.py usando subprocess
        subprocess.Popen(["python", "./interface.py"])

        # Exiba uma mensagem indicando que o sistema foi iniciado
        mensagem = f"O sistema foi iniciado.\n\nAcesse a página em:\nhttp://127.0.0.1:5001/"
        messagebox.showinfo("Sistema Iniciado", mensagem)

    except Exception as e:
        # Exiba uma mensagem de erro se houver algum problema
        messagebox.showerror("Erro", f"Erro ao iniciar o sistema: {str(e)}")

# Crie a janela principal
root = tk.Tk()
root.title("Iniciar Flask App")

# Adicione um botão para iniciar o sistema
button_start = tk.Button(root, text="Iniciar Sistema", command=start_flask_app)
button_start.pack(pady=20)

# Execute o loop principal da interface gráfica
root.mainloop()
