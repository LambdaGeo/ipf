# Lista de Exercícios: Haskell Avançado (Tipos e IO)

Esta página contém exercícios de fixação sobre tipos algébricos de dados (ADTs) e programação interativa (IO) em Haskell.

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

### Parte 1 – Fundamentos de IO

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

### Parte 2 – Lendo e escrevendo Strings

1. Implemente uma função que peça o nome do usuário e o cumprimente.
    
    ```haskell
    > Qual eh o seu nome?
    Sergio
    Bem vindo Sergio!
    
    ```
    
2. Escreva um programa que leia duas linhas do teclado e depois imprima a concatenação delas.

---

### Parte 3 – Do notation

1. Reescreva o seguinte programa sem usar `do` (usando `>>=`):
    
    ```haskell
    main = do
      nome <- getLine
      putStrLn ("Oi, " ++ nome)
    
    ```
    
2. Escreva um programa que peça a idade do usuário e diga se ele é maior de idade ou não.

---

### Parte 4 – Manipulação de arquivos

1. Escreva um programa que leia o conteúdo de um arquivo `"entrada.txt"` e imprima na tela.
2. Crie uma função que copie o conteúdo de `"entrada.txt"` para `"saida.txt"`.
3. Adapte o programa de remoção de stopwords (do exemplo) para que o nome dos arquivos de entrada e saída seja pedido ao usuário via teclado.

---

### Parte 5 – Desafios

1. Implemente um programa que conte quantas linhas existem em um arquivo de texto.
2. Escreva uma função `main` que:
    - pergunte ao usuário um número `n`,
    - leia uma lista de números de um arquivo,
    - some apenas os `n` primeiros números,
    - grave o resultado em outro arquivo.
3. Escreva um mini “chat”: o programa deve ler uma linha do usuário e imprimir de volta a mesma linha em maiúsculas até que ele digite `"sair"`.

---