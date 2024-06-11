import streamlit as st
import requests
from streamlit_option_menu import option_menu
from unidecode import unidecode
import datetime
import re
from functions import extract_functions, transform_functions, data_viz
import folium
from streamlit_folium import st_folium


# Função para verificar se o texto é válido
def texto_valido(texto):
    # Regex para verificar se o texto contém apenas letras e espaços
    return bool(re.match("^[A-Za-zÀ-ÿà-ÿ ]+$", texto))

# Função para converter o texto
def converter_texto(texto):
    texto_sem_acento = unidecode(texto)
    texto_maiusculo = texto_sem_acento.upper()
    return texto_maiusculo


MENU_LIST = ['Sobre',
             'Modelagem de Banco de dados',
             'Extração via API',
             'Transformação de dados',
             'Carregamento no Bando de Dados']


with st.sidebar:
    st.image('Imagens/logo.png', width=100)
    st.sidebar.title('Zebrinha Azul - Case DNC')
    selected = option_menu("",MENU_LIST, default_index=0)




def main():
    if selected == 'Sobre':
        st.write("## **Case Engenheiro de Dados Jr. - DNC**")
        st.write("### **Aurélio Guilherme**")
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
        with st.form(key='formulario_nome'):
            NOME = st.text_input("**Digite seu nome:**", placeholder="Digite aqui seu nome sem números ou caracteres especiais")

            ENDERECO_ORIGEM_INPUT =st.text_input("**Digite o nome da cidade e a sigla do estado onde está:**", 
                                         placeholder="Digite aqui o nome da cidade sem números ou caracteres especiais")
             
            ENDERECO_DESTINO_INPUT =st.text_input("**Digite o nome da cidade a sigla do estado onde quer ir:**", 
                                          placeholder="Digite aqui o nome da cidade sem números ou caracteres especiais")
             
            submit_button = st.form_submit_button(label='Enviar')

        # Verifica se o botão de envio foi pressionado
        if submit_button:
            if NOME:
                if texto_valido(NOME):
                    NOME = converter_texto(NOME)
                    
                else:
                    st.error("Erro: Nome inválido. Por favor, insira um nome que contenha apenas letras e espaços.")
            else:
                st.error("Erro: Por favor, digite um nome.")

            if ENDERECO_ORIGEM_INPUT:
                if texto_valido(ENDERECO_ORIGEM_INPUT):
                    ENDERECO_ORIGEM_INPUT = converter_texto(ENDERECO_ORIGEM_INPUT)
                    
                    
                else:
                    st.error("Erro: Endereço invalido. Por favor, insira um endereço contenha apenas letras e espaços.")
            else:
                st.error("Erro: Por favor, digite o endereço de origem.")

            if ENDERECO_DESTINO_INPUT:
                if texto_valido(ENDERECO_DESTINO_INPUT):
                    ENDERECO_DESTINO_INPUT = converter_texto(ENDERECO_DESTINO_INPUT)
                    
                else:
                    st.error("Erro: Endereço de destino inválido. Por favor, insira um endereço que contenha apenas letras e espaços.")
            else:
                st.error("Erro: Por favor, digite o endereço de destino.")

            # Mensagem de sucesso se tudo estiver válido
            if texto_valido(NOME) and texto_valido(ENDERECO_ORIGEM_INPUT) and texto_valido(ENDERECO_DESTINO_INPUT):
                st.success("Obrigado por fornecer informações válidas!")
                DATA_ATUAL = datetime.datetime.now().strftime("%d/%m/%Y")

            # Extração dados de trânsito
            transito_data_bronze = extract_functions.extracao_dados_de_trafico(ENDERECO_ORIGEM_INPUT, ENDERECO_DESTINO_INPUT)
            DISTANCIA, TEMPO, ENDERECO_ORIGEM, ENDERECO_DESTINO, LATITUDE_ORIGEM, LONGITUDE_ORIGEM, LATITUDE_DESTINO, LONGITUDE_DESTINO = transform_functions.transformacao_dados_transito(transito_data_bronze)
           

            # Extração dados climáticos
            cidade_origem_weather_data_bronze = extract_functions.extracao_dados_climaticos(LATITUDE_ORIGEM, LONGITUDE_ORIGEM)
            cidade_destino_weather_data_bronze = extract_functions.extracao_dados_climaticos(LATITUDE_DESTINO, LONGITUDE_DESTINO)
                        
            # Transformação
            CONDICAO_CLIMATICA_ORIGEM, TEMPERATURA_ORIGEM, SENSACAO_TERMICA_ORIGEM = transform_functions.transformacao_dados_climaticos(cidade_origem_weather_data_bronze)
            CONDICAO_CLIMATICA_DESTINO, TEMPERATURA_DESTINO, SENSACAO_TERMICA_DESTINO = transform_functions.transformacao_dados_climaticos(cidade_destino_weather_data_bronze)

            st.write('## **SUA ROTA**')
            st.write(f'Sua rota iniciasse em {ENDERECO_ORIGEM} com destino à/ao {ENDERECO_DESTINO}')             
            fig = data_viz.plotar_rota(transito_data_bronze)
            st.plotly_chart(fig)

            with st.expander('Temperatura'):
                st.info(f'**Temperatura - Origem:** {TEMPERATURA_ORIGEM} ºC')
                st.info(f'**Temperatura - Destino:** {TEMPERATURA_DESTINO} ºC')

            with st.expander('Condição Climática'):
                st.info(f'**Condição Climática - Origem:** {CONDICAO_CLIMATICA_ORIGEM}')
                st.info(f'**Condição Climática - Destino:** {CONDICAO_CLIMATICA_DESTINO}')
            with st.expander('Sensação Térmica'):
                st.info(f'**Sensação Térmica Origem:** {SENSACAO_TERMICA_ORIGEM} ºC')
                st.info(f'**Sensação Térmica Destino:** {SENSACAO_TERMICA_ORIGEM} ºC')
    
            
            



    

            

    elif selected == 'Modelagem de Banco de dados':
        st.title('Modelagem de Banco de dados')
        st.write('---')

        

    elif selected == 'Extração via API':
        st.title('Extração via API')
        st.write('---')


    elif selected == 'Transformação de dados':
        st.title('Transformação de dados')
        st.write('---')
     

    elif selected == 'Carregamento no Bando de Dados':
        st.title('Carregamento no Bando de Dados')
        st.write('---')




#st.write('https://dncgroupbr.notion.site/Engenheiro-de-Dados-d60059a87c874e479390d273b420f063')

if __name__ == '__main__':
    main()