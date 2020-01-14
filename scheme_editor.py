"""classy_scheme_editor.py

Attempting to refactor my scheme editor so it's a little easier to work with by
converting lots of functionality to classes. OOP gone too far?
"""
import os
import tkinter as tk
import tkinter.filedialog as filedialog
from collections import OrderedDict
from functools import partial
from binascii import unhexlify
from PIL import Image, ImageTk
from math import floor
from pprint import pprint

from options import OPTIONS, MAIN_MENU_OPTIONS, SPECIAL_MENU_OPTIONS, HIDDEN_OPTIONS
from weapons import WEAPONS, SUPER_WEAPONS

ROOT_DIR = os.path.dirname(__file__)
WORMS_DIR = os.path.dirname(ROOT_DIR)
DEFAULT_IMG_DIR = os.path.join(WORMS_DIR, 'graphics')
WEAPONS_IMGS_DIR = os.path.join(os.getcwd(), 'weapons_images')
# SCHEME_DIR = os.path.join(WORMS_DIR, 'User', 'Schemes')
SCHEME_DIR = os.path.join(ROOT_DIR, 'Schemes')

def load_image(imgpath, imgdir=DEFAULT_IMG_DIR):
    """Loads image in tkinter-friendly format so we can add to buttons, etc.
    
    Parameters
    ----------
    imgpath: iterable of strings
        Strings describing the path of the image WITHIN `imgdir`
    imgdir: path object; defaults to ``DEFAULT_IMG_DIR``
        Path to the root directory we expect image to be found in.
    """
    image = Image.open(os.path.join(imgdir, *imgpath))
    return ImageTk.PhotoImage(image)


class IntVar(tk.IntVar):
    """Class for dealing with 8 bit values. Can be signed or unsigned.
    Inherits from tkinter.IntVar so has same properties.

    Parameters
    ----------
    value: int
        int between 0-255. Not the hexadecimal representation.
    signed: bool; defaults to False
        Whether this byte is signed or not
    """
    def __init__(self, *, value, signed=False):
        super().__init__()
        self.signed = signed
        self.set(value)

    # Overriding default set value so we can restrict it
    def set(self, value):
        value = int(value)
        if self.signed:
            if value < -127:
                value = -127
            elif value > 127:
                value = 127
        else:
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
        return self._tk.globalsetvar(self._name, value)

    def get_encoded_value(self):
        if self.signed: 
            magnitude = abs(self.get())
            hex_str = '{value:02x}'.format(value=magnitude+128) # Converts to signed value (i.e. between 128-255 in hex)
        else:
            hex_str = '{value:02x}'.format(value=self.get())
        return bytes.fromhex(hex_str)

    def decode(self, raw_byte):
        if self.signed:
            return int.from_bytes(raw_byte, byteorder='little', signed=True)
        else:
            return int.from_bytes(raw_byte, byteorder='little')

    def __repr__(self):
        return f'Byte: {self.get()}'


class Option():
    """The base class for all options we can adjust."""
    def __init__(self, master, option, name):
        """
        Parameters
        ----------
        master: tk.Tk object or similar
            The master of this option
        option: dict
        """
        self.master = master
        try:
            self.grid_args = option['Grid Args']
        except KeyError: # For Weapon class
            pass
        self.name = name

    def button_command(self):
        """Used in StrOption and BoolOption.
        Changes button's image and the Option's value.
        """
        self.cycle_value()
        new_image = self.get_image()
        self.button['image'] = new_image
        self.button.image = new_image
        self.master.last_change.set(f'{self.name} set to {self.value.get()}')

    def on_value_change(self, *args):
        pass


class BoolOption(Option):
    """An option that can only be True or False
    
    Parameters
    ----------
    master: tkinter.Tk() or something similar
    grid_args: dict of keyword args
        To be used in tkinter.Button.grid(**grid_args)
    value: bool
    images: dict of imgpaths
        imgpaths should work with load_image()

    """
    def __init__(self, *, master, option, name):
        super().__init__(master=master, option=option, name=name)
        
        value = option['Default']
        images = option['Images']
        self.value = tk.BooleanVar(value=value)
        self.images = images

    def cycle_value(self):
        self.value.set(not self.value.get()) # Invert

    def get_encoded_value(self):
        if self.value.get() == False:
            return b'\x00'
        else:
            return b'\x01'

    def get_image(self):
        return load_image(self.images[self.value.get()])

    def __repr__(self):
        return f'BoolOption: {self.value.get()}'

    def decode(self, raw_bytes):
        if raw_bytes == b'\x00':
            return False
        elif raw_bytes == b'\x01':
            return True
        else:
            raise ValueError(f'{raw_bytes} could not be interpreted as bool!')


