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

# Verificar se o valor encontrado é um valor em reais R$
def verificar_valor(valor):
    #print('verificar_valor {valor', valor)
    if len(valor)>3:
        # Se o antepenúltimo valor não for uma virgula (exemplo: 1.000[',']00)
        if valor[-3]!=',':
            return False
        else:
            #print('verificar_valor {valor[:2]', valor[:-2])
            return True
    return False

# Se a verificação retornar False, ele irá tentar buscar outro valor na linha
def encontrar_valores_reais(linhas,indice):
    print('Encontramos erro para achar o valor de: ',linhas[indice])
    for posicao in range(indice,indice+6):
        valor = linhas[posicao]
        if len(valor)>3:
            if valor[-3]==',':
                print('Encontramos o valor:', valor)
                return valor
            
def buscar_descricao_e_valor(pdf_path, descricao):
    doc = fitz.open(pdf_path)
    #dados = [descricao]
    dados = []
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
                    retorno = verificar_valor(linhas[indice+2])
                    if retorno == False:
                        valor = encontrar_valores_reais(linhas,indice)
                    elif retorno == True:
                        valor = linhas[indice+2]
                    #print(descricao)
                    #print(linha+' pagina: '+str(pagina_numero+1))
                    #print(linhas[indice+2])
                    dados_encontrados = {'pagina':pagina_numero+1,'valor':valor, 'orgao':orgao, 'palavra_chave':descricao}
                    dicionario.append(dados_encontrados)
                    # Extrair valor da mesma linha (usando regex neste exemplo)
                indice = indice+1
                    
    doc.close()
    dados.append(dicionario)
    return dicionario

def salvar_lista_valores(valores):
    lista_valores = []
    for valor in valores:
        lista_valores.append(valor)
    return lista_valores
def dados_pdf(arquivo_selecionado, palavra_chave):
    if type(palavra_chave)==list:
        multiplos_dados = []
        for palavra in palavra_chave:
            dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra)
            multiplos_dados.append(dados)
        
        #print(multiplos_dados[0])
        return multiplos_dados
    else:
        # Faz a leitura e retorna os valores em dicionario
        dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra_chave)
        lista = [dados]
        return lista