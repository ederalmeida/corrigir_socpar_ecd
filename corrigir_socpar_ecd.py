import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
import os
import threading
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para procurar o arquivo
def procurar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo")
    entry_caminho.delete(0, tk.END)
    entry_caminho.insert(0, caminho_arquivo)

def start_thread():
    threading.Thread(target=executar_rotina).start()

# Função para a rotina a ser executada
def executar_rotina():
    resultado_texto.insert(tk.END, 'Iniciando o Processo' + '\n')
    resultado_texto.insert(tk.END, '' + '\n')
    janela.update_idletasks()
    caminho_arquivo = entry_caminho.get()
    if not caminho_arquivo:
        messagebox.showwarning("Aviso", "Por favor, selecione um arquivo.")
        return
    # Aqui você pode adicionar a lógica da rotina que você deseja executar
    diretorio_arquivo = os.path.dirname(caminho_arquivo)
    hora_Inicio = str(datetime.now().strftime('%H:%M:%S'))
    hora_Inicio_saida = str(datetime.now().strftime('%H_%M_%S'))
    f = '%H:%M:%S'

    caminho_arquivo_original = caminho_arquivo

    caminho_arquivo_corrigido = os.path.join(diretorio_arquivo, 'ECD_CORRIGIDO_' + hora_Inicio_saida + '.txt')

    ecd_corrigido = open(caminho_arquivo_corrigido, 'w', encoding="utf8")

    socpars = []
    socpars_jacorrigidas = []

    num_reg_corrigidos = 0

    with open(caminho_arquivo_original) as ECD:
        ja_executou_a_primeira_vez_o_i250 = False
        # Para cada linha do arquivo
        for linhaArquivo in ECD:
            # separar os campos pelo delimitador pipe "|"
            registro = linhaArquivo.split('|')

            if registro[1] == '0150':
                socpars.append(registro[2])
                ecd_corrigido.writelines(linhaArquivo)
                resultado_texto.insert(tk.END, 'Registro 0150 encontrato ==> ' + registro[2] + '\n' )
                resultado_texto.see(tk.END)
                janela.update_idletasks()
            
            elif registro[1] == 'I250':
                if ja_executou_a_primeira_vez_o_i250 == False:
                    resultado_texto.insert(tk.END, '' + '\n')
                    ja_executou_a_primeira_vez_o_i250 = True
                if (registro[9] in socpars) or (registro[9] == ''):
                    ecd_corrigido.writelines(linhaArquivo)
                else:
                    nova_linha = '|' + registro[1] + '|' + registro[2] + '|' + registro[3] + '|' + registro[4] + '|' + registro[5] + '|' + registro[6] + '|' + registro[7] + '|' + registro[8] + '||\n'
                    ecd_corrigido.writelines(nova_linha)
                    if registro[9] not in socpars_jacorrigidas:
                        socpars_jacorrigidas.append(registro[9])
                        resultado_texto.insert(tk.END,'Registro I250 corrigido ==> ' + registro[9] + '\n')
                        resultado_texto.see(tk.END)
                        janela.update_idletasks()
                    num_reg_corrigidos += 1
            
            else:
                ecd_corrigido.writelines(linhaArquivo)
                
    ecd_corrigido.close()
    ECD.close()
    resultado_texto.insert(tk.END,'' + '\n')
    resultado_texto.insert(tk.END,str(locale.format_string("%d", num_reg_corrigidos, grouping=True)) + ' registros corrigidos' + '\n')
    resultado_texto.insert(tk.END,'' + '\n')
    resultado_texto.see(tk.END)
    janela.update_idletasks()

    resultado_texto.insert(tk.END,'-----------------------------------------' + '\n')
    hora_Fim = str(datetime.now().strftime('%H:%M:%S'))
    tempoTotal = str(datetime.strptime(hora_Fim, f) - datetime.strptime(hora_Inicio, f))
    resultado_texto.insert(tk.END,'| INICIO DA EXECUCAO        ===>' + hora_Inicio + '|' + '\n')
    resultado_texto.insert(tk.END,'| FIM DA EXECUCAO           ===>' + hora_Fim + '|' + '\n')
    resultado_texto.insert(tk.END,'| TEMPO TOTAL DE EXECUÇÃO   ===> ' + tempoTotal + '|' + '\n')
    resultado_texto.insert(tk.END,'-----------------------------------------' + '\n')
    resultado_texto.insert(tk.END,'' + '\n')
    resultado_texto.insert(tk.END,'Processo finalizado')
    resultado_texto.see(tk.END)
    janela.update_idletasks()

# Criação da janela principal
janela = tk.Tk()
janela.title("Corrigir campo de Sociedade Parceira no ECD")

# Título
titulo = tk.Label(janela, text="Corrigir campo de Sociedade Parceira no ECD", font=("Helvetica", 16))
titulo.pack(pady=10)

# Frame para o campo de entrada e o botão de busca
frame_caminho = tk.Frame(janela)
frame_caminho.pack(pady=10, padx=10)

# Campo de entrada
entry_caminho = tk.Entry(frame_caminho, width=50)
entry_caminho.pack(side=tk.LEFT, padx=5)

# Botão de busca
botao_procurar = tk.Button(frame_caminho, text="Procurar", command=procurar_arquivo)
botao_procurar.pack(side=tk.LEFT)

# Botão para executar a rotina
botao_executar = tk.Button(janela, text="Corrigir", command=start_thread)
botao_executar.pack(pady=20)

# Frame para o widget de texto com rolagem
frame_texto = tk.Frame(janela)
frame_texto.pack(pady=10)

# Criação do widget de saída de texto
resultado_texto = tk.Text(frame_texto, height=20, width=50)
resultado_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Adicionando a barra de rolagem
scrollbar = tk.Scrollbar(frame_texto, command=resultado_texto.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
resultado_texto.config(yscrollcommand=scrollbar.set)

# Iniciar a aplicação
janela.mainloop()
