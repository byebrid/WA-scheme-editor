"""
scheme_editor.py

This script handles the GUI for the Worms Armageddon Scheme Editor, as well
as the logic for saving and loading .wsc files from/into a more user-friendly
format.

The scheme format was determined from https://worms2d.info/Game_scheme_file.

Note on unsigned bytes:
I've zombified the logic pertaining to signed bytes as the table retrieved from
the website above, which describes the type of each byte seemed to a bit off
with what it was calling signed bytes. Treating them as unsigned bytes seems
to have the desired results.
"""
import os
import pathlib
import sys
import tkinter as tk
import tkinter.filedialog as filedialog
from collections import OrderedDict
from functools import partial
from PIL import Image, ImageTk
from math import floor

from options import ALL_OPTIONS, MAIN_MENU_OPTIONS, SPECIAL_MENU_OPTIONS, HIDDEN_OPTIONS
from weapons import WEAPONS, SUPER_WEAPONS

if getattr(sys, 'frozen', False):
    # If the application is run by pyinstaller bundle, we can get the parent 
    # directory of this file with this below
    ROOT_DIR = pathlib.Path(sys.executable).parents[1]
else:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ALL_WEAPONS = OrderedDict({**WEAPONS, **SUPER_WEAPONS})

GRAPHICS_DIR = os.path.join(ROOT_DIR, 'graphics')
SCHEME_DIR = os.path.join(ROOT_DIR, 'schemes')
# SCHEME_DIR = os.path.join(WORMS_DIR, 'User', 'Schemes')

def load_image(imgpath):
    """Loads image in tkinter-friendly format so we can add to buttons, etc.
    
    Parameters
    ----------
    imgpath: iterable of strings
        Strings describing the path of the image

    Example
    -------
    >>> root = tk.Tk()
    >>> image = load_image(('Weapons', 'IconBazooka.png'))
    >>> button = tk.Button(master=root, image=image)
    >>> button.image = image # Avoid garbage collect
    >>> button.pack()
    """
    image = Image.open(os.path.join(GRAPHICS_DIR, *imgpath))
    return ImageTk.PhotoImage(image)


class IntVar(tk.IntVar):
    """Class for dealing with 8-bit values. Can be signed or unsigned.
    Inherits from tkinter.IntVar.
    
    Gets used in IntOption.

    Parameters
    ----------
    value: int
        If `signed` == False, this will be constrained to [0,    255]
        If `signed` == True, this will be constrained to  [-128, 127]
    signed: bool; defaults to False
        Whether this byte is signed or not

    Example
    -------
    >>> root = tk.Tk()
    >>> a = IntVar(value=10, signed=True)
    >>> a.set(-1000)
    >>> a.get()
    -128
    """
    def __init__(self, *, value, signed=False):
        super().__init__()
        self.signed = signed
        self.set(value)

    # Overriding default set value so we can restrict it
    def set(self, value):
        """Restricts int to within range [0, 255] if unsigned, and [-128, 127]
        if signed.
        """
        value = int(value)
        if self.signed:
            if value < -128:
                value = -128
            elif value > 127:
                value = 127
        else:
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
        return self._tk.globalsetvar(self._name, value)

    @property
    def encoded_value(self):
        if self.signed: 
            # magnitude = abs(self.get())
            # hex_str = '{value:02x}'.format(value=magnitude+128) # Converts to signed value (i.e. between 128-255 in hex)
            hex_str = '{value:02x}'.format(value=self.get())
        else:
            hex_str = '{value:02x}'.format(value=self.get())
        return bytes.fromhex(hex_str)

    def decode(self, raw_byte):
        if self.signed:
            # return int.from_bytes(raw_byte, byteorder='little', signed=True)
            return int.from_bytes(raw_byte, byteorder='little')
        else:
            return int.from_bytes(raw_byte, byteorder='little')

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value.get()}, signed={self.signed})'


