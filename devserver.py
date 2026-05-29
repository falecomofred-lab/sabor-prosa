import socket
import webbrowser
import threading
import time


def encontrar_porta_livre(inicio=5000, fim=5100):
    for porta in range(inicio, fim):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", porta))
                return porta
            except OSError:
                continue

    raise RuntimeError("Nenhuma porta livre encontrada")


def abrir_navegador(porta):
    def _abrir():
        time.sleep(1.5)
        webbrowser.open(f"http://127.0.0.1:{porta}")

    threading.Thread(target=_abrir).start()