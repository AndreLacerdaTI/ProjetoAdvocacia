'''
import fitz  # PyMuPDF
import re

def extrair_valores_na_linha(pdf_path, palavra_chave):
    doc = fitz.open(pdf_path)

    for pagina_numero in range(doc.page_count):
        pagina = doc[pagina_numero]
        texto = pagina.get_text()
        #print(texto)
        if palavra_chave in texto:
            # Encontrar a linha que contém a palavra-chave
            linhas = texto.split(',')
            for linha in linhas:
                if palavra_chave in linha:
                    # Extrair valores da mesma linha (usando regex neste exemplo)
                    valores = re.findall(r'\d+', linha)
                    print(f"Palavra-chave encontrada na página {pagina_numero + 1}, linha: {linha}")
                    print("Valores encontrados:", valores)
                    # Faça o que for necessário com os valores encontrados

    doc.close()
'''

import fitz  # PyMuPDF
import re

from app import *

def buscar_titulo(pdf_path, titulos_procurados):
    # Abrir o arquivo PDF
    pdf_document = fitz.open(pdf_path)
    titulos_procurados = ['SECRETARIA DE MEIO AMBIENTE','FUNDO MUNICIPAL DE SAÚDE']
    # Iterar sobre as páginas do PDF
    for pagina_num in range(pdf_document.page_count):
        pagina = pdf_document[pagina_num]

        # Extrair o texto da página
        texto_pagina = pagina.get_text()

        # Verificar se algum dos títulos procurados está na página
        for titulo_procurado in titulos_procurados:
            if titulo_procurado.lower() in texto_pagina.lower():
                print(f'Título encontrado na página {pagina_num + 1}: {titulo_procurado}')

    # Fechar o arquivo PDF
    pdf_document.close()

def buscar_descricao_e_valor(pdf_path, descricao):
    doc = fitz.open(pdf_path)
    dados = [descricao]
    dicionario = []
    for pagina_numero in range(doc.page_count):
        pagina = doc[pagina_numero]
        texto = pagina.get_text()
        if descricao in texto:
            # Encontrar a linha que contém a descrição
            linhas = texto.split('\n')
            indice = 0
            for linha in linhas:
                if linha=='Valor Orçado':
                    orgao = linhas[indice+1]
                if descricao in linha:
                    #print(descricao)
                    #print(linha+' pagina: '+str(pagina_numero+1))
                    #print(linhas[indice+2])
                    dados_encontrados = {'pagina':pagina_numero+1,'valor':linhas[indice+2], 'orgao':orgao}
                    dicionario.append(dados_encontrados)
                    # Extrair valor da mesma linha (usando regex neste exemplo)
                indice = indice+1
                    
    doc.close()
    dados.append(dicionario)
    return dados

def dados_pdf(arquivo_selecionado, palavra_chave):
    if type(palavra_chave)==list:
        multiplos_dados = []
        for palavra in palavra_chave:
            #print('teste',palavra_chave[0])
            dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra)
            #print(dados)
            #buscar_titulo('static/arquivos/'+arquivo_selecionado,palavra)
            valores = []
            # Retira o a palavra chave da lista
            palav_chave = dados[0]
            dados.pop(0)
            for dado in dados:
                indice_dic = 0
                for dic in dado:
                    #print('Dados', dado[indice_dic])
                    atual = dic['orgao']
                    anterior = dado[indice_dic-1]['orgao']
                    # Se o valor for o ultimo item da lista o proximo recebe o valor atual
                    if len(dado)-1==indice_dic:
                        proximo = dic['orgao']
                    else:
                        proximo = dado[indice_dic+1]['orgao']
                    
                    #  
                    if atual == anterior:
                        valores.append(dic['valor'])
                    # Se o orgao atual é diferente do anterior: ele salva
                    if atual != proximo and indice_dic!=0:
                        valores_float = converter_valores(valores)
                        total = somar_valores(valores_float)
                        total_formatado = formatar_valor_real(total)
                        relatorio = {'orgao':dado[indice_dic-1]['orgao'],
                                    'palavra_chave':palav_chave,
                                    'total':total_formatado
                                    }
                        print('Salvando',relatorio)
                        multiplos_dados.append(relatorio)
                        # Continuar 
                        valores = []
                        #print(dic['orgao'],dic['valor'])
                        valores.append(dic['valor'])
                    else:
                        valores.append(dic['valor'])
                        

                    indice_dic += 1
        print(multiplos_dados)
        return multiplos_dados
    else:
    # Faz a leitura e retorna os valores em dicionario
        dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra_chave)
        valores = []
        # Retira o a palavra chave da lista
        nome = dados[0]
        #print('Nome: ',nome)
        dados.pop(0)
        # Criando a lista de valores
        for i in dados:
            for dic in i:
                #print(dic['valor'])
                valores.append(dic['valor'])
        # Somando e formatando o total
        valores_float = converter_valores(valores)
        total = somar_valores(valores_float)
        total_real = formatar_valor_real(total)
        return total_real, dados