class StrOption(Option):
    """Option that cycles through a small list of possible values, stored as
    strings so I actually remember what they mean. An example would be the
    Sudden Death Event option, which can be either 'Round Ends' (b'\x00'), 
    'Nuclear Strike' (b'\x01'), etc.

    Parameters
    ----------
    master:
    grid_args:
    option: dict
        A copy or reference to option's dict in which this is stored. For
        example, if this was the StrVar for 'Stockpiling Mode', we would 
        expect:
            {
                'Type': 'str',
                'Default': 'Replenishing',
                'Conversions': {
                    'Replenishing': b'\x00',
                    'Accumulating': b'\x01',
                    'Reducing':     b'\x02'
                },
                'Images': {
                    'Replenishing': ('gameoptions', 'Stockpiling', '000001.bmp'),
                    'Accumulating': ('gameoptions', 'Stockpiling', '000002.bmp'),
                    'Reducing':     ('gameoptions', 'Stockpiling', '000003.bmp')
                },
                'Grid Args': {
                    'row': 0,
                    'column': 5
            }
    """
    def __init__(self, *, master, option, name):
        super().__init__(master=master, option=option, name=name)

        value = option['Default']
        conversions = option['Conversions']
        images = option['Images']
        self.value = tk.StringVar(value=value)
        self.conversions = conversions
        self.images = images

    def get_image(self):
        value = self.value.get()
        return load_image(self.images[value])

    def get_encoded_value(self):
        value = self.value.get()
        return self.conversions[value]

    def cycle_value(self):
        index = self._get_index()

        # Getting next index
        # Use modulo to wrap around if required (i.e. at end of list)
        new_index = (index + 1) % len(self.possible_values)
        new_value = self.possible_values[new_index]
        self.value.set(new_value)

    @property
    def possible_values(self):
        return list(self.conversions.keys())

    def _get_index(self):
        """Gets index of self within the list of possible values self can take"""
        return self.possible_values.index(self.value.get())

    def decode(self, raw_byte):
        """Can't be class method because StrVars vary too much in `conversion`, etc."""
        reverse_conversions = {v: k for k, v in self.conversions.items()}
        return reverse_conversions[raw_byte]


class IntOption(Option):
    """Option that takes the value of an integer. Can be signed or unsigned.
    Maximum length of 8 bits (1 byte).

    Parameters
    ----------
    master: tkinter.Tk() or something similar
    grid_args: dict of keyword args
        To be used in tkinter.Button.grid(**grid_args) 
    value: int
    image: imgpath
        imgpath should work with load_image()
    signed: bool; Default=False
        Whether byte is signed or unsigned
    """
    def __init__(self, *, master, option, name, signed=False):
        super().__init__(master=master, option=option, name=name)
        
        value = option['Default']
        self.value = IntVar(value=value, signed=signed)
        self.image = option['Image']
        self.popup_text = tk.StringVar()
        self.popup_text.set(option.get('Popup Text', ''))

    def get_image(self):
        return load_image(self.image)

    def get_encoded_value(self):
        """Returns the raw bytes (as hex representation) to be written to the
        scheme file, taking into account whether it's a signed byte or not.
        """
        return self.value.get_encoded_value()

    def decode(self, raw_byte):
        return self.value.decode(raw_byte=raw_byte)

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

            # Entry to change value
            popup.entry = tk.Entry(master=popup, textvariable=self.value)
            popup.entry.grid(row=1)
            popup.entry.focus_set()
            popup.entry.select_range(0, tk.END)
            popup.entry.icursor(tk.END)

            # 3 ways of leaving popup, including button to confirm
            tk.Button(master=popup, text="Confirm", fg='green', command=partial(destroy, popup)).grid(row=2)
            popup.bind("<Return>", partial(destroy, popup))
            popup.bind("<Escape>", partial(destroy, popup))

    def __repr__(self):
        return f'IntOption: {self.value.get()}'


class NoneOption(Option):
    """Class for dealing with options we shouldn't change, like the magic bytes
    at start of file."""
    def __init__(self, *, master, option, name):
        super().__init__(master=master, option=option, name=name)
        
        value = option['Default'] # Should be in bytes already
        self.value = value

    def get_encoded_value(self):
        return self.value

    def decode(self, value):
        """Doesn't actually need to decode since this value never changes"""
        return self.value


