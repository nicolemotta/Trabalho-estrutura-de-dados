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
        prefixo = prefixo.strip().lower()
        atual = self.raiz

        for letra in prefixo:
            if letra not in atual.filhos:
                return None

            atual = atual.filhos[letra]

        return atual

    def coletar_palavras(self, no, prefixo):
        palavras = []

        if no.eh_fim_de_palavra:
            palavras.append((prefixo, no.frequencia))

        for letra, filho in no.filhos.items():
            palavras.extend(
                self.coletar_palavras(filho, prefixo + letra)
            )

        return palavras

    def autocompletar(self, prefixo):
        prefixo = prefixo.strip().lower()

        if not prefixo:
            return []

        no = self.buscar_prefixo(prefixo)

        if no is None:
            return []

        palavras = self.coletar_palavras(no, prefixo)
        palavras.sort(key=lambda item: (-item[1], item[0]))

        return [palavra for palavra, freq in palavras[:3]]

    

def consultar_palavra(trie):
    palavra = input("Digite uma palavra: ").strip().lower()

    if not palavra:
        print("Digite uma palavra válida.")
        return

    atual = trie.buscar_prefixo(palavra)

    if atual is not None and atual.eh_fim_de_palavra:
        trie.incrementar_frequencia(palavra)
        print("Palavra encontrada no dicionário!")
    else:
        trie.inserir(palavra)
        print("Palavra não encontrada. Nova palavra aprendida!")


def menu():
    print("\n===== MENU TRIE =====")
    print("1 - Consultar palavra")
    print("2 - Autocompletar por prefixo")
    print("3 - Inserir palavra")
    print("4 - Remover palavra")
    print("0 - Sair")

    return input("Escolha uma opção: ")


def main():
    trie = Trie()
    trie.carregar_dicionario()

    try:
        while True:
            opcao = menu()

            if opcao == "1":
                consultar_palavra(trie)

            elif opcao == "2":
                prefixo = input("Digite um prefixo: ")
                sugestoes = trie.autocompletar(prefixo)

                if sugestoes:
                    print("Sugestões:")
                    for palavra in sugestoes:
                        print("-", palavra)
                else:
                    print("Nenhuma sugestão encontrada.")

            elif opcao == "3":
                palavra = input("Palavra para inserir: ")
                if palavra.strip():
                    trie.inserir(palavra)
                    print("Palavra inserida!")
                else:
                    print("Digite uma palavra válida.")

            elif opcao == "4":
                palavra = input("Palavra para remover: ")
                if palavra.strip():
                    trie.remover(palavra)
                    print("Operação de remoção concluída.")
                else:
                    print("Digite uma palavra válida.")

            elif opcao == "0":
                print("Encerrando programa...")
                break

            else:
                print("Opção inválida!")

    finally:
        trie.salvar_dicionario()
        print("Dicionário salvo!")


if __name__ == "__main__":
    main()




