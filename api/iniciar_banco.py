import os
import sqlite3

def inicializar_banco():
    caminho_base = os.path.dirname(os.path.abspath(__file__))
    pasta_db = os.path.join(caminho_base, 'db')
    os.makedirs(pasta_db, exist_ok=True)
    caminho_banco = os.path.join(pasta_db, 'landing.db')

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS leads (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo       TEXT    NOT NULL,
            email               TEXT    NOT NULL,
            telefone_whatsapp   TEXT    NOT NULL,
            mensagem            TEXT    DEFAULT NULL,
            data_cadastro       TEXT    DEFAULT (datetime('now','localtime')),
            status_atendimento  TEXT    DEFAULT 'novo'
                                        CHECK(status_atendimento IN ('novo','contatado','convertido','perdido'))
        );
        CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
        CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status_atendimento);
    ''')

    conexao.commit()
    conexao.close()
    print("Tabela leads criada/verificada com sucesso no SQLite (Python).")

if __name__ == "__main__":
    inicializar_banco()
