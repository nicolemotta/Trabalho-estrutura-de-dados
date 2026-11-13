#Nicole 
class NoTrie: # Nó da árvore Trie.
    def __init__(self):
        self.filhos = {} # Armazena os filhos do nó, usando cada letra como chave.
        self.eh_fim_de_palavra = False # Indica se o nó representa o final de uma palavra.
        self.frequencia = 0 # Quantidade de vezes que a palavra foi consultada.

class Trie: # Representa a árvore Trie.
    def __init__(self):
        self.raiz = NoTrie() # Nó raiz da árvore Trie.



    def inserir(self, palavra):
        palavra = palavra.strip().lower() # Converte a palavra para minúsculas e remove espaços em branco.

        if not palavra:
            return # Se a palavra estiver vazia, não faz nada.

        atual = self.raiz # Nó atual começa na raiz da árvore.

        # Percorre cada letra da palavra e cria nós filhos conforme necessário.
        for letra in palavra: 
            if letra not in atual.filhos:
                atual.filhos[letra] = NoTrie()

            atual = atual.filhos[letra]

        atual.eh_fim_de_palavra = True # Marca o nó atual como o final de uma palavra.



    def remover(self, palavra):
        palavra = palavra.lower()

        def _remover(no, palavra, indice):
            #  Verifica se chegou ao final da palavra.
            if indice == len(palavra):
                if not no.eh_fim_de_palavra:
                    return False
            
                no.eh_fim_de_palavra = False
                no.frequencia = 0

                return len(no.filhos) == 0 # Retorna True se o nó não tiver filhos, indicando que pode ser removido.

            letra = palavra[indice] # Obtém a letra atual da palavra.

            if letra not in no.filhos:
                return False # Se a letra não existir, a palavra não está na árvore, então retorna False.

            deve_remover = _remover(
                no.filhos[letra], palavra, indice + 1
            ) # Continua a remoção recursivamente para o próximo nó.

            if deve_remover:
                del no.filhos[letra] # Remove o nó quando ele não é mais necessário.

            return (
                not no.eh_fim_de_palavra
                and len(no.filhos) == 0
            ) # Verifica se o nó atual pode ser removido, retornando True se não for o final de uma palavra e não tiver filhos.

        _remover(self.raiz, palavra, 0) 

    
    def carregar_dicionario(self):
        try:
            with open("dicionario.txt", "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.strip().split(";") # Divide a linha em palavra e frequência usando o ponto e vírgula como separador.

                    if not dados[0]:
                        continue # Se a palavra estiver vazia, ignora a linha.

                    palavra = dados[0]
                    frequencia = int(dados[1]) if len(dados) > 1 and dados[1].isdigit() else 0 # Se a frequência não for fornecida ou não for um número, define como 0.

                    self.inserir(palavra) # Insere a palavra na árvore Trie.

                    atual = self.raiz # Nó atual começa na raiz da árvore.

                    for letra in palavra.lower():
                        atual = atual.filhos[letra] # Percorre cada letra da palavra para chegar ao nó correspondente.

                    atual.frequencia = frequencia # Atribui a frequência à palavra.

        except FileNotFoundError:
            print("Arquivo de dicionário não encontrado.") # Se o arquivo não for encontrado, exibe uma mensagem de aviso.



    def incrementar_frequencia(self,palavra):
        atual = self.raiz
        palavra = palavra.lower()

        for letra in palavra:
            if letra not in atual.filhos:
                return # Se a letra não existir, a palavra não está na árvore, então retorna.

            atual = atual.filhos[letra] 

        if atual.eh_fim_de_palavra:
            atual.frequencia += 1 # Incrementa somente se o nó atual for o final de uma palavra.


    def salvar_dicionario(self):
        palavras = []

        def percorrer(no, palavra): 
            if no.eh_fim_de_palavra:
                palavras.append(palavra + ";" + str(no.frequencia)) # Adiciona a palavra e sua frequência à lista de palavras.

            for letra, filho in no.filhos.items():
                percorrer(filho, palavra + letra) # Percorre recursivamente os nós filhos.

        percorrer(self.raiz, "") # Inicia a travessia a partir da raiz da árvore.

        with open("dicionario.txt", "w", encoding="utf-8") as arquivo:
            for palavra in palavras:
                arquivo.write(palavra + "\n") # Escreve cada palavra e sua frequência no arquivo, separadas por uma nova linha.


#Vinicius
    def buscar_prefixo(self, prefixo):
        prefixo = prefixo.strip().lower() #Converte o prefixo para letras minúsculas (padronizar a busca), e também remove os espaços em branco
        atual = self.raiz #Nó atual vai começar na raiz da árvore

        #loop para percorrer cada letra do prefixo para encontrar o nó correspondente
        for letra in prefixo:
            if letra not in atual.filhos:
                return None #Se caso a letra não existir, o prefixo não está na árvore, aí retorna

            atual = atual.filhos[letra] #vai para o próximo nó da árvore

        return atual #Retorna o nó correspondente ao final do prefixo

    def coletar_palavras(self, no, prefixo):
        palavras = [] #lista que vai armazenar as palavras encontradas 

        if no.eh_fim_de_palavra:
            palavras.append((prefixo, no.frequencia)) #adiciona a palavra e sua frequência (quantas vezes a palavra foi consultada) na lista

        #percorre os filhos para encontrar mais palavras
        for letra, filho in no.filhos.items():
            palavras.extend(
                self.coletar_palavras(filho, prefixo + letra)
            ) #adiciona na lista as palavras encontradas nos nós filhos

        return palavras #retorna a lista de palavras e suas frequências


    def autocompletar(self, prefixo):
        prefixo = prefixo.strip().lower() #converte o prefixo para letras minúsculas (padronizar a busca), e também remove os espaços em branco

        if not prefixo:
            return [] #se o prefixo estiver vazio, retorna uma lista vazia.

        no = self.buscar_prefixo(prefixo) #Busca o nó que corresponde o prefixo digitado

        if no is None:
            return [] #caso o prefixo não existir na árvore, vai retornar uma lista vazia

        palavras = self.coletar_palavras(no, prefixo) #coleta todas as palavras que começam com o prefixo
        palavras.sort(key=lambda item: (-item[1], item[0])) #ordena por frequência decrescente (se der empate, é por ordem alfabética)

        return [palavra for palavra, freq in palavras[:3]] #retorna apenas as três primeiras sugestões


# Funções de interação com o usuário (fora da classe Trie)

def consultar_palavra(trie):
    palavra = input("Digite uma palavra: ").strip().lower() #pede uma palavra e padroniza a entrada (letra minuscula, sem espaço em branco)

    if not palavra:
        print("Digite uma palavra válida.")
        return #se a palavra estiver vazia, vai encerrar a consulta 

    atual = trie.buscar_prefixo(palavra) #vai buscar o nó que corresponde a palavra digitada

    if atual is not None and atual.eh_fim_de_palavra:
        trie.incrementar_frequencia(palavra)  #Soma 1 a frequência da palavra, caso ela exista
        print("Palavra encontrada no dicionário!")
    else:
        trie.inserir(palavra) # se a palavra não existir, vai inserir ela automaticamente
        print("Palavra não encontrada. Nova palavra aprendida!")


def menu():
    #cria o menu com as opções pro usuario escolher
    print("\n===== MENU TRIE =====")
    print("1 - Consultar palavra")
    print("2 - Autocompletar por prefixo")
    print("3 - Inserir palavra")
    print("4 - Remover palavra")
    print("0 - Sair")

    return input("Escolha uma opção: ") #retorna a opção escolhida pelo usuário


def main():
    trie = Trie() #Cria uma nova árvore Trie
    trie.carregar_dicionario() #carrega as palavras do arquivo de dicionário para a árvore

    try:
        while True: #Mantém o programa em execução até o usuário escolher sair
            opcao = menu() # Exibe o menu e recebe a opção escolhida.

            if opcao == "1":
                consultar_palavra(trie) #Consulta uma palavra e atualiza sua frequência ou aprende uma nova

            elif opcao == "2":
                prefixo = input("Digite um prefixo: ")
                sugestoes = trie.autocompletar(prefixo) #busca até três sugestões para o prefixo que foi informado

                if sugestoes:
                    print("Sugestões:")
                    for palavra in sugestoes:
                        print("-", palavra) #Exibe cada palavra sugerida
                else:
                    print("Nenhuma sugestão encontrada.") # vai informar quando não existem palavras com o prefixo

            elif opcao == "3":
                palavra = input("Palavra para inserir: ")
                if palavra.strip():
                    trie.inserir(palavra) #insere a palavra informada na árvore
                    print("Palavra inserida!")
                else:
                    print("Digite uma palavra válida.")

            elif opcao == "4":
                palavra = input("Palavra para remover: ")
                if palavra.strip():
                    trie.remover(palavra) #remove a palavra da árvore, caso ela exista
                    print("Operação de remoção concluída.")
                else:
                    print("Digite uma palavra válida.")

            elif opcao == "0":
                print("Encerrando programa...")
                break #encerra o laço de repetição e finaliza o programa

            else:
                print("Opção inválida!") #vai informar quando a opção digitada não existe no menu

    finally:
        trie.salvar_dicionario() #salva as palavras e suas frequências no arquivo antes de encerrar.
        print("Dicionário salvo!")

if __name__ == "__main__":
    main() # Inicia o programa quando o arquivo é executado diretamente



