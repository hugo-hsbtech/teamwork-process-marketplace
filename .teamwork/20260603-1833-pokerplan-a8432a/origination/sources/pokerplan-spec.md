# PokerPlan - Documento de Requisitos e Regras de Negócio

## Visão Geral

PokerPlan é uma plataforma virtual para realização de sessões de Planning Poker, permitindo que equipes realizem estimativas colaborativas de forma remota, mantendo todas as regras tradicionais do processo físico.

---

# Conceitos Fundamentais

## Objetivo

Permitir que equipes estimem esforço, complexidade ou tamanho relativo de tarefas através de votações secretas e consenso colaborativo.

## Participantes

### Host / Facilitador
Responsável por conduzir a sessão.

Permissões:
- Criar sala
- Gerenciar participantes
- Adicionar tarefas
- Iniciar votações
- Revelar cartas
- Encerrar rodadas
- Definir consenso

### Participante

Permissões:
- Entrar na sala
- Visualizar tarefas
- Votar
- Participar das discussões
- Alterar voto antes da revelação

### Observador

Permissões:
- Acompanhar a sessão
- Visualizar resultados
- Não pode votar

---

# Escalas de Estimativa

## Fibonacci

- 0
- 1
- 2
- 3
- 5
- 8
- 13
- 21
- 34
- 55
- 89
- ?
- ∞
- ☕

## T-Shirt

- PP
- P
- M
- G
- GG

---

# Fluxo Tradicional

## Etapa 1 - Apresentação da Tarefa

O facilitador apresenta a tarefa que será estimada.

Exemplo:

- Implementar Login Social
- Criar Dashboard Financeiro
- Desenvolver Integração com API

## Etapa 2 - Discussão Inicial

Os participantes esclarecem dúvidas antes da votação.

## Etapa 3 - Votação Secreta

Cada participante escolhe uma carta.

Regras:
- Os votos não podem ser visualizados pelos demais participantes.
- O voto pode ser alterado até a revelação.

## Etapa 4 - Revelação

Os votos são exibidos simultaneamente.

## Etapa 5 - Discussão

Quando existem divergências significativas, os participantes discutem os motivos.

Recomendação:
- Ouvir o menor voto.
- Ouvir o maior voto.

## Etapa 6 - Nova Rodada

Uma nova votação pode ser realizada após a discussão.

## Etapa 7 - Consenso

O grupo define a estimativa final.

Observação:
O consenso não precisa ser média matemática.

## Etapa 8 - Encerramento

A tarefa recebe sua estimativa final e a próxima tarefa é iniciada.

---

# Regras de Negócio

## RN-001

Os votos devem permanecer secretos até a revelação.

## RN-002

O participante pode alterar seu voto enquanto a rodada estiver aberta.

## RN-003

Somente o host pode revelar os votos.

## RN-004

Opcionalmente a sala pode utilizar revelação automática quando todos tiverem votado.

## RN-005

Somente o host pode encerrar uma rodada.

## RN-006

Uma tarefa pode possuir múltiplas rodadas.

## RN-007

O histórico de todas as rodadas deve ser armazenado.

## RN-008

Participantes que entrarem após o encerramento da rodada não podem votar retroativamente.

## RN-009

O host pode cancelar uma rodada.

## RN-010

A estimativa final deve ser registrada separadamente dos votos individuais.

---

# Modelo Conceitual

## Sala

Campos sugeridos:

- id
- nome
- código
- proprietário
- status
- data_criação
- data_encerramento

Status:

- CREATED
- IN_PROGRESS
- FINISHED

## Participante

Campos sugeridos:

- id
- nome
- avatar
- online
- tipo

Tipos:

- HOST
- PARTICIPANT
- OBSERVER

## Tarefa

Campos sugeridos:

- id
- título
- descrição
- ordem
- estimativa_final
- status

Status:

- PENDING
- VOTING
- ESTIMATED

## Rodada

Campos sugeridos:

- id
- task_id
- número
- status
- data_abertura
- data_fechamento

Status:

- OPEN
- REVEALED
- CLOSED

## Voto

Campos sugeridos:

- id
- rodada_id
- participante_id
- valor
- comentário_opcional
- data_voto

---

# Fluxo Digital

## Criação da Sala

O host cria uma sala e recebe um link compartilhável.

Exemplo:

https://pokerplan.app/r/ABC123

## Entrada dos Participantes

Participantes entram utilizando apenas um nome.

## Cadastro das Tarefas

O host adiciona tarefas manualmente ou através de integrações.

## Início da Votação

A tarefa atual é apresentada para todos.

## Votação

Os participantes selecionam suas cartas.

## Progresso

O sistema exibe apenas a quantidade de votos recebidos.

Exemplo:

5 de 7 participantes votaram.

## Revelação

Os votos são exibidos simultaneamente.

## Discussão

Participantes discutem divergências.

## Nova Rodada

Opcional.

## Consenso

O host define a estimativa final.

---

# Estatísticas

Após a revelação o sistema pode calcular:

- Menor valor
- Maior valor
- Média
- Mediana
- Moda
- Desvio entre votos

---

# Funcionalidades do MVP

## MVP V1

- Criar sala
- Compartilhar link
- Entrar sem autenticação
- Cadastro de tarefas
- Votação secreta
- Revelação de votos
- Múltiplas rodadas
- Definição de consenso
- Histórico da sessão

## MVP V1.1

- Cronômetro
- Auto Reveal
- Estatísticas automáticas
- Exportação CSV

## MVP V2

- Integração com Jira
- Integração com Linear
- Times permanentes
- Histórico organizacional
- Dashboard de métricas
- Comparação entre rodadas
- Comentários anônimos por voto

---

# Diferenciais Recomendados

## Comentário por Voto

Permitir justificar estimativas.

Exemplo:

"Votei 13 porque existe integração externa."

## Comparação de Rodadas

Visualizar evolução do consenso.

## Sugestão de Consenso

O sistema pode sugerir:

- Média
- Moda
- Mediana

## Exportação

Formatos:

- CSV
- Excel
- PDF

---

# Objetivo do Produto

Digitalizar completamente a dinâmica tradicional do Planning Poker, preservando todas as regras de colaboração, votação secreta, discussão e consenso, adicionando recursos digitais que aumentem produtividade, rastreabilidade e transparência das estimativas.
