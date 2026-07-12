# 4. Listas

Já vimos um pouco sobre o tipo lista e nas atividades no repl.it. 

- **Definição e criação de listas**
    
    [https://www.youtube.com/watch?v=GCAiO8IYcJo](https://www.youtube.com/watch?v=GCAiO8IYcJo)
    
    - Uma das principais estruturas em linguagens funcionais.
    - Representa uma coleção de valores de um determinado tipo.
    - Todos os valores são sempre do **mesmo** tipo.
    - **Definição recursiva**
        
        Uma lista ou é   vazia `[]` ou ela tem uma cabeça do tipo genérico `*a*` , e uma cauda do tipo lista de `*a*`.
        
        ```haskell
        data [] a = [] | a : [a]
        ```
        
        (:) - construtor da lista 
        
        Seguindo essa definição, a lista `[1, 2, 3, 4]` é representada por:
        
        ```haskell
        lista = 1 : 2 : 3 : 4 :[]
        ```
        
        ![nse-5945902912878263011-887793285.png](4%20Listas/nse-5945902912878263011-887793285.png)
        
        Veremos mais a frente sobre criação de tipos de dados algébricos. Então entenderão melhor a definição anterior.
        
        - **Criação**
            
            A forma anterior de escrever uma lista é muito verbosa. Então existem diversos *syntax sugar* para criação de listas (ainda bem):
            
            ```haskell
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ```
            
            Faixa de valores inclusivos:
            
            ```haskell
            [1..10]   == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ```
            
            Faixa de valores inclusivos com tamanho do passo:
            
            ```haskell
            [0,2..10] == [0, 2, 4, 6, 8, 10]
            ```
            
            Uma `String` no Haskell é uma lista de `Char`:
            
            ```haskell
            > "Ola Mundo" == ['O','l','a',' ','M','u','n','d','o']
            ```
            
            Lista infinita:
            
            ```haskell
            [0,2..]   == [0, 2, 4, 6, 8, 10,..]
            ```
            
            - Ao infinito e além
                
                Como o Haskell permite a criação de listas infinitas?
                
                Uma vez que a avaliação é preguiçosa, ao fazer:
                
                ```haskell
                lista = [0,2..]
                ```
                
                ele cria apenas uma **promessa** de lista.
                
                Efetivamente ele faz:
                
                ```haskell
                lista = 0 : 2 : geraProximo
                ```
                
                sendo `geraProximo` uma função que gera o próximo elemento da lista.
                
                Conforme for necessário, ele gera e avalia os elementos da lista sequencialmente.
                
                Então a lista infinita não existe em memória, apenas uma função que gera quantos elementos você precisar dela.
                
- **Funções e operadores sobre listas**
    
    [https://www.youtube.com/watch?v=vXFYAEcfhpw](https://www.youtube.com/watch?v=vXFYAEcfhpw)
    
    - Recuperar elementos
        
        O operador `!!` recupera o i-ésimo elemento da lista, com índice começando do 0:
        
        ```haskell
        > lista = [0..10]
        > lista !! 2
        2
        ```
        
        Note que esse operador é custoso para listas ligadas! Não abuse dele!
        
        Essa imagem do livro [Learn You a Haskell for Great Good](http://learnyouahaskell.com/starting-out#an-intro-to-lists) ilustra essas funções.
        
        ![](4%20Listas/Untitled.png)
        
        A função `head` retorna o primeiro elemento da lista:
        
        ```haskell
        > head [0..10]
        0
        ```
        
        A função `tail` retorna a lista sem o primeiro elemento (sua cauda):
        
        ```haskell
        > tail [0..10]
        [1,2,3,4,5,6,7,8,9,10]
        ```
        
        - Outras funções
            
            A função `take` retorna os `n` primeiros elementos da lista:
            
            ```haskell
            > take 3 [0..10]
            [0,1,2]
            ```
            
            E a função `drop` retorna a lista sem os `n` primeiros elementos:
            
            ```haskell
            > drop 6 [0..10]
            [6,7,8,9,10]
            ```
            
        
    - Tamanho da lista
        
        O tamanho da lista é dado pela função `length`:
        
        ```haskell
        > length [1..10]
        10
        ```
        
    - Somatória e Produto
        
        As funções `sum` e `product` retorna a somatória e produtória da lista:
        
        ```haskell
        > sum [1..10]
        55
        > product [1..10]
        3628800
        ```
        
    - Concatenando listas
        
        Para concatenar utilizamos o operador `++` para concatenar duas listas ou o `:` para adicionar um valor ao começo da lista:
        
        ```haskell
        > [1..3] ++ [4..10] == [1..10]
        True
        > 1 : [2..10] == [1..10]
        True
        ```
        
- **Pattern Matching**
    
    [https://www.youtube.com/watch?v=-t18RppTDjI](https://www.youtube.com/watch?v=-t18RppTDjI)
    
    Quais padrões podemos capturar em uma lista?
    
    - Lista vazia: `[]`
    - Lista com um elemento: `(x : [])`
    - Lista com um elemento seguido de vários outros: `(x : xs)`
    
    E qualquer um deles pode ser substituído pelo curinga `_`.
    
    ```haskell
    f [] = 0
    f [x] = x
    f (x:xs) = 
    ```
    
    Por exemplo, para saber se uma lista está vazia utilizamos a função `null`:
    
    ```haskell
    null :: [a] -> Bool
    null [] = True
    null _  = False
    ```
    
    A função `length` poderia ser implementada recursivamente da seguinte forma:
    
    ```haskell
    length :: [a] -> Int
    length [] = 0
    length (_:xs) = 1 + length xs
    ```
    
- **Recursão em lista**
    
    [https://app.notion.com](https://app.notion.com)
    
    A definição de uma lista encadeada é recursiva, de modo que funções recursivas são muito bem definidas para essa estrutura.
    
    ```haskell
    sum :: Num a => [a] -> a
    sum []     = 0
    sum (n:ns) = n + sum ns
    
    ```
    
    - Como ficaria a função `product` baseado na função `sum` ?
        
        ```haskell
        product :: Num a => [a] -> a
        product []     = 1
        product (n:ns) = n * product ns
        
        ```
        
    - E a função `length`?
        
        ```haskell
        length :: [a] -> Int
        length []     = 0
        length (n:ns) = 1 + length ns
        
        ```
        
    - Padrões e funções de alta ordem
        
        Reparem que muitas soluções recursivas (principalmente com listas) seguem um mesmo esqueleto. Uma vez que vocês dominem esses padrões, fica fácil determinar uma solução.
        
        Nas próximas aulas vamos criar funções que generalizam tais padrões.
        
    - Exemplo: Invertendo uma lista
        
        Considere a função `reverse`:
        
        ```haskell
        > :t reverse
        reverse :: [a] -> [a]
        > reverse [1,2,3]
        [3,2,1]
        
        ```
        
        Como poderíamos implementá-la?
        
        Vamos considerar alguns casos, para poder então generalizar.
        
        - Caso 1:
            
            O inverso de uma lista vazia, é vazia:
            
            ```haskell
            reverse :: [a] -> [a]
            reverse [] = []
            ```
            
        
        - Caso 2:
            
            O inverso de uma lista com um elemento, é ela mesma:
            
            ```haskell
            reverse :: [a] -> [a]
            reverse []  = []
            reverse [x] = [x]
            
            ```
            
        - Caso 3:
            
            O inverso de uma lista com dois elementos é:
            
            ```haskell
            reverse :: [a] -> [a]
            reverse []    = []
            reverse [x]   = [x]
            reverse [x,y] = [y,x]
            
            ```
            
        - Caso 4:
            
            O inverso de uma lista com três elementos é:
            
            ```haskell
            reverse :: [a] -> [a]
            reverse []      = []
            reverse [x]     = [x]
            reverse [x,y]   = [y,x]
            reverse [x,y,z] = [z,y,x]
            
            ```
            
        - Generalizando
            
            Esse último caso base nos dá uma ideia de como generalizar! Note que:
            
            ```haskell
            > reverse [1,2,3] == reverse [2,3] ++ [1]
            
            ```
            
            - Então ....
                
                ```haskell
                reverse :: [a] -> [a]
                reverse []     = []
                reverse (x:xs) = reverse xs ++ [x]
                
                ```
                
    - Exemplo: vários argumentos
        
        Funções com mais de um argumento também podem ser definido usando recursão. Por exemplo:
        
        ```haskell
        Prelude> zip [1,2,3] [4,5,6]
        [(1,4),(2,5),(3,6)]
        ```
        
        - Casos bases:
            
            ```haskell
            zip :: [a] -> [b] -> [(a,b)]
            zip [] _ = []
            zip _ [] = []
            
            ```
            
        - Caso recursivo (generalizando):
            
            ```haskell
            zip :: [a] -> [b] -> [(a,b)]
            zip [] _          = []
            zip _ []          = []
            zip (x:xs) (y:ys) = (x,y) : zip xs ys
            
            ```
            
    - Dicas para criar uma função recursiva
        
        Vamos considerar a função `drop` que remove os `n` primeiros elementos de uma lista:
        
        ```haskell
        > drop 3 [1..10]
        [4,5,6,7,8,9,10]
        
        ```
        
        - Passo 1: defina a assinatura da função
            
            A função `drop` recebe um `Int` e uma lista e retorna outra lista, sem restrições:
            
            ```haskell
            drop :: Int -> [a] -> [a]
            
            ```
            
        - Passo 2: enumere os casos
            
            Para o primeiro argumento da função, podemos ter o caso trivial `0` que não faz nada e o caso genérico `n`.
            
            O segundo argumento pode ter a lista vazia `[]` e o caso genérico `(x:xs)`. Vamos criar as combinações desses casos:
            
            ```haskell
            drop :: Int -> [a] -> [a]
            drop 0 []     =
            drop 0 (x:xs) =
            drop n []     =
            drop n (x:xs) =
            
            ```
            
        - Passo 3: defina os casos simples
            
            Se eu não quero remover nada, retorno a própria lista, se eu quero remover algo de uma lista vazia, o retorno é vazio:
            
            ```haskell
            drop :: Int -> [a] -> [a]
            drop 0 []     = []
            drop 0 lista = lista
            drop n []     = []
            drop n (x:xs) =
            
            ```
            
        - Passo 4: defina os casos restantes
            
            Como remover o primeiro elemento de `(x:xs)`? Removendo `x` e retornando apenas `xs`.
            
            ```haskell
            drop :: Int -> [a] -> [a]
            drop 0 []     = []
            drop 0 (x:xs) = x:xs
            drop n []     = []
            drop n (x:xs) = drop (n-1) xs
            
            ```
            
        - Passo 5: Simplifique
            
            O primeiro e terceiro caso são redundantes, o segundo caso não precisa de pattern matching na lista:
            
            ```haskell
            drop :: Int -> [a] -> [a]
            drop _ []     = []
            drop 0 xs     = xs
            drop n (x:xs) = drop (n-1) xs
            
            ```
            
    
- **Compreensão de Listas**
    
    [https://www.youtube.com/watch?v=c6ke1skMvRI](https://www.youtube.com/watch?v=c6ke1skMvRI)
    
    Na matemática, quando falamos em conjuntos, definimos da seguinte forma:
    
    ![](4%20Listas/Untitled%201.png)
    
    que é lido como *x ao quadrado para todo x do conjunto de um a cinco*.
    
    No Haskell podemos utilizar uma sintaxe parecida:
    
    ```haskell
    > [x^2 | x <- [1..5]]
    [1,4,9,16,25]
    ```
    
    que é lido como *x ao quadrado tal que x vem da lista de valores de um a cinco*.mbem
    
    - Python também suporta compreensão de listas, porém um pouco mais verboso
        
        ```python
        >>> [i ** 2 for i in range (1,6)]
        [1, 4, 9, 16, 25]
        ```
        
    - As compreensões de lista são formadas por:
        - E**xpressão geradora**
            
            A expressão `x <- [1..5]` é chamada de **expressão geradora**, pois ela gera valores na sequência conforme eles forem requisitados. Outros exemplos:
            
            ```haskell
            > [toLower c | c <- "OLA MUNDO"]
            "ola mundo"
            > [(x, even x) | x <- [1,2,3]]
            [(1, False), (2, True), (3, False)]
            ```
            
            Podemos combinar mais do que um gerador e, nesse caso, geramos uma lista da combinação dos valores deles. Aqui estamos gerando um produto cartesiano:
            
            ```haskell
            >[(x,y) | x <- [1..4], y <- [4..5]]
            [(1,4),(1,5),(2,4),(2,5),(3,4),(3,5),(4,4),(4,5)]
            ```
            
            Se invertermos a ordem dos geradores, geramos a mesma lista mas em ordem diferente:
            
            ```haskell
            > [(x,y) | y <- [4..5], x <- [1..4]]
            [(1,4),(2,4),(3,4),(4,4),(1,5),(2,5),(3,5),(4,5)]
            ```
            
            Isso é equivalente a um laço `for` encadeado!
            
            - Geradores dependentes
                
                Um gerador pode depender do valor gerado pelo gerador anterior:
                
                ```haskell
                > [(i,j) | i <- [1..5], j <- [i+1..5]]
                [(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,4),(3,5),(4,5)]
                ```
                
                - Equivalente a:
                    
                    ```c
                    for (i=1; i<=5; i++) {
                      for (j=i+1; j<=5; j++) {
                         // faça algo
                      }
                    }
                    ```
                    
                - Exemplo: concat
                    
                    A função `concat` transforma uma lista de listas em uma lista única concatenada (conhecido em outras linguagens como `flatten`):
                    
                    ```haskell
                    > concat [[1,2],[3,4]]
                    [1,2,3,4]
                    ```
                    
                    Ela pode ser definida utilizando compreensão de listas:
                    
                    ```haskell
                    concat xss = [x | xs <- xss, x <- xs]
                    ```
                    
        - **Guards**
            
            Nas compreensões de lista podemos utilizar o conceito de **guardas** para filtrar o conteúdo dos geradores condicionalmente:
            
            ```haskell
            > [x | x <- [1..10], even x]
            [2,4,6,8,10]
            ```
            
        - Exemplo: Divisores
            
            Vamos criar uma função chamada `divisores` que retorna uma lista de todos os divisores de `n`. 
            
            - Qual a assinatura?
                
                ```haskell
                divisores :: Int -> [Int]
                ```
                
            - Quais os parâmetros?
                
                ```haskell
                divisores :: Int -> [Int]
                divisores n = [???]
                ```
                
            - Qual o gerador?
                
                ```haskell
                divisores :: Int -> [Int]
                divisores n = [x | x <- [1..n]]
                ```
                
            - Qual o guard?
                
                ```haskell
                divisores :: Int -> [Int]
                divisores n = [x | x <- [1..n], n `mod` x == 0]
                ```
                
            - Testando
                
                ```haskell
                > divisores 15
                [1,3,5,15]
                ```