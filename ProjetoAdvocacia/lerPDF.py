from app import *
import fitz  # PyMuPDF
import re


def buscar_valores_repetidos(pdf_path):
    # Inicializa uma lista vazia para armazenar todos os valores
    dados = []

    # Inicializa uma lista vazia para armazenar os valores repetidos
    valores_repetidos = []

    # Cria um dicionário para contar a ocorrência de cada elemento na lista
    contagem = {}


    doc = fitz.open('static/arquivos/'+pdf_path)
    for pagina_numero in range(doc.page_count):
        pagina = doc[pagina_numero]
        texto = pagina.get_text()
        linhas = texto.split('\n')
        for palavra in linhas:
            try:
                int(palavra[:2])
            except:
                if (verificar_valor(palavra)==False) and "." not in palavra and ":" not in palavra and "/" not in palavra and palavra!='':
                    #if palavra.isupper():
                    dados.append(palavra)
    # Percorre a lista original
    for elemento in dados:
        #print(elemento)
        # Incrementa a contagem do elemento no dicionário
        contagem[elemento] = contagem.get(elemento, 0) + 1
        # Se o elemento já apareceu mais de uma vez, adiciona à lista de valores repetidos
        if contagem[elemento] == 2:
            valores_repetidos.append(elemento)
    return valores_repetidos

# Encontrar o parametro de busca para o orgão reconhecendo padrões do documento
def palavra_mais_frequente(lista):
    # cria um dicionário para armazenar a frequência de cada palavra
    frequencia = {}
    for palavra in lista:
        # converte a palavra para minúscula
        #palavra = palavra.lower()
        # incrementa a frequência da palavra no dicionário
        frequencia[palavra] = frequencia.get(palavra, 0) + 1
    # encontra a palavra com a maior frequência
    max_frequencia = 0
    palavra_mais_frequente = None
    for palavra, frequencia in frequencia.items():
        # se a frequência for maior que a máxima atual, atualiza a palavra mais frequente
        if frequencia > max_frequencia:
            max_frequencia = frequencia
            palavra_mais_frequente = palavra
    # retorna a palavra mais frequente e sua frequência
    return palavra_mais_frequente

def buscar_titulo(pdf_path, titulos_procurados):
    # Abrir o arquivo PDF
    pdf_document = fitz.open('static/arquivos/'+pdf_path)
    parametros = []
    # Iterar sobre as páginas do PDF
    for pagina_num in range(pdf_document.page_count):
        pagina = pdf_document[pagina_num]

        # Extrair o texto da página
        texto_pagina = pagina.get_text()
        # Verificar se algum dos títulos procurados está na página
        for titulo_procurado in titulos_procurados:
            if titulo_procurado in texto_pagina:
                #print(f'Título encontrado na página {pagina_num + 1}: {titulo_procurado}')
                linha = texto_pagina.split('\n')
                indice = 0
                # Busca o parametro para encontrar todos os orgaos
                for palavra in linha:
                    if titulo_procurado==palavra and titulo_procurado!=linha[indice-1]:
                        #print('parametro: ',linha[indice-1])
                        parametros.append(linha[indice-1])
                    indice += 1
    parametro = palavra_mais_frequente(parametros)
    # Fechar o arquivo PDF
    pdf_document.close()
    return parametro

def buscar_descricao_e_valor(pdf_path, descricao, parametro):
    #print('Parametro para busca', parametro)
    doc = fitz.open(pdf_path)
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
                if linha==parametro:
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

def salvar_lista_valores(valores):
    lista_valores = []
    for valor in valores:
        lista_valores.append(valor)
    return lista_valores

def dados_pdf(arquivo_selecionado, palavra_chave, parametro):
    if type(palavra_chave)==list:
        multiplos_dados = []
        for palavra in palavra_chave:
            dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado, palavra, parametro)
            multiplos_dados.append(dados)
        
        #print(multiplos_dados[0])
        return multiplos_dados
    else:
        # Faz a leitura e retorna os valores em dicionario
        dados = buscar_descricao_e_valor('static/arquivos/'+arquivo_selecionado,palavra_chave,parametro)
        lista = [dados]
        return lista