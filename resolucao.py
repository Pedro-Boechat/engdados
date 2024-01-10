import pandas as pd
import re
from datetime import datetime
import sys
import openpyxl


class restaurante:    

    def __init__(self):

        self._colunas_dic = {'1': 'Name', '2': 'Code'}

        try:
            self._products = pd.read_excel('produtos_data.xlsx')

        except FileNotFoundError:
            print("Arquivo 'produtos_data.xlsx' não encontrado.")
            sys.exit()

        self._products['Packs'] = self._products['Packs'].apply(lambda x: x.split(', '))

        # O df _aux tem por objetivo auxiliar o usuário na visualização da tabela
        self._aux = self._products.copy()
        self._aux['Packs'] = self._aux['Packs'].apply(lambda x: ', '.join(map(str, x)))            

    def add_produto(self):
        nome = input("Digite o nome do produto: ")
        codigo = input("Digite o código do produto: ")

        # Este loop evita que o usuário insira produtos mal formatados
        while True:
            pacotes = input('Digite os packs do produto, separados por vírgula, no formato "tamanho @ $XX.XX": ')
            if re.match(r'\d+ @ \$\d+\.\d+', pacotes):
                break
            else:
                print("Formato incorreto. Por favor, insira os packs corretamente.")
        
        packs = [pack.strip() for pack in pacotes.split(',')]

        self._products.loc[len(self._products)] = [nome, codigo, packs]
        self._aux.loc[len(self._aux)] = [nome, codigo, pacotes]


    def remove_produto(self):

        print("Você deseja excluir pelo código ou nome do produto?")
        print("1: Nome.")
        print("2: Código.")
        print()
        chave = self._colunas_dic[input()]
        print()

        print(chave)

        if chave == 'Name':
            valor = input("Digite o nome do produto a ser excluído.\n")
        
        if chave == 'Code':
            valor = input("Digite o código do produto a ser excluído.\n")


        self._products = self._products[self._products[chave] != valor]

        # Excluir também do dataframe de visualização para o usuário não se confundir
        self._aux = self._aux[self._aux[chave] != valor]


    def visualizar_tabela(self):

        print(self._aux)

    def visualizar_produto(self):

        print("Você deseja pesquisar pelo código ou nome do produto?")
        print("1: Nome.")
        print("2: Código.")
        print()
        chave = self._colunas_dic[input()]
        print()

        if chave == 'Name':
            valor = input("Digite o nome do produto a ser pesquisado.\n")

            if valor != '':

                produto_selecionado = self._aux.loc[self._products['Name'] == valor]

                if not produto_selecionado.empty:
                    print(produto_selecionado)
                
                else:
                    print("Produto não encontrado.")
        
        if chave == 'Code':

            valor = input("Digite o código do produto a ser pesquisado.\n")

            if valor != '':

                codigo_selecionado = self._aux.loc[self._products['Code'] == valor]

                if not codigo_selecionado.empty:
                    print(codigo_selecionado)

                else:
                    print("Produto não encontrado.")

    def modifica_produto(self):
        
        print("Você deseja modificar pelo código ou nome do produto?")
        print("1: Nome.")
        print("2: Código.")
        print()
        chave = self._colunas_dic[input("")]
        print()

        if chave == 'Name':
            valor = input("Digite o nome do produto a ser modificado.\n")
        
        if chave == 'Code':
            valor = input("Digite o código do produto a ser modificado.\n")

        if valor not in self._products[chave].values:
            print(f'O produto "{valor}" não está presente na base de dados.')
            return

        print("Digite o novo nome deste produto.")
        novo_nome = input("Pressione Enter se não quiser modificar o nome.\n")

        print("Digite o novo código deste produto.")
        novo_codigo = input("Pressione Enter se não quiser modificar o código.\n")

        print('Digite os novos packs deste produto no formato "Tamanho @ $XX.XX, Tamanho @ $XX.XX.')
        print("Lembre-se: insira todos os packs do produto.")

        # Loop para evitar que o usuário coloque uma formatação errada no banco de dados.
        while True:
            novo_packs = input('Pressione Enter se não quiser modificar os packs\n')
            if re.match(r'\d+ @ \$\d+\.\d+', novo_packs) or novo_packs == '':
                break
            else:
                print("Formato incorreto. Por favor, insira os packs corretamente.")

        filtro = self._products[chave] == valor

        if novo_nome != '':
            self._products.loc[filtro, 'Name'] = novo_nome
            self._aux.loc[filtro, 'Name'] = novo_nome

        if novo_codigo != '':
            self._products.loc[filtro, 'Code'] = novo_codigo
            self._aux.loc[filtro, 'Code'] = novo_codigo

        if novo_packs != '':
            pacotes_lista = [p.strip() for p in novo_packs.split(',')]
            if type(pacotes_lista) == str:
                pacotes_lista = [pacotes_lista]
            else:
                self._products.loc[filtro, 'Packs'] = pacotes_lista

            self._aux.loc[filtro, 'Packs'] = pacotes_lista
    
    def processa_pedido(self):
        self._pedido = {}
        pedido = set_pedido()

        for produto in pedido:
            item = produto.split()
            if len(item) == 2:
                quantidade, codigo = item
                self._pedido[codigo] = int(quantidade)

        return self._pedido
    
    def calculo_packs(self, pedido:dict):
        df_historico = pd.read_excel('historico_pedidos.xlsx')
        dfs = []
        data_hora = datetime.now()
        codigos = list(pedido.keys())
        preco_total = 0

        for produto in codigos:

            coluna_packs = self._products.loc[self._products['Code'] == produto, 'Packs'].values[0]

            preco_packs = {int(re.search(r'^(\d+)', item).group(1)): float(re.search(r'\$([\d.]+)', item).group(1)) for item in coluna_packs}

            tamanhos_packs = [int(re.search(r'^(\d+)', item).group(1)) for item in coluna_packs]

            tamanhos_packs.sort()  # Para este algoritmo, é necessário ordenar os tamanhos dos packs sempre no início
            qtd_pedido = pedido[produto]
            
            min_packs = [float('inf')] * (qtd_pedido + 1) # Todos os casos são setados inicialmente como se usassem infinitos packs
            min_packs[0] = 0  # Para 0 itens (caso impossível) setar 0 em vez de inf. Isso permite o algoritmo a ter um lugar de início
            # Setar como default -1. Isso é importante para checar casos em que a quantidade é impossível:
            tamanhos_usados = [-1] * (qtd_pedido + 1) 

            # Para cada tamanho disponível, verificar como cada um pode ser usado, e as melhores combinações
            # O array min_packs mostra as melhores combinações de packs, identificando as de menor quantidade
            # O array tamanhos_usados mostra quais packs foram usados
            for tamanho in tamanhos_packs:
                for i in range(tamanho, qtd_pedido + 1):
                    # A lógica deste if abaixo é: se o número de packs com essa nova combinação é menor, então
                    # compensa mudar a combinação usada
                    if min_packs[i - tamanho] + 1 < min_packs[i]:
                        min_packs[i] = min_packs[i - tamanho] + 1
                        tamanhos_usados[i] = tamanho

            packs_usados = []
            i = qtd_pedido
            while i > 0:
                tamanho_pack = tamanhos_usados[i]

                if tamanho_pack < 0: # Se essa variavel for -1, significa que não houve pack disponível para a qtd pedida
                    print("Quantidade inatingível com os packs disponíveis.")
                    return

                packs_usados.append(tamanho_pack)
                i -= tamanho_pack # Retira o tamanho que foi usado nesse pack

            preco_final_produto = 0

            print(f'{qtd_pedido} {produto}: ')
            for pacote in set(packs_usados):

                qtd_pack = packs_usados.count(pacote)
                preco_cada_pack = preco_packs[pacote]
                print(f'{qtd_pack}x ${preco_cada_pack} = ${qtd_pack * preco_cada_pack:.2f}')
                preco_final_produto += qtd_pack * preco_cada_pack
                preco_total += qtd_pack * preco_cada_pack


            print(f'Total deste produto: ${preco_final_produto:.2f}\n')

            # Abaixo, a sequência para salvar o histórico dos dados de pedidos

            df_produto = pd.DataFrame({
            'Código do Produto': [produto],
            'Quantidade': [qtd_pedido],
            'Packs Usados': [packs_usados], # Armazena o tamanho dos pacotes que foram usados. Ex: Se foram usados 4 packs de
                                            # tamanho 5, essa variável tem [5,5,5,5]
            'Preço Total': [preco_final_produto],
            'Data e Hora da Compra': [data_hora]
            })

            dfs.append(df_produto)

        df_pedido = pd.concat(dfs, ignore_index=True)

        df_final = pd.concat([df_pedido, df_historico], ignore_index=True)

        total_row_index = df_final[df_final['Código do Produto'] == 'Total'].index
        df_final_temp = df_final.drop(total_row_index)

        soma_quantidade = df_final_temp['Quantidade'].sum()
        soma_preco_total = df_final_temp['Preço Total'].sum()

        df_final.loc[total_row_index, 'Quantidade'] = soma_quantidade
        df_final.loc[total_row_index, 'Preço Total'] = soma_preco_total

        df_final.to_excel(f'historico_pedidos.xlsx', index=False, engine='openpyxl')

        print(f'\nTotal da compra: ${preco_total:.2f}')

    def visualizar_teste(self):
        print("Teste 1:")
        print("Criação do produto TEST123, com packs de 2, e 9 unidades.")
        print("Ao fazer um pedido com 14 unidades, o sistema deve ser capaz de identificar")
        print("que um pack de 9 unidades não se aplica a esse pedido, mas sim 7 de 2 unidades.\n")

        self.calculo_packs(pedido={'TEST123': 14})

        print("\nTeste 2:")
        print("Pedido com quantidade inatingível pelos tamanhos de packs.")
        print("Para este teste, será feito um pedido de 3 unidades do produto TEST123.\n")

        self.calculo_packs(pedido={'TEST123': 3})

        print("\nTeste 3:")
        print("Pedido que usa diversos tamanhos de packs diferentes.")
        print("Para este teste, serão pedidas 17 unidades de CBF19203.\n")

        self.calculo_packs(pedido={'CBF19203': 17})

        print("\nTeste 4:")
        print("Pedido feito com mais de um produto.\n")

        self.calculo_packs(pedido={'CI00432': 10, 'PO01098': 14, 'CBF19203': 13})



    def salvar_dados(self):

        self._products['Packs'] = self._products['Packs'].apply(lambda x: ', '.join(map(str, x)) if len(x) > 1 else x[0])
        self._products.to_excel('produtos_data.xlsx', index=False, engine='openpyxl')

                


    
