from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.config import Config
import requests

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '750')

Config.write()

class MovilApp(MDApp):
    selected_service = StringProperty("")

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "200"
        self.theme_cls.accent_palette = "Blue"
        return Builder.load_file("movil.kv")

    def validar_reserva(self, nro_reserva, apellido):
        url = "http://186.129.182.168:8080/api/v1/validar_reserva"
        payload = {"nro_reserva": nro_reserva, "apellido": apellido}
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.root.get_screen("services").manager.current = "services"
            else:
                self.mostrar_error("Reserva no encontrada")
        except requests.exceptions.RequestException as e:
            self.mostrar_error(f"Error al conectar con el servidor: {e}")

    def mostrar_error(self, mensaje):
        from kivymd.uix.dialog import MDDialog
        dialog = MDDialog(
            title="Error", 
            text=mensaje,
            size_hint=(0.8, 0.4),
            buttons=[],
        )
        dialog.open()

        
    def contratar_servicio(self):
        
        service_ids = {
            "Masajes": 1,
            "Desayuno": 2,
            "Rio": 3
        }

        id_servicio = service_ids.get(self.selected_service, None)
        
        if id_servicio is None:
            self.mostrar_dialogo("Error", "El servicio seleccionado no es válido.")
            return

        url = "http://186.129.182.168:8080/api/v1/contratar_servicio"
        payload = {
            "id_reserva": self.root.ids.nro_reserva.text,
            "id_servicio": id_servicio
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.mostrar_dialogo("Éxito", f"{self.selected_service} contratado con éxito.")
            elif response.status_code == 409:
                self.mostrar_dialogo("Atención", f"El servicio {self.selected_service} ya fue contratado.")
                self.root.get_screen("services").manager.current = "services"
            else:
                self.mostrar_dialogo("Error", "No se pudo contratar el servicio.")
        except requests.exceptions.RequestException as e:
            self.mostrar_dialogo("Error", f"Error al conectar con el servidor: {e}")

    def mostrar_dialogo(self, titulo, mensaje):
        from kivymd.uix.dialog import MDDialog
        dialog = MDDialog(
            title=titulo,
            text=mensaje,
            size_hint=(0.8, 0.4),
            buttons=[],
        )
        dialog.open()

    def update_details(self, service_name):
        self.selected_service = service_name
        details = {
            "Masajes": {"image": "img/masajes.png", "price": "$13.000"},
            "Desayuno": {"image": "img/desayuno.png", "price": "$3.000"},
            "Rio": {"image": "img/rio.png", "price": "$10.000"}
        }
        service_details = details.get(service_name, {"image": "", "price": ""})
        self.root.ids.details_image.source = service_details["image"]
        self.root.ids.details_price.text = service_details["price"]


if __name__ == "__main__":
    MovilApp().run()