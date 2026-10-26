from pynput import mouse
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
import time


class Acciones:
    def __init__(self):
        self.mouse= Controller()
        self.keyboard= Controller()
        self.comandos = {
            "click_izquierdo": self.click_izquierdo,
            "click_derecho": self.click_derecho,
            "doble_click": self.doble_click,
            "scroll_mouse": self.scroll_mouse,
            "control_mouse": self.control_mouse,
            "tecla_a": lambda: self.tecla("a"),
            "tecla_b": lambda: self.tecla("b"),
            "tecla_c": lambda: self.tecla("c"),
            "tecla_d": lambda: self.tecla("d"),
            "tecla_e": lambda: self.tecla("e"),
            "tecla_f": lambda: self.tecla("f"),
            "tecla_g": lambda: self.tecla("g"),
            "tecla_h": lambda: self.tecla("h"),
            "tecla_i": lambda: self.tecla("i"),
            "tecla_j": lambda: self.tecla("j"),
            "tecla_k": lambda: self.tecla("k"),
            "tecla_l": lambda: self.tecla("l"),
            "tecla_m": lambda: self.tecla("m"),
            "tecla_n": lambda: self.tecla("n"),
            "tecla_o": lambda: self.tecla("o"),
            "tecla_p": lambda: self.tecla("p"),
            "tecla_q": lambda: self.tecla("q"),
            "tecla_r": lambda: self.tecla("r"),
            "tecla_s": lambda: self.tecla("s"),
            "tecla_t": lambda: self.tecla("t"),
            "tecla_u": lambda: self.tecla("u"),
            "tecla_v": lambda: self.tecla("v"),
            "tecla_w": lambda: self.tecla("w"),
            "tecla_x": lambda: self.tecla("x"),
            "tecla_y": lambda: self.tecla("y"),
            "tecla_z": lambda: self.tecla("z"),
            "tecla_1": lambda: self.tecla("1"),
            "tecla_2": lambda: self.tecla("2"),
            "tecla_3": lambda: self.tecla("3"),
            "tecla_4": lambda: self.tecla("4"),
            "tecla_5": lambda: self.tecla("5"),
            "tecla_6": lambda: self.tecla("6"),
            "tecla_7": lambda: self.tecla("7"),
            "tecla_8": lambda: self.tecla("8"),
            "tecla_9": lambda: self.tecla("9"),
            "tecla_0": lambda: self.tecla("0"),
            "tecla_enter": lambda: self.tecla("enter"),
            "tecla_space": lambda: self.tecla("space"),
            "tecla_backspace": lambda: self.tecla("backspace"),
            "tecla_tab": lambda: self.tecla("tab"),
            "tecla_capslock": lambda: self.tecla("capslock"),
            "tecla_shift": lambda: self.tecla("shift"),
            "tecla_ctrl": lambda: self.tecla("ctrl"),
            "tecla_alt": lambda: self.tecla("alt"),
            "tecla_win": lambda: self.tecla("win"),
            "tecla_f1": lambda: self.tecla("f1"),
            "tecla_f2": lambda: self.tecla("f2"),
            "tecla_f3": lambda: self.tecla("f3"),
            "tecla_f4": lambda: self.tecla("f4"),
            "tecla_f5": lambda: self.tecla("f5"),
            "tecla_f6": lambda: self.tecla("f6"),
            "tecla_f7": lambda: self.tecla("f7"),
            "tecla_f8": lambda: self.tecla("f8"),
            "tecla_f9": lambda: self.tecla("f9"),
            "tecla_f10": lambda: self.tecla("f10"),
            "tecla_f11": lambda: self.tecla("f11"),
            "tecla_f12": lambda: self.tecla("f12"),
        }
    def click_izquierdo(self):
        self.mouse.click(Button.left, 1)
        time.sleep(0.1)
    def click_derecho(self):
        self.mouse.click(Button.right, 1)
        time.sleep(0.1)
    def doble_click(self):
        self.mouse.click(Button.left, 2)
        time.sleep(0.1)
    def scroll_mouse(self, direction):
        self.mouse.scroll(0, 6*direction)
        time.sleep(0.1)
    def control_mouse(self):
        pass
    def tecla(self, tecla):
        self.keyboard.press(tecla)
        self.keyboard.release(tecla)
        time.sleep(0.1)
    def Alt_Tap(self,Nummber):
        self.keyboard.press(Key.alt)
        for i in range(Nummber):
            self.keyboard.press(Key.tab)
            self.keyboard.release(Key.tab)
            time.sleep(0.1)
        self.keyboard.release(Key.alt)
            


Acc=Acciones()
Acc.Alt_Tap(1)