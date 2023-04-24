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
            saldo_jugadores[i] += 36 * 10

    # Apuestas a par/impar
    for i in range(4, 8):
        par_impar_apostado = random.choice(['par', 'impar'])
        saldo_jugadores[i] -= 10
        if par_impar_apostado == par_impar_ganador:
            saldo_jugadores[i] += 2 * 10

    # Apuestas con martingala
    for i in range(8, 12):
        if saldo_jugadores[i] >= 10:
            if 'martingala_apostado' not in multiprocessing.current_process()._dict:
                numero_apostado = random.randint(1, 36)
                multiprocessing.current_process()._dict['martingala_apostado'] = numero_apostado
            else:
                numero_apostado = multiprocessing.current_process()._dict['martingala_apostado']
            saldo_jugadores[i] -= 10
            if numero_apostado == numero_ganador:
                saldo_jugadores[i] += 36 * 10
                multiprocessing.current_process()._dict.pop('martingala_apostado', None)
            else:
                martingala_apuesta_anterior = multiprocessing.current_process()._dict.get('martingala_apuesta_anterior', 10)
                if saldo_jugadores[i] >= martingala_apuesta_anterior:
                    saldo_jugadores[i] -= martingala_apuesta_anterior
                    multiprocessing.current_process()._dict['martingala_apuesta_anterior'] = martingala_apuesta_anterior * 2
                    multiprocessing.current_process()._dict['martingala_apostado'] = numero_apostado
                else:
                    saldo_jugadores[i] = 0
                    multiprocessing.current_process()._dict.pop('martingala_apostado', None)
                    multiprocessing.current_process()._dict.pop('martingala_apuesta_anterior', None)

    # Actualizar saldo de la banca
    saldo_banca += sum(saldo_jugadores)

    return saldo_jugadores, saldo_banca

# Función para simular múltiples rondas de apuestas
def simular_juego(num_rondas):
    # Generar números ganadores y par/impar gan
