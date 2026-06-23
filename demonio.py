import os
import sys
import time
import sqlite3
import threading
import requests
import json
import socket
from datetime import datetime
from colorama import Fore, Style, init

# --- CONFIGURAÇÃO E CORES ---
init(autoreset=True)
ROXO = Fore.MAGENTA + Style.BRIGHT
BRANCO = Fore.WHITE
RED = Fore.RED
RESET = Style.RESET_ALL
DB_NAME = "demonio.db"

# --- BANCO DE DADOS E LOGS ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY, alvo TEXT, tipo TEXT, info TEXT, data TEXT)''')
    conn.commit()
    conn.close()

def log(alvo, tipo, info):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO logs (alvo, tipo, info, data) VALUES (?, ?, ?, ?)", 
              (alvo, tipo, info, timestamp))
    conn.commit()
    conn.close()

# --- CLASSES DE MÓDULOS (EXPANSÃO DE CÓDIGO) ---

class NetworkScanner:
    """Módulo para análise de infraestrutura e alvos de rede"""
    def __init__(self, target):
        self.target = target
        
    def get_dns_info(self):
        print(f"{ROXO}[*] Resolvendo DNS de: {self.target}")
        try:
            ip = socket.gethostbyname(self.target)
            print(f"{ROXO}[+] IP Resolvido: {ip}")
            log(self.target, "DNS", ip)
        except Exception as e:
            print(f"{RED}[-] Falha no DNS: {e}")

class SocialEngine:
    def __init__(self, target):
        self.target = target
        self.sites = ["github", "twitter", "instagram", "tiktok", "reddit", "twitch", "pinterest", "flickr", "steam"]

    def worker(self, site):
        url = f"https://{site}.com/{self.target}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"{ROXO}[+] ENCONTRADO: {url}")
                log(self.target, "SOCIAL", url)
        except: pass

    def hunt(self):
        threads = []
        for site in self.sites:
            t = threading.Thread(target=self.worker, args=(site,))
            threads.append(t)
            t.start()
        for t in threads: t.join()

class DorkEngine:
    """Motor de busca profunda (OSINT Dorking)"""
    def __init__(self, target):
        self.target = target
        self.patterns = ["intext:{}", "filetype:pdf {}", "site:pastebin.com {}", "intitle:index of {}"]

    def run(self):
        for p in self.patterns:
            query = p.format(self.target)
            print(f"{ROXO}[...] Varrendo dorks: {query}")
            time.sleep(1) # Delay anti-ban

# --- ENGINE DE RELATÓRIO ---
def exportar_relatorio():
    print(f"{ROXO}[!] Gerando relatorio em JSON...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    
    with open("report.json", "w") as f:
        json.dump(rows, f, indent=4)
    print(f"{ROXO}[+] Relatório salvo como report.json")
    conn.close()

# --- FUNÇÕES DE SISTEMA ---
def banner():
    print(ROXO + """
    ██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗██╗ ██████╗ 
    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║██║██╔═══██╗
    ██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║██║██║   ██║
    ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║   ██║
    ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║╚██████╔╝
    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚════██╗
    """)
    print(BRANCO + "Quem gostaria que eu conceda a visão, mestre CM_FX?\n")

# --- MAIN LOOP (CONTROLE TOTAL) ---
def main():
    init_db()
    os.system('clear')
    banner()
    
    while True:
        print(f"\n{ROXO}1. Social | 2. Rede | 3. Dorks | 4. Exportar | 5. Histórico | 0. Sair")
        opt = input(f"{ROXO}>> ")
        
        if opt == '1':
            target = input("Username: ")
            SocialEngine(target).hunt()
        elif opt == '2':
            target = input("Alvo (ex: google.com): ")
            NetworkScanner(target).get_dns_info()
        elif opt == '3':
            target = input("Alvo Dork: ")
            DorkEngine(target).run()
        elif opt == '4':
            exportar_relatorio()
        elif opt == '5':
            conn = sqlite3.connect(DB_NAME)
            for row in conn.execute("SELECT * FROM logs"):
                print(row)
            conn.close()
        elif opt == '0':
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] O Demônio encerra a conexão.")
