import threading
class Banco:
    def __init__(self,saldo_inicial):
            self.saldo=saldo_inicial
            self.lock=threading.Lock
    def ingresar(self,cantidad):
        with self.lock:
            self.saldo+=cantidad
    def retirar(self,cantidad):
        with self.lock:
            self.saldo-=cantidad
    def get_saldo(self):
        with self.lock:
            return self.saldo
        
        
        
    