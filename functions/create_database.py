import sqlite3


def main():
    # Criação banco de dados zebrinha_azul
    conn = sqlite3.connect('zebrinha_azul.db')
    cursor = conn.cursor()

    # CRIAÇÃO DE TABELAS

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS pessoas (
                id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS cidades (
                id_cidade INTEGER PRIMARY KEY AUTOINCREMENT,
                cidade_name TEXT UNIQUE,
                latitude REAL,
                longitude REAL
            )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS clima (
                id_condicao_climatica INTEGER PRIMARY KEY AUTOINCREMENT,
                condicao_climatica TEXT UNIQUE
            )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS viagem (
                id_viagem INTEGER PRIMARY KEY AUTOINCREMENT,
                id_viajante INTEGER,
                data DATE,
                id_origem INTEGER,
                id_destino INTEGER,
                distancia REAL,
                tempo_viagem TEXT,
                FOREIGN KEY (id_viajante) REFERENCES pessoas (id_pessoa),
                FOREIGN KEY (id_origem) REFERENCES cidades (id_cidade),
                FOREIGN KEY (id_destino) REFERENCES cidades (id_cidade)
            )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_clima (
            data DATE,
            cidade INTEGER,
            condicao_climatica INTEGER,
            temperatura REAL,
            sensacao_termica REAL,
            FOREIGN KEY (cidade) REFERENCES cidades (id_cidade),
            FOREIGN KEY (condicao_climatica) REFERENCES clima (id_condicao_climatica),
            UNIQUE (data, cidade)
        )
    ''')


    conn.commit()

    conn.close()

if __name__ == '__main__':
    main()
