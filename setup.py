import sys
import os
from cx_Freeze import setup, Executable


os.environ['TCL_LIBRARY'] = 'C:/Python/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Python/tcl/tk8.6'
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = dict(
    includes = ["idna.idnadata"],
    packages = ["tkinter", "numpy", "pandas", "pandas_datareader"],
    excludes = [],
    include_files = ['c:/Python/DLLs/tcl86t.dll', 'c:/Python/DLLs/tk86t.dll'])

base = None
if sys.platform == "win32":
    base = "Win32GUI"

# GUI applications require a different base on Windows (the default is for a
# console application).    
setup(name = 'HistoricalPricingApp',
      version = '0.1',
      options = {"build_exe": build_exe_options},
      description = 'Research equity prices and import to excel.',
      executables = [Executable("historical_pricing_app.py")])
