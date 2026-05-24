import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ============================================
# CORES
# ============================================

BG_COLOR = "#1E1E1E"
FRAME_COLOR = "#2A2A2A"
TEXT_COLOR = "#FFFFFF"
BTN_COLOR = "#4CAF50"
BTN_HOVER = "#45A049"
ENTRY_COLOR = "#333333"
LOG_BG = "#151515"

# ============================================
# MAPEAMENTO DE EXTENSÕES
# ============================================

MAPEAMENTO = {
    ".jpg": "Imagens",
    ".jpeg": "Imagens",
    ".png": "Imagens",
    ".gif": "Imagens",
    ".bmp": "Imagens",
    ".webp": "Imagens",
    ".svg": "Imagens",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    ".pdf": "Documentos",
    ".docx": "Documentos",
    ".doc": "Documentos",
    ".txt": "Documentos",

    ".xlsx": "Planilhas",
    ".xls": "Planilhas",
    ".csv": "Planilhas",

    ".zip": "Compactados",
    ".rar": "Compactados",
    ".7z": "Compactados",

    ".mp3": "Musicas",
    ".wav": "Musicas",

    ".py": "Python",
    ".js": "JavaScript",
    ".html": "HTML",
    ".css": "CSS",
    ".sh": "shellscript",

    ".exe": "Executaveis",
    ".msi": "Executaveis",
    ".deb": "Executaveis",
}

PASTA_OUTROS = "Outros"

# ============================================
# LÓGICA
# ============================================

def selecionar_pasta():
    pasta = filedialog.askdirectory()

    if pasta:
        entrada_pasta.delete(0, tk.END)
        entrada_pasta.insert(0, pasta)

def organizar_pasta():

    pasta = entrada_pasta.get()

    if not pasta:
        messagebox.showwarning("Aviso", "Selecione uma pasta.")
        return

    pasta = Path(pasta)

    if not pasta.exists():
        messagebox.showerror("Erro", "A pasta não existe.")
        return

    arquivos = [a for a in pasta.iterdir() if a.is_file()]

    if not arquivos:
        messagebox.showinfo("Info", "Nenhum arquivo encontrado.")
        return

    log_text.delete(1.0, tk.END)

    total = len(arquivos)

    progresso["value"] = 0
    janela.update_idletasks()

    for i, arquivo in enumerate(arquivos):

        extensao = arquivo.suffix.lower()

        nome_pasta = MAPEAMENTO.get(extensao, PASTA_OUTROS)

        pasta_destino = pasta / nome_pasta
        pasta_destino.mkdir(exist_ok=True)

        destino_final = pasta_destino / arquivo.name

        # Evitar sobrescrever
        contador = 1
        while destino_final.exists():
            novo_nome = f"{arquivo.stem}_{contador}{arquivo.suffix}"
            destino_final = pasta_destino / novo_nome
            contador += 1

        shutil.move(str(arquivo), str(destino_final))

        log_text.insert(
            tk.END,
            f"[OK] {arquivo.name} → {nome_pasta}\n"
        )

        log_text.see(tk.END)

        porcentagem = ((i + 1) / total) * 100
        progresso["value"] = porcentagem

        janela.update_idletasks()

    messagebox.showinfo(
        "Concluído",
        f"{total} arquivos organizados com sucesso."
    )

# ============================================
# INTERFACE
# ============================================

janela = tk.Tk()
janela.title("Organizador de Arquivos")
janela.geometry("800x600")
janela.configure(bg=BG_COLOR)
janela.resizable(False, False)

# ============================================
# ESTILO
# ============================================

style = ttk.Style()
style.theme_use("default")

style.configure(
    "TProgressbar",
    thickness=18,
    troughcolor="#333333",
    background="#4CAF50",
    bordercolor="#333333",
    lightcolor="#4CAF50",
    darkcolor="#4CAF50"
)

# ============================================
# TÍTULO
# ============================================

titulo = tk.Label(
    janela,
    text="📂 Organizador Automático",
    font=("Segoe UI", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
titulo.pack(pady=20)

# ============================================
# FRAME SUPERIOR
# ============================================

frame_topo = tk.Frame(
    janela,
    bg=FRAME_COLOR
)
frame_topo.pack(pady=10, padx=20, fill="x")

entrada_pasta = tk.Entry(
    frame_topo,
    width=60,
    font=("Segoe UI", 11),
    bg=ENTRY_COLOR,
    fg=TEXT_COLOR,
    insertbackground="white",
    relief="flat"
)
entrada_pasta.pack(
    side=tk.LEFT,
    padx=10,
    pady=15,
    ipady=8
)

btn_pasta = tk.Button(
    frame_topo,
    text="Selecionar Pasta",
    command=selecionar_pasta,
    bg="#3A3A3A",
    fg="white",
    activebackground="#505050",
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=8,
    cursor="hand2"
)
btn_pasta.pack(side=tk.LEFT, padx=10)

# ============================================
# BOTÃO ORGANIZAR
# ============================================

btn_organizar = tk.Button(
    janela,
    text="ORGANIZAR ARQUIVOS",
    command=organizar_pasta,
    bg=BTN_COLOR,
    fg="white",
    activebackground=BTN_HOVER,
    activeforeground="white",
    relief="flat",
    font=("Segoe UI", 13, "bold"),
    padx=30,
    pady=12,
    cursor="hand2"
)
btn_organizar.pack(pady=20)

# ============================================
# BARRA DE PROGRESSO
# ============================================

progresso = ttk.Progressbar(
    janela,
    orient="horizontal",
    length=700,
    mode="determinate"
)
progresso.pack(pady=10)

# ============================================
# LOG
# ============================================

log_text = tk.Text(
    janela,
    height=18,
    width=90,
    bg=LOG_BG,
    fg="#00FF88",
    insertbackground="white",
    font=("Consolas", 10),
    relief="flat",
    borderwidth=0
)
log_text.pack(padx=20, pady=20)

# ============================================
# RODAPÉ
# ============================================

rodape = tk.Label(
    janela,
    text="Arquivos serão separados automaticamente por extensão.",
    bg=BG_COLOR,
    fg="#AAAAAA",
    font=("Segoe UI", 9)
)
rodape.pack(pady=5)

janela.mainloop()