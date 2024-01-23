import tabula

from app import *

def extrair_valores_na_linha(pdf_path, termo_pesquisa):
    valores = []
    # Extrair tabelas do PDF
    tabelas = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    for tabela_numero, tabela in enumerate(tabelas):
        for linha in tabela.itertuples():
            # Procurar a palavra chave em cada linha do pdf
            if termo_pesquisa in str(linha[1]):
                # Buscar o valor que é o ultimo item da linha
                try:
                    tamanhoLinha = len(linha)-1
                    valor = linha[tamanhoLinha]
                # Se houver um erro para extrair esse valor ele printará as informações destacadamente no console
                except IndexError as e:
                    print(35*'-')
                    print('tamanho', len(linha))
                    print(e)
                    tamanhoLinha = len(linha)-1
                    print(linha[tamanhoLinha])
                    print(35*'-')

                valores.append(valor)
    return valores

def execucao(palavra_chave,arquivo_selecionado):
    pdf_path = "static/arquivos/"+arquivo_selecionado
    valores = extrair_valores_na_linha(pdf_path, palavra_chave)
    valores_float = converter_valores(valores)
    total = somar_valores(valores_float)
    total_real = formatar_valor_real(total)
    print('Encontrados: ',len(valores))
    print('Total dos itens "%s": R$ %s' % (palavra_chave,total_real))
    return total_real

def extrair_palavras_chave(pdf_path):
    palavras_chave = []
    # Extrair tabelas do PDF
    tabelas = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    for tabela_numero, tabela in enumerate(tabelas):
        for linha in tabela.itertuples():
            dados = linha.split(' ')
        print(dados)
        palavras_chave = dados
    return palavras_chave