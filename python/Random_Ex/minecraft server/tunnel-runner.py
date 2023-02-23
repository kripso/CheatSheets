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

nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=NEXTCLOUD_USERNAME, password=NEXTCLOUD_PASSWORD)
mods = nxc.list_folders('/458ca755-495d-40e2-9cc9-437a9389e244/mods', depth=1, all_properties=True)
datapacks = nxc.list_folders('/458ca755-495d-40e2-9cc9-437a9389e244/datapacks', depth=1, all_properties=True)


def file_diff_download(path: str, nxt_files) -> None:
    os.makedirs(f'{MINECRAFT_PATH}/{path}', exist_ok=True)
    os.chdir(f'{MINECRAFT_PATH}/{path}')

    active_files = {re.split(r'\d?\W\d', item)[0]: item for item in os.listdir()}

    for file in nxt_files.data:
        if not file.href.endswith(f'/{path}/'):
            try:
                active_file = file.href.replace(f'{WEBDAV_PREFIX}/minecraft/{SERVER_NAME}/{path}/', '')
                file_name = re.split(r'\d?\W\d', active_file)[0]
                if file_name in active_files.keys() and active_file != active_files[file_name]:
                    os.remove(active_files[file_name])
                    print(f'{active_file} -> removed')
                print(active_file, end = ' -> ')
                file.download()
                print('downloaded')
            except Exception as err:
                print(err)
    os.chdir(ACTIVE_DIR)


print()
print('-'*25, 'checking mods', '-'*25)
print()
if mods.is_ok:
    file_diff_download('mods', mods)
else:
    print('download mods manualy at: https://nextcloud.kripso-world.com/s/KnTY3RR9J98QWq5')


print()
print('-'*25, 'checking datapacks', '-'*25)
print()
if datapacks.is_ok:
    file_diff_download('datapacks', datapacks)
else:
    print('download datapacks manualy at: https://nextcloud.kripso-world.com/s/KnTY3RR9J98QWq5')


#
# Tunnels
#
print()
print('-'*25, 'routing tunnels', '-'*25)
print()

commands = [
    f'cmd /c "{ACTIVE_DIR}/cloudflared.exe" access tcp --hostname minecraft-server.kripso-world.com --url localhost:23423',
    f'cmd /c "{ACTIVE_DIR}/cloudflared.exe" access tcp --hostname minecraft-modded.kripso-world.com --url localhost:23424',
]

procs = [ subprocess.Popen(command, shell=True) for command in commands ]

for p in procs:
   p.wait()