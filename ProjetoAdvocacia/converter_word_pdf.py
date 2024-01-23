import pythoncom
from docx2pdf import convert
# Substitua 'seu_arquivo.docx' pelo caminho real do seu arquivo Word
#caminho_arquivo_word = 'static/arquivos/QDDL - PAC 2024 - Geral - Atualizado - Finalizado - Oliveira.docx'
def converter(caminho_arquivo_word):
    pythoncom.CoInitialize()
    try:
        convert(caminho_arquivo_word)
        print("Arquivo convertido com sucesso.")
        
        pythoncom.CoUninitialize()
    except Exception as e:
        print(f"Erro ao converter: {str(e)}")
        pythoncom.CoUninitialize()