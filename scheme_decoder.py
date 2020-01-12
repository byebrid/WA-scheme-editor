"""
scheme_decoder.py by Byebrid.
-----------------------------
Designed to examine a Worms Armageddon Scheme file (.wsc), which describes
the settings to be used in an offline (maybe online too) match.

Info about the file format based off https://worms2d.info/Game_scheme_file

Value types
-----------
char[4]: Treated as 4 character string
byte/ubyte: Not sure if distinguished in game; Unsinged byte
sbyte: Signed byte
bool: Boolean; \x00==False, \x01==True
"""
import csv
import base64
import os
import tkinter as tk
import tkinter.filedialog as filedialog
import math
from PIL import Image, ImageTk
from functools import partial
from options import OPTIONS
from weapons import WEAPONS, SUPER_WEAPONS
from pprint import pprint

# Filepaths
WORMSA_DIR = os.path.normpath(os.getcwd() + os.sep + os.pardir)
WORMS_DEFAULT_GRAPHICS_DIR = os.path.join(WORMSA_DIR, 'graphics')
WEAPONS_IMGS_DIR = os.path.join(os.getcwd(), 'weapons_images')
SCHEME_DIR = os.path.join(WORMSA_DIR, 'User', 'Schemes')

# Particular options
IGNORE = ('Signature', 'Bounty Mode', 'Team Weapons', 'Super Weapons in Crates')
SPECIAL = (
    'Blood', 'Aqua Sheep', 'Sheep Heaven', 'God Worms', 'Indestructible Land', 
    'Upgraded Grenade', 'Upgraded Shotgun', 'Upgraded Clusters','Upgraded Longbow',
)

def read_scheme(scheme_file):
    """Reads a .wsc Worms scheme file into a dictionary with all its values"""
    result = get_scheme_format()
    with open(scheme_file, 'rb') as f:
        # Get offset and size of each chunk of file format encoding
        for chunk in result:
            value = f.read(chunk['Size'])
            value = decode(value, chunk['Type'])
            chunk['Value'] = value
        
        # result[1] is version, either 0x01=Standard Scheme or
        # 0x02=Extended Scheme (super weapons enabled)
        version = result[1]['Value']
        if version == 1:
            num_weapons = 45
        elif version == 2:
            num_weapons = 64

        # Parsing all the weapons settings (in chunks of 4 bytes)
        for weapon in get_weapon_list()[:num_weapons]:
            weapon_setting = {'Name': weapon['Weapon Name']}
            for field in ['Ammo', 'Power', 'Delay', 'Crate Probability']:
                weapon_setting[field] = decode(f.read(1), value_type='ubyte')
            result.append(weapon_setting)

    return result
        
# def get_blank_scheme(extended=False):
#     """Get template for new scheme"""
#     scheme = get_scheme_format()
#     # This has to be set to 'SCHM'
#     scheme[0]['Value'] = 'SCHM'

#     for setting in scheme[1:]:
#         setting['Value'] = None

#     # If scheme is standard (no super weapons) or extended (including super weapons)
#     if extended == False:
#         num_weapons = 45
#     elif extended == True:
#         num_weapons = 64

#     weapon_list = get_weapon_list()
#     for i, weapon in enumerate(get_weapon_list()[:num_weapons]):
#         weapon_name = weapon_list[i]['Weapon Name']
#         weapon_setting = {
#             'Name': weapon_name,
#             'Ammo': 0,
#             'Delay': 0,
#             'Crate Probability': 0
#         }
#         scheme.append(weapon_setting)
    
#     return scheme

def get_scheme_format():
    """
    Returns
    -------
    list of dicts:
        dicts describe each row of file_format.csv
    """
    # Drop last row describing weapons settings
    result = csv_to_list_dicts('scheme_format.csv')[:-1]
    for row in result:
        # If description has commas in it:
        if None in row.keys():
            end_of_desc = row.pop(None)
            row['Description'] += ''.join(end_of_desc)

        # Convert offset to base10 (?) int
        offset_base10 = int(row['Offset'], 16)
        row['Offset'] = offset_base10   

        # Convert size to int
        row['Size'] = int(row['Size'])

    return result

# def get_weapon_format():
#     result = csv_to_list_dicts('weapon_format.csv')
#     for row in result:
#         # If description has commas in it:
#         if None in row.keys():
#             end_of_desc = row.pop(None)
#             row['Description'] += ''.join(end_of_desc)
        
#         # Convert offset to base10 (?) int
#         offset_base10 = int(row['Offset'], 16)
#         row['Offset'] = offset_base10

#     return result

def get_weapon_list():
    return csv_to_list_dicts('weapons_list.csv')

