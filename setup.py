from cx_Freeze import setup, Executable
import sys
import os
os.environ['TCL_LIBRARY'] = "C:\\Users\\ysyoon\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\ysyoon\\AppData\\Local\\Programs\\Python\\Python37-32\\tcl\\tk8.6"

build_exe_options= dict(packages = ["blpapi","pybbg","numpy","pandas","cx_oracle"],
	excludes = [])

base = None



setup(
    name='Bloomberg Application',
    version = '0.1',
    author = "hsYun",
    description = "BloombergProject",
    options={"build_exe": build_exe_options},
    executables=[Executable("bloomberg_beta.py", base=base, targetName="bloomberg_beta.exe")]
)


