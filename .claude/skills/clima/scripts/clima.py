#!/usr/bin/env python3
"""Consulta el clima actual de una ciudad usando la API gratuita de Open-Meteo."""
import sys
import json
import urllib.request
import urllib.parse

CIUDAD_POR_DEFECTO = "Quito, Ecuador"

WEATHER_CODES = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Niebla", 48: "Niebla con escarcha",
    51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna intensa",
    56: "Llovizna helada ligera", 57: "Llovizna helada intensa",
    61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia intensa",
    66: "Lluvia helada ligera", 67: "Lluvia helada intensa",
    71: "Nevada ligera", 73: "Nevada moderada", 75: "Nevada intensa", 77: "Granizo",
    80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos violentos",
    85: "Chubascos de nieve ligeros", 86: "Chubascos de nieve intensos",
    95: "Tormenta eléctrica", 96: "Tormenta con granizo ligero", 99: "Tormenta con granizo intenso",
}


def geocodificar(ciudad):
    url = "https://geocoding-api.open-meteo.com/v1/search?" + urllib.parse.urlencode({
        "name": ciudad, "count": 1, "language": "es", "format": "json"
    })
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.load(resp)
    resultados = data.get("results")
    if not resultados:
        raise ValueError(f"No se encontró la ciudad: {ciudad}")
    r = resultados[0]
    return r["latitude"], r["longitude"], r.get("name", ciudad), r.get("country", "")


def obtener_clima(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode({
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "timezone": "auto",
    })
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.load(resp)
    return data["current"]


def main():
    ciudad = " ".join(sys.argv[1:]).strip() or CIUDAD_POR_DEFECTO
    lat, lon, nombre, pais = geocodificar(ciudad)
    actual = obtener_clima(lat, lon)

    codigo = actual.get("weather_code")
    descripcion = WEATHER_CODES.get(codigo, "Desconocido")

    print(f"Clima en {nombre}, {pais}")
    print(f"Condición: {descripcion}")
    print(f"Temperatura: {actual['temperature_2m']}°C (sensación térmica {actual['apparent_temperature']}°C)")
    print(f"Humedad: {actual['relative_humidity_2m']}%")
    print(f"Viento: {actual['wind_speed_10m']} km/h")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
