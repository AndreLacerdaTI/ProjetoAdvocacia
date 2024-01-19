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

def buscar_descricao_e_valor(pdf_path, descricao):
    doc = fitz.open(pdf_path)

    for pagina_numero in range(doc.page_count):
        pagina = doc[pagina_numero]
        texto = pagina.get_text()

        if descricao in texto:
            # Encontrar a linha que contém a descrição
            linhas = texto.split('\n')
            for linha in linhas:
                if descricao in linha:
                    # Extrair valor da mesma linha (usando regex neste exemplo)
                    valor = re.search(r'\d+', linha)
                    if valor:
                        valor_encontrado = valor.group()
                        print(f"Descrição '{descricao}' encontrada na página {pagina_numero + 1}, linha: {linha}")
                        print(f"Valor encontrado: {valor_encontrado}")
                        # Faça o que for necessário com o valor encontrado

    doc.close()

if __name__ == "__main__":
    pdf_path = "Anexo QDD- Quadro de Detalhamento de Despesas.pdf"
    palavra_chave = "Material de Consumo"
    buscar_descricao_e_valor(pdf_path, palavra_chave)