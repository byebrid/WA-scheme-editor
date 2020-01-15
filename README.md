# Worms Armageddon Scheme Editor
Notes
-----
- If I need to repackage this into a single 'application', I just need to run this command due to pyinstaller sucking a little:

    ```pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' scheme_editor.py```
