import multiprocessing

class Cuenta:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
    
    def ingresar(self, cantidad):
        self.saldo += cantidad
    
    def retirar(self, cantidad):
        if self.saldo >= cantidad:
            self.saldo -= cantidad
    
def proceso_ingresar(cuenta, cantidad):
    cuenta.ingresar(cantidad)

def proceso_retirar(cuenta, cantidad):
    cuenta.retirar(cantidad)

if __name__ == '__main__':
    cuenta = Cuenta(100)
    procesos = []
    
    # Crear procesos para ingresos
    for i in range(40):
        procesos.append(multiprocessing.Process(target=proceso_ingresar, args=(cuenta, 100)))
    for i in range(20):
        procesos.append(multiprocessing.Process(target=proceso_ingresar, args=(cuenta, 50)))
    for i in range(60):
        procesos.append(multiprocessing.Process(target=proceso_ingresar, args=(cuenta, 20)))
    
    # Crear procesos para retiros
    for i in range(40):
        procesos.append(multiprocessing.Process(target=proceso_retirar, args=(cuenta, 100)))
    for i in range(20):
        procesos.append(multiprocessing.Process(target=proceso_retirar, args=(cuenta, 50)))
    for i in range(60):
        procesos.append(multiprocessing.Process(target=proceso_retirar, args=(cuenta, 20)))
    
    # Iniciar todos los procesos
    for proceso in procesos:
        proceso.start()
    
    # Esperar a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()
    
    # Comprobar el saldo final
    saldo_final = cuenta.saldo
    if saldo_final == 100:
        print("El saldo final es correcto: ", saldo_final)
    else:
        print("El saldo final es incorrecto: ", saldo_final)
