import os
import sys
import time
import sqlite3
import threading
import requests
import socket
from datetime import datetime
from colorama import Fore, Style, init

# Inicialização visual
init(autoreset=True)
ROXO = Fore.MAGENTA + Style.BRIGHT
BRANCO = Fore.WHITE
RED = Fore.RED
RESET = Style.RESET_ALL
DB_NAME = "demonio.db"

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS logs (alvo TEXT, tipo TEXT, info TEXT, data TEXT)')
    conn.commit()
    conn.close()

def log(alvo, tipo, info):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?,?,?,?)", (alvo, tipo, info, timestamp))
    conn.commit()
    conn.close()

# --- CLASSES DE MÓDULOS ---
class Engine:
    def __init__(self, target):
        self.target = target
        self.sites = ["github", "twitter", "instagram", "tiktok", "reddit", "twitch", "pinterest", "flickr", "steam", "telegram"]

    def social_scan(self):
        print(f"{ROXO}[*] Iniciando caça social...")
        for s in self.sites:
            try:
                url = f"https://{s}.com/{self.target}"
                r = requests.get(url, timeout=3)
                if r.status_code == 200:
                    print(f"{ROXO}[+] ENCONTRADO: {url}")
                    log(self.target, "SOCIAL", url)
            except: pass

class NetScanner:
    @staticmethod
    def ip_recon(target):
        try:
            ip = socket.gethostbyname(target)
            print(f"{ROXO}[*] IP resolvido: {ip}")
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()
            if data['status'] == 'success':
                res = f"Cidade: {data['city']}, Pais: {data['country']}"
                print(f"{ROXO}[+] Geo: {res}")
                log(target, "GEO", res)
        except Exception as e:
            print(f"{RED}[!] Erro de rede: {e}")

# --- INTERFACE ---
def banner():
    os.system('clear')
    print(ROXO + """
    ██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗██╗ ██████╗ 
    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║██║██╔═══██╗
    ██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║██║██║   ██║
    ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║   ██║
    ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║╚██████╔╝
    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚════██╗
    """)
    print(BRANCO + "Quem gostaria que eu conceda a visão, mestre CM_FX?\n")

def main():
    init_db()
    while True:
        banner()
        print(f"{ROXO}[1] Caça Social | [2] Rastrear IP/Host | [3] Ver Histórico | [0] Sair")
        opt = input(f"{ROXO}>> ")
        
        if opt == '1':
            target = input(f"{ROXO}Username: ")
            Engine(target).social_scan()
            input(f"\n{BRANCO}Enter para continuar...")
        elif opt == '2':
            target = input(f"{ROXO}Host (ex: google.com): ")
            NetScanner.ip_recon(target)
            input(f"\n{BRANCO}Enter para continuar...")
        elif opt == '3':
            conn = sqlite3.connect(DB_NAME)
            for row in conn.execute("SELECT * FROM logs"):
                print(row)
            conn.close()
            input(f"\n{BRANCO}Enter para continuar...")
        elif opt == '0':
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
