import tabula
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

#if __name__ == "__main__":
def execucao(palavra_chave,arquivo_selecionado):
    pdf_path = "static/arquivos/"+arquivo_selecionado
    valores = extrair_valores_na_linha(pdf_path, palavra_chave)
    valores_float = converter_valores(valores)
    total = somar_valores(valores_float)
    total_real = formatar_valor_real(total)
    print('Encontrados: ',len(valores))
    print('Total dos itens "%s": R$ %s' % (palavra_chave,total_real))
    return total_real