class Button(tk.Button):
    """Subclass of tkinter.Button which handles all the image/command-setting.
    
    Parameters
    ----------
    master: tkinter master
    option: Option object
    gui: GUI object
        The main GUI of the program (the frame for the main menu)
    """
    def __init__(self, master, option, gui):
        super().__init__(master=master)
        self.option = option # To retrieve new image in self.update_image()
        self.gui = gui

        self['command'] = option.button_command
        self.update_image()
        self.grid(**option.grid_args)
        
        self.bind("<Enter>", partial(self.update_help_text, option, False))
        self.bind("<Leave>", partial(self.update_help_text, option, True))

    def update_help_text(self, option, default=False, event=None):
        """Callback for when button is hovered onto or off of."""
        if default == False:
            self.gui.help_text.set(f"{option.name}: {option.value.get()}")
        else:
            self.gui.help_text.set(self.gui.default_help_text)

    def update_image(self):
        self['image'] = self.option.image
        self.image = self.option.image # Avoids garbage collect (why tkinter, why?)

    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master}, option={self.option}, gui={self.gui})'


class Option():
    """The base class for all options we can adjust. No option ends up using
    this directly, only inheriting from it.
    
    Parameters
    ----------
    master: tkinter master
        The master of this option
    name: str
        The human-friendly name of this option. I.e. 'Dud Mines'. 
        WARNING: This name must be a key in `ALL_OPTIONS`.
    """
    def __init__(self, master, name):        
        self.master = master
        self.name = name

    @property
    def dict(self):
        for name, value in ALL_OPTIONS.items():
            if name == self.name:
                return value
        raise KeyError(f"Could not find {self.name} 'in options.py'!")

    @property
    def image(self):
        try:
            return self.__image
        except AttributeError:
            raise AttributeError(
                f"Tried to retrieve {self.__class__.__name__}.image but image wasn't found!"
            )
        except Exception:
            raise
    
    @image.setter
    def image(self, imgpath):
        self.__image = load_image(imgpath)

    @property
    def images(self):
        """Used in BoolOption and ChoiceOption"""
        return self.__images

    @images.setter
    def images(self, value_to_img_dict):
        """Converts the imgpaths into usable tkinter images so we don't have
        to call load_image over and over again."""
        self.__images = {}
        for value, imgpath in value_to_img_dict.items():
            self.__images[value] = load_image(imgpath)

    @property
    def grid_args(self):
        return self.dict['Grid Args']

    def button_command(self):
        """Used in ChoiceOption and BoolOption.
        Changes button's image and the Option's value.
        """
        self.cycle_value()
        self.button.update_image()
        self.button.update_help_text(option=self)
        self.master.last_change.set(f'{self.name} set to {self.value.get()}')

    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master}, name={self.name})'


class BoolOption(Option):
    """An option that can only be True or False
    
    Parameters
    ----------
    master: tkinter master
    name: str
        The human-friendly name of this option. I.e. 'Dud Mines'. 
        WARNING: This name must be a key in `ALL_OPTIONS`.
    """
    def __init__(self, *, master, name):
        super().__init__(master=master, name=name)
        
        self.value = tk.BooleanVar(value=self.dict['Default'])
        self.images = self.dict['Images']

    def cycle_value(self):
        self.value.set(not self.value.get()) # False -> True; True -> False

    @property
    def encoded_value(self):
        if self.value.get() == False:
            return b'\x00'
        else:
            return b'\x01'

    @property
    def image(self):
        return self.images[self.value.get()]

    def decode(self, raw_bytes):
        if raw_bytes == b'\x00':
            return False
        elif raw_bytes == b'\x01':
            return True
        else:
            raise ValueError(f'{raw_bytes} could not be interpreted as bool!')


