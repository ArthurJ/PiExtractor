import multiprocessing as mp
from time import sleep
from tools import time_it, apresentar, ask_pi_comparado, ask_parameters, print_relatorio, compare_pi_comparado
from decimal import getcontext, Decimal

'''
Created on 01/06/2011
Refactored on 2017/01/03
'''
__author__ = '@arthurj'

mypi = 0


def spi(inicio, fim, quatro=4, dois=2, um=1):
    return sum((int(((quatro // (n8 + 1)) -
                     (dois // (n8 + 4)) -
                     (um // (n8 + 5)) -
                     (um // (n8 + 6))) // (16 ** n))
                for n, n8 in ((x, 8 * x) for x in range(inicio, fim))))


def separa_intervalos(ini, fim, num_de_partes, casas):
    shift = (fim - ini) // num_de_partes
    return [(ini + shift * i, shift * (i + 1), casas)
            for i in range(num_de_partes)]


def calc(*args):
    # Não é a a melhor das práticas, mas compensa na limpeza do código, nesse caso
    global mypi
    mypi += spi(args[0], args[1], args[3], args[4], args[5])


# @time_it(string_explicativa='\nTempo de conversão de Hexadecimal para Decimal: {} segundos')
def float_hex_2_float(str_pi_hex_digits, precisao) -> Decimal:
    getcontext().prec = precisao
    mypi10 = Decimal(0)
    casas_invalidas = int(0.01 * precisao)
    for i in range(len(str_pi_hex_digits) - casas_invalidas, -1, -1):
        mypi10 += int(str_pi_hex_digits[i], base=16) * Decimal(16) ** -i
    return mypi10


@time_it(string_explicativa='\n\nTempo de execução do processamento: {} segundos')
def engine(numero_de_processos, intervalos):
    global mypi
    mypi = 0

    processos = [0] * numero_de_processos

    quatro = 4 << intervalos[0][2]
    dois = 2 << intervalos[0][2]
    um = 1 << intervalos[0][2]

    for i in range(numero_de_processos):
        processos[i] = mp.Process(target=calc, args=(*intervalos[i], quatro, dois, um))
        processos[i].start()
        processos[i].run()

    k = 0
    while numero_de_processos > 0:
        k = k % numero_de_processos
        if not processos[k].is_alive():
            numero_de_processos -= 1
        else:
            sleep(.1)
        k += 1


if __name__ == '__main__':

    apresentar()
    iteracoes, digitos, partes_do_processo, arquivo_saida = ask_parameters()
    pi_comparado, hexa = ask_pi_comparado()

    engine(partes_do_processo, separa_intervalos(0, iteracoes, partes_do_processo, digitos))

    resultado = f'{mypi:x}'
    convertido = float_hex_2_float(resultado, int(iteracoes))
    print_relatorio(resultado, arquivo_saida, convertido)

    if pi_comparado:
        if hexa:
            compare_pi_comparado(pi_comparado, resultado)
        else:
            compare_pi_comparado(pi_comparado, str(convertido))
