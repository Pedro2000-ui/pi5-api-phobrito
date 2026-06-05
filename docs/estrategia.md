# Agente Heurístico BOT CARILLE para Jogo de Tabuleiro 5x5

## Objetivo

O objetivo do agente é selecionar a melhor jogada possível a cada turno utilizando uma estratégia baseada em heurísticas.

Ao invés de utilizar algoritmos de busca profunda como Minimax, o agente avalia todas as jogadas disponíveis no estado atual do tabuleiro e atribui uma pontuação para cada alternativa, escolhendo aquela que apresenta o maior valor.

A proposta foi desenvolver uma solução de baixo custo computacional, capaz de responder rapidamente e apresentar comportamento estratégico consistente.

---

## Técnica de Inteligência Artificial Utilizada

Foi utilizado um agente reativo baseado em função heurística.

O funcionamento segue os seguintes passos:

1. Gerar todas as jogadas válidas.
2. Simular cada jogada.
3. Avaliar as consequências imediatas da ação.
4. Atribuir uma pontuação utilizando uma função heurística.
5. Selecionar a jogada de maior valor.

---

## Modelagem do Problema

Cada estado do jogo é composto por:

* Tabuleiro 5x5.
* Nível de cada construção (0 a 4).
* Localização dos professores.
* Time atual.

Cada ação possível é composta por:

* Movimento de um professor.
* Escolha de uma célula para mentoria.

A mentoria aumenta em uma unidade o nível da construção escolhida, respeitando o limite máximo permitido pelo jogo.

---

## Estratégia de Posicionamento Inicial

Durante a fase de posicionamento inicial dos professores, o agente utiliza uma heurística baseada no controle da região central do tabuleiro.

O objetivo é maximizar a mobilidade dos professores desde os primeiros turnos da partida.

Casas localizadas na região central possuem maior quantidade de células adjacentes, permitindo um número maior de movimentos e opções de mentoria ao longo do jogo.

Essa decisão permite que ambos atuem em conjunto na região central, aumentando a capacidade de controle territorial e oferecendo maior flexibilidade para ações ofensivas e defensivas nos turnos seguintes.

### Benefícios da Estratégia

A utilização dessa heurística proporciona:

- Maior mobilidade dos professores.
- Maior quantidade de movimentos disponíveis.
- Melhor controle da região central do tabuleiro.
- Maior facilidade para construir e acessar estruturas de níveis elevados.
- Melhor capacidade de resposta a ameaças adversárias.

Dessa forma, o agente inicia a partida ocupando posições estrategicamente vantajosas, reduzindo a dependência de decisões aleatórias durante a fase de setup.

---

## Estratégia Utilizada

A estratégia adotada é predominantemente defensiva.

Antes de analisar benefícios próprios, o agente verifica se determinada jogada permite que o adversário possua uma vitória imediata no próximo turno.

Caso uma jogada elimine uma ameaça de vitória do adversário, ela recebe prioridade máxima.

Quando não existe ameaça imediata, o agente passa a buscar o fortalecimento de sua própria posição no tabuleiro.

Portanto, o comportamento pode ser resumido como:

* Primeiro defender, depois atacar.

---

## Função Heurística

Cada jogada recebe uma pontuação baseada em critérios estratégicos.

### 1. Impedir Vitória Imediata do Adversário

Após simular uma jogada, o agente verifica se o adversário ainda possui alguma ação vencedora disponível.

Caso a ameaça seja eliminada, a jogada recebe a maior bonificação da avaliação.

Esse é o principal fator considerado pelo algoritmo.

---

### 2. Evolução de Nível dos Professores

O agente valoriza movimentos que posicionam seus professores em construções mais altas.

Quanto maior o nível alcançado, maior a pontuação recebida.

A ideia é aumentar as possibilidades futuras de movimentação e aproximação de condições de vitória.

---

### 3. Aproveitamento de Oportunidades de Vitória

Caso uma jogada permita que um professor alcance uma construção de nível 3, ela recebe uma bonificação adicional.

Essa condição representa uma oportunidade imediata de vitória.

Importante destacar que a vitória não é tratada como prioridade absoluta. Ela se torna relevante principalmente quando não existem ameaças adversárias urgentes para serem tratadas.

---

### 4. Construção Estratégica

Ações de mentoria que elevam construções para níveis mais altos também recebem bonificações.

