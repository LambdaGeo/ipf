# 2. Tipos e Classes

Fonte: Capítulo 3: Types and classes, do livro Programming in Haskell (Graham Hutton)

- Sistemas de tipos e tipos de dados básicos
    
    [https://www.youtube.com/watch?v=lhQNjDbBsCQ](https://www.youtube.com/watch?v=lhQNjDbBsCQ)
    
    Duas excelentes referência sobre sistema de tipos são:
    
    - Cardelli - On understanding types, data abstraction, and polymorphism
    - Benjamin C. Pierce - Advanced topics in types and programming languages
    
    Segundo estes autores:
    
    > Type systems are generally formulated as collections of rules for checking the “consistency” of programs. (Piercy, 2004)
    > 
    
    > In mathematics as in programming, types impose constraints which help to enforce correctness (Cardelli 1985).
    > 
    
    > "The fundamental purpose of a type system is to prevent the 
    occurrence of execution errors during the running of a program." 
    (Cardelli, 2004)
    > 
    - Tipos de dados
        
        Um tipo é uma coleção de valores relacionados entre si.
        
        Exemplos:
        
        - *Int* compreende todos os valores de números inteiros.
        - *Bool* contém apenas os valores *True* e *False*, representando valores lógicos
    - Checagem e erros de tipos
        - As checagem de tipos podem ser executadas em
            - **tempo de compilação** (estática),
            - em **tempo de execução** (dinamica),
            - ou em ambos.
        - Um erro de tipo ocorre se o programa executa uma operação com tipos
        incompatíveis, tais como multiplicar uma string por um valor booleano
        - Uma linguagem é dita **fortemente tipada** se os erros
        de tipo são sempre detectados, seja em tempo de compilação ou em tempo
        de execução. Por exemplo, a linguagem C é fracamente tipada, mesmo
        tendo verificação de tipos em tempo de compilação.
        - Por exemplo, no ghci, experimente a seguinte expressão:
        
        ```haskell
        ghci> 1 + False
        ```
        
        No laboratório veremos outros casos.
        
    - Sistema de tipos do Haskell
        
        Há três aspectos interessantes sobre tipos em Haskell:
        
        - eles são *fortes*,
        - eles são *estáticos*,
        - e podem ser automaticamente *inferidos*.
        
        Além disso , o Haskell tem suporte avançado para abstração de dados.
        
    - Tipos de dados básicos
        
        No Haskell, os tipos são definidos pela notação
        
        ```haskell
        v :: T
        ```
        
        significando que *v* define um valor do tipo *T*.
        
        No ghci é fácil saber o tipo de qualquer valor. Por exemplo:
        
        ```haskell
        ghci> :type 'a'
        'a' :: Char
        ```
        
        O compilador GHC já vem com suporte nativo a diversos tipos básicos para uso.
        
        Durante o curso veremos como definir alguns deles.
        
        Os tipos são:
        
        - **Bool:** contém os valores **True** e **False**.
        - **Char:** contém todos os caracteres no sistema **Unicode**.
        - **String:** sequências de caracteres delimitados por aspas duplas: “Olá Mundo”.
        - **Int:** inteiros com precisão fixa em 64 bits.
        - **Integer:** inteiros de precisão arbitrária. Representa valores inteiros de qualquer precisão, a memória é o limite. Mais lento do que operações com *Int*.
        - **Float:** valores em ponto-flutuante de precisão simples. Permite representar números com um total de 7 dígitos, em média.
        - **Double:** valores em ponto-flutuante de precisão dupla. Permite representar números com quase 16 dígitos, em média.
- Tipo Lista e Tupla
    
    [https://www.youtube.com/watch?v=h7kOcTCU_qY](https://www.youtube.com/watch?v=h7kOcTCU_qY)
    
    **Listas** são sequência de elementos do mesmo tipo agrupados por colchetes e separados por vírgula:
    
    ```haskell
    [1,2,3,4]
    ```
    
    Uma lista de tipo `T` tem tipo `[T]`:
    
    ```haskell
    [1,2,3,4] :: [Int]
    [False, True, True] :: [Bool]
    ['o', 'l', 'a'] :: [Char]
    ```
    
    Veremos melhor sobre tipos polimorficos.
    
    O tamanho da lista (*length*) representa a quantidade de elementos nela. Um lista vazia é representada por `[]` e listas com um elemento, como `[1]`, `[False]`, `[[]]` são chamadas *singleton*.
    
    Podemos ter listas de listas:
    
    ```haskell
    [ [1,2,3], [4,5] ] :: [[Int]]
    [ [ 'o','l','a'], ['m','u','n','d','o'] ] :: [[Char]]
    ```
    
    <aside>
    📌 Ainda teremos uma aula apenas sobre listas
    
    </aside>
    
    Notem que:
    
    - O tipo da lista não especifica seu tamanho
    - Não existe limitações quanto ao tipo da lista
    - Não existe limitações quanto ao tamanho da lista
    - Tipo tupla
        
        Tuplas são sequências finitas de componentes, contendo zero ou mais tipos diferentes:
        
        ```haskell
        (True, False) :: (Bool, Bool)
        (1.0, "Sim", False) :: (Double, String, Bool)
        ```
        
        O tipo da tupla é definido como `(T1, T2,...,Tn)`.
        
        O número de componentes de uma lista é chamado *aridade*. Uma tupla de aridade zero, a tupla vazia, é representada por `()`, tuplas de tamanho dois são conhecidas como *duplas*, tamanho três são *triplas*.
        
        Notem que:
        
        - O tipo da tupla especifica seu tamanho
        - Não existe limitações dos tipos associados a tupla (podemos ter tuplas de tuplas)
        - Tuplas **devem** ter um tamanho finito
        - Tuplas de aridade 1 não são permitidas para manter compatibilidade do uso de parênteses como ordem de avaliação
- Tipo função e polimorfismo
    
    [https://www.youtube.com/watch?v=qQe-Cu3bb70](https://www.youtube.com/watch?v=qQe-Cu3bb70)
    
    Funções são mapas de argumentos de um tipo para resultados em outro tipo. O tipo de uma função é escrita como `T1 -> T2`, ou seja, o mapa do tipo `T1` para o tipo `T2`:
    
    ```haskell
    not  :: Bool -> Bool
    even :: Int -> Bool
    ```
    
    - Nome da função deve começar com caixa baixa. O estilo padrão é o *camelCase*.
    - Funções curry
        - Vídeo de Hutton sobre Curry
            
            [https://youtu.be/psmu_VAuiag](https://youtu.be/psmu_VAuiag)
            
        
        Toda função no Haskell mapeia um valor para outro valor:
        
        ```haskell
        somaUm :: Integer -> Integer
        somaUm x = x + 1
        ```
        
        - A definição dessa função pode ser lida como:
            - A função, dado um valor x…
            - …é definida como…
            - …a expressão x + 1.
            
        
        Funções com múltiplos argumentos podem ser definidas de uma outra forma, inicialmente não óbvia, mas que torna sua representação mais natural.
        
        Como não existe restrições de tipos, uma função pode retornar uma outra função:
        
        ```haskell
        soma' :: Int -> (Int -> Int)
        soma' x y = x + y
        ```
        
        Ela recebe um valor *x* e retorna uma função que recebe um *y* e retorna *y + x* (aprenderemos sobre *\y* mais adiante).
        
        ```haskell
        soma' :: Int -> (Int -> Int)
        soma' x = \y -> x + y
        ```
        
        Da mesma forma podemos ter:
        
        ```haskell
        mult :: Int -> (Int -> (Int -> Int))
        mult x y z = x*y*z
        ```
        
        Para evitar escrever um monte de parênteses (como no Lisp), a seguinte sintaxe é válida:
        
        ```haskell
        soma' :: Int -> Int -> Int
        soma' x y = x + y
        
        mult :: Int -> Int -> Int -> Int
        mult x y z = x*y*z
        ```
        
    - Funções parciais e totais
        
        Uma função pode ser **total** se ela for definida para qualquer valor do tipo de entrada ou **parcial** se existem algumas entradas para qual ela não tem valor de saída definido:
        
        ```haskell
        > head []
        *** Exception: Prelude.head: empty list
        ```
        
        No medium escrevi um artigo breve, que discute mais sobre funções parciais e totais: [https://medium.com/@sergiocosta/princípios-e-padrões-de-programação-funcional-parte-1-fa3bff0d6d2d](https://medium.com/@sergiocosta/princ%C3%ADpios-e-padr%C3%B5es-de-programa%C3%A7%C3%A3o-funcional-parte-1-fa3bff0d6d2d)
        
    - Tira dúvidas sobre funções parciais e aplicação parcial
        
        [https://youtu.be/kl0Oq9x7dws](https://youtu.be/kl0Oq9x7dws)
        
    - Tipos polimórficos
        
        Considere a função `length` que retorna o tamanho de uma lista. Ela deve funcionar para qualquer uma dessas listas:
        
        ```haskell
        [1,2,3,4] :: [Int]
        [False, True, True] :: [Bool]
        ['o', 'l', 'a'] :: [Char]
        ```
        
        Qual o tipo de `length`?
        
        ```haskell
        length :: [a] -> Int
        ```
        
        Quem é `a`?
        
        Em Haskell, `a` é conhecida como **variável de tipo** e ela indica que a função deve funcionar para listas de qualquer tipo.
        
        As variáveis de tipo devem seguir a mesma convenção de nomes do Haskell, iniciar com letra minúscula. Como convenção utilizamos `a, b, c,...`.
        
- Classes de tipos
    
    [https://www.youtube.com/watch?v=vpIh2QlCfP0](https://www.youtube.com/watch?v=vpIh2QlCfP0)
    
    - Restrição de tipos (polimorfismo adhoc)
        
        Considere agora a função `(+)`, diferente de `length` ela pode ter um comportamento diferente para tipos diferentes.
        
        Internamente somar dois `Int` pode ser diferente de somar dois `Integer`. De todo modo, essa função **deve** ser aplicada a tipos numéricos.
        
        A ideia de que uma função possa ser aplicada a apenas uma classe de tipos é explicitada pela **Restrição de classe** (**class constraint**). E é escrita na forma `C a`, onde `C` é o nome da classe e `a` uma variável de tipo.
        
        ```haskell
        (+) :: Num a => a -> a -> a
        ```
        
        O operador `+` recebe dois tipos de uma classe numérica e retorna um valor desse tipo.
        
        Note que nesse caso, ao especificar a entrada como `Int` para o primeiro argumento, todos os outros **devem** ser `Int` também.
        
        ```haskell
        Prelude> :t (+)
        (+) :: Num a => a -> a -> a
        ```
        
        Uma vez que uma função contém uma restrição de classe, pode ser necessário definir **instâncias** dessa função para diferentes tipos pertencentes a classe.
        
        Os valores também podem ter restrição de classe:
        
        ```haskell
        Prelude> :t 3
        3 :: Num p => p
        ```
        
        Lembrando:
        
        - **Tipo:** coleção de valores relacionados.
        - **Classe:** coleção de tipos que suportam certas funções ou operadores.
        - **Métodos:** funções requisitos de uma classe.
    - Classes básicas
        
        
        ![](2%20Tipos%20e%20Classes/Untitled.png)
        
        Veremos como criar classes de tipos mais a frente no curso. Agora iremos destacar as mais básicas e usadas nos programas em Haskell.
        
        - Eq - classe da igualdade
            
            Tipos que podem ser comparados em igualdade e desigualdade:
            
            ```haskell
            (==) :: a -> a -> Bool
            (/=) :: a -> a -> Bool
            ```
            
            Exemplos de aplicação
            
            ```haskell
            > 1 == 2
            False
            > [1,2,3] == [1,2,3]
            True
            > "Ola" /= "Alo"
            True
            ```
            
        - Classe de ordem
            
            A classe `Eq` acrescido de operadores de ordem:
            
            ```haskell
            (<) :: a -> a -> Bool
            (<=) :: a -> a -> Bool
            (>) :: a -> a -> Bool
            (>=) :: a -> a -> Bool
            min :: a -> a -> a
            max :: a -> a -> a
            ```
            
            Exemplos:
            
            ```haskell
            > 4 < 6
            > min 5 0
            > max 'c' 'h'
            > "Ola" <= "Olaf"
            ```
            
        - Show - classe imprimíveis
            
            A classe `Show` define como imprimir um valor de um tipo:
            
            ```
            show :: a -> String
            ```
            
            Exemplo:
            
            ```
            > show 10.0
            > show [1,2,3,4]
            ```
            
        - Read - classe legíveis
            
            A classe `Read` define como ler um valor de uma String:
            
            ```
            read :: String -> a
            ```
            
            Precisamos especificar o tipo que queremos extrair da String:
            
            ```
            > read "12.5" :: Double
            > read "False" :: Bool
            > read "[1,3,4]" :: [Int]
            ```
            
        - Num - classe numérica
            
            A classe `Num` define todos os tipos numéricos e deve ter as instâncias de:
            
            ```
            (+) :: a -> a -> a
            (-) :: a -> a -> a
            (*) :: a -> a -> a
            negate :: a -> a
            abs :: a -> a
            signum :: a -> a
            fromInteger :: Integer -> a
            ```
            
            Exemplo:
            
            ```
            > 1 + 3
            > 6 - 9
            > 12.3 * 5.6
            ```
            
            O que as seguintes funções fazem? (use o `:t` para ajudar)
            
            ```
            > negate 2
            > abs 6
            > signum (-1)
            > fromInteger 3
            ```
            
            - Resposta
                - **negate:** inverte o sinal do argumento.
                - **abs:** retorna o valor absoluto.
                - **signum:** retorna o sinal do argumento.
                - **fromInteger:** converte um argumento do tipo inteiro para numérico.
                
                Note que os valores negativos devem ser escritos entre parênteses para não confundir com o operador de subtração.
                
            
        - Integral - classe de números inteiros
            
            A classe `Integral` define todos os tipos numéricos inteiros e deve ter as instâncias de:
            
            ```haskell
            quot :: a -> a -> a
            rem :: a -> a -> a
            div :: a -> a -> a
            mod :: a -> a -> a
            quotRem :: a -> a -> (a, a)
            divMod :: a -> a -> (a, a)
            toInteger :: a -> Integer
            ```
            
            O uso de crases transforma uma função em operador infixo.
            
            ```haskell
            > quot 10 3 == 10 `quot` 3
            ```
            
            Exemplos:
            
            ```haskell
            > 10 `quot` 3
            > 10 `rem` 3
            > 10 `div` 3
            > 10 `mod` 3
            ```
            
            As funções `quot` e `rem` arredondam para o 0, enquanto `div` e `mod` para o infinito negativo.
            
        - Fractional - classe de números inteiros
            
            A classe `Fractional` define todos os tipos numéricos fracionários e deve ter as instâncias de:
            
            ```haskell
            (/) :: a -> a -> a
            recip :: a -> a
            ```
            
            Exemplos:
            
            ```haskell
            > 10 / 3
            > recip 10
            ```
            
    - Info
        
        No ghci, o comando `:info` mostra informações sobre os tipos e as classes de tipo:
        
        ```
        > :info Integral
        class (Real a, Enum a) => Integral a where
          quot :: a -> a -> a
          rem :: a -> a -> a
          div :: a -> a -> a
          mod :: a -> a -> a
          quotRem :: a -> a -> (a, a)
          divMod :: a -> a -> (a, a)
          toInteger :: a -> Integer
          {-# MINIMAL quotRem, toInteger #-}
        ```