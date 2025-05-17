import requests
import tkinter as tk
from tkinter import messagebox

API_KEY = "ecd5f1b1e196dd440435fa7e"
BASE_URL = f"https://v6.exchangerate-api.com/v6/ecd5f1b1e196dd440435fa7e/latest/"

MOEDAS_DISPONIVEIS = [
    "USD", "BRL", "EUR", "GBP", "JPY", "ARS", "CAD", "AUD", "CNY", "CHF"
]

historico = []

def converter():
    origem = origem_var.get()
    destino = destino_var.get()

    try:
        valor = float(entry_valor.get())
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido")
        return

    url = BASE_URL + origem
    response = requests.get(url)

    if response.status_code != 200:
        messagebox.showerror("Erro", "Erro ao acessar a API")
        return

    data = response.json()

    if destino not in data["conversion_rates"]:
        messagebox.showerror("Erro", "Moeda de destino inválida")
        return

    taxa = data["conversion_rates"][destino]
    convertido = valor * taxa
    resultado = f"{valor:.2f} {origem} = {convertido:.2f} {destino}"
    
    mostrar_resultado_popup(resultado)
    adicionar_ao_historico(resultado)

def mostrar_resultado_popup(mensagem):
    popup = tk.Toplevel(janela)
    popup.title("Resultado da Conversão")
    popup.geometry("300x100")
    popup.resizable(False, False)

    tk.Label(popup, text=mensagem, font=("Arial", 12, "bold")).pack(pady=20)
    tk.Button(popup, text="OK", command=popup.destroy).pack()

def adicionar_ao_historico(conversao):
    historico.append(conversao)
    atualizar_historico()

def atualizar_historico():
    historico_text.delete(1.0, tk.END)
    for item in historico[-10:][::-1]:  # mostra os últimos 10, do mais recente pro mais antigo
        historico_text.insert(tk.END, item + "\n")

# Interface principal
janela = tk.Tk()
janela.title("Conversor de Moedas")
janela.geometry("400x400")
janela.resizable(False, False)

tk.Label(janela, text="Moeda de origem:").pack()
origem_var = tk.StringVar(janela)
origem_var.set(MOEDAS_DISPONIVEIS[0])
tk.OptionMenu(janela, origem_var, *MOEDAS_DISPONIVEIS).pack()

tk.Label(janela, text="Moeda de destino:").pack()
destino_var = tk.StringVar(janela)
destino_var.set(MOEDAS_DISPONIVEIS[1])
tk.OptionMenu(janela, destino_var, *MOEDAS_DISPONIVEIS).pack()

tk.Label(janela, text="Valor a converter:").pack()
entry_valor = tk.Entry(janela)
entry_valor.pack()

tk.Button(janela, text="Converter", command=converter).pack(pady=10)

tk.Label(janela, text="Histórico de conversões:").pack(pady=5)
historico_text = tk.Text(janela, height=8, width=45)
historico_text.pack()

janela.mainloop()
