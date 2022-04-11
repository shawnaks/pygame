import cx_Freeze

executables = [cx_Freeze.Executable("pong.py")]

cx_Freeze.setup(
    name="Pong",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["001-ping-pong.png", "ping-pong.png"]}},
    executables = executables

    )