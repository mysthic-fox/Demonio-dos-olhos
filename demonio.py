import os
from colorama import Fore, Style, init

# Inicialização
init(autoreset=True)
ROXO = Fore.MAGENTA + Style.BRIGHT
BRANCO = Fore.WHITE
RESET = Style.RESET_ALL

def banner():
    # O os.system('clear') garante que tudo antes seja limpo
    os.system('clear')
    print(ROXO + """
    ██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗██╗ ██████╗ 
    ██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║██║██╔═══██╗
    ██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║██║██║   ██║
    ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║██║██║   ██║
    ██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║╚██████╔╝
    ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ 
    """)
    # Saudação personalizada removendo o 'Mod fatal'
    print(BRANCO + "Quem gostaria que eu conceda a visão, mestre CM_FX?\n")

def main():
    # Limpa a tela imediatamente ao iniciar
    os.system('clear')
    
    while True:
        banner()
        print(f"{ROXO}[1] Caçar Social [2] Rastrear IP [3] Ver Histórico [0] Sair")
        opt = input(f"{ROXO}>> ")
        
        # ... resto do seu código ...
