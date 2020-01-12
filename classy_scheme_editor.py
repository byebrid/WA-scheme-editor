"""classy_scheme_editor.py

Attempting to refactor my scheme editor so it's a little easier to work with by
converting lots of functionality to classes. OOP gone too far?
"""
import tkinter as tk
from options import OPTIONS

class Option():
    _instances = set()

    def __init__(self, name=None, button=None, master=None, grid_args=None):
        """
        Parameters
        ----------
        button: tk.Button
            Tkinter button
        master: tk.Tk object or similar
            The master of this option
        grid_args: dict
            Dictionary of keyword arguments to be passed into `button`.grid()
            so we know where to position the button in `master`.
        """
        self._instances.add(self)

        self.name = name
        self.button = button
        self.master = master
        self.grid_args = grid_args


class BoolOption(Option):
    _instances = set()

    def __init__(self, name=None, button=None, master=None, value=False, images=None):
        self._instances.add(self)
        super().__init__(self, button=button, master=master)
        
        self.name = name
        self.value = tk.BooleanVar(value=value)
        if images is None:
            self.images = {
                False: None, 
                True: None
            }
        else:
            self.images = images

    def get_encoded_value(self):
        if self.value.get() == False:
            return b'\x00'
        else:
            return b'\x01'


class IntOption(Option):
    _instances = set()

    def __init__(self, button=None, master=None, value=0):
        self._instances.add(self)
        super().__init__(self, button=button, master=master)


class SignedIntOption(IntOption):
    _instances = set()

    def __init__(self, value=0, button=None):
        self._instances.add(self)
        super().__init__(self, button=button)

        self.value = value


class Byte():
    """Class for dealing with 8 bit values. Can be signed or unsigned."""
    def __init__(self, value, signed=False):
        """
        Parameters
        ----------
        value: int
            int between 0-255. Not the hexadecimal representation.
        signed: bool
            Whether this byte is signed or not
        """
        self.signed = signed
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        new_value = int(new_value)
        if self.signed:
            if new_value < -127:
                self.__value = -127
            elif new_value > 127:
                self.__value = 127
            else:
                self.__value = new_value
        else:
            if new_value < 0:
                self.__value = 0
            elif new_value > 255:
                self.__value = 255
            else:
                self.__value = new_value

    def get_encoded_value(self):
        if self.signed: 
            hex_str = '{value:#04x}'.format(value=abs(self.value)+128) # Converts to signed value (i.e. between 128-255 in hex)
        else:
            hex_str = '{value:#04x}'.format(value=self.value)
        return bytes(hex_str, 'utf-8')

    def __repr__(self):
        return f'Byte: {self.value}'


class Weapon(Option):
    _instances =set()

    def __init__(self, name='Default_Name', ammo=0, crate_probability=0, 
        delay=0, power=0, image=None, is_super=False):
        """
        Parameters
        ----------
        name: str
            Name of the weapon
        ammo: int
            How much ammo user starts off with
        crate_probability: int
            Probability weapon appears in crate
        delay: int
            Number of turns until weapon can be used
        image: ImageTk.PhotoImage
            Image to display on the button used to edit this weapon's values in 
            GUI. Should be 68x68 pixels.
        """

        self._instances.add(self)
        super().__init__(self)

        self.name = name
        # Next four written in order as they appear in scheme file
        self.ammo = Byte(value=ammo) # 10 or 128-255 means infinite ammo
        self.power = Byte(value=power)
        self.delay = Byte(value=delay) # 128-255 means it's 'blocked'
        self.crate_probability = Byte(value=crate_probability)
        
        self.image = image
        self.is_super = is_super

    def __repr__(self):
        return {self.name}
        

class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_main_menu()

    def create_main_menu(self):
        for option in OPTIONS:
            pass


# root = tk.Tk()
# root.title('Worms Armageddon Scheme Editor')
# gui = GUI(master=root)
# gui.mainloop()