O objetivo é preparar o tabuleiro para futuras movimentações favoráveis.

Construções que atingem níveis intermediários ou elevados são consideradas mais valiosas pelo agente.

---

## Fluxo de Execução

### Fase de Posicionamento Inicial ([choose_setup](choose_setup.md))

Durante a fase de setup, o agente recebe o professor que deve ser posicionado e analisa o estado atual do tabuleiro.

#### 1. Identificação do professor
O algoritmo recebe o nome do professor através do campo:

```python
professor_to_place
```

Exemplos:

```python
CLARO
REY
KARIN
BEATRIZ
```

#### 2. Verificação do Professor Parceiro
Cada professor possui um parceiro definido:

```python
PAIRS = {
    "CLARO": "REY",
    "REY": "CLARO",
    "KARIN": "BEATRIZ",
    "BEATRIZ": "KARIN",
}
```
O agente verifica se o parceiro já foi posicionado no tabuleiro.

Por exemplo:

- Se estiver posicionando o professor REY, o algoritmo procura o professor CLARO.
- Se estiver posicionando a professora BEATRIZ, o algoritmo procura a professora KARIN.

#### 3. Posicionamento próximo ao parceiro

Caso o parceiro já esteja presente no tabuleiro, o agente tenta ocupar uma das células adjacentes disponíveis.

Exemplo:

```python
. . . . .
. . . . .
. . C . .
. . . . .
. . . . .
```

Ao posicionar REY o algoritmo procura uma posição próxima a CLARO.

```python
. . . . .
. . R . .
. . C . .
. . . . .
. . . . .
```

Essa estratégia permite que ambos atuem de forma coordenada e mantenham controle conjunto da região central.

#### 4. Controle da Região Central

Caso o parceiro ainda não tenha sido posicionado, o agente utiliza uma lista de prioridades baseada na proximidade do centro do tabuleiro:

```python
PRIORITIES = [
    (2, 2),

    (2, 1),
    (2, 3),
    (1, 2),
    (3, 2),

    (1, 1),
    (1, 3),
    (3, 1),
    (3, 3),
]
```

A posição central ```(2,2)``` possui prioridade máxima.

Se ela não estiver disponível, o algoritmo seleciona a próxima posição mais próxima do centro.

Exemplo:

```python
1ª prioridade → (2,2)

. . . . .
. . . . .
. . X . .
. . . . .
. . . . .
```

Caso esteja ocupada:

```python
2ª prioridade → (2,1)

. . . . .
. . . . .
. X . . .
. . . . .
. . . . .
```

#### 5. Escolha de posição

A primeira posição válida encontrada é selecionada como resposta do agente.

O algoritmo verifica:

- se a posição está dentro dos limites do tabuleiro;
- se a construção possui nível 0;
- se não existe professor ocupando a célula.

```python
def is_available(row: int, col: int) -> bool:
        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and board[row][col].level == 0
            and board[row][col].professor is None
        )
```

#### 6. Fallback

Em situações excepcionais, caso nenhuma posição prioritária esteja disponível, o agente seleciona aleatoriamente uma das casas válidas restantes.

Esse mecanismo garante que sempre exista uma resposta válida para o orquestrador da partida.

```python
#
# Fallback
#
candidates = [
    (r, c)
    for r in range(BOARD_SIZE)
    for c in range(BOARD_SIZE)
    if is_available(r, c)
]

row, col = random.choice(candidates)

return SetupResponse(
    row=row,
    col=col,
)
```

### Fase de Jogo ([choose_turn](choose_turn.md))

Durante cada turno, o agente recebe o estado completo da partida e executa uma sequência de etapas para identificar a melhor jogada possível.

#### 1. Geração de Jogadas Válidas

Inicialmente, o algoritmo percorre todos os professores pertencentes ao time atual.

Para cada professor, são analisadas todas as células adjacentes possíveis.

Uma movimentação somente é considerada válida quando:

- a célula de destino está desocupada;
- a célula não possui nível 4;
- a diferença de altura respeita as regras do jogo (subida máxima de um nível).

Para cada movimentação válida, também são geradas todas as mentorias possíveis.

O resultado dessa etapa é uma lista contendo todas as ações legalmente permitidas naquele turno.

Exemplo:

