# 7. Declarando tipos e classes

Markdow criado pelos professores Fabrício Olivetti de França e Emilio Francesquini. Original pode ser acessado em [http://pesquisa.ufabc.edu.br/haskell/posts/basico/11-ADT.html](http://pesquisa.ufabc.edu.br/haskell/posts/basico/11-ADT.html).

- Tipos e sinônimos
    
    [https://www.youtube.com/watch?v=k_lRWxOgNL8](https://www.youtube.com/watch?v=k_lRWxOgNL8)
    
    A definição de novos tipos de dados, além dos tipos primitivos, permite manter a legibilidade do código e facilita a organização de seu programa.
    
    - Declaração de tipo
        
        A forma mais simples de definir um novo tipo é criando *apelidos* para tipos existentes:
        
        ```haskell
        type String = [Char]
        ```
        
        Todo nome de tipo deve começar com uma letra maiúscula. As definições de tipo podem ser encadeadas!
        
        Suponha a definição de um tipo que armazena uma coordenada e queremos definir um tipo de função que transforma uma coordenada em outra:
        
        ```haskell
        type Coord = (Int, Int)
        type Trans = Coord -> Coord
        ```
        
        Porém, não podemos definir tipos recursivos:
        
        ```haskell
        type Tree = (Int, [Tree])
        ```
        
        mas temos outras formas de definir tais tipos…
        
        A declaração de tipos pode conter variáveis de tipo:
        
        ```haskell
        type Pair a = (a, a) 
        type Assoc k v = [(k,v)]
        ```
        
        Com isso podemos definir funções utilizando esses tipos:
        
        ```haskell
        find :: Eq k => k -> Assoc k v -> v
        find k t = head [v | (k',v) <- t, k == k']
        
        > find 2 [(1,3), (5,4), (2,3), (1,1)]
        3
        ```
        
        Como esses tipos são apenas apelidos, eu posso fazer:
        
        ```haskell
        array = [(1,3), (5,4), (2,3), (1,1)] :: [(Int, Int)]
        > find 2 array
        3
        ```
        
        O compilador não distingue um do outro.
        
- Tipos de Dados Algébricos
    
    [https://www.youtube.com/watch?v=ZEMIv22ZjOk](https://www.youtube.com/watch?v=ZEMIv22ZjOk)
    
    - Características
        - Tipos completamente novos.
        - Pode conter tipos primitivos.
        - Permite expressividade.
        - Permite checagem em tempo de compilação
    - Por que algébricos ?
        
        Interessante post:
        
        [The algebra (and calculus!) of algebraic data types](https://codewords.recurse.com/issues/three/algebra-and-calculus-of-algebraic-data-types)
        
    - Exemplos
        - Tipo soma
            
            ```haskell
            data Bool = True | False
            ```
            
            - data: declara que é um novo tipo
            - Bool: nome do tipo
            - True | False: poder assumir ou True ou False
            
            Vamos criar um tipo que define a direção que quero andar:
            
            ```haskell
            data Dir = Norte | Sul | Leste | Oeste
            ```
            
            Com isso podemos criar a função `para`:
            
            ```haskell
            data Dir = Norte | Sul | Leste | Oeste
            
            para :: Dir -> Trans
            para Norte (x,y) = (x,y+1)
            para Sul   (x,y) = (x,y-1)
            para Leste (x,y) = (x+1,y)
            para Oeste (x,y) = (x-1,y)
            ```
            
        - Tipo produto
            
            ```haskell
            data Ponto = Ponto Double Double
            ```
            
            - data: declara que é um novo tipo
            - Ponto: nome do tipo
            - Ponto: construtor (ou envelope)
            - Double Double: tipos que ele encapsula
            
            Para ser possível imprimir esse tipo:
            
            ```haskell
            data Ponto = Ponto Double Double deriving (Show)
            ```
            
            - deriving: derivado de outra classe
            - Show: tipo imprimível
            
            Isso faz com que o Haskell crie automaticamente uma instância da função *show* para esse tipo de dado.
            
            Para usá-lo em uma função devemos sempre envelopar a variável com o construtor.
            
            ```haskell
            dist :: Ponto -> Ponto -> Double
            dist (Ponto x y) (Ponto x' y') = sqrt $ (x-x')^2 + (y-y')^2
            
            > dist (Ponto 1 2) (Ponto 1 1)
            1.0
            ```
            
            - Podemos misturar os tipos soma e produto:
                
                ```haskell
                data Forma = Circulo Ponto Double 
                           | Retangulo Ponto Double Double
                
                -- um quadrado é um retângulo com os dois lados iguais
                quadrado :: Ponto -> Double -> Forma
                quadrado p n = Retangulo p n n
                ```
                
                `Circulo` e `Retangulo` são funções construtoras:
                
                ```haskell
                > :t Circulo
                Circulo :: Ponto -> Double -> Forma
                
                > :t Retangulo
                Retangulo :: Ponto -> Double -> Double -> Forma
                ```
                
            
        - Tipos parametrizados
            
            
            As declarações de tipos também podem ser parametrizados, considere o tipo `Maybe`:
            
            ```haskell
            data Maybe a = Nothing | Just a
            ```
            
            A declaração indica que um tipo `Maybe a` pode não ser nada ou pode ser apenas o valor de um tipo `a`.
            
            Esse tipo pode ser utilizado para ter um melhor controle sobre erros e exceções:
            
            ```haskell
            safeDiv :: Int -> Int -> Maybe Int
            safeDiv _ 0 = Nothing
            safeDiv m n = Just (m `div` n)
            
            safeHead :: [a] -> Maybe a
            safeHead [] = Nothing
            safeHead xs = Just (head xs)
            ```
            
            Eses erros podem ser capturados com a expressão `case`:
            
            ```haskell
            divComErro :: Int -> Int -> Int
            divComErro m n = case (safeDiv m n) of
                                 Nothing -> error "divisão por 0"
                                 Just x  -> x
            ```
            
            Seria equivalente aos optionals, presentes em linguagens como Swif, Kotlin, TypeScript, C# e até no Java :)
            
            Outras tipo interessante é o `Either` definido como:
            
            ```haskell
            data Either a b = Left a | Right b
            ```
            
            Esse tipo permite que uma função retorne dois tipos diferentes, dependendo da situação. É muito usado na linguagem Elixir
            
            ```haskell
            -- ou retorna uma String ou um Int
            safeDiv' :: Int -> Int -> Either String Int
            safeDiv' _ 0 = Left "divisão por 0"
            safeDiv' m n = Right (m `div` n)
            
            > safeDiv' 2 2
            1
            > safeDiv' 2 0
            "divisão por 0"
            ```
            
        - Tipos Recursivos
            
            [https://www.youtube.com/watch?v=kiSCuoczz0A](https://www.youtube.com/watch?v=kiSCuoczz0A)
            
            Alguns exemplos
            
            - Números Naturais
                
                A definição de números naturais era definida por um **Zero** e uma sequência de aplicações de uma função `f`. Podemos replicar essa definição como:
                
                ```haskell
                data Nat = Zero | Succ Nat
                ```
                
                ou seja, ou o número é Zero ou ele é a aplicação do construtor `Succ` em outro valor de `Nat`.
                
                Então os primeiros números são definidos como:
                
                ```haskell
                zero = Zero
                um   = Succ Zero
                dois = Succ (Succ Zero)
                tres = Succ (Succ (Succ Zero))
                ```
                
                Podemos então definir uma função `nat2int` e outra `int2nat` como:
                
                ```haskell
                nat2int :: Nat -> Int
                nat2int Zero     = 0
                nat2int (Succ n) = 1 + nat2int n
                
                int2nat :: Int -> Nat
                int2nat 0 = Zero
                int2nat n = Succ (int2nat (n-1))
                ```
                
                Recursivamente, poderiamos ainda definir as operações de soma, subtração, multiplicação e divisão natural.
                
            - Árvore Binária
                
                Um outro exemplo de tipo recursivo é a árvore binária, que pode ser definida como:
                
                ```haskell
                data Tree a = Leaf a | Node (Tree a) a (Tree a)
                ```
                
                ou seja, ou é um nó folha contendo um valor do tipo *a*, ou é um nó contendo uma árvore à esquerda, um valor do tipo *a* no meior e uma árvore à direita.
                
                A seguinte árvore, 
                
                poderia ser escrita como:
                
                ```haskell
                t :: Tree Int
                t = Node (Node (Leaf 1) 3 (Leaf 4)) 5
                       (Node (Leaf 6) 7 (Leaf 9))
                ```
                
                Podemos definir uma função `contem` que indica se um elemento `x` está contidado em uma árvore `t`:
                
                ```haskell
                contem :: Eq a => Tree a -> a -> Bool
                contem (Leaf y) x     = x == y
                contem (Node l y r) x = x == y || l `contem` x 
                                               || r `contem` x
                
                > t `contem` 5
                True
                > t `contem` 0
                Fals
                ```
                
            - Lista encadeada
                
                Lembrem que a lista encadeada é um outro exemplo de tipo recursivo.
                
                ```haskell
                data Lista = Vazia | Cons Int Lista deriving Show
                ```
                
                Poderiamos 
                
                ```haskell
                Prelude>  10 `Cons` (10 `Cons`  Vazia)
                Cons 10 (Cons 20 Vazia)
                ```
                
                a definição reescrita usando tipos paramêtricos:
                
                ```haskell
                data Lista a = Vazia | Cons a (Lista a) deriving Show
                ```
                
                Na biblioteca padrão, o vazia é substitúdo`[]` e o `Cons` por `:`
                
                ```haskell
                data [] a = [] | a : [a]
                ```
                
    - Newtype
        
        Uma terceira forma de criar um novo tipo é com a função `newtype`, que permite apenas um construtor:
        
        ```haskell
        newtype Nat = N Int
        ```
        
        - A diferença entre `newtype` e `type` é que o primeiro define um novo tipo enquanto o segundo é um sinônimo.
        - A diferença entre `newtype` e `data` é que o primeiro define um novo tipo até ser compilado, depois ele é substituído como um sinônimo. Isso ajuda a garantir a checagem de tipo em tempo de compilação.
- Classes de tipos (type class)
    
    [https://www.youtube.com/watch?v=qKsYW7hTzuo](https://www.youtube.com/watch?v=qKsYW7hTzuo)
    
    - Criando classes
        
        Aprendemos em uma aula anterior sobre as classes de tipo, classes que definem grupos de tipos que devem conter algumas funções especificadas.  Aqui veremos como criar as nossas classes.
        
        Para criar um novo tipo utilizamos a função `class`:
        
        ```haskell
        class Eq a where
           (==), (/=) :: a -> a -> Bool
        
           x /= y = not (x == y)
        ```
        
        Essa declaração diz: *para um tipo `a` pertencer a classe `Eq` deve ter uma implementação das funções `(==)` e `(/=)`*.
        
        Além disso, ela já define uma definição padrão da função `(/=)`, então basta definir `(==)`.
        
    - Extendendo classes
        
        Uma classe pode extender outra para forma uma nova classe. Considere a classe `Ord`:
        
        ```haskell
        class Eq a => Ord a where
           (<), (<=), (>), (>=) :: a -> a -> Bool
           min, max             :: a -> a -> a
           
           min x y | x <= y    = x
                   | otherwise = y
        
           max x y | x <= y    = y
                   | otherwise = x
        ```
        
        Ou seja, antes de ser uma instância de `Ord`, o tipo deve ser **também** instância de `Eq`.
        
    - Instânciando  classes
        
        Para definirmos uma nova **instância** de uma classe basta declarar:
        
        ```haskell
        instance Eq Bool where
           False == False = True
           True  == True  = True
           _     == _     = False
        ```
        
        Apenas tipos definidos por `data` e `newtype` podem ser instâncias de alguma classe.
        
        No caso da classe Ord temos:
        
        ```haskell
        instance Ord Bool where
            False < True = True
            _     < _    = False
            
            b <= c = (b < c) || (b == c)
            b > c  = c < b
            b >= c = c <= b
        ```
        
        - Derivação de instâncias
            
            Em muitos casos o Haskell consegue inferir as instâncias das classes mais comuns, nesses casos basta utilizar a palavra-chave `deriving` ao definir um novo tipo:
            
            ```haskell
            data Bool = False | True
                        deriving (Eq, Ord, Show, Read)
            ```
            
        - Exemplo, criando e instanciando
            
            ```haskell
            data Retangulo = Retangulo Double Double  deriving (Show)
            
            data Circulo =  Circulo Double  deriving (Show)
            
            class Metricas a where
              area :: a -> Double
            
            instance Metricas Retangulo where
             area (Retangulo base altura) = base * altura
            
            instance Metricas Circulo where
             area (Circulo raio) = pi * raio * raio
              where
               pi = 3.14159
            ```