import random
import multiprocessing

# Función para realizar una ronda de apuestas
def ronda_apuestas(numero_ganador, par_impar_ganador):
    saldo_jugadores = [1000] * 12
    saldo_banca = 50000

    # Apuestas a números concretos
    for i in range(4):
        numero_apostado = random.randint(1, 36)
        saldo_jugadores[i] -= 10
        if numero_apostado == numero_ganador:
            saldo_jugadores[i] += 360

    # Apuestas a par/impar
    for i in range(4, 8):
        par_impar_apostado = random.choice(['par', 'impar'])
        saldo_jugadores[i] -= 10
        if par_impar_apostado == par_impar_ganador:
            saldo_jugadores[i] += 20

    # Apuestas con martingala
    for i in range(8, 12):
        if saldo_jugadores[i] >= 10:
            if 'martingala_apostado' not in multiprocessing.current_process().dict:
                numero_apostado = random.randint(1, 36)
                multiprocessing.current_process().dict['martingala_apostado'] = numero_apostado
            else:
                numero_apostado = multiprocessing.current_process().dict['martingala_apostado']
            saldo_jugadores[i] -= 10
            if numero_apostado == numero_ganador:
                saldo_jugadores[i] += 360
                multiprocessing.current_process().dict.pop('martingala_apostado', None)
            else:
                martingala_apuesta_anterior = multiprocessing.current_process().dict.get('martingala_apuesta_anterior', 10)
                if saldo_jugadores[i] >= martingala_apuesta_anterior:
                    saldo_jugadores[i] -= martingala_apuesta_anterior
                    multiprocessing.current_process().dict['martingala_apuesta_anterior'] = martingala_apuesta_anterior * 2
                    multiprocessing.current_process().dict['martingala_apostado'] = numero_apostado
                else:
                    saldo_jugadores[i] = 0
                    multiprocessing.current_process().dict.pop('martingala_apostado', None)
                    multiprocessing.current_process().dict.pop('martingala_apuesta_anterior', None)

    # Actualizar saldo de la banca
    saldo_banca += sum(saldo_jugadores)

    return saldo_jugadores, saldo_banca

# Función para simular múltiples rondas de apuestas
def simular_juego(num_rondas):
    # Generar números ganadores y par/impar ganador para todas las rondas
    numeros_ganadores = [random.randint(0, 36) for _ in range(num_rondas)]
    par_impar_ganadores = ['par' if n % 2 == 0 else 'impar' for n in numeros_ganadores]

    # Crear procesos para simular las rondas de apuestas
    pool = multiprocessing.Pool()
    resultados = pool.starmap(ronda_apuestas, zip(numeros_ganadores, par_impar_ganadores))
    pool.close()

    # Sumar los saldos finales de los jugadores y de la banca
    saldo_jugadores_total = [0] * 12
    saldo_banca_total = 50000
    for resultado in resultados:
        saldo_jugadores_total = [x + y for x, y in zip(saldo_jugadores_total, resultado[0])]
        saldo_banca_total += resultado[1]