```python
CLARO -> mover para (2,1) e mentorar (1,1)
CLARO -> mover para (2,1) e mentorar (1,2)
CLARO -> mover para (2,1) e mentorar (3,1)
REY   -> mover para (3,0) e mentorar (2,0)
...
```

#### 2. Simulação das Jogadas

Cada jogada gerada é simulada individualmente.

Para isso, o algoritmo cria uma cópia temporária do tabuleiro e aplica:

1. o movimento do professor;
2. a mentoria correspondente.

```python
def apply_move(board, move):

    board = copy.deepcopy(board)

    pos = find_professor(
        board,
        move.professor,
    )

    if pos is None:
        return board

    src_row, src_col = pos

    dst_row = move.move_to.row
    dst_col = move.move_to.col

    board[src_row][src_col].professor = None

    board[dst_row][dst_col].professor = move.professor

    if move.mentor_at is not None:

        mr = move.mentor_at.row
        mc = move.mentor_at.col

        if board[mr][mc].level < 4:
            board[mr][mc].level += 1

    return board
```

Essa simulação permite avaliar as consequências da ação sem alterar o estado real da partida.

#### 3. Verificação de Ameaças Adversárias

Após a simulação, o agente verifica se o adversário ainda possui alguma jogada vencedora disponível no próximo turno.

Essa análise é realizada pela função:

```python
enemy_has_immediate_win()
```

O algoritmo gera todas as jogadas possíveis do oponente e verifica se alguma delas permite alcançar uma célula de nível 3.

Exemplo:

```python
KARIN está em uma construção de nível 2
Existe uma construção de nível 3 adjacente

→ ameaça detectada

```

Caso a jogada simulada elimine essa possibilidade, ela recebe a maior bonificação da avaliação.

---

#### 4. Avaliação Heurística

Cada jogada recebe uma pontuação baseada em quatro critérios.

<strong>Critério 1 — Neutralização de Vitória Adversária</strong>

Se após a jogada o adversário não possuir mais uma vitória imediata disponível:

```python
score += 10000
```
Esse é o fator mais importante da avaliação.

<strong>Critério 2 — Evolução de Nível</strong>

O agente valoriza movimentos que posicionam seus professores em construções mais altas.

A pontuação é calculada considerando:

- a diferença de altura entre origem e destino;
- o nível final alcançado.

Exemplo:

```python
nível 0 → nível 1
```

recebe mais pontos que

```python
nível 0 → nível 0
```

<strong>Critério 3 — Vitória Própria</strong>

Caso o professor alcance uma construção de nível 3:

```python
score += 1000
```

A jogada é considerada vantajosa, pois representa uma condição imediata de vitória.

Entretanto, essa bonificação possui peso inferior ao critério defensivo.

Isso faz com que o agente priorize impedir uma vitória adversária antes de buscar sua própria vitória.

<strong>Critério 4 — Construção Estratégica</strong>

Ações de mentoria também são avaliadas.

O agente atribui pontos extras para construções que evoluem para:

```python
nível 2
nível 3
nível 4
```

A intenção é preparar futuras oportunidades de movimentação e controle do tabuleiro.

#### 5. Comparação das Alternativas

Após todas as jogadas serem avaliadas, suas pontuações são comparadas.

Exemplo:

```python
Jogada A → 10.150 pontos
Jogada B → 9.850 pontos
Jogada C → 10.300 pontos
```

#### 6. Seleção da Melhor Jogada

O algoritmo mantém armazenada a jogada com maior pontuação encontrada durante a análise.

Ao final do processo ```best_move``` contém a melhor alternativa disponível naquele turno.

#### 7. Retorno ao Orquestrador

A jogada escolhida é retornada para o orquestrador da partida contendo:

- professor selecionado;
- posição de destino;
- posição da mentoria.

Exemplo:

```json
{
  "professor": "REY",
  "move_to": {
    "row": 3,
    "col": 1
  },
  "mentor_at": {
    "row": 2,
    "col": 2
  }
}
```

## Características do Agente

A ordem de prioridade utilizada pelo agente é:

1. Impedir vitória imediata do adversário
2. Posicionar professores em níveis mais altos
3. Aproveitar oportunidades de vitória
4. Construir estruturas favoráveis

O agente prioriza a eliminação de ameaças imediatas do adversário e, na ausência delas, procura fortalecer sua própria posição até criar oportunidades de vitória.

## Testes
