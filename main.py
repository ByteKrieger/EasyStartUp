import subprocess
import os
import tempfile
from rich.console import Console
from rich.table import Table
from time import sleep
from art import *
console = Console()
from tkinter import *
import webbrowser

table = Table(title="Hinweise: ")
table.add_column('Nr: ', style='blue')
table.add_column('Aufgaben: ', style='bold blue')
table.add_row('0', 'Tool schließen')
table.add_row('1', 'Reboot in Sec')
table.add_row('2', 'Herunterfahren abbrechen')
table.add_row('3', 'Herunterfahren in Sec')
table.add_row('4', 'Sofortiger Neustart ins BIOS')
table.add_row('5', 'Sofortiger Neustart ins Windows Menu')
table.add_row('6', 'Sofortiges Herunterfahren (force)')
table.add_row('7', 'Sofortiges Herunterfahren (soft)')

batch_script_lines = [
    '@echo off',
    'if "%2" == "firstrun" exit',
    'cmd /c "%0" null firstrun',
    'if "%1" == "skipuac" goto skipuacstart',
    ':checkPrivileges',
    'NET FILE 1>NUL 2>NUL',
    'if "%errorlevel%" == "0" ( goto gotPrivileges ) else ( goto getPrivileges )',
    ':getPrivileges',
    'if "%1" == "ELEV" (shift & goto gotPrivileges)',
    'setlocal DisableDelayedExpansion',
    'set "batchPath=%~0"',
    'setlocal EnableDelayedExpansion',
    'ECHO Set UAC = CreateObject^("Shell.Application"^) > "%temp%\\OEgetPrivileges.vbs"',
    'ECHO UAC.ShellExecute "!batchPath!", "ELEV", "", "runas", 1 >> "%temp%\\OEgetPrivileges.vbs"',
    '"%temp%\\OEgetPrivileges.vbs"',
    'exit /B',
    ':gotPrivileges',
    'setlocal & pushd .',
    'cd /d %~dp0',
    'cmd /c "%0" skipuac firstrun',
    'cd /d %~dp0',
    ':skipuacstart',
    'if "%2" == "firstrun" exit',
    'shutdown -r -fw',
    'pause'
]

eingabe = 99

while True:
    try:
        os.system('cls')
        hallo = text2art('Easy Start Up Menu')
        print(hallo)

        try:
            console.print(table)
            eingabe = int(input("Bitte Wählen: "))
        except ValueError:
            console.print("Eingabe fehlerhaft. Nochmals als Int. eingeben!", style='red bold underline')
            sleep(2)
            continue
        except:
            console.print('Unbekannter Fehler in Eingabe', style='red bold underline')

        if eingabe == 1:
            try:
                timer = int(input("Eingabe der Zeit: "))
                subprocess.call(f'shutdown -g -t {timer}')
                console.print(f'Das System startet sich in {timer} Sekunden neu.', style='green')
                sleep(3)
                continue
            except ValueError:
                console.print('Ungültiger Eingabewert in Option 1', style='red bold underline')
                sleep(3)
            except:
                console.print('Unbekannter Fehler in Option 1', style='red bold underline')
                sleep(3)
                continue

        elif eingabe == 2:
            try:
                subprocess.call(f'shutdown -a')
                sleep(1)
                continue
            except subprocess.CalledProcessError:
                console.print('Subprozess Fehler Option 2', style='red bold underline')
                sleep(3)
                continue
            except:
                console.print("Fehler", style='red bold underline')
                sleep(3)
                continue

        elif eingabe == 3:
            try:
                timer = int(input("Eingabe der Zeit: "))
                subprocess.call(f'shutdown -s -t {timer}')
                console.print(f'Das System schaltet sich in {timer} Sekunden ab.', style='green')
                sleep(3)
                continue
            except subprocess.CalledProcessError:
                console.print('Subprozess Fehler Option 3', style='red bold underline')
                sleep(3)
                continue

        elif eingabe == 4:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bat') as temp_file:
                for line in batch_script_lines:
                    temp_file.write(line + '\n')
                    temp_file.flush()
                    continue
            try:
                subprocess.run(temp_file.name, shell=True)
                sleep(3)
                continue
            except:
                console.print('Fehler: BIOS Reboot!', style='red bold underline')
                sleep(3)
                continue

        elif eingabe == 5:
            try:
                subprocess.call('shutdown.exe /r /o /f /t 00')
                console.print('STARTE ABGESICHERTEN MODUS...', style='red')
            except subprocess.CalledProcessError:
                console.print('Subprozess Fehler Option 5', style='red bold underline')
                sleep(3)
                continue
                
        elif eingabe == 6:
            try:
                subprocess.call('shutdown.exe /s /f /t 00')
            except subprocess.CalledProcessError:
                console.print('Subprozess Fehler Option 6', style='red bold underline')
                sleep(3)
                continue
                
        elif eingabe == 7:
            try:
                subprocess.call('shutdown.exe /s /soft /t 00')
            except subprocess.CalledProcessError:
                console.print('Subprozess Fehler Option 7', style='red bold underline')
                sleep(3)
                continue
                
        elif eingabe == 0:
            console.print('Danke für Ihre Nutzung meines EasyStartUp Menu.', style='green bold underline')
            sleep(3)
            break 

        else:
            console.print('END oder ERROR', style='red bold underline')

    except KeyboardInterrupt:
        break

    except:
        continue

sleep(5)
webbrowser.open_new('https://bytekrieger.de')
