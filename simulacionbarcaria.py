import multiprocessing

class Cuenta:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
    
    def ingresar(self, cantidad):
        self.saldo += cantidad
    
    def retirar(self, cantidad):
        if self.saldo >= cantidad:
            self.saldo -= cantidad
    
def proceso_ingresar(cantidad):
    cuenta.ingresar(cantidad)

def proceso_retirar(cantidad):
    cuenta.retirar(cantidad)

if __name__ == '__main__':
    cuenta = Cuenta(100)
    with multiprocessing.Pool(processes=4) as pool:
        # Crear procesos para ingresos
        for i in range(40):
            pool.apply_async(proceso_ingresar, args=(100,))
        for i in range(20):
            pool.apply_async(proceso_ingresar, args=(50,))
        for i in range(60):
            pool.apply_async(proceso_ingresar, args=(20,))
        
        # Crear procesos para retiros
        for i in range(40):
            pool.apply_async(proceso_retirar, args=(100,))
        for i in range(20):
            pool.apply_async(proceso_retirar, args=(50,))
        for i in range(60):
            pool.apply_async(proceso_retirar, args=(20,))
        
        # Esperar a que todos los procesos terminen
        pool.close()
        pool.join()
    
    # Comprobar el saldo final
    saldo_final = cuenta.saldo
    if saldo_final == 100:
        print("El saldo final es correcto: ", saldo_final)
    else:
        print("El saldo final es incorrecto: ", saldo_final)
