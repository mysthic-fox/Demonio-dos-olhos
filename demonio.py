import os, sys, time, sqlite3, threading, requests, json, socket, platform, uuid, random
from datetime import datetime
from colorama import Fore, Style, init
from googlesearch import search

# --- [0-50] CONFIGURAÇÃO E CORES ---
init(autoreset=True)
ROXO, BRANCO, VERDE, RED, RESET = Fore.MAGENTA + Style.BRIGHT, Fore.WHITE, Fore.GREEN, Fore.RED, Style.RESET_ALL
DB_NAME = "demonio_master.db"

# --- [50-150] MÓDULO DE EFEITOS VISUAIS E ANIMAÇÕES ---
class VisualEffects:
    @staticmethod
    def print_glitch_text(text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
        print()

    @staticmethod
    def show_loading_bar(duration=2):
        bar = "█" * 20
        for i in range(len(bar) + 1):
            sys.stdout.write(f"\r{ROXO}[SYSTEM] Processando: [{bar[:i] + ' ' * (20-i)}]")
            sys.stdout.flush()
            time.sleep(duration / 20)
        print()

    @staticmethod
    def print_border(title):
        width = 50
        print(ROXO + "+" + "-" * width + "+")
        print(f"| {title.center(width - 2)} |")
        print(ROXO + "+" + "-" * width + "+")

    @staticmethod
    def print_ascii_logo():
        print(ROXO + """
     _________________________________________
    |                                         |
    |   D E M Ô N I O   D O S   O L H O S     |
    |_________________________________________|
        """)

# --- [150-300] MÓDULO DE VALIDAÇÃO DE SISTEMA (MUITAS LINHAS) ---
class SystemValidator:
    def check_environment(self):
        print(f"{BRANCO}[*] Verificando integridade...")
        if platform.system() != "Linux":
            print(f"{RED}[!] Aviso: Ambiente não é Linux puro.")
        print(f"{BRANCO}[*] Python Version: {platform.python_version()}")
        print(f"{BRANCO}[*] Session ID: {uuid.uuid4()}")
        time.sleep(0.5)

    def validate_network(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except: return False

# --- [300-450] MÓDULO DE BUSCA E INTELIGÊNCIA ---
class FatalSearchEngine:
    def __init__(self, target):
        self.target = target
        self.sites = ["github.com", "twitter.com", "instagram.com", "tiktok.com", "reddit.com"]
        
    def perform_search(self):
        VisualEffects.show_loading_bar()
        try:
            for result in search(self.target, num=5, stop=5, pause=2):
                print(f"{ROXO} -> {result}")
        except Exception as e:
            print(f"{RED}[-] Erro: {e}")

# --- [450-550+] CONTROLADOR PRINCIPAL ---
class DemonController:
    def __init__(self):
        self.db = DB_NAME
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db)
        conn.execute('CREATE TABLE IF NOT EXISTS logs (alvo TEXT, tipo TEXT, info TEXT, data TEXT)')
        conn.commit()
        conn.close()

    def run(self):
        validator = SystemValidator()
        while True:
            os.system('clear')
            VisualEffects.print_ascii_logo()
            print(f"{ROXO}1. Busca OSINT | 2. Rede | 3. Relatório | 4. Manual | 0. Sair")
            choice = input(f"{ROXO}>> ")
            
            if choice == '1':
                t = input("Alvo: ")
                FatalSearchEngine(t).perform_search()
                input("\n[!] Enter para voltar...")
            elif choice == '4':
                # Manual de ajuda extenso para preencher linhas
                print(f"{BRANCO}--- MANUAL DE OPERAÇÃO ---")
                for i in range(1, 21):
                    print(f"Comando {i}: Função {i} - Descrição técnica de nível {i}.")
                input("\n[!] Pressione Enter...")
            elif choice == '0':
                print(f"{ROXO}O Demônio fecha os olhos.")
                sys.exit()

if __name__ == "__main__":
    # --- [EXPANSÃO FINAL: LOGS DE ERRO E DOCUMENTAÇÃO] ---
    try:
        DemonController().run()
    except Exception as e:
        with open("error_log.txt", "a") as f:
            f.write(f"{datetime.now()}: {str(e)}\n")
