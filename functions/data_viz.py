import plotly.graph_objects as go

# Função para decodificar a polyline
def decode_polyline(polyline_str):
    index, lat, lng, coordinates = 0, 0, 0, []

    while index < len(polyline_str):
        shift, result = 0, 0

        while True:
            byte = ord(polyline_str[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if not byte >= 0x20:
                break

        delta_lat = ~(result >> 1) if result & 1 else (result >> 1)
        lat += delta_lat

        shift, result = 0, 0
        while True:
            byte = ord(polyline_str[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if not byte >= 0x20:
                break

        delta_lng = ~(result >> 1) if result & 1 else (result >> 1)
        lng += delta_lng

        coordinates.append((lat / 1e5, lng / 1e5))

    return coordinates

# Função para plotar a rota usando plotly
def plotar_rota(data):
    # Extrair a rota
    route = data['routes'][0]['overview_polyline']['points']
    coordinates = decode_polyline(route)

    lats, lngs = zip(*coordinates)

    # Criar a figura plotly
    fig = go.Figure(go.Scattermapbox(
        mode="markers+lines",
        lon=lngs,
        lat=lats,
        marker={'size': 10},
        line=dict(width=2.5, color='blue')
    ))

    fig.update_layout(
        mapbox={
            'style': "open-street-map",
            'center': {'lon': sum(lngs) / len(lngs), 'lat': sum(lats) / len(lats)},
            'zoom': 8
        },
        showlegend=False
    )

    return fig