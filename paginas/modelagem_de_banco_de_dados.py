import streamlit as st
def view():
    st.write('''
                A criação do banco de dados relacional zebrinha_azul foi realizada utilizando SQLite. 
             O banco de dados contém cinco tabelas, cada uma com suas chaves primárias e relacionamentos 
             adequados, incluindo relações de um para muitos.
             
             A criação das tabelas foi realizada utilizando comandos SQL 
             **`CREATE TABLE IF NOT EXISTS`**, assegurando que as tabelas só sejam criadas caso ainda não existam, evitando duplicação
               
            ''')
    st.subheader('Estrutura das Tabelas')
    st.image('Imagens/Diagrama.png', use_column_width=True)

    st.write('''
             **Tabela Pessoas:**            
            - `id_pessoa`: Chave primária auto-incrementável (identificador único para cada pessoa).
             
            - `nome`: Texto (armazena o nome da pessoa, não permitindo duplicatas e valores nulos).
             
            **Objetivo**: Armazenar informações sobre os indivíduos, garantindo a unicidade de cada nome.
             ''')
    with st.expander('**Mostrar código:**'):
        st.code(
            '''
            CREATE TABLE IF NOT EXISTS pessoas (
                id_pessoa INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
                )
            ''', language='sql')
    st.write('---')    

    st.write('''
             **Tabela Cidades:**            
            - `id_cidade`: Chave primária auto-incrementável (identificador único para cada cidade).
             
            - `cidade_name`: Texto (armazena o nome da cidade, não permitindo duplicatas).
            
            - `latitude`: Real (representa a latitude geográfica da cidade).
             
            - `longitude`: Real (representa a longitude geográfica da cidade).
             
            **Objetivo**: Registrar as cidades e suas respectivas coordenadas, assegurando a singularidade do nome da cidade.
             ''')
    with st.expander('**Mostrar código:**'):
        st.code(
            '''
            CREATE TABLE IF NOT EXISTS cidades (
                id_cidade INTEGER PRIMARY KEY AUTOINCREMENT,
                cidade_name TEXT UNIQUE,
                latitude REAL,
                longitude REAL
                )
            ''', language='sql')
        
    st.write('---')


    st.write('''
             **Tabela Clima:**            
            - `id_condicao_climatica`: Chave primária auto-incrementável (identificador único para cada condição climática)
             
            - `condicao_climatica`: Texto (descreve a condição climática, não permitindo duplicatas)
             
            **Objetivo**: Armazenar as diferentes condições climáticas, garantindo que cada descrição seja única.
             ''')
    with st.expander('**Mostrar código:**'):
        st.code(
            '''
            CREATE TABLE IF NOT EXISTS clima (
                id_condicao_climatica INTEGER PRIMARY KEY AUTOINCREMENT,
                condicao_climatica TEXT UNIQUE
                )
            ''', language='sql')
        
    st.write('---')


    st.write('''
             **Tabela Viagem:**            
            - `id_viagem`: Chave primária auto-incrementável (identificador único para cada viagem).
             
            - `id_viajante`: Inteiro (chave estrangeira que referencia o id_pessoa na tabela Pessoas).
             
            - `data`: Data (registra a data da viagem).
             
            - `id_origem`: Inteiro (chave estrangeira que referencia o id_cidade na tabela Cidades, representando a cidade de origem).
            - `id_destino`: Inteiro (chave estrangeira que referencia o id_cidade na tabela Cidades, representando a cidade de destino).
            - `distancia`: Real (indica a distância percorrida na viagem).
            - `tempo_viagem`: Texto (descreve o tempo gasto na viagem).
             
             **Relações:**

            - `id_viajante` está vinculada ao `id_pessoa` da tabela **pessoas**, garantindo a identificação do viajante.
            - `id_origem` e `id_destino` estão vinculadas ao `id_cidade` da tabela **cidades**, relacionando as viagens às cidades de origem e destino.
             
            **Objetivo**: Registrar as viagens realizadas por pessoas, incluindo detalhes sobre origem, destino, distância e tempo de viagem.
             ''')
    with st.expander('**Mostrar código:**'):
        st.code(
            '''
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
            ''', language='sql')
        
    st.write('---')


    st.write('''
             **Tabela Histórico do Clima:**            
            - `data`: Data (registra a data da medição).
            - `cidade`: Inteiro (chave estrangeira que referencia o id_cidade na tabela Cidades).
            - `condicao_climatica`: Inteiro (chave estrangeira que referencia o id_condicao_climatica na tabela Clima).
            - `temperatura`: Real (indica a temperatura registrada).
            - `sensacao_termica`: Real (descreve a sensação térmica no momento da medição)
             
             **Relações:**

            - `cidade` está vinculada ao `id_cidade` da tabela **cidades**, identificando a cidade onde a medição foi realizada.
            - `condicao_climatica` está vinculada ao `id_condicao_climatica` da tabela **clima**, classificando a condição climática registrada.
            **Restrição:**
            -  Uma restrição `UNIQUE` é aplicada à combinação de `data` e `cidade`, garantindo que não haja mais de um registro de clima para a mesma cidade em uma data específica.
             
            **Objetivo**: Registrar o histórico climático de diferentes cidades em datas precisas, incluindo temperatura e sensação térmica.
             ''')
    with st.expander('**Mostrar código:**'):
        st.code(
            '''
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
            ''', language='sql')
        
        
        