def set_pedido():
    pedido_usuario = []

    print('Digite o pedido no formato "Quantidade Código".')

    while True:
        linha = input("Digite um item do pedido ou 'sair' para encerrar: \n")
        if linha.lower() == 'sair':
            break
            
        if linha != '':
            pedido_usuario.append(linha)
        
    print(f"Pedido final: {pedido_usuario}")

    while True:

        confirmacao = input("Confirma? S ou N: \n")
        print()
        if confirmacao == 'S' or confirmacao == 's':
            return pedido_usuario
            
        if confirmacao == 'N' or confirmacao == 'n':
            return set_pedido()
        
def tela_inicio():
    print("\nEscolha a ação desejada.")
    print("1: Fazer pedido.")
    print("2: Visualizar tabela de produtos.")
    print("3: Obter informações de um determinado produto.")
    print("4: Adicionar novo produto ao sistema.")
    print("5: Remover produto do sistema.")
    print("6: Modificar produto no sistema.")
    print("7: Visualizar casos de teste.")
    print("8: Sair")
    print()

    resposta = input("Ação: ")
    print()


    if resposta == '1':
        pedido_feito = restaurante_instance.processa_pedido()
        restaurante_instance.calculo_packs(pedido=pedido_feito)

    if resposta == '2':
        restaurante_instance.visualizar_tabela()

    if resposta == '3':
        restaurante_instance.visualizar_produto()

    if resposta == '4':
        restaurante_instance.add_produto()

    if resposta == '5':
        restaurante_instance.remove_produto()

    if resposta == '6':
        restaurante_instance.modifica_produto()

    if resposta == '7':
        restaurante_instance.visualizar_teste()

    if resposta == '8':
        sys.exit()
    
    print("\n\nDeseja continuar usando o sistema?")
    print("1: Sim")
    print("2: Não")
    continua = input()

    if continua == '1':
        tela_inicio()
        
        

restaurante_instance = restaurante()

print("Bem-vindo ao sistema interno de pedidos CB.")
tela_inicio()

restaurante_instance.salvar_dados()