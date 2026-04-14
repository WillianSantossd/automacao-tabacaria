import sqlite3

def criar_banco():
    # Conecta ao arquivo (se não existir, ele cria na hora)
    conn = sqlite3.connect('estoque_oasis.db')
    cursor = conn.cursor()
    
    # Cria a tabela com as mesmas colunas que usamos na planilha
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            marca TEXT,
            valor TEXT,
            disponibilidade TEXT,
            link TEXT,
            data_coleta TEXT,
            SE TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_no_banco(dados):
    conn = sqlite3.connect('estoque_oasis.db')
    cursor = conn.cursor()
    
    # Inserindo os dados capturados
    for item in dados:
        cursor.execute('''
            INSERT INTO produtos (nome, marca, valor, disponibilidade, link, data_coleta, SE)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (item['PRODUTO'], item['MARCA'], item['VALOR'], item['DISPONIBILIDADE'], item['LINK'], item['DATA'], "0"))
    
    conn.commit()
    conn.close()
    print("[SQL] Dados salvos com sucesso no banco de dados!")


def listar_produtos(filtro=None):
    conn = sqlite3.connect('estoque_oasis.db')
    cursor = conn.cursor()

    if filtro:
        filtro_texto = f"%{filtro}%"
        cursor.execute('''
            SELECT nome, marca, valor, disponibilidade, link, data_coleta
            FROM produtos
            WHERE nome LIKE ? OR marca LIKE ?
            ORDER BY data_coleta DESC, id DESC
        ''', (filtro_texto, filtro_texto))
    else:
        cursor.execute('''
            SELECT nome, marca, valor, disponibilidade, link, data_coleta
            FROM produtos
            ORDER BY data_coleta DESC, id DESC
        ''')

    linhas = cursor.fetchall()
    conn.close()

    return [
        {
            'PRODUTO': linha[0],
            'MARCA': linha[1],
            'VALOR': linha[2],
            'DISPONIBILIDADE': linha[3],
            'LINK': linha[4],
            'DATA': linha[5]
        }
        for linha in linhas
    ]