def decode(value, value_type):
    """Decodes the `value` read from the scheme based on its type as described
    by `value_type`

    Parameters
    ----------
    value: bytes object
        Represents the value as read from the scheme file
    value_type: str
        The type of `value` as described in 'scheme_format.csv'
    """
    if value_type == 'char[4]':
        return value.decode('utf-8')
    elif value_type in ('byte', 'ubyte'):
        return int.from_bytes(value, byteorder="little")
    elif value_type == 'sbyte':
        return int.from_bytes(value, byteorder="little", signed=True)
    elif value_type == 'bool':
        if value == b'\x00':
            return False
        elif value == b'\x01':
            return True
        else:
            raise ValueError(f"value {value} was not 0 or 1 (as byte)")
    else:
        raise ValueError(f"Didn't know how to decode value with type {value_type}")
    
def encode(value, value_type):
    """Reverses decode()"""
    if value_type == 'char[4]':
        return value.encode('utf-8')
    elif value_type in ('byte', 'ubyte'):
        hex_str = "{0:#0{1}x}".format(value,4)
        return bytes(hex_str, 'utf-8')
    elif value_type == 'sbyte':
        hex_str = "{0:#0{1}x}".format(value & 0xff,4)
        return bytes(hex_str, 'utf-8')
    elif value_type == 'bool':
        if value == False:
            return b'\x00'
        elif value == True:
            return b'\x01'
        else:
            raise ValueError(f"value {value} was not False or True")
    else:
        raise ValueError(f"Didn't know how to encode value with type {value_type}")

def csv_to_list_dicts(filepath):
    """Reads csv file to list of dicts, assuming first row is labels for columns."""
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def get_bitmap(*args, graphics_dir=WORMS_DEFAULT_GRAPHICS_DIR):
    image = Image.open(os.path.join(graphics_dir, *args))
    return ImageTk.PhotoImage(image)


