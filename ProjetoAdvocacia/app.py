import os
import pandas as pd
import numpy as np
import locale


def listarDiretorio():
    # Diretório onde estão os arquivos
    directory = 'static/arquivos'
    
    # Obtém a lista de arquivos existentes no diretório
    file_list = os.listdir(directory)
    
    print('arquivos',file_list)

    return file_list

def apagar_arquivo(nome_arquivo):
    try:
        os.remove('static/arquivos/'+nome_arquivo)
        return 'Arquivo '+nome_arquivo+' apagado com sucesso!'
    except:
        return 'Erro'

# Converter os valores formatados em Real(R$ 1.000,00) para Float(1000.00)
def converter_valores_reais(valores):
    valores_float = []
    #print(valores)
    print(len(valores))
    posicao = 0
    for valor in valores:
        if valor=='valor':
            print('Achou')
            del valores[posicao]
        posicao = posicao+1
        valor_sem_cifrao = valor.replace('r$ ', '')
        valor_sem_ponto = valor_sem_cifrao.replace('.', '')
        valor_convertido = valor_sem_ponto.replace(',', '.')
        valores_float.append(valor_convertido)
    #print(valores_float)
    print(len(valores_float))
    return valores_float

# Converter os valores formatados em Real(R$ 1.000,00) para Float(1000.00)
def converter_valores(valores):
    valores_float = []
    for valor in valores:
        valor_sem_ponto = valor.replace('.', '')
        valor_convertido = valor_sem_ponto.replace(',', '.')
        valores_float.append(valor_convertido)
    return valores_float

# Soma de todos os valores encontrados
def somar_valores(valores):
    total = 0.0
    for valor in valores:
        total = total + float(valor)
    return total

# Converter o total de Float para Real(R$) para exibir para o usuario
def formatar_valor_real(valor):
    # Configurar a formatação para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # Formatar o valor como Real R$
    valor_formatado = locale.currency(valor, grouping=True, symbol='R$')

    return valor_formatado
