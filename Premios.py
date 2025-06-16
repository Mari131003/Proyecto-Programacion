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
        self.tipo_cambio = self.obtener_venta()  # Valor de prueba

        if test_mode:
            print(f"[DEBUG] Modo prueba: Tipo de cambio = {self.tipo_cambio}")
        else:
            print(f"[DEBUG] Tipo de cambio real obtenido = {self.tipo_cambio}")

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
        
    def guardar_puntaje(self, nombre: str, intentos: int):
        """Guarda un nuevo puntaje en el archivo pickle solo si es válido."""
        if not nombre or nombre.strip() == "" or intentos <= 0:
            print("Nombre vacío o intentos inválidos. Registro no guardado.")
            return

        try:
            if os.path.exists("puntajes_memory.pkl"):
                with open("puntajes_memory.pkl", 'rb') as f:
                    puntajes = pickle.load(f)
            else:
                puntajes = []

            # Agregar nuevo jugador
            puntajes.append({
                'nombre': nombre,
                'intentos': intentos,
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # Guardar actualizado
            with open("puntajes_memory.pkl", 'wb') as f:
                pickle.dump(puntajes, f)

        except Exception as e:
            print(f"Error guardando puntaje: {e}")

    def eliminar_jugador(self, nombre, intentos=None):
        """
        Elimina un jugador del archivo de puntajes.
    
        Args:
            nombre (str): Nombre del jugador a eliminar.
            intentos (int, optional): Si se da, elimina solo registros específicos.
        """
        try:
            if not os.path.exists("puntajes_memory.pkl"):
                print("No hay datos para eliminar")
                return False

            with open("puntajes_memory.pkl", 'rb') as f:
                puntajes = pickle.load(f)

            # Filtrar los puntajes que NO coincidan con el nombre (y opcionalmente intentos)
            original_count = len(puntajes)
            if intentos is not None:
                puntajes = [j for j in puntajes if j['nombre'] != nombre or j['intentos'] != intentos]
            else:
                puntajes = [j for j in puntajes if j['nombre'] != nombre]

            nuevos_registros = len(puntajes)

            # Guardar cambios
            with open("puntajes_memory.pkl", 'wb') as f:
                pickle.dump(puntajes, f)

            return original_count > nuevos_registros
        except Exception as e:
            print(f"Error eliminando jugador: {e}")
            return False