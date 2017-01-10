import sys
from time import time
from functools import wraps
import multiprocessing as mp


def time_it(funcao_captora=None, string_explicativa="Tempo de execução: {} segundos", repeat=1):
    """
    :param string_explicativa: String a mostrar detalhes da função monitorada. default = 1
    :param funcao_captora: Recebe o tempo, afim de disponíbilizar o resultado do decorator
    :param repeat: Número de vezes que o processo deve ser executado para obter uma média de tempo de execução
        Decorator que mede e imprime o tempo de execução em segundos,
        opcionalmente recebe uma função que recebe o tempo, e pode enviar a outro objeto.
    """

    def decorador(method):
        @wraps(method)
        def wrapper(*args, **kw):
            ts = time()
            result = None
            for i in range(repeat):
                result = method(*args, **kw)
            te = time()

            delta = (te - ts) / repeat

            if funcao_captora:
                funcao_captora(delta)

            print(string_explicativa.format(delta))
            return result

        return wrapper

    return decorador


def apresentar():
    print('\nFui escrito para calcular os digitos de π em base hexadecimal.')
    print('Leve em consideração que o processador ' +
          'deste computador tem {} núcleo(s).\n'.format(mp.cpu_count()))


def ask_pi_comparado(default='npix8k'):
    default = input(f'\nQual o arquivo com o a referência para comparar o resultado?\n[{default}] -> ') or default

    try:
        pi_padrao = open(default, 'r').read()
    except IOError:
        print(f'Não foi possível carregar o arquivo {default}', file=sys.stderr)
        return ''
    resposta_hexa = input('O valor está em Hexadecimal? [Y/n] -> ') in ('', 'y', 'Y')
    return pi_padrao, resposta_hexa


def ask_parameters(num_iteracoes=9999, num_processos=int(mp.cpu_count() * .75), nome='meupix'):
    numero_de_iteracoes = int(input(f'Número de Iterações à realizar?\n[{num_iteracoes}] -> ') or num_iteracoes)
    casas = int(3.2*numero_de_iteracoes)
    numero_de_processos = int(input(f'Dividir o processo em quantas partes?\n[{num_processos}] -> ') or num_processos)
    nome_arquivo = input(f'\nQual o nome do arquivo de saída?\n[{nome}] ->') or nome

    return numero_de_iteracoes, casas, numero_de_processos, nome_arquivo


def pi_line_braker(converted_result):
    converted_result = str(converted_result)
    for i in range(len(converted_result)):
        print(f'{converted_result[i]}', end='')
        if i % 100 == 0:
            print()


def print_relatorio(result, nome_saida, converted_result):
    print('\n\nValor Hexadecimal:')
    pi_line_braker(result)

    print('\n\nValor Decimal:')
    pi_line_braker(converted_result)

    print(f'\nNúmero de dígitos hexadecimais obtidos: {str(len(result))}\n')

    nome_saida = open(nome_saida, 'w')
    print(result, file=nome_saida)


@time_it(string_explicativa='\nTempo de execução da comparação: {} segundos')
def compare_pi_comparado(pi_referencia, result):
    for casa in range(len(pi_referencia)):
        if casa < len(result) \
                and result[casa] == pi_referencia[casa].lower():
            casa += 1
        else:
            break
    print(casa, 'digitos idênticos consecutivos.')
