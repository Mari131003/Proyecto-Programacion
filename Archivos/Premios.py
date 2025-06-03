import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pickle
import os

class Premios:
    def __init__(self, test_mode=False):
        self.correo = "mariajosesolano14@gmail.com"
        self.token = "OJ9PAAOAL2"
        self.url = "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos"
        self.tipo_cambio = self.obtener_venta() if not test_mode else 505  # Valor de prueba

    def calcular_premio(self, intentos: int) -> float:
        """Calcula el premio en colones"""
        try:
            return (1 / intentos) * 100 * self.tipo_cambio
        except ZeroDivisionError:
            return 0.0

    def obtener_tipo_cambio(self, indicador: str) -> float:
        fecha = datetime.now().strftime("%d/%m/%Y")
        params = {
            "Indicador": indicador,
            "FechaInicio": fecha,
            "FechaFinal": fecha,
            "Nombre": "PremiosApp",
            "SubNiveles": "N",
            "CorreoElectronico": self.correo,
            "Token": self.token
        }
        response = requests.get(self.url, params=params)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        valor = root.find('.//NUM_VALOR').text
        return float(valor)

    def obtener_venta(self) -> float:
        return self.obtener_tipo_cambio("318")

    def obtener_top5(self) -> list:
        """Devuelve los top 5 jugadores con premios calculados"""
        try:
            if not os.path.exists("puntajes_memory.pkl"):
                return []
            
            with open("puntajes_memory.pkl", 'rb') as f:
                puntajes = pickle.load(f)
            
            # Calcular premio para cada jugador
            for jugador in puntajes:
                jugador['premio'] = self.calcular_premio(jugador['intentos'])
            
            # Ordenar por premio (mayor primero)
            puntajes.sort(key=lambda x: x['premio'], reverse=True)
            
            return puntajes[:5]
        except Exception as e:
            print(f"Error obteniendo top 5: {e}")
            return []