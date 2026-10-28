from evdev import UInput, ecodes as e
import time

class Acciones:
    def __init__(self):
        # Crear dispositivo virtual de teclado
        self.ui = UInput()
        time.sleep(0.3)  # Esperar a que el kernel registre el dispositivo

        # Mapeo de nombres de teclas especiales a keycodes de evdev
        self.EspecialKey = {
            "enter": e.KEY_ENTER,
            "space": e.KEY_SPACE,
            "backspace": e.KEY_BACKSPACE,
            "tab": e.KEY_TAB,
            "capslock": e.KEY_CAPSLOCK,
            "shift": e.KEY_LEFTSHIFT,
            "ctrl": e.KEY_LEFTCTRL,
            "alt": e.KEY_LEFTALT,
            "windows": e.KEY_LEFTMETA,
            "esc": e.KEY_ESC,
            "delete": e.KEY_DELETE,
            "home": e.KEY_HOME,
            "end": e.KEY_END,
            "pageup": e.KEY_PAGEUP,
            "pagedown": e.KEY_PAGEDOWN,
            "up": e.KEY_UP,
            "down": e.KEY_DOWN,
            "left": e.KEY_LEFT,
            "right": e.KEY_RIGHT,
        }

        # Mapeo de caracteres individuales a keycodes
        self._char_map = {}
        for c in "abcdefghijklmnopqrstuvwxyz":
            self._char_map[c] = getattr(e, f"KEY_{c.upper()}")
        for n in "0123456789":
            self._char_map[n] = getattr(e, f"KEY_{n}")

    def _resolver_tecla(self, tecla):
        """Convierte un string de tecla a su keycode de evdev"""
        tecla_lower = tecla.lower() if isinstance(tecla, str) else tecla
        # Primero buscar en teclas especiales
        if tecla_lower in self.EspecialKey:
            return self.EspecialKey[tecla_lower]
        # Luego en caracteres individuales
        if tecla_lower in self._char_map:
            return self._char_map[tecla_lower]
        # Si es un string de un solo carácter, intentar mapear
        if isinstance(tecla, str) and len(tecla) == 1:
            key_name = f"KEY_{tecla.upper()}"
            keycode = getattr(e, key_name, None)
            if keycode is not None:
                return keycode
        print(f"Advertencia: tecla '{tecla}' no reconocida")
        return None

    def ejecutar(self, Accion):
        if Accion["tipo"] == "tecla":
            self.ejecutar_Tecla(Accion["valor"])
        elif Accion["tipo"] == "tecla_combo":
            self.ejecutarCombo(Accion["valor"])
        elif Accion["tipo"] == "click":
            self.ejecutar_click()
        elif Accion["tipo"] == "scroll":
            self.ejecutar_scroll(Accion["valor"])

    def ejecutar_Tecla(self, tecla):
        keycode = self._resolver_tecla(tecla)
        if keycode is None:
            return
        self.ui.write(e.EV_KEY, keycode, 1)  # Key down
        self.ui.syn()
        self.ui.write(e.EV_KEY, keycode, 0)  # Key up
        self.ui.syn()
        print("ejecucion exitosa de tecla", tecla)
        time.sleep(0.1)

    def ejecutarCombo(self, teclas):
        try:
            keycodes = []
            for tecla in teclas:
                kc = self._resolver_tecla(tecla)
                if kc is None:
                    print(f"Error: tecla '{tecla}' no reconocida en combo")
                    return
                keycodes.append(kc)

            # Presionar todas las teclas
            for kc in keycodes:
                self.ui.write(e.EV_KEY, kc, 1)
            self.ui.syn()

            # Soltar todas las teclas (en orden inverso)
            for kc in reversed(keycodes):
                self.ui.write(e.EV_KEY, kc, 0)
            self.ui.syn()

            time.sleep(0.1)
            print("ejecucion exitosa de tecla combo", teclas)
        except Exception as ex:
            print("Error al ejecutar combo", ex)

    def ejecutar_click(self):
        try:
            self.ui.write(e.EV_KEY, e.BTN_LEFT, 1)
            self.ui.syn()
            self.ui.write(e.EV_KEY, e.BTN_LEFT, 0)
            self.ui.syn()
            time.sleep(0.1)
        except Exception as ex:
            print(ex)

    def ejecutar_scroll(self, direccion):
        try:
            self.ui.write(e.EV_REL, e.REL_WHEEL, 6 * direccion)
            self.ui.syn()
            time.sleep(0.1)
        except Exception as ex:
            print(ex)

    def __del__(self):
        """Liberar el dispositivo virtual al destruir el objeto"""
        try:
            self.ui.close()
        except Exception:
            pass