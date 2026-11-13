class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.eh_fim_de_palavra = False
        self.frequencia = 0

class Trie:
    def __init__(self):
        self.raiz = NoTrie()



    def inserir(self, palavra):
        palavra = palavra.strip().lower()

        if not palavra:
            return

        atual = self.raiz

        for letra in palavra:
            if letra not in atual.filhos:
                atual.filhos[letra] = NoTrie()

            atual = atual.filhos[letra]

        atual.eh_fim_de_palavra = True



    def remover(self, palavra):
        palavra = palavra.lower()

        def _remover(no, palavra, indice):
            if indice == len(palavra):
                if not no.eh_fim_de_palavra:
                    return False
            
                no.eh_fim_de_palavra = False
                no.frequencia = 0

                return len(no.filhos) == 0

            letra = palavra[indice]

            if letra not in no.filhos:
                return False

            deve_remover = _remover(
                no.filhos[letra], palavra, indice + 1
            )

            if deve_remover:
                del no.filhos[letra]

            return (
                not no.eh_fim_de_palavra
                and len(no.filhos) == 0
            )

        _remover(self.raiz, palavra, 0)

    
    def carregar_dicionario(self):
        try:
            with open("dicionario.txt", "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.strip().split(";")

                    if not dados[0]:
                        continue

                    palavra = dados[0]
                    frequencia = int(dados[1]) if len(dados) > 1 and dados[1].isdigit() else 0

                    self.inserir(palavra)

                    atual = self.raiz

                    for letra in palavra.lower():
                        atual = atual.filhos[letra]

                    atual.frequencia = frequencia

        except FileNotFoundError:
            print("Arquivo de dicionário não encontrado.")



    def incrementar_frequencia(self,palavra):
        atual = self.raiz
        palavra = palavra.lower()

        for letra in palavra:
            if letra not in atual.filhos:
                return

            atual = atual.filhos[letra]

        if atual.eh_fim_de_palavra:
            atual.frequencia += 1


    def salvar_dicionario(self):
        palavras = []

        def percorrer(no, palavra):
            if no.eh_fim_de_palavra:
                palavras.append(palavra + ";" + str(no.frequencia))

            for letra, filho in no.filhos.items():
                percorrer(filho, palavra + letra)

        percorrer(self.raiz, "")

        with open("dicionario.txt", "w", encoding="utf-8") as arquivo:
            for palavra in palavras:
                arquivo.write(palavra + "\n")


    
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




