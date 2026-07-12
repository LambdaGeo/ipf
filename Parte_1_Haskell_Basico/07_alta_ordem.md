# Funções de Alta Ordem, Currying e Composição

Neste capítulo, encerraremos nossa primeira unidade explorando o recurso que confere a máxima expressividade ao paradigma funcional: as **Funções de Alta Ordem** (*Higher-Order Functions*). Ao tratar funções como valores comuns, aprenderemos a parametrizar comportamentos, reutilizar padrões de iteração genéricos (`map`, `filter`, `fold`) e encadear transformações de dados de maneira matemática através da composição.

---

## 1. O que são Funções de Alta Ordem?

Uma **Função de Alta Ordem** é simplesmente uma função que atende a pelo menos um dos seguintes requisitos:
1. Recebe uma ou mais funções como argumento.
2. Retorna uma função como resultado.

Essa flexibilidade é viabilizada pelo fato de que, em Haskell, as funções são **Cidadãs de Primeira Classe** (*First-Class Citizens*). Elas podem ser armazenadas em estruturas de dados, passadas como parâmetros e manipuladas exatamente como inteiros, booleanos ou strings.

Considere a função `duasVezes`, que recebe uma função `f` e aplica essa função consecutivamente a um valor `x`:

```haskell
duasVezes :: (a -> a) -> a -> a
duasVezes f x = f (f x)
```

Podemos utilizá-la passando comportamentos diferentes como argumentos:

```haskell
Prelude> duasVezes (*2) 4
16

Prelude> duasVezes reverse [1, 2, 3]
[1, 2, 3]
```

---

## 2. Currying e Aplicação Parcial

Em Haskell, **todas as funções recebem formalmente apenas um argumento**. Quando declaramos uma função que parece aceitar múltiplos parâmetros, como `soma :: Int -> Int -> Int`, o compilador na verdade cria uma função que recebe o primeiro `Int` e retorna outra função, que por sua vez recebe o segundo `Int` e finalmente calcula o resultado. 

Esse processo de transformar uma função de múltiplos parâmetros em uma cadeia de funções de um único parâmetro é chamado de **Currying**.

### Aplicação Parcial
Como as funções funcionam por Currying, podemos chamá-las passando **menos argumentos** do que o total esperado. Isso nos retorna uma nova função especializada:

```haskell
-- Função base:
multiplicar :: Int -> Int -> Int
multiplicar x y = x * y

-- Aplicação parcial: passamos apenas o primeiro argumento
dobro :: Int -> Int
dobro = multiplicar 2

triplo :: Int -> Int
triplo = multiplicar 3
```

A aplicação parcial é um mecanismo fantástico para criar funções auxiliares dinâmicas na hora de passar para funções de alta ordem.

---

## 3. O Trio de Ouro: Map, Filter e Fold

A maioria dos processamentos sobre listas na programação funcional baseia-se em três funções de alta ordem que evitam o uso de laços recursivos manuais.

```text
       Lista de Entrada ─────► [ 1, 2, 3, 4, 5 ]
                                    │
       ┌───────────────┬────────────┴────────────┬──────────────┐
       ▼               ▼                         ▼              ▼
     [Map]          [Filter]                  [Foldr]        [Foldl]
  (Transformar)    (Selecionar)            (Acumular Dir) (Acumular Esq)
       │               │                         │              │
       ▼               ▼                         ▼              ▼
  [ 2,4,6,8,10 ]   [ 2, 4 ]                     15              15
```

### 1. `map`
A função `map` recebe uma função transformadora e uma lista, aplicando a função a cada elemento individual da lista para gerar uma nova lista de resultados de mesmo tamanho.

```haskell
map :: (a -> b) -> [a] -> [b]
map _ []     = []
map f (x:xs) = f x : map f xs
```

```haskell
Prelude> map (+10) [1, 2, 3]
[11, 12, 13]
```

### 2. `filter`
A função `filter` recebe uma função predicado (que retorna `True` ou `False`) e uma lista, retornando uma nova lista contendo apenas os elementos que satisfizeram o predicado.

```haskell
filter :: (a -> Bool) -> [a] -> [a]
filter _ []     = []
filter p (x:xs)
    | p x       = x : filter p xs
    | otherwise = filter p xs
```

```haskell
Prelude> filter even [1..6]
[2, 4, 6]
```

### 3. `foldr` e `foldl` (Acumuladores)
A família `fold` (também conhecida como *reduce* em outras linguagens) serve para reduzir ou acumular os elementos de uma lista em um único valor final. Ela recebe um valor inicial (um elemento neutro), uma função acumuladora e uma lista.

* **`foldr` (Fold Right)**: Associa os elementos da direita para a esquerda. É útil para trabalhar com listas infinitas devido à avaliação preguiçosa.
* **`foldl` (Fold Left)**: Associa da esquerda para a direita. É mais eficiente para acumular valores de forma estrita em computações numéricas.

Exemplo de soma de uma lista usando `foldr`:

```haskell
somaLista :: [Int] -> Int
somaLista = foldr (+) 0
```

---

## 4. Composição de Funções e Point-Free Style

Na matemática, se temos duas funções $f(x)$ e $g(x)$, a composição de ambas é dada por $(f \circ g)(x) = f(g(x))$. Em Haskell, representamos esse operador de composição por meio do caractere ponto **`.`**:

```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
f . g = \x -> f (g x)
```

Isso nos permite encadear transformações de dados de forma incrivelmente limpa, construindo pipelines de execução:

```haskell
-- Função que dobra um número e depois soma 1:
dobroMaisUm :: Int -> Int
dobroMaisUm = (+1) . (*2)
```

### Estilo Point-Free (Livre de Pontos)
Note que na definição de `dobroMaisUm = (+1) . (*2)`, nós não declaramos o argumento da função (`x`). Nós apenas declaramos como as funções se combinam. 

Essa omissão do argumento de entrada é chamada de **Point-Free Style** e resulta em códigos muito limpos, focados puramente na combinação de funções e no fluxo dos dados.

Com isso, encerramos a **Unidade 1**! Agora você domina as bases teóricas do paradigma funcional e a modelagem matemática básica no Haskell.