class Weapon(Option):   
    """
    Parameters
    ----------
    master:
    option: dict
    name: str
    is_super: bool
    """ 
    def __init__(self, master, option, name, is_super=False):
        super().__init__(master=master, option=option, name=name)

        # Written in order as they appear in scheme file
        self.ammo = IntVar(value=option['Ammo']) # 10 or 128-255 means infinite ammo
        self.power = IntVar(value=option['Power'])
        self.delay = IntVar(value=option['Delay']) # 128-255 means it's 'blocked'
        self.crate_probability = IntVar(value=option['Crate Probability'])
        
        self.image = option['Image']
        self.is_super = is_super

        # dummy variable really
        self.value = tk.BooleanVar()

    def __repr__(self):
        return {self.name}

    @property
    def grid_args(self):
        # Getting index of weapon in weapons lists
        if self.is_super:
            weapons = SUPER_WEAPONS.items()
        else:
            weapons = WEAPONS.items()
        names = [w[0] for w in weapons]
        index = names.index(self.name)

        if self.is_super:
            index += 45
        # Converting index to grid_args
        return {'row': floor(index / 8), 'column': index % 8}

    def get_image(self):
        return load_image(self.image, imgdir=WEAPONS_IMGS_DIR)

    def get_encoded_value(self):
        encoded_values = b''
        for thing in (self.ammo, self.power, self.delay, self.crate_probability):
            encoded_values += thing.get_encoded_value()

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

            # self.master.last_change.set(f'{self.name} set to {self.value.get()}')

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
            text = ("If ammo is set to 10 or 128-255, you'll get unlimited ammo.\n"
                    "If delay is set to 128-255, weapon will never appear in crates."
            )
            tk.Label(master=weapon_popup, text=text).grid(row=0, columnspan=2)

            # Entries to change values and assoicated labels
            tk.Label(master=weapon_popup, text='Ammo').grid(row=1)
            weapon_popup.ammo_entry = tk.Entry(master=weapon_popup, textvariable=self.ammo)
            weapon_popup.ammo_entry.grid(row=1, column=1)
            tk.Label(master=weapon_popup, text='Delay').grid(row=2)
            weapon_popup.delay_entry = tk.Entry(master=weapon_popup, textvariable=self.delay)
            weapon_popup.delay_entry.grid(row=2, column=1)
            tk.Label(master=weapon_popup, text='Power').grid(row=3)
            weapon_popup.power_entry = tk.Entry(master=weapon_popup, textvariable=self.power)
            weapon_popup.power_entry.grid(row=3, column=1)
            tk.Label(master=weapon_popup, text='Crate probability').grid(row=4)
            weapon_popup.crate_probability_entry = tk.Entry(master=weapon_popup, textvariable=self.crate_probability)
            weapon_popup.crate_probability_entry.grid(row=4, column=1)

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
        super().__init__(master)
        self.master = master
        self.pack()

        # Using OrdererDicts since we need to know this order when saving scheme
        self.all_options = OrderedDict() # inneficient to have copies but easier to manage
        self.main_menu_options = OrderedDict()
        self.special_menu_options = OrderedDict()
        self.hidden_options = OrderedDict()
        self.weapons = OrderedDict()
        self.super_weapons = OrderedDict()

        self.init_all_options()

        self.create_widgets()

    def __repr__(self):
        return "MAIN GUI OBJECT"

    def create_widgets(self):
        self.create_main_menu()

        # Button to access weapons_menu
        weapons_menu_image = load_image(('optionsmenu', 'weaponoptions.bmp'))
        weapons_menu_btn = tk.Button(master=self, image=weapons_menu_image)
        weapons_menu_btn.image = weapons_menu_image # Avoid garbage collect
        weapons_menu_btn['command'] = self.create_weapons_menu
        weapons_menu_btn.grid(row=2, column=4, columnspan=2)

        # Button to access special stuff
        special_menu_image = load_image(('Custom', 'secretstar.bmp'))
        special_menu_btn = tk.Button(master=self, image=special_menu_image)
        special_menu_btn.image = special_menu_image # Avoid garbage collect
        special_menu_btn['command'] = self.create_special_menu
        special_menu_btn.grid(row=2, column=6)

        # To display help text
        self.default_help_text = "Welcome to Lex's Worms Armageddon Scheme Editor!"
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
        for name, option in OPTIONS.items():
            # Figuring out which dict to store this option in
            if name in MAIN_MENU_OPTIONS:
                d = self.main_menu_options
            elif name in SPECIAL_MENU_OPTIONS:
                d = self.special_menu_options
            elif name in HIDDEN_OPTIONS:
                d = self.hidden_options
            
            # Ignoring option['Type'] == None since we can't change those options
            if option['Type'] == 'bool':
                option_obj = BoolOption(master=self, name=name, option=option)
            elif option['Type'] == 'str':
                option_obj = StrOption(master=self, name=name, option=option)
            elif option['Type'] in ('ubyte', 'byte', 'sbyte'):
                if option['Type'] == 'sbyte':
                    signed = True
                else:
                    signed = False
                option_obj = IntOption(master=self, name=name, 
                    option=option, signed=signed
                )
            elif option['Type'] == None:
                option_obj = NoneOption(master=self, name=name, option=option)

            d[name] = option_obj
            self.all_options[name] = option_obj

        for name, weapon in WEAPONS.items():
            self.weapons[name] = Weapon(master=self, name=name, option=weapon)

        for name, weapon in SUPER_WEAPONS.items():
            self.super_weapons[name] = Weapon(master=self, name=name, option=weapon, is_super=True)

    def create_main_menu(self):
        for name, option in self.main_menu_options.items():
            if type(option) == NoneOption:
                continue

            button = tk.Button(master=self)
            option.button = button # Keep reference to button

            image = option.get_image()
            button['image'] = image
            button.image = image # To avoid garbage collect

            value = option.value.get()
            button['textvariable'] = value

            button['command'] = option.button_command

            def set_help_text(option, default=False, event=None):
                """Callback for when button is hovered onto or off of."""
                if default == False:
                    self.help_text.set(f"{option.name}: {option.value.get()}")
                else:
                    self.help_text.set(self.default_help_text)
            button.bind("<Enter>", partial(set_help_text, option, False))
            button.bind("<Leave>", partial(set_help_text, option, True))

            button.grid(**option.grid_args)

    def create_popup_menu(self, menu_options, popup_name, popup_title, graphics_dir=DEFAULT_IMG_DIR):
        def destroy(popup_menu, popup_name, *args):
            popup_menu.destroy()
            delattr(self, popup_name)
            # self.value.set(self.value.get()) # To ensure int is restricted to 0-255  or -127-127
            # self.master.last_change.set(f'{self.name} set to {self.value.get()}')

        def set_help_text(option, default=False, event=None):
            """Callback for when button is hovered onto or off of."""
            if default == False:
                self.help_text.set(f"{option.name}: {option.value.get()}")
            else:
                self.help_text.set(self.default_help_text)
        
        try:
            getattr(self, popup_name).focus_set() # if popup already open
        except: # create new popup
            popup_menu = tk.Toplevel(master=self)
            setattr(self, popup_name, popup_menu)

            popup_menu.title(popup_title)
            popup_menu.bind("<Return>", partial(destroy, popup_menu, popup_name))
            popup_menu.bind("<Escape>", partial(destroy, popup_menu, popup_name))

            for name, option in menu_options.items():
                button = tk.Button(master=popup_menu)
                option.button = button # Keep reference to button

                image = option.get_image()
                button['image'] = image
                button.image = image # To avoid garbage collect

                value = option.value.get()
                button['textvariable'] = value

                button['command'] = option.button_command
                
                button.bind("<Enter>", partial(set_help_text, option, False))
                button.bind("<Leave>", partial(set_help_text, option, True))

                button.grid(**option.grid_args)

    def create_special_menu(self):
        self.create_popup_menu(menu_options=self.special_menu_options, popup_name='special_menu', popup_title='Special things')

    def create_weapons_menu(self):
        if self.main_menu_options['Super Weapons'].value.get() == 'True':
            weapons = {**self.weapons, **self.super_weapons}
        else:
            weapons = self.weapons

        self.create_popup_menu(menu_options=weapons, popup_name='weapons_menu', popup_title='Weapons')

    # def create_special_menu(self):
    #     def destroy(popup_menu, *args):
    #         popup_menu.destroy()
    #         delattr(self, 'weapons_menu')
    #         self.master.last_change.set(f'{self.name} set to {self.value.get()}')

    #     try:
    #         self.special_menu.focus_set()
    #     except:
    #         special_menu = tk.Toplevel(master=self)
    #         self.special_menu = special_menu
            
    #         special_menu.title('Special things')

    #         for name, option in self.special_menu_options.items():
    #             button = tk.Button(master=special_menu)
    #             option.button = button # Keep reference to button

    #             image = load_image(*option.get_image())
    #             button['image'] = image
    #             button.image = image # To avoid garbage collect

    #             value = option.value.get()
    #             button['textvariable'] = value

    #             button['command'] = option.button_command

    #             def set_help_text(option, default=False, event=None):
    #                 """Callback for when button is hovered onto or off of."""
    #                 if default == False:
    #                     self.help_text.set(f"{option.name}: {option.value.get()}")
    #                 else:
    #                     self.help_text.set(self.default_help_text)
    #             button.bind("<Enter>", partial(set_help_text, option, False))
    #             button.bind("<Leave>", partial(set_help_text, option, True))

    #             button.grid(**option.grid_args)

    # def create_weapons_menu(self):
    #     def destroy(weapons_menu, *args):
    #         weapons_menu.destroy()
    #         delattr(self, 'weapons_menu')
    #         # self.value.set(self.value.get()) # To ensure int is restricted to 0-255  or -127-127
    #         # self.master.last_change.set(f'{self.name} set to {self.value.get()}')

    #     try:
    #         self.weapons_menu.focus_set()
    #     except (tk.TclError, AttributeError) as e:
    #         weapons_menu = tk.Toplevel(master=self) # Maybe change master to main menu?
    #         self.weapons_menu = weapons_menu
    #         weapons_menu.title('Weapons')
    #         weapons_menu.bind("<Return>", partial(destroy, weapons_menu))
    #         weapons_menu.bind("<Escape>", partial(destroy, weapons_menu))

    #         if self.main_menu_options['Super Weapons'].value.get() == True:
    #             weapons_dict = {**self.weapons, **self.super_weapons} 
    #         else:
    #             weapons_dict = self.weapons

    #         for i, (name, option) in enumerate(weapons_dict.items()):
    #             button = tk.Button(master=weapons_menu)
                
    #             # Setting button's image
    #             image = load_image(option.image, imgdir=WEAPONS_IMGS_DIR)
    #             button['image'] = image
    #             button.image = image # To avoid garbage collect

    #             # Setting button's command
    #             button['command'] = option.button_command

    #             # Positioning button
    #             row = floor(i / 8)
    #             column = i % 8
    #             button.grid(row=row, column=column)
        
    def save_scheme(self, *args):
        """For the love of God DO NOT TOUCH!"""
        f = filedialog.asksaveasfile(mode='wb', initialdir=SCHEME_DIR,
            defaultextension='.wsc')

        if f is None: # If user presses cancel button
            return

        for name, option in self.all_options.items():
            value = option.get_encoded_value()
            print(f'{name} = {value}')
            f.write(value)

        # Seeing if we should write super weapons to file too
        if self.main_menu_options['Super Weapons'].value.get() == 'True':
            weapons = {**self.weapons, **self.super_weapons}
        else:
            weapons = self.weapons

        for name, option in weapons.items():
            value = option.get_encoded_value()
            print(f'{name} = {value}')
            f.write(value)
        f.close()    

    def load_scheme(self):
        f = filedialog.askopenfile(mode='rb', initialdir=SCHEME_DIR)

        if f is None:
            return

        for name, option in self.all_options.items():
            expected_len = len(option.get_encoded_value())
            raw_bytes = f.read(expected_len)

            # Don't try to decode or change NoneOptions, but we have read required bytes
            if name in self.hidden_options:
                continue

            new_value = option.decode(raw_bytes)
            option.value.set(new_value)
            if hasattr(option, 'button'):
                new_image = option.get_image()
                option.button['image'] = new_image
                option.button.image = new_image

        # Determining if scheme has super weapons or not
        f.seek(0, 2) # Goes to end of file
        if f.tell() == 297: # has super weapons
            weapons = {**self.weapons, **self.super_weapons}
        elif f.tell() == 221: # does not have super weapons
            weapons = self.weapons

        f.seek(41) # Go back to start of weapons data
        for name, option in weapons.items():
            # We know weapons are 4 bytes
            for key in ['ammo', 'power', 'delay', 'crate_probability']:
                raw_byte = f.read(1)
                new_value = getattr(option, key).decode(raw_byte) 
                getattr(option, key).set(new_value)

        f.close()


root = tk.Tk()
root.title('Worms Armageddon Scheme Editor')

gui = GUI(master=root)
gui.mainloop()