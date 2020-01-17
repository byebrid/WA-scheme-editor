# Worms Armageddon Scheme Editor
This is a relatively simple Worms Armageddon scheme editor, built using Python.

Key features
------------
- You can load schemes (stored as .wsc files) into the editor if you want to start with a template.
- You can edit schemes by clicking on the tiles, (designed to somewhat mirror the in-game editor) and adjusting values as required.
- You can save your scheme into a .wsc file, ready to be played!

How to install
--------------
If you're unfamiliar with github (the website you're on), you can simply click on the *Clone or download* button at the top of the home page (click the *Code* tab near the top to get to the home page). You can then download this a zip file, and double-click once it is downloaded to extract it. 

How to run
----------
If you know how to make a virtual environment, I would suggest doing so. Otherwise go to your command line and navigate to the directory of this scheme editor. Then type in the following:
```
pip install --upgrade pip
pip install -r requirements.txt
python scheme_editor.py
```
This was only tested on macOS Catalina, using python3, so results may vary on windows, etc.

How to use
----------
- Install and run the scheme editor using the instructions above.
- Load a .wsc file using the *Load scheme* button if you wish (maybe if you only want to slightly modify a pre-existing scheme).
- Hover over buttons to see what they are for. Click on them to change their values (or open up another menu).
- Once you are happy with the options, you can save your scheme by clicking the *Save scheme* button on the main window.
- Once you have saved your scheme, simpy move/copy it into the game's scheme folder found at: *Worms Armageddon/User/Schemes*. 

If you've downloaded the game from steam, you can find the *Worms Aramageddon* folder by right-clicking on its name in your steam library and clicking the *Local Files* option.

Limitations
-----------
Some options have quite unintuitive behaviours and I haven't yet bothered trying to account for this to make it easier on the user. I would suggest you read [Changing Options](docs/Changing%20Options.md) to get a better idea of what numbers you should be putting in for desired results.

Developer Note on bundling
--------------------------
- If I need to repackage this into a single 'application' (on my mac), I just need to run this command due to pyinstaller sucking a little:
    ```
    pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' scheme_editor.py
    ```
