import tabula

def extrair_valores_na_linha(pdf_path, termo_pesquisa):
    # Extrair tabelas do PDF
    tabelas = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    for tabela_numero, tabela in enumerate(tabelas):
        #print(tabela)
        for linha in tabela.itertuples():
            #linhas = str(linha).split(' ')
            #print(linhas)
            if termo_pesquisa in str(linha).lower():
                print(f"Termo '{termo_pesquisa}' encontrado na tabela {tabela_numero + 1}, linha: {linha.Index + 1}")
                # Extrair todos os valores da mesma linha
                valores = [valor for valor in linha if isinstance(valor, (int, float))]
                print("Valores encontrados:", valores)
                # Faça o que for necessário com os valores encontrados

if __name__ == "__main__":
    pdf_path = "Anexo QDD- Quadro de Detalhamento de Despesas.pdf"
    termo_pesquisa = "Material de Consumo"
    extrair_valores_na_linha(pdf_path, termo_pesquisa)
