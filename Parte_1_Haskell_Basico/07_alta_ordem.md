# 5. Funções de alta ordem

- Definição
    
    [https://youtu.be/fJsMD8-qlHk](https://youtu.be/fJsMD8-qlHk)
    
    - As funções que recebem uma ou mais funções como argumento, ou que retornam uma função são denominadas **Funções de alta ordem** (*high order functions*).
    - O uso de funções de alta ordem permitem aumentar a expressividade do Haskell quando confrontamos padrões recorrentes.
    
    ```haskell
    duasVezes :: (a -> a) -> a -> a
    duasVezes f x = f (f x)
    ```
    
    Essas funções são aplicáveis em diversas situações:
    
    ```haskell
    > duasVezes (*2) 4
    16
    > duasVezes reverse [1,2,3]
    [1,2,3]
    ```
    
    Além disso podemos fazer uma **aplicação parcial** da função, com apenas um argumento, para gerar outras funções
    
    ```haskell
    quadruplica = duasVezes (*2)
    ```
    
    - Funções como valores de primeira classe
        
        Funções de alta ordem e funções como valores de primeira classe são conceitos relacionados mas distintos.
        
        - Tratar as funções como valores de primeira classe é uma característica da linguagem.
        - Uma função de alta ordem é uma característica de uma função.
        
        Então tratar as funções como valores de primeira classe possibilita criar funções de alta ordem.
        
- Os padrões map, filter e reduce
    - Um vídeo anterior que fiz para a disciplina de paradigmas de programação
        
        [https://youtu.be/XiqvhOOV1FE](https://youtu.be/XiqvhOOV1FE)
        
    
    [https://youtu.be/ZDwRNkkstqY](https://youtu.be/ZDwRNkkstqY)
    
    Muito comum, e presente em diversas linguagens mais modernas. Esse padrão pode ser implementado por três funções de alta ordem.
    
    - Map
        
        A função de alta ordem chamada map aplica uma função para todos os elementos de uma lista. Por exemplo:
        
        ```haskell
        > map (+1) [1,2,3]
        [2,3,4]
        > map even [1,2,3]
        [False, True, False]
        > map reverse ["ola", "mundo"]
        ["alo", "odnum"]
        ```
        
        Sua assinatura é:
        
        ```haskell
        map :: (a -> b) -> [a] -> [b]
        ```
        
        Uma função que transforma uma lista do tipo `a` para o tipo `b` utilizando uma função `f :: a -> b`.
        
        Poderiamos definir a função `map` usando compreensão de listas:
        
        ```haskell
        map :: (a -> b) -> [a] -> [b]
        map f xs = [f x | x <- xs]
        ```
        
        Ou através de funções recursivas
        
        ```haskell
        map :: (a -> b) -> [a] -> [b]
        map f []     = []
        map f (x:xs) = f x : map f xs
        ```
        
        Lembrando que essa função já está definida na biblioteca padrão do Haskell (prelude)
        
        - Observações sobre o map
            
            1 Ela uma função genérica, recebe qualquer tipo de lista
            2 Ela pode ser aplicada a ela mesma, ou seja, aplicável em listas de listas:
            
            ```haskell
            > map (map (+1)) [[1,2],[3,4]]
               => [ map (+1) xs | xs <- [[1,2],[3,4]] ]
               => [ [x+1 | x <- xs] | xs <- [[1,2],[3,4]] ]
            
            ```
            
    - Filter
        
        A função de alta ordem filter seleciona todos os elementos de uma lista que satisfaça um predicado. Por exemplo:
        
        ```haskell
        > filter (>5) [1..10]
        [6,7,8,9,10]
        > filter (/= ' ') "abc def ghi"
        "abcdefghi"
        > filter even [1..10]
        [2,4,6,8,10]
        > filter primo [1..10]
        [2,3,5,7]
        ```
        
        Podemos definir a função de alta ordem `filter` da seguinte forma:
        
        ```haskell
        filter :: (a -> Bool) -> [a] -> [a]
        filter p xs = [x | x <- xs, p x]
        ```
        
        `filter` retorna uma lista de todos os valores cujo o predicado `p` de `x` retorna `True`.
        
        Ou usando recursividade:
        
        ```haskell
        filter :: (a -> Bool) -> [a] -> [a]
        filter p [] = []
        filter p (x:xs) 
        	| p x       = x : filter p xs                
          | otherwise = filter p xs
        ```
        
        - Map e Filter
            
            As duas funções `map` e `filter` costumam serem utilizadas juntas, assim como na compreensão de listas:
            
            ```haskell
            somaQuadPares :: [Int] -> Int
            somaQuadPares ns = sum [n^2 | n <- ns, even n]
            
            somaQuadPares :: [Int] -> Int
            somaQuadPares ns = sum (map (^2) (filter even ns))
            ```
            
        - Operador pipe
            
            Podemos utilizar o operador `$` para separar as aplicações das funções e remover os parênteses:
            
            ```haskell
            somaQuadPares :: [Int] -> Int
            somaQuadPares ns = sum 
                             $ map (^2) 
                             $ filter even ns
            ```
            
            A execução é de baixo para cima.
            
    - Reduce (ou fold)
        
        Vamos recapitular algumas das funções recursivas da aula anterior:
        
        ```haskell
        sum []     = 0
        sum (x:xs) = x + sum xs
        
        product []     = 1
        product (x:xs) = x * product xs
        
        length []     = 0
        length (_:xs) = 1 + length xs
        ```
        
        Podemos generalizar essas funções da seguinte forma:
        
        ```haskell
        f _ v [] = v
        f g _ (x:xs)  = g x (f xs)
        ```
        
        Essa funções podem ser chamadas de reduce em algumas linguagens ou `fold` em Haskell;
        
        ```haskell
        foldr :: (a -> b -> b) -> b -> [a] -> b
        foldr f v [] = v
        foldr f v (x:xs) = f x (foldr f v xs)
        ```
        
        Reduce, por que ela reduz uma coleção de valores em um único valor.
        
        - Entendendo a função
            
            Considere uma função pela sua definição
            
            ```haskell
            a1 : (a2 : (a3 : []))
            ```
            
            Trocando `:` pela função `f` e `[]` pelo valor `v`:
            
            ```haskell
            a1 `f` (a2 `f` (a3 `f` v))
            ```
            
            Ou seja:
            
            ```haskell
            foldr (+) 0 [1,2,3]
            ```
            
            se torna:
            
            ```haskell
            1 + (2 + (3 + 0))
            ```
            
        - Reescrevendo soma, produto e tamanho.
            
            ```haskell
            sum = foldr (+) 0
            product = foldr (*) 1
            length = foldr (\_ n -> 1+n) 0
            ```
            
    - Outras funções de alta ordem
        
        Outras funções úteis durante o curso:
        
        ```haskell
        > all even [2,4,6,8]
        True
        
        > any odd [2,4,6,8]
        False
        
        > takeWhile even [2,4,6,7,8]
        [2,4,6]
        
        > dropWile even [2,4,6,7,8]
        [7,8]
        ```
        
- Composição de funções
    
    Na matemática a composição de função `*f* ∘ *g*` define uma nova função *z* tal que `*z*(*x*) = *f*(*g*(*x*))`.
    
    No Haskell temos o operador `(.)`:
    
    ```haskell
    (.) :: (b -> c) -> (a -> b) -> (a -> c)
    f . g = \x -> f (g x)
    ```
    
    Dada uma função que mapeia do tipo `b` para o tipo `c`, e outra que mapeia do tipo `a` para o tipo `b`, gere uma função que mapeie do tipo `a` para o tipo `c`.
    
    - Propriedades da composição
        
        A composição de função é associativa:
        
        ```haskell
        (f . g) . h == f . (g . h)
        ```
        
        E tem um elemento nulo que é a função `id`:
        
        ```haskell
        f . id = id . f = f
        ```
        
        Essas duas propriedades são importantes durante a construção de programas, pois elas permitem o uso do `foldr` (e dentre outras funções de alta ordem):
        
        ```haskell
        -- cria uma função que é a composição de uma lista de funções
        compose :: [a -> a] -> (a -> a)
        compose = foldr (.) id
        ```