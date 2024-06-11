def transformacao_dados_climaticos(data):
    # Extração da decrição da condição climatica
    CONDICAO_CLIMATICA = data['weather'][0]['description']

    # Extração de dados de temperatura e sensação termica - conversão para graus celsius e arredondamento para duas casas
    '''
    data['main']['temp'] -> temperatura em Kelvin
    Subtri-se por -273,15 para obter dados em Gráus Celsius
    '''
    TEMPERATURA = round((data['main']['temp']) -273.15, 2)
    SENSACAO_TERMICA = round((data['main']['feels_like']) -273.15, 2)
    
    return CONDICAO_CLIMATICA, TEMPERATURA, SENSACAO_TERMICA


def transformacao_dados_transito(data):
    # Distancia metros
    DISTANCIA = data['routes'][0]['legs'][0]['distance']['value']

    # tempo em minutos
    TEMPO = data['routes'][0]['legs'][0]['duration']['value']

    ENDERECO_ORIGEM = data['routes'][0]['legs'][0]['start_address']

    ENDERECO_DESTINO = data['routes'][0]['legs'][0]['end_address'] 
    LATITUDE_ORIGEM, LONGITUDE_ORIGEM = data['routes'][0]['legs'][0]['start_location'].values()  
    LATITUDE_DESTINO, LONGITUDE_DESTINO = data['routes'][0]['legs'][0]['end_location'].values()  

    return DISTANCIA, TEMPO, ENDERECO_ORIGEM, ENDERECO_DESTINO, LATITUDE_ORIGEM, LONGITUDE_ORIGEM, LATITUDE_DESTINO, LONGITUDE_DESTINO