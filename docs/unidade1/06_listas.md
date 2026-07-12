# Listas, Recursão e Compreensão

As listas são a estrutura de dados mais fundamental e amplamente utilizada na programação funcional. Neste capítulo, estudaremos a definição de listas em Haskell, aprenderemos a realizar operações recursivas sobre elas por meio de casamento de padrões, e exploraremos a sintaxe expressiva de compreensões de listas.

---

## 1. O que é uma Lista em Haskell?

Em Haskell, uma lista é uma coleção homogênea de elementos, o que significa que **todos os elementos devem ter exatamente o mesmo tipo**. A estrutura de dados de uma lista é inerentemente **recursiva** e implementada como uma lista simplesmente encadeada.

Uma lista em Haskell é definida formalmente por dois construtores:
1. **Lista Vazia (`[]`)**: Representa a ausência de elementos.
2. **O Construtor Cons (`:`)**: Um operador que recebe um elemento (a cabeça) e o anexa no início de outra lista (a cauda).

Por exemplo, a lista `[1, 2, 3, 4]` é avaliada de forma encadeada como:

```haskell
lista = 1 : 2 : 3 : 4 : []
```

### Açúcares Sintáticos (Syntax Sugar)
Escrever o operador `:` consecutivamente seria muito verboso. Haskell oferece açúcares sintáticos amigáveis para a criação de listas:

* **Listas Explícitas**: `[1, 2, 3, 4]`
* **Faixas de Valores (Ranges)**: `[1..10]` gera uma lista de 1 a 10.
* **Ranges com Passo**: `[0, 2..10]` gera a lista de pares `[0, 2, 4, 6, 8, 10]`.
* **Strings**: Lembre-se que `"Haskell"` é apenas uma notação abreviada para a lista de caracteres `['H', 'a', 's', 'k', 'e', 'l', 'l']`.

---

## 2. Funções Essenciais sobre Listas

A biblioteca padrão do Haskell fornece funções prontas para inspecionar e transformar listas:

* **`head`**: Retorna o primeiro elemento (a cabeça) da lista. Exige que a lista não esteja vazia.
* **`tail`**: Retorna a lista sem o seu primeiro elemento (a cauda).
* **`null`**: Retorna `True` se a lista estiver vazia.
* **`length`**: Calcula o número de elementos na lista.
* **`(++)`**: Concatena duas listas. Ex: `[1, 2] ++ [3, 4] = [1, 2, 3, 4]`.
* **`(!!)`**: Acessa um elemento por índice (0-indexado). Ex: `[10, 20, 30] !! 1 = 20`.
* **`take`**: Extrai os primeiros $n$ elementos de uma lista.
* **`drop`**: Remove os primeiros $n$ elementos de uma lista.

---

## 3. Pattern Matching e Recursão sobre Listas

Como a estrutura de uma lista é definida pelo construtor de cabeça/cauda (`:`), podemos utilizar o casamento de padrões para separar a cabeça do restante da lista utilizando a notação `(x:xs)` (onde `x` é a cabeça e `xs` é a cauda).

### Exemplo 1: Somando elementos de uma lista
Para calcular a soma de uma lista de números recursivamente, definimos dois casos:
1. **Caso Base**: A soma de uma lista vazia `[]` é `0`.
2. **Caso Recursivo**: A soma de uma lista não vazia `(x:xs)` é a cabeça `x` somada ao resultado da chamada recursiva para a cauda `xs`.

```haskell
somarLista :: Num a => [a] -> a
somarLista []     = 0
somarLista (x:xs) = x + somarLista xs
```

### Exemplo 2: O Clássico Quicksort em Haskell
A expressividade do casamento de padrões e da recursão sobre listas permite implementar o famoso algoritmo de ordenação **Quicksort** de forma incrivelmente compacta em Haskell:

```haskell
quicksort :: Ord a => [a] -> [a]
quicksort []     = []
quicksort (x:xs) = quicksort menores ++ [x] ++ quicksort maiores
  where
    menores = [a | a <- xs, a <= x]
    maiores = [a | a <- xs, a >  x]
```

Nesta função, tomamos a cabeça `x` como o pivô. Usamos compreensões de lista para filtrar os elementos da cauda `xs` que são menores que o pivô (`menores`) e maiores que o pivô (`maiores`), ordenando cada uma dessas partes de forma recursiva antes de juntar tudo.

---

## 4. Compreensão de Listas

A **Compreensão de Listas** é uma notação matemática poderosa para filtrar e transformar coleções de dados, baseada na definição matemática de conjuntos. Sua sintaxe básica é:

```text
[ expressao | gerador, filtros ]
```

### Componentes:
* **Gerador (`x <- lista`)**: Extrai valores da lista um por um.
* **Filtros (Predicados Booleanos)**: Expressões booleanas que determinam se o valor gerado deve ser incluído na computação.

### Exemplos de Compreensão:

1. **Dobrar apenas os números ímpares de 1 a 10**:
   ```haskell
   Prelude> [x * 2 | x <- [1..10], odd x]
   [2, 6, 10, 14, 18]
   ```

2. **Gerar todas as coordenadas de um tabuleiro 3x3 (Produto Cartesiano)**:
   ```haskell
   Prelude> [(x, y) | x <- [1..3], y <- [1..3]]
   [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)]
   ```

No próximo capítulo, veremos como abstrair loops e processamentos repetitivos de listas utilizando **Funções de Alta Ordem**.