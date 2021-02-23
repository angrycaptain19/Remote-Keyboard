pyinstaller ./main.py --onefile --hidden-import="pynput.keyboard._win32" ^
--hidden-import="pynput.mouse._win32" -n "Remote_Keyboard.exe" ^
--add-data "./templates/HTML.html;./templates" ^
--add-data "./templates/css/style.css;./templates/css" ^
--add-data "./templates/js/script.js;./templates/js" ^
--add-data "./Instructions.txt;." ^
--hidden-import "./Handler.py"

copy .\dist\Remote_Keyboard.exe C:\Users\alanv\PycharmProjects\Original\Executable /Y