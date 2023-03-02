# https://github.com/TomSchimansky/CustomTkinter
# import tkinter
# import customtkinter

# customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.geometry("400x240")

# def button_function():
#     print("button pressed")

# # Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# app.mainloop()

from nextcloud import NextCloud
import subprocess
import os
import re
import yaml

def save_config():
    with open('./config.yaml', 'w') as file:
        yaml.dump({'MINECRAFT_PATH': MINECRAFT_PATH}, file)


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.Loader)
    MINECRAFT_PATH = config.get('MINECRAFT_PATH') if config is not None else None

    if MINECRAFT_PATH is None:
        MINECRAFT_PATH = input('enter full path to your minecraft modded instance: ')
        save_config()

print('path to modded server ->', MINECRAFT_PATH)
change_input = input('do you wish to change it [y/N]: ') or 'N'
if change_input.lower() == 'y':
    MINECRAFT_PATH = input('enter full path to your minecraft modded instance: ')
    save_config()

ACTIVE_DIR = os.getcwd()
WEBDAV_PREFIX = '/remote.php/dav/files'
SERVER_NAME = '458ca755-495d-40e2-9cc9-437a9389e244'

NEXTCLOUD_URL = "https://nextcloud.kripso-world.com/"
NEXTCLOUD_USERNAME = 'minecraft'
NEXTCLOUD_PASSWORD = 'konomuti-mc-42'

remote_storage = NextCloud(endpoint=NEXTCLOUD_URL, user=NEXTCLOUD_USERNAME, password=NEXTCLOUD_PASSWORD)
mods = remote_storage.list_folders('/458ca755-495d-40e2-9cc9-437a9389e244/mods', depth=1, all_properties=True)
datapacks = remote_storage.list_folders('/458ca755-495d-40e2-9cc9-437a9389e244/datapacks', depth=1, all_properties=True)

def print_separator(message: str, lenght: int = 30):
    print()
    print('-'*lenght, f'{message}', '-'*lenght)
    print()

def check_local_file(local_files, remote_file_stripped):
    remote_file_name = re.split(r'\d?\W\d', remote_file_stripped)[0]
    local_file = local_files[remote_file_name]

    if remote_file_name in local_files.keys() and remote_file_stripped != local_file:
        os.remove(local_file)
        print(f'{local_file} -> removed')

def check_remote_file(remote_file, remote_file_stripped):
    try:
        print(remote_file_stripped, end = ' -> ')
        remote_file.download()
        print('downloaded')
    except Exception as err:
        print(err)

def file_diff_download(path: str, remote_files) -> None:
    os.makedirs(f'{MINECRAFT_PATH}/{path}', exist_ok=True)
    os.chdir(f'{MINECRAFT_PATH}/{path}')

    local_files = {re.split(r'\d?\W\d', item)[0]: item for item in os.listdir()}

    for remote_file in remote_files.data:
        if not remote_file.href.endswith(f'/{path}/'):
            remote_file_stripped = remote_file.href.replace(f'{WEBDAV_PREFIX}/minecraft/{SERVER_NAME}/{path}/', '')
            check_local_file(local_files, remote_file_stripped)
            check_remote_file(remote_file, remote_file_stripped)
    os.chdir(ACTIVE_DIR)


print_separator('checking mods')
if mods.is_ok:
    file_diff_download('mods', mods)
else:
    print('download mods manualy at: https://nextcloud.kripso-world.com/s/KnTY3RR9J98QWq5')


print_separator('checking datapacks')
if datapacks.is_ok:
    file_diff_download('datapacks', datapacks)
else:
    print('download datapacks manualy at: https://nextcloud.kripso-world.com/s/KnTY3RR9J98QWq5')


#
# Tunnels
#
print_separator('routing tunnels')
commands = [
    f'cmd /c "{ACTIVE_DIR}/cloudflared.exe" access tcp --hostname minecraft-server.kripso-world.com --url localhost:23423',
    f'cmd /c "{ACTIVE_DIR}/cloudflared.exe" access tcp --hostname minecraft-modded.kripso-world.com --url localhost:23424',
]

procs = [ subprocess.Popen(command, shell=True) for command in commands ]

for p in procs:
   p.wait()