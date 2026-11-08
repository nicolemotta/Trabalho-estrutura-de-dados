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

