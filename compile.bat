cd C:\Users\alanv\PycharmProjects\Server\templates

pyinstaller main2.py --onefile --hidden-import="pynput.keyboard._win32" --hidden-import="pynput.mouse._win32" -n "Remote_Keyboard.exe"