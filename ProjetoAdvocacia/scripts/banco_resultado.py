import sqlite3
"""
# Conectar ao banco de dados SQLite (ou criá-lo se não existir)
conn = sqlite3.connect('exemplo.db')
cursor = conn.cursor()

# Criação da tabela Orgao
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orgao (
        id_orgao INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
    )
''')

# Criação da tabela PalavraChave
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PalavraChave (
        id_palavra_chave INTEGER PRIMARY KEY,
        palavra TEXT NOT NULL
    )
''')

# Criação da tabela Total
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Total (
        id_valor INTEGER PRIMARY KEY,
        valor REAL NOT NULL,
        id_orgao INTEGER,
        id_palavra_chave INTEGER,
        FOREIGN KEY (id_orgao) REFERENCES Orgao (id_orgao),
        FOREIGN KEY (id_palavra_chave) REFERENCES PalavraChave (id_palavra_chave)
    )
''')
# Commit e fechar a conexão
conn.commit()
conn.close()

"""
# Conectar ao banco de dados SQLite
conn = sqlite3.connect('exemplo.db')
cursor = conn.cursor()

# Executar uma consulta para obter os dados da tabela Relacionamento
cursor.execute('SELECT * FROM Orgao')
orgao = cursor.fetchall()
cursor.execute('SELECT * FROM PalavraChave')
palavra = cursor.fetchall()
cursor.execute('SELECT * FROM Total')
total = cursor.fetchall()

'''
# Imprimir os resultados
print("Tabela Total:")
for id in total:
    print('id total: ',id[0])
    print('Total: ',id[1])
    id_orgao = id[2]
    print('Orgao: ',orgao[0])
    print('Palavra-chave: ',id[3])
    #print(orgao[id[1]])
'''
def select_total_orgao(orgao,palavra_chave):
    cursor.execute("SELECT id_orgao FROM Orgao WHERE nome = ?", (orgao,))
    id = cursor.fetchall()
    cursor.execute("SELECT * FROM PalavraChave WHERE palavra = ?", (palavra_chave,))
    palavra = cursor.fetchall()
    cursor.execute("SELECT * FROM Total WHERE id_orgao = ? AND id_palavra_chave = ?", (id[0][0],palavra[0][0]))
    total = cursor.fetchall()
    #print(total[0][1])
    return total[0][1]

def inserir_dados(id_palavra_chave, id_orgao, valor):
    select_total_orgao(id_orgao, id_palavra_chave)
    cursor.execute('INSERT INTO Total (id_palavra_chave, id_orgao, valor) VALUES (?, ?, ?)', (id_palavra_chave, id_orgao, valor))

retorno = select_total_orgao('CHEFIA DE GABINETE','Material de Consumo')

# Fechar a conexão
conn.close()
