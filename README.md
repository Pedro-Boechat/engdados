# Desafio Engenharia de Dados

## Introdução
O desafio proposto consiste na determinação de quais pacotes devem ser utilizados em cada pedido, e seus respectivos preços ao usuário.

A fim de solucionar com excelência e demonstrar habilidades em diferentes frentes da engenharia e ciência de dados, opto por ir além do problema proposto: foi realizado o desenvolvimento do algoritmo de atribuição de pedidos, e a implementação de um banco de dados para os produtos, e de um sistema capaz de adicionar, remover, modificar, e visualizar produtos, fazer pedidos, e verificar casos de teste.

Adicionalmente a isso, o sistema é capaz de manter um histórico de todos os pedidos feitos por ele. Também foi criado um dashboard dinâmico usando a ferramenta Power BI para visualização e breakdown dos dados do histórico.

## O algoritmo

O ponto focal do desafio é a implementação do algoritmo. Tendo vistas ao Knapsack Problem, um conhecido problema de programação dinâmica envolvendo inserção de itens em caixas, foi desenvolvida uma adaptação de sua solução, uma vez que a situação proposta pela equipe CBLab é única e diferente daquela abordada classicamente.

- O primeiro passo é ordenar os tamanhos dos packs do produto em questão em ordem crescente.
- É iterado o uso do menor pacote disponível;
- É verificada a possibilidade de otimização do resultado final para cada outro tamanho de pacote;

Casos de teste em que é pedida uma quantidade inatingível de unidades de um produto são cobertos.

Foi necessária especial atenção ao fato de que não é possível atacar o problema iniciando os cálculos pelo maior pacote disponível, uma vez que isso pode tornar o problema impossível. Por exemplo:
Foram solicitadas 14 unidades de um produto cujos pacotes disponíveis têm tamanhos 2, e 9. Caso o raciocínio parta do uso de um pacote de 9 unidades, o problema não tem solução.

Em vez disso, o raciocínio adotado foi o de usar o pacote de menor tamanho possível, e depois verificar a possibilidade de otimização da entrega final.

## O sistema

Visto o longo prazo de entrega da solução, decidi fazer implementações adicionais que são de valia ao cargo.

Desenvolvi um sistema capaz de manipular um banco de dados (neste caso, no excel, embora haja outras possibilidades mais sofisticadas) a fim de gerenciar todos os produtos do restaurante.
O sistema tem como funcionalidades a adição, remoção, alteração e visualização de todos os produtos. A formatação de todos os campos é garantida pelo sistema, mesmo com inputs de usuário (quando um input é inválido, o usuário é convidado a refazer a formatação).
Além disso, conta com a possibilidade de realizar pedidos, e a visualização de alguns casos de teste notáveis do algoritmo de pedidos implementado.

## Dashboard

O sistema atualiza automaticamente uma planilha contendo todo o histórico de pedidos realizado.
Utilizando esse histórico, foi elaborado um dashboard na ferramenta Power BI, a fim de destacar o faturamento total e médio por dia, um breakdown de faturamento por cada produto (para identificação de produtos de maior sucesso), um mapeamento de restaurantes com maior volume de pedidos (para identificação de restaurantes com maior fluxo de clientes, e posterior levantamento de melhorias aos demais pontos, tendo em vista o de maior sucesso), e um funil de número de pacotes utilizado (para identificação da adequação dos tamanhos de pacotes disponibilizados aos clientes).
O mapeamento de fluxo por restaurante não foi implementável, uma vez que a natureza dos dados disponível não se aplica.
Outra possibilidade a ser implementada é o rastreamento do perfil dos clientes do Coco Bambu.

## Como executar o código

Foi disponibilizado um arquivo requirements.txt, contendo as bibliotecas cuja instalação se faz necessária.
Além disso, é necessário ter Python instalado em sua máquina.

## Como utilizar o sistema

Ao executar o código no seu prompt de comando, são disponibilizadas 8 opções de ações ao usuário.
Cada uma delas segue com instruções de como proceder para alcançar o objetivo do usuário.
Ao final de cada ação, o sistema questiona se o usuário quer continuar ou sair do programa.