class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.options = OPTIONS
        self.weapons = WEAPONS
        self.super_weapons = SUPER_WEAPONS
        self.default_help_text = (
            "Welcome to Lex's scheme editor! Mouse over buttons to see what they do "
            "and click on buttons to change their values."
        )
        self.create_widgets()

    def save_scheme(self):
        f = filedialog.asksaveasfile(mode='wb', initialdir=SCHEME_DIR,
            defaultextension='.wsc')

        if f is None: # If user presses cancel button
            return

        # print("self.options:")
        # print("----------------------------------")
        # pprint(self.options)

        # print()
        # print("self.weapons:")
        # print("----------------------------------")
        # pprint(self.weapons)

        # print()
        # print("self.super_weapons:")
        # print("----------------------------------")
        # pprint(self.super_weapons)

        # Writing main options to file. 
        for name, option in self.options.items():
            if name in IGNORE:
                value = option['Default']
            else:
                print(f"Getting var for {name}")
                var = option['var']
                if type(var.get()) == int:
                    value = encode(var.get(), value_type=option['Type_Native'])
                else:
                    index = self.get_index(option=option, var=option['var'])
                    value = option['Values_Images'][index][0]
            print(f"{name} = {value}")
            f.write(value)
        
        # Figuring out if we need to write super weapons too
        if self.options['Super Weapons']['var'].get() == True:
            weapons = {**self.weapons, **self.super_weapons}
            print("Including Super Weapons...")
        else:
            print("Excluding Super Weapons...")
            weapons = self.weapons
        
        # Writing encoded weapon data
        for name, option in weapons.items():
            value = b''
            for k, v in option.items():
                if k in ('Image', 'button'):
                    continue
                encoded_val = encode(v.get(), value_type='byte')
                value += encoded_val
            
            print(f"{name} = {value}")
            f.write(value)

        f.close()

    def get_index(self, option, var):
        # var is stored in human readable form
        human_readables = [e[1] for e in option['Values_Images']]
        return human_readables.index(var.get())

    def create_button(self, option_name, pos=None):
        # Getting parameters for button based on whether it's for weapon or normal option
        if option_name in (*WEAPONS, *SUPER_WEAPONS):
            if option_name in WEAPONS:
                option = self.weapons[option_name]
            else:
                option = self.super_weapons[option_name]

            # Turn values into tk variables if not already done, using Ammo as eg
            try:
                option['Ammo'].get() # Works if tk variable
            except AttributeError:
                print(f'Turning {option_name} into tkVars')
                for key in ['Ammo', 'Crate Probability', 'Delay', 'Power']:
                    value = option[key]
                    option[key] = tk.IntVar(value=value)

            image = get_bitmap(option['Image'], graphics_dir=WEAPONS_IMGS_DIR)
            command = partial(self.get_weapon_popup, option_name)
            master = self.weapon_menu

        elif option_name in OPTIONS:
            option = self.options[option_name]
            # Getting list of values and associated images
            values_images = option['Values_Images']

            # If var was already created (say if special menu was already opened)
            try:
                var = option['var']
                index = self.get_index(option=option, var=var)
                imgpath = values_images[index][-1]
            # Else create var
            except KeyError as e:  
                human_readable, imgpath = values_images[0][1:]

                # Deciding what king of tkVar we should store
                if type(human_readable) == str:
                    var = tk.StringVar()
                elif type(human_readable) == bool:
                    var = tk.BooleanVar()
                elif type(human_readable) == int:
                    var = tk.IntVar()
                else:
                    raise ValueError("{human_readable} was not of type str, bool or int!")

                var.set(human_readable)
                option['var'] = var

            image = get_bitmap(*imgpath)
            command = partial(self.get_option_popup, self, option_name)
            if option_name in SPECIAL:
                master = self.special_menu
            else:
                master = self
            pos = option['Position']

        # Making button
        button = tk.Button(master=master, image=image, command=command)
        button.grid(**pos)
        button.image = image # prevent garbage collection

        # For displaying tooltips
        button.bind("<Enter>", partial(self.display_help_text, option_name))
        button.bind("<Leave>", partial(self.hide_help_text))

        option['button'] = button # Keep reference

    def create_widgets(self):
        # Box in centre-middle to display tooltips for each button
        self.help_text = tk.StringVar()
        self.help_text.set(self.default_help_text)
        tk.Label(self, textvariable=self.help_text, wraplength=200,
            borderwidth=2, relief='ridge').grid(row=4, column=1, columnspan=3, sticky='N'+'E'+'S'+'W')

        # Box to confirm/display what last setting was just changed to
        self.change_text = tk.StringVar()
        tk.Label(self, textvariable=self.change_text, wraplength=132,
            borderwidth=2, relief='ridge').grid(row=4, column=4, columnspan=2, sticky='N'+'E'+'S'+'W')

        # Button to save the scheme to a .wsc file
        tk.Button(self, text='Save scheme', fg='green', 
            borderwidth=2, relief='ridge',
            command=self.save_scheme).grid(row=4, column=6)

        # Button to enter special options popup
        doors_img = get_bitmap('Custom', 'door2.bmp')
        self.special_btn = tk.Button(self, image=doors_img)
        self.special_btn.image = doors_img # Prevents garbage collect
        self.special_btn.grid(row=1, rowspan=2, column=6)
        self.special_btn['command'] = self.get_special_menu

        # Button to enter weapons popup
        weapon_img = get_bitmap('OptionsMenu', 'weaponoptions.bmp')
        self.weapon_btn = tk.Button(self, image=weapon_img)
        self.weapon_btn.image = weapon_img # Prevents garbage collect
        self.weapon_btn.grid(row=2, column=4, columnspan=2)
        self.weapon_btn['command'] = self.get_weapon_menu

        # Create buttons based on options.py
        for option_name in self.options:
            # SPECIAL has its own popup menu, IGNORE obviously ignoring
            if option_name in (*SPECIAL, *IGNORE):
                continue

            self.create_button(option_name=option_name)
        
    def get_special_menu(self, *args):
        """Summons popup to change special options like blood, aquasheep, etc."""
        # See if special_menu is already open
        try:
            self.special_menu.focus_set()
        except AttributeError:
            special_menu = tk.Toplevel(self)
            special_menu.title("Special")
            self.special_menu = special_menu # stop garbage collection

            def cancel(*args):
                    special_menu.destroy()
                    delattr(self, 'special_menu')
            
            # If user leaves window without setting value, just destroy the popup
            special_menu.protocol('WM_DELETE_WINDOW', cancel)
            special_menu.bind("<Escape>", cancel)
            special_menu.bind("<Return>", cancel)

            for option in SPECIAL:
                self.create_button(option_name=option)

    def get_weapon_menu(self, *args):
        """Summons popup to change weapons options."""
        # See if weapon_menu is already open
        try:
            self.weapon_menu.focus_set()
        except AttributeError:
            weapon_menu = tk.Toplevel(self)
            weapon_menu.title("Weapons")
            self.weapon_menu = weapon_menu # stop garbage collection

            def cancel(*args):
                weapon_menu.destroy()
                delattr(self, 'weapon_menu')
            
            # If user leaves window without setting value, just destroy the popup
            weapon_menu.protocol('WM_DELETE_WINDOW', cancel)
            weapon_menu.bind("<Escape>", cancel)
            weapon_menu.bind("<Return>", cancel)

            # Seeing if we should display special weapons or not
            if self.options['Super Weapons']['var'].get() == True:
                weapons_dict = {**WEAPONS, **SUPER_WEAPONS}
            else:
                weapons_dict = WEAPONS

            for i, weapon_name in enumerate(weapons_dict):
                pos = {
                    'row': math.floor(i / 8),
                    'column': i % 8
                }
                self.create_button(option_name=weapon_name, pos=pos)

    def get_weapon_popup(self, weapon_name):
        def exit_popup(*args):
            print(f"{weapon_name}: Ammo: {weapon['Ammo'].get()}")
            self.weapon_popup.destroy()
            delattr(self, 'weapon_popup')

        try:
            self.weapon_popup
            exit_popup()
        except Exception:
            pass
        
        weapon_popup = tk.Toplevel(self.weapon_menu)
        weapon_popup.title(weapon_name)
        self.weapon_popup = weapon_popup
        
        # If user leaves window without setting value, just destroy the popup
        weapon_popup.protocol('WM_DELETE_WINDOW', exit_popup)
        weapon_popup.bind("<Escape>", exit_popup)

        if weapon_name in WEAPONS:
            weapon = self.weapons[weapon_name]
        elif weapon_name in SUPER_WEAPONS:
            weapon = self.super_weapons[weapon_name]

        tk.Label(weapon_popup, text='Ammo:').grid(row=0, column=0)
        tk.Entry(weapon_popup, textvariable=weapon['Ammo']).grid(row=0, column=1)

        tk.Label(weapon_popup, text='Crate Probability:').grid(row=1, column=0)
        tk.Entry(weapon_popup, textvariable=weapon['Crate Probability']).grid(row=1, column=1)

        tk.Label(weapon_popup, text='Delay:').grid(row=2, column=0)
        tk.Entry(weapon_popup, textvariable=weapon['Delay']).grid(row=2, column=1)

        tk.Label(weapon_popup, text='Power:').grid(row=3, column=0)
        tk.Entry(weapon_popup, textvariable=weapon['Power']).grid(row=3, column=1)

    def display_help_text(self, option_name, event):
        if option_name in (*WEAPONS, *SUPER_WEAPONS):
            help_text = option_name
        else:
            help_text = f"{option_name}: {self.options[option_name]['var'].get()}"
        self.help_text.set(help_text)

    def hide_help_text(self, event):
        self.help_text.set(self.default_help_text)

    def get_option_popup(event, self, option_name):
        """Callback that updates tkinter variable associated with `option_name`
        
        Parameters
        ----------
        event: tkinter event (i.e. clicked button/image)
        self: GUI object
            Has to go after event since this func is a callback
        option_name: str
            The name of the option that we're changing (i.e. "Automatic Replays")
        
        """
        # Get reference to option in dictionary for easier reading
        option = self.options[option_name]

        var = option['var']
        if type(var.get()) != int: # Doesn't require numerical input, change button
            values = option['Values_Images']

            # Wrap around index if reached end of list
            index = self.get_index(option=option, var=var)
            next_index = (index + 1) % len(values)
            next_raw, next_var, next_imgpath = values[next_index]

            # Update state
            var.set(next_var)

            # Update graphics
            next_image = get_bitmap(*next_imgpath)
            option['button']['image'] = next_image
            option['button'].image = next_image # Required for when image changes so garbage collect doesn't delete it
            self.change_text.set(f"{option_name} set to {option['var'].get()}")
            self.display_help_text(option_name=option_name, event=None)
        elif type(var.get()) == int: # Numerical input required, set popup
            try:
                # Don't make another window if we already have one
                self.popup.entry.focus_set()
            except AttributeError:
                popup = tk.Toplevel(self)
                self.popup = popup # Keep track of it so we don't create another window
                popup.title(f'Setting {option_name}')
                
                def cancel(*args):
                    popup.destroy()
                    delattr(self, 'popup')

                # If user leaves window without setting value, just destroy the popup
                popup.protocol('WM_DELETE_WINDOW', cancel)
                popup.bind("<Escape>", cancel)

                note = option['Special Note']
                tk.Label(popup, text=note).pack(side='top')
                popup.entry = tk.Entry(popup, textvariable=var)
                popup.entry.pack(side='top')
                popup.entry.selection_range(0, tk.END)
                popup.entry.icursor(tk.END)
                popup.entry.focus_set()

                def confirm(*args):
                    popup.destroy()
                    self.change_text.set(f"{option_name} set to {var.get()}")
                    self.display_help_text(option_name=option_name, event=None)
                    delattr(self, 'popup')

                # If user presses enter or confirm button
                popup.bind("<Return>", confirm)
                tk.Button(popup, text='Confirm', fg='green',
                    command=confirm).pack(side='top')
                
# root = tk.Tk()
# root.title("Worms Armageddon: Scheme Editor")
# gui = GUI(master=root)
# gui.mainloop()

# pprint(read_scheme('{{02}} Intermediate.wsc'))
pprint(read_scheme('test.wsc'))
