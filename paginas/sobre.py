import streamlit as st
import datetime
from functions import extract_functions, transform_functions, data_viz, load_data_database   
import sqlite3 
import pandas as pd
    

def view(conn):
        st.header("Projeto ETL - Zebrinha Azul")
        st.write()
        st.write('''
                    A **Zebrinha Azul** é uma startup inovadora que se destaca no mercado por sua expertise em 
                    lidar com dados de clima e tráfego. A empresa fornece soluções avançadas para otimizar 
                    operações logísticas e proporcionar relatórios para clientes de diversos setores. Como 
                    um engenheiro de dados, minha missão foi desenvolver um sistema robusto e escalável 
                    para integrar, processar e analisar os dados de clima e tráfego que a Zebrinha Azul coleta.
                ''')
        st.write()

        st.write('---')

        st.subheader('Formulário')
        st.write('''
                    Ao preencher o formulário, você receberá a rota e as informações climáticas atuais de onde está e do seu destino.

                    Essas informações ficarão salvas no banco de dados, permitindo que você extraia informações sobre o seu histórico 
                    de viagens futuramente.
                 ''')
  

        # Inclusão do formulário inicial com os inputs do usuário.
        with st.form(key='formulario_nome'):
            NOME = st.text_input("**Digite seu nome:**", placeholder="Digite aqui seu nome sem números ou caracteres especiais")

            ENDERECO_ORIGEM_INPUT =st.text_input("**Digite o nome da cidade e a sigla do estado onde está:**", 
                                         placeholder="EXEMPLO: São Paulo SP obs:(sem caracteres especiais ou números)")
             
            ENDERECO_DESTINO_INPUT =st.text_input("**Digite o nome da cidade a sigla do estado onde quer ir:**", 
                                          placeholder="EXEMPLO: Rio de Janeiro RJ obs:(sem caracteres especiais ou números)")
             
            submit_button = st.form_submit_button(label='Enviar')

        # Verifica se o botão de envio foi pressionado
        if submit_button:
            if NOME:
                if transform_functions.texto_valido(NOME):
                    NOME = transform_functions.converter_texto(NOME)
                    
                else:
                    st.error("Erro: Nome inválido. Por favor, insira um nome que contenha apenas letras e espaços.")
            else:
                st.error("Erro: Por favor, digite um nome.")

            if ENDERECO_ORIGEM_INPUT:
                if transform_functions.texto_valido(ENDERECO_ORIGEM_INPUT):
                    ENDERECO_ORIGEM_INPUT = transform_functions.converter_texto(ENDERECO_ORIGEM_INPUT)
                    
                    
                else:
                    st.error("Erro: Endereço invalido. Por favor, insira um endereço contenha apenas letras e espaços.")
            else:
                st.error("Erro: Por favor, digite o endereço de origem.")

            if ENDERECO_DESTINO_INPUT:
                if transform_functions.texto_valido(ENDERECO_DESTINO_INPUT):
                    ENDERECO_DESTINO_INPUT = transform_functions.converter_texto(ENDERECO_DESTINO_INPUT)
                    
                else:
                    st.error("Erro: Endereço de destino inválido. Por favor, insira um endereço que contenha apenas letras e espaços.")
            else:
                st.error("Erro: Por favor, digite o endereço de destino.")

            # Mensagem de sucesso se tudo estiver válido
            if transform_functions.texto_valido(NOME) and transform_functions.texto_valido(ENDERECO_ORIGEM_INPUT) and transform_functions.texto_valido(ENDERECO_DESTINO_INPUT):
                st.success("Obrigado por fornecer informações válidas!")

                # Optem data atual para inserir posteriormente no banco de dados.
                DATA_ATUAL = datetime.datetime.now().strftime("%Y-%m-%d")            


            # Extração e transformação dados de trânsito 
            transito_data_bronze = extract_functions.extracao_dados_de_trafico(ENDERECO_ORIGEM_INPUT, ENDERECO_DESTINO_INPUT)
            DISTANCIA, TEMPO, ENDERECO_ORIGEM, ENDERECO_DESTINO, LATITUDE_ORIGEM, LONGITUDE_ORIGEM, LATITUDE_DESTINO, LONGITUDE_DESTINO = transform_functions.transformacao_dados_transito(transito_data_bronze)
           
            # Extração dados climáticos
            cidade_origem_weather_data_bronze = extract_functions.extracao_dados_climaticos(LATITUDE_ORIGEM, LONGITUDE_ORIGEM)
            cidade_destino_weather_data_bronze = extract_functions.extracao_dados_climaticos(LATITUDE_DESTINO, LONGITUDE_DESTINO)
                        
            # Transformação
            CONDICAO_CLIMATICA_ORIGEM, TEMPERATURA_ORIGEM, SENSACAO_TERMICA_ORIGEM = transform_functions.transformacao_dados_climaticos(cidade_origem_weather_data_bronze)
            CONDICAO_CLIMATICA_DESTINO, TEMPERATURA_DESTINO, SENSACAO_TERMICA_DESTINO = transform_functions.transformacao_dados_climaticos(cidade_destino_weather_data_bronze)

            # Plotagem de rota
            st.write('## **SUA ROTA**')
            st.write(f'Sua rota iniciasse em {ENDERECO_ORIGEM} com destino à/ao {ENDERECO_DESTINO}')             
            fig = data_viz.plotar_rota(transito_data_bronze)
            st.plotly_chart(fig)

            # Mostrando informações obtidas nas API's
            with st.expander('Temperatura'):
                st.info(f'**Temperatura - Origem:** {TEMPERATURA_ORIGEM} ºC')
                st.info(f'**Temperatura - Destino:** {TEMPERATURA_DESTINO} ºC')

            with st.expander('Condição Climática'):
                st.info(f'**Condição Climática - Origem:** {CONDICAO_CLIMATICA_ORIGEM}')
                st.info(f'**Condição Climática - Destino:** {CONDICAO_CLIMATICA_DESTINO}')
            with st.expander('Sensação Térmica'):
                st.info(f'**Sensação Térmica Origem:** {SENSACAO_TERMICA_ORIGEM} ºC')
                st.info(f'**Sensação Térmica Destino:** {SENSACAO_TERMICA_DESTINO} ºC')

            
            # CARREGANDO DADOS NO BANCO DE DADOS

            # Tabela pessoas
            load_data_database.insert_pessoas(conn, NOME)       
     
            # Tabela cidades
            load_data_database.insert_city(conn, ENDERECO_ORIGEM, LATITUDE_ORIGEM, LONGITUDE_ORIGEM)
            load_data_database.insert_city(conn, ENDERECO_DESTINO, LATITUDE_DESTINO, LONGITUDE_DESTINO)

            # Tabela Clima
            load_data_database.insert_clima(conn, CONDICAO_CLIMATICA_ORIGEM)
            load_data_database.insert_clima(conn, CONDICAO_CLIMATICA_DESTINO)

            # Tabela viagem
            load_data_database.insert_viagem(conn, NOME, DATA_ATUAL, ENDERECO_ORIGEM, ENDERECO_DESTINO, DISTANCIA, TEMPO)

            # Tabela historico climatico
            load_data_database.insert_historico_clima(conn, DATA_ATUAL,ENDERECO_ORIGEM, CONDICAO_CLIMATICA_ORIGEM, TEMPERATURA_ORIGEM, SENSACAO_TERMICA_ORIGEM)
            load_data_database.insert_historico_clima(conn, DATA_ATUAL,ENDERECO_DESTINO, CONDICAO_CLIMATICA_DESTINO, TEMPERATURA_DESTINO, SENSACAO_TERMICA_DESTINO)

def run_query(query):
    conn = sqlite3.connect('zebrinha_azul.db')
    try:
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao executar a query: {e}")
    finally:
        conn.close()


            