from random import randint
from time import sleep
import json

arquivo = 'ranks.json'

def carregar_ranking():
    try:
        with open(arquivo, 'r', encoding='utf-8') as arq:
            return json.load(arq)
    except FileNotFoundError:
        return []


def salvar_ranking(ranking):
    with open(arquivo, 'w', encoding='utf-8') as arq:
        json.dump(ranking, arq, ensure_ascii=False, indent=4)


def adicionar_jogador(nome, pontuacao):
    ranking = carregar_ranking()

    for jogador in ranking:
        if jogador['nome'] == nome:
            jogador['pontuacao'] = max(jogador['pontuacao'], pontuacao)
            break
    else:
        ranking.append({
            'nome': nome,
            'pontuacao': pontuacao
        })

    salvar_ranking(ranking)


def obter_ranking_ordenado():
    ranking = carregar_ranking()
    return sorted(ranking, key=lambda x: x['pontuacao'], reverse=True)


def imprimir_ranking():
    ranking = obter_ranking_ordenado()

    if not ranking:
        print('Ainda não há jogadores no ranking!!!')
        return

    print('=' * 40)
    print('RANKING DE TESTE')
    print('=' * 40)

    for i, jogador in enumerate(ranking, start=1):
        print(f'{i:>2}º {jogador["nome"]:<15} {jogador["pontuacao"]:.2f}')

    print('=' * 40)


def calcponto(vitorias, chance, peso, auxponto, victactual):
    if vitorias == 0:
        ponto = 0
    else:
        ponto = victactual*(peso*(int((1.25*(chance+1)**3-5*(chance+1)**2+28.75*(chance+1)+75)/10)*10))
        ponto += auxponto
    return ponto


def verificar():
    while True:
        print('-' * 100)
        vdd = lernome('Digite S para jogar, ou N para fechar: ').upper().strip()
        if vdd != 'N' and vdd != 'S':
            print('Somente S ou N!!!')
            continue
        print('-' * 100)
        if vdd == 'N':
            return False
        else:
            return True

def terminar(vitorias, tent, ponto):
    if tent == 1:
        if vitorias == 0:
            print(f'Você venceu nenhuma vez em {tent} tentativa!\nPontuação: {ponto:.2f}')
        else:
            print(f'Você venceu 1 vez em 1 tentativa!\nPontuação: {ponto:.2f}')
    else:
        if vitorias == 1:
            print(f'Você venceu {vitorias} vez em {tent} tentativas!\nPontuação: {ponto:.2f}')
        elif vitorias == 0:
            print(f'Você venceu nenhuma vez em {tent} tentativas!\nPontuação: {ponto:.2f}')
        else:
            print(f'Você venceu {vitorias} vezes em {tent} tentativas!\nPontuação: {ponto:.2f}')
    return False


def lernome(mensagem):
    while True:
        nome = input(mensagem).strip()
        if nome:
            return nome
        print("Nome inválido! Não pode ser vazio.")


def lerint(mensagem, minimo = None, maximo = None):
    usererror = 0
    while True:
        if usererror == 3:
            print('JOGO ENCERRADO POR ERROS SUCESSIVOS...')
            raise SystemExit
        try:
            valor = int(input(mensagem))
            if valor == 3824:
                print('03/08/2024')
                sleep(3)
                print('Essa data é muito especial')
                sleep(3)
                print('Eu jurei solenemente fazer tudo de bom com ela')
                sleep(3)
                print('Nos dias mais claros e noites mais densas')
                sleep(3)
                print('Te amarei por todo o sempre')
                sleep(3)
                nic = 'Nicole Gomes Felizardo'
                love = 'Eu Amo Você'
                for c in range(len(nic)):
                    print(nic[c], end = '')
                    sleep(0.3)
                print('\n')
                for c in range(len(love)):
                    print(love[c], end = '')
                    sleep(0.3)
                sleep(1)
                print('\n')
                print(100*'\u2764\uFE0F')
                sleep(2)
                print('-' * 100)
                continue

            if minimo is not None and valor < minimo:
                raise ValueError
            if maximo is not None and valor > maximo:
                raise ValueError
            return valor
        except ValueError:
            print("Entrada inválida!!!")
            usererror += 1

def jogar(nome, vitorias, auxponto, tent):
    while True:
        pc = randint(0, 100)
        diff = lerint(f'Selecione a dificuldade:\n1) Fácil\n2) Médio\n3) Difícil\n0) Mostrar Ranking\nSelecione: ', 0, 3)
        if diff == 0:
            imprimir_ranking()
            continue
        elif diff == 1:
            chancemax = chance = 7
            peso = 1
        elif diff == 2:
            chancemax = chance = 5
            peso = 2.5
        else:
            chancemax = chance = 3
            peso = 5
        while chance > 0:
            if chance == 1:
                print('-' * 100)
                n = lerint(f'Você tem {chance} chance. Digite um número de 0 a 100: ', 0, 100)
            else:
                print('-' * 100)
                n = lerint(f'Você tem {chance} chances. Digite um número de 0 a 100: ', 0, 100)
            chance -= 1
            if n == pc:
                if chance == 6:
                    print('-' * 100)
                    print(f'Parabéns! Você venceu em 1 tentativa!')
                else:
                    print('-' * 100)
                    print(f'Parabéns! Você venceu em {chancemax - chance} tentativas!')
                vitorias += 1
                victactual = 1
                auxponto = calcponto(vitorias, chance, peso, auxponto, victactual)
                jogando = verificar()
                if not jogando:
                    adicionar_jogador(nome, auxponto)
                    terminar(vitorias, tent, auxponto)
                    return
                tent += 1
                break
            else:
                print(f'Errou!')
                if n > pc:
                    print(f'É menor!')
                else:
                    print(f'É maior!')
            if chance == 0:
                print(f'Você perdeu! Suas {chancemax} tentativas já foram... O número era {pc}.')
                victactual = 0
                auxponto = calcponto(vitorias, chance, peso, auxponto, victactual)
                jogando = verificar()
                if not jogando:
                    adicionar_jogador(nome, auxponto)
                    terminar(vitorias, tent, auxponto)
                    return
                tent += 1
                break

def main():
    nome = lernome('Insira seu nome: ')
    vitorias = auxponto = 0
    tent = 1
    jogar(nome, vitorias, auxponto, tent)


if __name__ == '__main__':
    main()