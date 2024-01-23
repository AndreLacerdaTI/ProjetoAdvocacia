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
                if descricao in linha:
                    #print(linha+' pagina: '+str(pagina_numero+1))
                    #print(linhas[indice+2])
                    dados_encontrados = {'pagina':pagina_numero+1,'valor':linhas[indice+2]}
                    dicionario.append(dados_encontrados)
                    # Extrair valor da mesma linha (usando regex neste exemplo)
                indice = indice+1
                    
    doc.close()
    dados.append(dicionario)
    return dados

def dados_pdf(arquivo_selecionado,palavra_chave):
    if len(palavra_chave)>1:
        multiplos_dados = []
        for palavra in palavra_chave:
            dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra)
            valores = []
            # Retira o a palavra chave da lista
            nome = dados[0]
            dados.pop(0)
            for i in dados:
                for dic in i:
                    #print(dic['valor'])
                    valores.append(dic['valor'])
            # Somando e formatando o total
            valores_float = converter_valores(valores)
            total = somar_valores(valores_float)
            total_formatado = formatar_valor_real(total)
            #print('nome: ',nome)
            #print('total: ',total_formatado)
            #print('informacoes:', dados)
            #multiplos_dados.append([total_formatado,dados])
            dicionario = {  'palavra_chave':nome,
                            'total':total_formatado,
                            'informacoes':dados
                            }
            multiplos_dados.append(dicionario)
        #print('Lista[dicionario]:',dados)
        #return multiplos_dados
        return multiplos_dados
    else:
    # Faz a leitura e retorna os valores em dicionario
        dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra_chave)
        valores = []
        # Retira o a palavra chave da lista
        nome = dados[0]
        print('Nome: ',nome)
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
