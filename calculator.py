import multiprocessing as mp
from time import sleep
from tools import time_it, apresentar, ask_pi_comparado, ask_parameters, print_relatorio, compare_pi_comparado
from decimal import getcontext, ROUND_FLOOR, Decimal

'''
Created on 01/06/2011
Editado em 2017/01/03
'''
__author__ = '@arthurj'


def range8(*args):
    return ((x, 8 * x) for x in range(*args))


def spi(inicio, fim, digitos):
    return sum(int(((4 << digitos) // (n8 + 1) -
                    (2 << digitos) // (n8 + 4) -
                    (1 << digitos) // (n8 + 5) -
                    (1 << digitos) // (n8 + 6)) // (16 ** n))
               for n, n8 in range8(inicio, fim))


def separa_intervalos(ini, fim, num_de_partes, casas):
    shift = (fim - ini) // num_de_partes
    return [(ini + shift * i, shift * (i + 1), casas)
            for i in range(num_de_partes)]


def calc(args):
    # Não é a a melhor das práticas, mas compensa na limpeza do código nesse caso
    global mypi
    mypi += spi(args[0], args[1], args[2])


def float_hex_2_float(str_pi_hex_digits, precisao) -> Decimal:
    getcontext().prec = precisao
    getcontext().rounding = ROUND_FLOOR
    mypi10 = Decimal(0)
    for i in range(len(str_pi_hex_digits) - 1, -1, -1):
        mypi10 += Decimal(int(str_pi_hex_digits[i], base=16) * 16 ** -i)
    return mypi10


@time_it(string_explicativa='\n\nTempo de execução do processamento: {} segundos')
def engine(numero_de_processos, intervalos):
    processos = [0] * numero_de_processos
    for i in range(numero_de_processos):
        processos[i] = mp.Process(target=calc, args=(intervalos[i],))
        processos[i].start()
        processos[i].run()

    k = 0
    while numero_de_processos > 0:
        k = k % numero_de_processos
        if not processos[k].is_alive():
            numero_de_processos -= 1
        else:
            sleep(.01)
        k += 1


if __name__ == '__main__':

    apresentar()
    iteracoes, digitos, partes_do_processo, arquivo_saida = ask_parameters()
    pi_comparado = ask_pi_comparado()

    mypi = 0

    engine(partes_do_processo, separa_intervalos(0, iteracoes, partes_do_processo, digitos))

    resultado = f'{mypi:x}'
    print_relatorio(resultado, arquivo_saida, float_hex_2_float(resultado, int(iteracoes / 3.2)))

    if pi_comparado:
        compare_pi_comparado(pi_comparado, resultado)