class ChoiceOption(Option):
    """Option that cycles through a small list of possible values, stored as
    strings so I actually remember what they mean. An example would be the
    Sudden Death Event option, which can be either 'Round Ends' (b'\x00'), 
    'Nuclear Strike' (b'\x01'), etc.

    Parameters
    ----------
    master: tkinter master
    name: str
        The human-friendly name of this option. I.e. 'Dud Mines'. 
        WARNING: This name must be a key in `ALL_OPTIONS`.
    """
    def __init__(self, *, master, name):
        super().__init__(master=master, name=name)

        self.value = tk.Variable(value=self.dict['Default'])
        self.conversions = self.dict['Conversions']
        self.images = self.dict['Images']

    @property
    def encoded_value(self):
        value = self.value.get()
        return self.conversions[value]

    @property
    def possible_values(self):
        return list(self.conversions.keys())

    @property
    def index(self):
        """Gets index of self within the list of possible values self can take"""
        return self.possible_values.index(self.value.get())

    @property
    def image(self): # Override Option's .image
        # print(f"value = {self.value.get()}; images = {self.images}")
        return self.images[self.value.get()]

    def cycle_value(self):
        # Getting next index
        # Use modulo to wrap around if required (i.e. at end of list)
        new_index = (self.index + 1) % len(self.possible_values)
        new_value = self.possible_values[new_index]
        self.value.set(new_value)
        # self.button.update_image()

    def decode(self, raw_byte):
        """Can't be class method because StrVars vary too much in `conversion`, etc."""
        reverse_conversions = {v: k for k, v in self.conversions.items()}
        return reverse_conversions[raw_byte]


class IntOption(Option):
    """Option that takes the value of an integer. Can be signed or unsigned.
    Maximum length of 8 bits (1 byte).

    Parameters
    ----------
    master: tkinter master
    name: str
        The human-friendly name of this option. I.e. 'Dud Mines'. 
        WARNING: This name must be a key in `ALL_OPTIONS`.
    signed: bool; Default=False
        Whether byte is signed or unsigned
    """
    def __init__(self, *, master, name, signed=False):
        super().__init__(master=master, name=name)
        
        self.value = IntVar(value=self.dict['Default'], signed=signed)
        self.image = self.dict['Image']
        self.popup_text = tk.StringVar()
        self.popup_text.set(self.dict.get('Popup Text', ''))

    @property
    def encoded_value(self):
        return self.value.encoded_value

    def button_command(self, *args): # Override default button_command set in Option cls
        def destroy(popup, *args):
            popup.destroy()
            delattr(self.master, 'popup')
            self.value.set(self.value.get()) # To ensure int is restricted to 0-255  or -127-127
            self.master.last_change.set(f'{self.name} set to {self.value.get()}')

        try:
            destroy(self.master.popup)
        except (tk.TclError, AttributeError) as e:
            pass
        finally:
            popup = tk.Toplevel(master=self.master)
            self.master.popup = popup # Assign to master so only one popup at a time

            popup.title(self.name)
            popup.name = self.name

            # Brief little help text to display above entry
            tk.Label(master=popup, textvariable=self.popup_text).grid(row=0)

            # Entry to change value and setting focus on the entry box
            popup.entry = tk.Entry(master=popup, textvariable=self.value)
            popup.entry.grid(row=1)
            popup.entry.focus_set()
            popup.entry.select_range(0, tk.END)
            popup.entry.icursor(tk.END)

            # 3 ways of leaving popup, including button to confirm
            tk.Button(master=popup, text="Confirm", fg='green', command=partial(destroy, popup)).grid(row=2)
            popup.bind("<Return>", partial(destroy, popup))
            popup.bind("<Escape>", partial(destroy, popup))

    def decode(self, raw_byte):
        return self.value.decode(raw_byte=raw_byte)

    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master}, name={self.name}, signed={self.value.signed})'


