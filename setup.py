import cx_Freeze

build_exe_options = {
'include_msvcr': True,
"excludes": ["unittest"],
    "zip_include_packages": ["encodings"]
}

exe = [cx_Freeze.Executable('corrigir_socpar_ecd.py',
                            base = 'Win32GUI',
                            target_name = 'corrigir_socpar_ecd.exe')]

cx_Freeze.setup(name = 'corrigir_socpar_ecd',
                options = {'build_exe': build_exe_options},
                executables = exe
)