import cx_Freeze

executables = [cx_Freeze.Executable('main_interface.py', base="Win32GUI")]
excludes = []

cx_Freeze.setup(
    name="Chess",
    options={"build_exe":
                 {'include_msvcr': True,
                  "packages": ["PyQt5", "PIL"],
                  "zip_include_packages": ["PyQt5_sip", 'sqlite3', 'datetime'],
                  "include_files": ['green/', 'saves/', 'sprites/', 'music/',
                                    'images/', 'backgrounds/', 'requirements.txt', 'datebase.db',
                                    'chess_back.py', 'painting.py',
                                    'stylesheets.py', 'ui_forms.py'],
                  "excludes": excludes}},
    executables=executables
)