import os
import pandas as pd
import numpy as np
import locale

from lerPDF import *
from scripts.banco import *

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
    print('converter_valores_reais',len(valores))
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
        if valor[:3]=='R$ ':
            valor = valor[3:]
        valor_sem_ponto = valor.replace('.', '')
        valor_convertido = valor_sem_ponto.replace(',', '.')
        valores_float.append(valor_convertido)
    
    print('converter_valores',valores_float)
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


def formatar_string_lista(lista_string):
    lista = lista_string.replace('[','')
    lista = lista.replace(']','')
    lista = lista.replace(" '",'')
    lista = lista.replace("'",'')
    lista = lista.split(',')
    return lista

def dicionario_orgao_palavra(dados):
    
    palavras_chave_listadas = []
    orgaos_listados = []
    dados_encontrados = []
    for palavra in dados:
        #palavra = [{'pagina': 1, 'valor': '30.000,00', 'orgao': 'CHEFIA DE GABINETE', 'palavra_chave': 'Material de Consumo'}]
        for dado in palavra:
            if dado['orgao'] not in orgaos_listados and dado['palavra_chave'] not in palavras_chave_listadas:
                #print(dado['orgao']+' E '+dado['palavra_chave']+' E '+dado['valor'])
                orgao_palavra = {'orgao':dado['orgao'],
                                     'palavra_chave':dado['palavra_chave'],
                                     }
                
                dados_encontrados.append(orgao_palavra)
                # Adiciona os às listadas para que não se repitam 
                palavras_chave_listadas.append(dado['palavra_chave'])
                orgaos_listados.append(dado['orgao'])
                # Zera a lista para inciar uma nova busca em outro orgao
            palavras_chave_listadas = []
        orgaos_listados = []
    return dados_encontrados