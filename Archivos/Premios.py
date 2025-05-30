import requests
from datetime import datetime
import xml.etree.ElementTree as ET

class Premios:
    def __init__(self,test_mode=False):
        # Código para consulta de tipos de cambio (inactivo por ahora)
        self.correo = "mariajosesolano14@gmail.com"  # Reemplazar con tu correo
        self.token = "OJ9PAAOAL2"  # Reemplazar con tu token
        self.url = (
                   "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/"
            "ObtenerIndicadoresEconomicos"  # URL del servicio web del BCCR. Está en la documentación oficial del BCCR
        ) 
        
        if test_mode:  # Si estamos en modo prueba
            self.test_connection()

    def test_connection(self):
        """Prueba la conexión e imprime resultados en consola"""
        print("\n=== PRUEBA DE CONEXIÓN AL BCCR ===")
        try:
            compra = self.obtener_compra()
            venta = self.obtener_venta()
            print(f"Tipo de cambio de compra: {compra}")
            print(f"Tipo de cambio de venta: {venta}")
            print("=== PRUEBA EXITOSA ===\n")
        except requests.RequestException as e:
            print(f"Error al consultar el servicio del BCCR: {e}")
            print("=== PRUEBA FALLIDA ===\n")

    def obtener_tipo_cambio(self, indicador: str, fecha: datetime = None) -> float:
        """Método para obtener tipo de cambio (no se ejecuta automáticamente)"""
        if fecha is None:
            fecha = datetime.now()

        fecha_str = fecha.strftime("%d/%m/%Y")
        

        params = {
            "Indicador": indicador,
            "FechaInicio": fecha_str,
            "FechaFinal": fecha_str,
            "Nombre": "consulta-api",
            "SubNiveles": "N",
            "CorreoElectronico": self.correo,
            "Token": self.token
        }

        response = requests.get(self.url, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        valor = root.find('.//NUM_VALOR')
        return float(valor.text) if valor is not None else None

    def obtener_compra(self) -> float:
        """Obtiene tipo de cambio de compra (317)"""
        return self.obtener_tipo_cambio("317")

    def obtener_venta(self) -> float:
        """Obtiene tipo de cambio de venta (318)"""
        return self.obtener_tipo_cambio("318")
