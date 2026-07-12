# Lista de Exercícios Consolidados (Haskell)

Esta página contém todas as listas de exercícios práticos da Unidade 1, servindo como material de estudo e fixação dos conceitos fundamentais de Haskell.

---


## 📘 Lista 1: Funções Básicas e Recursão em Haskell

Conteúdo: [https://profsergiocosta.notion.site/3-Fun-es-c7eaa942530f4ccbaadd0aed2f9ec13e](https://app.notion.com/p/3-Fun-es-c7eaa942530f4ccbaadd0aed2f9ec13e?pvs=21)

### 1. Funções básicas

1. Defina uma função `quad` que receba um número e devolva o seu quadrado.
2. Escreva uma função `hipotenusa` que receba os catetos de um triângulo retângulo e devolva a hipotenusa.
    - **Dica:** use `sqrt`.

---

### 2. Definições locais (`where` e `let`)

1. Reescreva a função `hipotenusa` usando `where` para definir variáveis auxiliares.
2. Reescreva a mesma função usando `let … in …`.

---

### 3. Condicionais e guards

1. Defina a função `sinal` usando `if-then-else` que devolva:
    - `1` se o número for negativo
    - `0` se for zero
    - `1` se for positivo
2. Reescreva a função `sinal` usando **guards**.
3. Implemente a função `classificaNota` que recebe um número (0–10) e retorna:
    - `"Reprovado"` se menor que 5
    - `"Recuperação"` se entre 5 e 6.9
    - `"Aprovado"` se maior ou igual a 7.

---

### 4. Pattern Matching

1. Reescreva a função `negar :: Bool -> Bool` usando **pattern matching**.
2. Defina a função `diasSemana` que recebe um número de 1 a 7 e retorna o nome do dia correspondente (1 → "Domingo", 2 → "Segunda", etc.).
    - Use **padrões explícitos**.
3. Defina a função fatorial com **pattern matching** nos casos base.

---

### 5. Recursão

1. Implemente a função `potencia b e` que calcula beb^ebe usando recursão (sem usar `(^)`).
2. Escreva uma função `mdc a b` que calcule o máximo divisor comum (algoritmo de Euclides).
3. Defina a sequência de Fibonacci de forma recursiva simples.
4. Refaça a função de Fibonacci usando a técnica de **recursão em cauda**.

---

## 📙 Lista 2: Listas e Compreensão em Haskell

### 1. Definição e Criação de Listas

1. Escreva manualmente a lista `[5,6,7]` usando apenas o construtor `(:)`.
2. Use **syntax sugar** para criar:
    - a lista de números de 1 a 20.
    - a lista de números pares de 0 a 20.
    - a lista de múltiplos de 3 de 0 a 30.
3. Represente a string `"HASKELL"` como lista de caracteres.

---

### 2. Funções e Operadores sobre Listas

1. Dada a lista `lista = [10..20]`, calcule:
    - `head lista`
    - `tail lista`
    - `take 5 lista`
    - `drop 7 lista`
    - `lista !! 3`
2. Escreva expressões em Haskell que retornem:
    - o tamanho da lista `[1..100]`.
    - a soma dos números de 1 a 50.
    - o produto dos números de 1 a 5.
3. Mostre duas formas diferentes de construir a lista `[1..10]` a partir da concatenação de sublistas.

---

### 3. Pattern Matching

1. Implemente uma função `primeiroOuZero :: [Int] -> Int` que retorna o primeiro elemento da lista, ou `0` se a lista for vazia.
2. Implemente uma função `segundoElemento :: [a] -> Maybe a` que retorna o segundo elemento de uma lista (ou `Nothing` se não existir).

---

### 4. Recursão em Listas

1. Implemente a função `meuLength :: [a] -> Int` que calcula o tamanho de uma lista usando recursão.
2. Implemente a função `meuSum :: Num a => [a] -> a` que soma os elementos de uma lista usando recursão.
3. Reescreva a função `reverse` utilizando recursão.
4. Implemente a função `meuDrop :: Int -> [a] -> [a]`, removendo os `n` primeiros elementos de uma lista.

---

### 5. Funções com Vários Argumentos

1. Implemente a função `meuZip :: [a] -> [b] -> [(a,b)]` que une duas listas em uma lista de pares.
2. Teste sua função `meuZip` com as listas `[1,2,3]` e `['a','b','c']`.

---

### 6. Compreensão de Listas

1. Gere, usando compreensão de listas:
- uma lista com os quadrados dos números de 1 a 10.
- uma lista com apenas os números pares de 1 a 20.
- o produto cartesiano entre `[1,2,3]` e `[‘a’,’b’]`.
1. Defina a função `divisores :: Int -> [Int]` que retorna a lista de todos os divisores de um número.
2. Defina a função `ehPrimo :: Int -> Bool` que verifica se um número é primo usando `divisores`.
3. Usando compreensão de listas, gere todos os pares `(x,y)` com `1 <= x < y <= 10` tais que `x + y` seja par.

---

## 📗 Lista 3: Funções de Alta Ordem e Composição

### 🔹 Parte 1 – Aquecendo com HOFs

1. Defina a função `duasVezes :: (a -> a) -> a -> a` e teste com:
    - `duasVezes (*3) 2`
    - `duasVezes reverse [1,2,3]`
2. Usando **aplicação parcial**, defina:
    - `triplica = (*3)`
    - `mais10 = (+10)`
        
        Teste essas funções em valores diferentes.
        

---

### 🔹 Parte 2 – Map

1. Use `map` para:
    - Somar 1 a todos os elementos da lista `[10,20,30]`
    - Converter todos os números de `[1..5]` em valores booleanos indicando se são pares.
2. Defina uma função `maiusculas :: [String] -> [String]` que transforma todas as palavras de uma lista em maiúsculas usando `map`.

---

### 🔹 Parte 3 – Filter

1. Use `filter` para:
    - Selecionar apenas os números maiores que 100 da lista `[50,150,200,80,120]`.
    - Remover os espaços em branco de uma string.
2. Combine `map` e `filter`:
    
    Defina `quadradosPares :: [Int] -> [Int]` que devolve os quadrados apenas dos números pares de uma lista.
    

---

### 🔹 Parte 4 – Fold (Reduce)

1. Reescreva com `foldr`:
    - A soma (`sum`) de uma lista
    - O produto (`product`) de uma lista
    - O tamanho (`length`) de uma lista
2. Defina uma função `concatena :: [String] -> String` usando `foldr` que junte todas as strings de uma lista em uma só.

---

### 🔹 Parte 5 – Outras HOFs

1. Use:
    - `all` para verificar se todos os números de `[2,4,6,8]` são pares.
    - `any` para verificar se há algum múltiplo de 7 em `[10..20]`.
    - `takeWhile` para pegar os primeiros números pares de `[2,4,6,7,8,10]`.
    - `dropWhile` para descartar os primeiros números pares da mesma lista.

---

### 🔹 Parte 6 – Composição

1. Defina `dobroMaisUm = (+1) . (*2)` e teste em `[1..5]` com `map`.
2. Escreva uma função `processaLista :: [Int] -> [Int]` que:
- multiplique todos os números por 2,
- some 1,
- filtre apenas os números maiores que 10.
    
    Use **composição** para encadear os passos.
    
1. (Desafio) Defina `compose :: [a -> a] -> (a -> a)` que recebe uma lista de funções e retorna a composição delas.
    
    Teste com:
    

```haskell
compose [(+1), (*2), (^2)] 3
-- deve aplicar (^2), depois (*2), depois (+1)

```

---

---

## 📕 Lista 4: Tipos Algébricos, Sinônimos e Pattern Matching

### **1. Sinônimos de tipos (`type`)**

1. Crie um **sinônimo de tipo** `Nome` para `String` e `Idade` para `Int`.
    
    Escreva uma função `apresenta :: Nome -> Idade -> String` que retorne `"Meu nome é X e tenho Y anos"`.
    
2. Explique a diferença entre `type` e `newtype` em Haskell.
3. Crie um **sinônimo de tipo** `Ponto` para `(Float, Float)`.
    
    Escreva uma função `distancia :: Ponto -> Ponto -> Float` que calcule a distância euclidiana entre dois pontos.
    

---

### **2. Novos tipos (`newtype`)**

1. Crie um `newtype` chamado `Dolar` que envolve `Float`.
    
    Escreva uma função `converterParaReal :: Dolar -> Float` considerando 1 Dólar = 5,50 BRL.
    
2. Explique por que `newtype` é mais eficiente que `data` para tipos que envolvem **um único construtor com um único campo**.

---

### **3. Tipos algebricos (`data`)**

1. Defina um tipo `DiaSemana` com os sete dias da semana.
    
    Escreva uma função `proximoDia :: DiaSemana -> DiaSemana`.
    
2. Defina um tipo `Cor` com `Vermelho | Verde | Azul | Amarelo`.
    
    Crie uma função `ehPrimaria :: Cor -> Bool` que retorne `True` se a cor for primária.
    
3. Crie um tipo `Forma` com `Circulo Float | Retangulo Float Float | Quadrado Float`.
    
    Escreva uma função `area :: Forma -> Float` que calcule a área de qualquer forma.
    
4. Crie um tipo `Conta` com `Corrente Float | Poupanca Float Float` (saldo e juros).
    
    Escreva uma função `saldoTotal :: Conta -> Float` que retorne o saldo total considerando juros na poupança.
    

---

### **4. Pattern Matching**

1. Reescreva a função `area` do exercício 8 usando **pattern matching**.
2. Escreva uma função `ehFimDeSemana :: DiaSemana -> Bool` usando pattern matching.
3. Crie uma função `descricaoConta :: Conta -> String` que descreva a conta (`"Conta Corrente: R$..."` ou `"Conta Poupança: R$... com juros..."`).
4. Escreva uma função `somaPontos :: Ponto -> Ponto -> Ponto` usando pattern matching em tuplas.

---

### **5. Funções que usam tipos algebricos**

1. Crie um tipo `Resultado` com `Sucesso String | Erro String`.
    
    Escreva uma função `processar :: Bool -> Resultado` que retorne `Sucesso "OK"` se `True`, ou `Erro "Falha"` se `False`.
    
2. Crie um tipo `Expressao` para representar expressões matemáticas simples:
    
    `Valor Int | Soma Expressao Expressao | Multiplicacao Expressao Expressao`.
    
    Escreva uma função `avaliar :: Expressao -> Int` que calcule o valor da expressão.
    
3. Crie um tipo `Opcao` com `Sim | Nao | Talvez`.
    
    Escreva uma função `resposta :: Opcao -> String` que retorne `"Aceito"`, `"Recuso"` ou `"Indeciso"`.
    

---

### **6. Exercícios mistos avançados**

1. Crie um tipo `Pessoa` com `Nome String` e `Idade Int`.
    
    Escreva uma função `maiorIdade :: Pessoa -> Bool` usando pattern matching.
    
2. Crie um tipo `Livro` com `Titulo String | Autor String | Ano Int`.
    
    Escreva uma função `descricaoLivro :: Livro -> String`.
    
3. Defina um tipo `Arvore a` com `Folha a | No (Arvore a) (Arvore a)`.
    
    Escreva uma função `contaNos :: Arvore a -> Int` que conte os nós de uma árvore.
    
4. Escreva uma função `mapArvore :: (a -> b) -> Arvore a -> Arvore b` que aplique uma função a todos os elementos da árvore.

---

## 📓 Lista 5: Entrada/Saída (IO) e Programação Interativa

[https://profsergiocosta.notion.site/6-Programas-interativos-1d9441f881934142bba7ed420410e978](https://app.notion.com/p/6-Programas-interativos-1d9441f881934142bba7ed420410e978?pvs=21)

### 🔹 Parte 1 – Fundamentos de IO

1. Escreva um programa que leia um caractere do teclado e o imprima duas vezes na tela.
    
    ```haskell
    -- exemplo de execução
    > a
    aa
    
    ```
    
2. Crie um programa que leia dois caracteres e os imprima separados por um espaço.
    
    ```haskell
    > a
    > b
    a b
    
    ```
    
3. Escreva uma versão simplificada do `putStrLn`, chamada `putStrSimples`, que recebe uma string e a imprime caractere por caractere, finalizando com `\n`.

---

### 🔹 Parte 2 – Lendo e escrevendo Strings

1. Implemente uma função que peça o nome do usuário e o cumprimente.
    
    ```haskell
    > Qual eh o seu nome?
    Sergio
    Bem vindo Sergio!
    
    ```
    
2. Escreva um programa que leia duas linhas do teclado e depois imprima a concatenação delas.

---

### 🔹 Parte 3 – Do notation

1. Reescreva o seguinte programa sem usar `do` (usando `>>=`):
    
    ```haskell
    main = do
      nome <- getLine
      putStrLn ("Oi, " ++ nome)
    
    ```
    
2. Escreva um programa que peça a idade do usuário e diga se ele é maior de idade ou não.

---

### 🔹 Parte 4 – Manipulação de arquivos

1. Escreva um programa que leia o conteúdo de um arquivo `"entrada.txt"` e imprima na tela.
2. Crie uma função que copie o conteúdo de `"entrada.txt"` para `"saida.txt"`.
3. Adapte o programa de remoção de stopwords (do exemplo) para que o nome dos arquivos de entrada e saída seja pedido ao usuário via teclado.

---

### 🔹 Parte 5 – Desafios

1. Implemente um programa que conte quantas linhas existem em um arquivo de texto.
2. Escreva uma função `main` que:
    - pergunte ao usuário um número `n`,
    - leia uma lista de números de um arquivo,
    - some apenas os `n` primeiros números,
    - grave o resultado em outro arquivo.
3. Escreva um mini “chat”: o programa deve ler uma linha do usuário e imprimir de volta a mesma linha em maiúsculas até que ele digite `"sair"`.

---