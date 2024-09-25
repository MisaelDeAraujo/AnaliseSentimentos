import os
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from textblob import TextBlob
import matplotlib.pyplot as plt

# Dicionário de palavras-chave e seus respectivos sentimentos
palavras_chave = {
    "excelente": "Muito bom",
    "ótimo": "Bom",
    "bom": "Bom",
    "satisfeito": "Bom",
    "neutro": "Neutro",
    "ruim": "Ruim",
    "péssimo": "Muito ruim",
    "insatisfeito": "Muito ruim",
}

# Função para analisar sentimentos por palavras-chave
def analisar_sentimentos(dataframe):
    resultados = []
    for texto in dataframe['comentarios']:
        resultado = "Neutro"  # Valor padrão
        texto_lower = texto.lower()  # Normaliza o texto para minúsculas
        # Verifica palavras-chave
        for palavra, sentimento in palavras_chave.items():
            if palavra in texto_lower:
                resultado = sentimento
                break  # Para ao encontrar a primeira palavra-chave
        resultados.append(resultado)
    return resultados

# Função para calcular sentimento com TextBlob
def calcular_sentimento_textblob(texto):
    blob = TextBlob(texto)
    return blob.sentiment.polarity  # Retorna um valor entre -1 e 1

# Função para carregar e processar o arquivo
def carregar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo CSV", filetypes=[("CSV Files", "*.csv")])
    if caminho_arquivo:
        try:
            df = pd.read_csv(caminho_arquivo, encoding='ISO-8859-1')
            if 'comentarios' not in df.columns:
                messagebox.showwarning("Aviso", "O arquivo deve conter uma coluna chamada 'comentarios'.")
                return

            # Análise dos sentimentos por palavras-chave
            df['sentimento_chave'] = analisar_sentimentos(df)
            # Análise de sentimentos com TextBlob
            df['sentimento_blob'] = df['comentarios'].apply(calcular_sentimento_textblob)

            # Caminho para salvar o arquivo na área de trabalho
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "resultados_sentimentos.csv")
            df.to_csv(desktop_path, index=False)
            messagebox.showinfo("Sucesso", f"Análise concluída! Resultados salvos em '{desktop_path}'.")

            # Gerar gráfico
            gerar_grafico(df)

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Gerar gráfico
def gerar_grafico(df):
    plt.figure(figsize=(12, 6))

    # Histograma para sentimentos do TextBlob
    plt.subplot(1, 2, 1)
    plt.hist(df['sentimento_blob'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Distribuição de Sentimentos (TextBlob)')
    plt.xlabel('Polaridade')
    plt.ylabel('Frequência')

    # Contagem de sentimentos por palavras-chave
    plt.subplot(1, 2, 2)
    contagem_sentimentos = df['sentimento_chave'].value_counts()
    plt.bar(contagem_sentimentos.index, contagem_sentimentos.values, color='lightgreen', alpha=0.7)
    plt.title('Sentimentos por Palavras-Chave')
    plt.xlabel('Sentimento')
    plt.ylabel('Frequência')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Criar a interface gráfica
def criar_interface():
    root = tk.Tk()
    root.title("Análise de Sentimentos em Lote")

    tk.Label(root, text="Clique para carregar um arquivo CSV:").pack(pady=10)

    botao_carregar = tk.Button(root, text="Carregar Arquivo CSV", command=carregar_arquivo)
    botao_carregar.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