class NoneOption(Option):
    """Class for dealing with options we shouldn't change, like the magic bytes
    at start of file.
    
    Parameters
    ----------
    master: tkinter master
    name: str
        The human-friendly name of this option. I.e. 'Dud Mines'. 
        WARNING: This name must be a key in `ALL_OPTIONS`.
    """
    def __init__(self, *, master, name):
        super().__init__(master=master, name=name)
        
        self.value = tk.Variable(value=self.dict['Default']) # Should be in bytes already

    @property
    def encoded_value(self):
        return self.value.get()

    def decode(self, value):
        """Doesn't actually need to decode since this value never changes"""
        return self.value.get()


class Weapon(Option):   
    """
    Parameters
    ----------
    master: tkinter master
    name: str
        The human-friendly name of this weapon. I.e. 'Bazooka'. 
        WARNING: This name must be a key in `ALL_WEAPONS`.
    """ 
    def __init__(self, master, name):
        super().__init__(master=master, name=name)
        self.image = self.dict['Image']
    
        # Written in order as they appear in scheme file
        self.ammo = IntVar(value=self.dict['Ammo'])
        self.power = IntVar(value=self.dict['Power'])
        self.delay = IntVar(value=self.dict['Delay'])
        self.crate_probability = IntVar(value=self.dict['Crate Probability'])

    # Overrided Option class' self.dict
    @property
    def dict(self):
        for name, value in ALL_WEAPONS.items():
            if name == self.name:
                return value
        raise KeyError(f"Did not find {self.name} in 'weapons.py'!")

    @property
    def is_super(self):
        return self.name in SUPER_WEAPONS

    @property
    def value(self):
        value_text = (
            f'\nAmmo: {self.ammo.get()}, Power: {self.power.get()}, Delay: '
            f'{self.delay.get()}, Crate probability: {self.crate_probability.get()}'
        )
        return tk.StringVar(value=value_text)

    @property
    def grid_args(self):
        # Getting index of weapon in weapons lists
        names = [w for w in ALL_WEAPONS.keys()]
        # print(f'names=\n{names}')
        index = names.index(self.name)

        return {'row': floor(index / 8), 'column': index % 8}

    @property
    def encoded_value(self):
        encoded_values = b''
        for thing in (self.ammo, self.power, self.delay, self.crate_probability):
            encoded_values += thing.encoded_value

        return encoded_values

    def button_command(self):
        def destroy(weapon_popup, *args):
            weapon_popup.destroy()
            delattr(self.master, 'weapon_popup')
            # Ensuring values are between 0-255
            self.ammo.set(self.ammo.get())
            self.power.set(self.power.get())
            self.delay.set(self.delay.get())
            self.crate_probability.set(self.crate_probability.get())

            self.master.last_change.set(f'{self.name} updated!')

        try:
            destroy(self.master.weapon_popup)
        except (tk.TclError, AttributeError) as e:
            pass
        finally:
            weapon_popup = tk.Toplevel(master=self.master)
            self.master.weapon_popup = weapon_popup # Assign to master so only one weapon_popup at a time

            weapon_popup.title(self.name)
            weapon_popup.name = self.name

            # Brief little help text to display above entry
            text = (
                "If ammo is set to 10 or 128-255, you'll get unlimited ammo.\n"
                "If delay is set to 128-255, weapon will never appear in crates."
            )
            tk.Label(master=weapon_popup, text=text).grid(row=0, columnspan=2)

            # Entries to change values and associated labels
            # Generates weapon_popup.delay_entry, weapon_popup.crate_probability_entry, etc.
            for i, (label, attribute) in enumerate(zip(
                ('Ammo', 'Delay', 'Power', 'Crate Probability'),
                ('ammo', 'delay', 'power', 'crate_probability'),
            )):
                row = i + 1
                tk.Label(master=weapon_popup, text=label).grid(row=row, column=0)
                entry = tk.Entry(master=weapon_popup, textvariable=getattr(self, attribute)) 
                setattr(weapon_popup, attribute + '_entry', entry)
                getattr(weapon_popup, attribute + '_entry').grid(row=row, column=1)

            # Setting focus to first entry
            weapon_popup.ammo_entry.focus_set()
            weapon_popup.ammo_entry.select_range(0, tk.END)
            weapon_popup.ammo_entry.icursor(tk.END)

            # 3 ways of leaving weapon_popup, including button to confirm
            tk.Button(master=weapon_popup, text="Confirm", fg='green', command=partial(destroy, weapon_popup)).grid(row=5, columnspan=2)
            weapon_popup.bind("<Return>", partial(destroy, weapon_popup))
            weapon_popup.bind("<Escape>", partial(destroy, weapon_popup))
        

class GUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)
        self.master = master
        self.default_help_text = "Welcome to Lex's Worms Armageddon Scheme Editor!"

        self.pack()

        self.init_all_options()

        self.create_widgets()

    @property
    def all_weapons(self):
        if self.main_menu_options['Super Weapons'].value.get() == True:
            return OrderedDict({**self.weapons, **self.super_weapons})
        else:
            return self.weapons

    def create_widgets(self):
        self.create_main_menu()

        def create_menu_button(imgpath, command, grid_args):
            image = load_image(imgpath)
            button = tk.Button(master=self, image=image)
            button.image = image # Avoid garbage collect
            button['command'] = command
            button.grid(**grid_args)
            return button

        # Button to access weapons_menu
        weapons_btn = create_menu_button(
            imgpath=('optionsmenu', 'weaponoptions.bmp'),
            command=self.create_weapons_menu,
            grid_args={'row': 2, 'column': 4, 'columnspan': 2}
        )
        weapons_btn.bind("<Enter>", lambda event: self.help_text.set("Open Weapons menu"))
        weapons_btn.bind("<Leave>", lambda event: self.help_text.set(self.default_help_text))

        # Button to access special stuff
        special_btn = create_menu_button(
            imgpath=('Custom', 'secretstar.bmp'),
            command=self.create_special_menu,
            grid_args={'row': 2, 'column': 6}
        )
        special_btn.bind("<Enter>", lambda event: self.help_text.set("Open Special menu"))
        special_btn.bind("<Leave>", lambda event: self.help_text.set(self.default_help_text))

        # To display help text
        self.help_text = tk.StringVar()
        self.help_text.set(self.default_help_text)
        tk.Label(master=self, textvariable=self.help_text, wraplength=200,
            borderwidth=2, relief='ridge').grid(row=4, column=1, columnspan=3, 
            sticky='N'+'E'+'S'+'W'
        )
    
        # Box to confirm/display what last setting was just changed to
        self.last_change = tk.StringVar(value="")
        tk.Label(master=self, textvariable=self.last_change, wraplength=132,
            borderwidth=2, relief='ridge').grid(row=4, column=4, columnspan=2, 
            sticky='N'+'E'+'S'+'W'
        )

        # Load scheme button
        tk.Button(master=self, text='Load Scheme', wraplength=68, fg='blue', 
            command=self.load_scheme).grid(row=3,column=6)

        # Save scheme button
        tk.Button(master=self, text='Save Scheme', wraplength=68, fg='green', 
            command=self.save_scheme).grid(row=4,column=6)

    def init_all_options(self):
        # Using OrdererDicts since we need to know this order when saving scheme
        self.all_options = OrderedDict() # inneficient to have copies but easier to manage
        self.main_menu_options = OrderedDict()
        self.special_menu_options = OrderedDict()
        self.hidden_options = OrderedDict()
        self.weapons = OrderedDict()
        self.super_weapons = OrderedDict()

        for name, option_dict in ALL_OPTIONS.items():
            # Figuring out which dict to store this option in
            if name in MAIN_MENU_OPTIONS:
                d = self.main_menu_options
            elif name in SPECIAL_MENU_OPTIONS:
                d = self.special_menu_options
            elif name in HIDDEN_OPTIONS:
                d = self.hidden_options
            
            # option = make_option(master=self, name=name, option_dict=option_dict)
            # Determining what kind of Option this should be
            if option_dict['Type'] == 'bool':
                option = BoolOption(master=self, name=name)
            elif option_dict['Type'] == 'choice':
                option = ChoiceOption(master=self, name=name)
            elif option_dict['Type'] == None:
                option = NoneOption(master=self, name=name)
            elif option_dict['Type'] in ('ubyte', 'byte', 'sbyte'):
                if option_dict['Type'] == 'sbyte':
                    signed = True
                else:
                    signed = False
                option = IntOption(master=self, name=name, signed=signed)
            
            d[name] = option
            self.all_options[name] = option # Adding them in order

        for name, weapon in ALL_WEAPONS.items():
            if name in SUPER_WEAPONS:
                d = self.super_weapons
            else:
                d = self.weapons
            d[name] = Weapon(master=self, name=name)

    def create_main_menu(self):
        for name, option in self.main_menu_options.items():
            if type(option) == NoneOption:
                continue

            button = Button(master=self, option=option, gui=self)
            option.button = button # Keep reference to button

    def create_popup_menu(self, menu_options, popup_name, popup_title):
        def destroy(popup_menu, popup_name, *args):
            popup_menu.destroy()
            delattr(self, popup_name)
            # self.value.set(self.value.get()) # To ensure int is restricted to 0-255  or -127-127
            # self.master.last_change.set(f'{self.name} set to {self.value.get()}')
        
        try:
            getattr(self, popup_name).focus_set() # if popup already open
        except: # create new popup
            popup_menu = tk.Toplevel(master=self)
            setattr(self, popup_name, popup_menu)

            popup_menu.title(popup_title)
            popup_menu.bind("<Return>", partial(destroy, popup_menu, popup_name))
            popup_menu.bind("<Escape>", partial(destroy, popup_menu, popup_name))

            for name, option in menu_options.items():
                button = Button(master=popup_menu, option=option, gui=self)
                option.button = button # Keep reference to button

    def create_special_menu(self):
        self.create_popup_menu(menu_options=self.special_menu_options, popup_name='special_menu', popup_title='Special things')

    def create_weapons_menu(self):
        self.create_popup_menu(menu_options=self.all_weapons, popup_name='weapons_menu', popup_title='Weapons')
        
    def save_scheme(self, *args):
        """For the love of God DO NOT TOUCH!"""
        f = filedialog.asksaveasfile(mode='wb', initialdir=SCHEME_DIR,
            defaultextension='.wsc')

        if f is None: # If user presses cancel button
            return

        for name, option in self.all_options.items():
            value = option.encoded_value
            print(f'{name} = {value}')
            f.write(value)

        for name, option in self.all_weapons.items():
            value = option.encoded_value
            print(f'{name} = {value}')
            f.write(value)

        f.close()    

    def load_scheme(self):
        f = filedialog.askopenfile(mode='rb', initialdir=SCHEME_DIR)

        if f is None:
            return

        for name, option in self.all_options.items():
            expected_len = len(option.encoded_value)
            raw_bytes = f.read(expected_len)

            # Don't try to decode or change NoneOptions, but we have read required bytes
            if name in self.hidden_options:
                continue

            new_value = option.decode(raw_bytes)
            option.value.set(new_value)
            if hasattr(option, 'button'):
                option.button.update_image()

        # Since 'Super Weapons' option should already be set from above
        # Note: all_weapons will include super weapons if it's meant to
        for name, option in self.all_weapons.items():
            # We know weapons are 4 bytes
            for key in ['ammo', 'power', 'delay', 'crate_probability']:
                raw_byte = f.read(1)
                new_value = getattr(option, key).decode(raw_byte) 
                getattr(option, key).set(new_value)

        f.close()

    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master})'


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Worms Armageddon Scheme Editor')
    gui = GUI(master=root)
    gui.mainloop()