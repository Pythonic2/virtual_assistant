import sqlite3

def create_database():
    conn = sqlite3.connect('data/access_control.db')
    cursor = conn.cursor()

    # Cria a tabela de permissões
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS permissions (
        cpf TEXT PRIMARY KEY,
        empresa TEXT,
        documentos TEXT  -- Armazena documentos permitidos como uma string separada por vírgulas
    )
    ''')

    # Insere dados fictícios
    cursor.executemany('''
    INSERT OR REPLACE INTO permissions (cpf, empresa, documentos) VALUES (?, ?, ?)
    ''', [
        ("12345678901", "Empresa A", "beneficios,acessos"),
        ("98765432100", "Empresa B", "beneficios,suporte"),
        ("11122233344", "Empresa C", "acessos,treinamentos")
    ])

    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso.")

if __name__ == "__main__":
    create_database()
