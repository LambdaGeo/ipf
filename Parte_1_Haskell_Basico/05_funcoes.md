# 3. Funções

- Definição de funções
    
    [https://youtu.be/UPscxxix1g4](https://youtu.be/UPscxxix1g4)
    
    Funções generalizam expressões, por exemplo a função matemática `f(x) = x ^ 2` seria definida em Haskell como:
    
    ```haskell
    f x = x ^ 2
    ```
    
    A aplicação dessa função em Haskell não requer parênteses:
    
    ```haskell
    > f 4
    8
    ```
    
    Por ter inferência de tipos, em Haskell não é necessário anotar os tipos a uma função. Porém, uma assinatura possível para a função acima seria:
    
    ```haskell
    f :: Double -> Double
    f x = x ^ 2
    ```
    
    Funções podem ter mais de um parâmetro. Por exemplo:
    
    ```haskell
    delta a b c = (b ^ 2) + (4 * a * c)
    ```
    
    - Definições locais
        
        Para organizar nosso código, podemos utilizar a cláusula **`where`** ou **`let`** para definir nomes intermediários.
        
        Por exemplo, a distancia euclidiana entre dois pontos:
        
        ![](3%20Fun%C3%A7%C3%B5es/Untitled.png)
        
        - Cláusula where
            
            As definições de cláusula where aplicam ao código que a antecede.
            
            Usando a cláusula `where`, poderia ser escrito em Haskell como:
            
            ```haskell
            distance (x1, y1) (x2, y2)  = sqrt sxy
              where
            		sxy = dx + dy
                dx = (x2 - x1) ^ 2
                dy = (y2 - y1) ^ 2
                
            ```
            
        - Expressão let
            
            Essa estrutura é muito comum em linguagens da família ML, como F# e OCaml. 
            
            A forma do `let` é :
            
            `let <bindings> in <expression>` 
            
            Os nomes definidos em let são acessíveis à expressão após a parte in.
            
            A mesma função de cálculo de distância euclidiana poderia ser escrito da seguinte maneira:
            
            ```haskell
            distance (x1, y1) (x2, y2) = 
              let dx = (x2 - x1) ^ 2
                  dy = (y2 - y1) ^ 2
                  sxy = dx + dy
                  in sqrt sxy
            ```
            
        
        Ambos exemplos podem ser experimentados em: [https://repl.it/@SergioSouza1/exemplo-where-let](https://repl.it/@SergioSouza1/exemplo-where-let)
        
- Expressões condicionais e guardadas
    
    [https://youtu.be/kHPSVwRYgXQ](https://youtu.be/kHPSVwRYgXQ)
    
    Funções podem usar expressões condicionais `if-then-else`:
    
    ```haskell
    signum n = if n < 0 then -1 else
                if n == 0 then 0 else 1
    ```
    
    e
    
    ```haskell
    abs :: Num a => a -> a
    abs n = if (n >= 0) then n else (-n)
    ```
    
    Porém, vale ressalta que aqui temos uma "expressão" condicional. Nas linguagens imperativas temos "comandos" condicionais. Então a clausula `else` é obrigatória, e ela deve retornar o mesmo tipo
    
    - Expressões *guardadas* (Guard Expressions)
        
        Uma alternativa ao uso de `if-then-else` é o uso de *guards* (`|`) que deve ser lido como *tal que*:
        
        ```haskell
        signum n 
        	| n == 0    =  0  
          | n > 0     =  1
          | otherwise = -1
        ```
        
        `otherwise` é o caso contrário e é definido como `otherwise = True`. Ou seja, sempre é verdade
        
        Note que as expressões guardadas são avaliadas de cima para baixo, o primeiro verdadeiro será executado e o restante ignorado.
        
        ```haskell
        classificaIMC :: Double -> String
        classificaIMC imc 
            | imc <= 18.5 = "abaixo do peso"
            -- não preciso fazer && imc > 18.5
            | imc <= 25.0 = "no peso correto"
            | imc <= 30.0 = "acima do peso"
            | otherwise   = "muito acima do peso"
        ```
        
        Reescrever if-then-else
        
- Pattern Matching
    
    [https://youtu.be/YnLUK7U1LLY](https://youtu.be/YnLUK7U1LLY)
    
    Muitas funções têm uma definição particularmente clara usando
    pattern matching em seus argumentos
    
    Considere a seguinte função usando expressões condicionais:
    
    ```haskell
    negar :: Bool -> Bool
    negar x = if (x == True) then False else True
    ```
    
    Podemos reescreve-la utilizando guardas:
    
    ```haskell
    negar :: Bool -> Bool
    negar x | x == True  = False
          | x == False = True
    ```
    
    Quando temos comparações de igualdade nos guardas, podemos definir as expressões substituindo diretamente os argumentos:
    
    ```haskell
    negar :: Bool -> Bool
    negar True  = False
    negar False = True
    ```
    
    Assim como os guards, os padrões são avaliados do primeiro definido até o último.
    
    Podemos usar pattern patching com diversos outros tipos. Por exemplo, no caso de numeros inteiros podemos definir alguns casos e usar uma variável para o caso geral:
    
    ```haskell
    fat 0 = 1
    fat 1 = 1
    fat 2 = 2
    fat n = n * fat (n-1)
    ```
    
    - Uso de caracter curinga.
        
        Podemos indicar que não importa o que está presente em parte de um padrão. A notação para isto é o caractere sublinhado `_`, que chamamos de um curinga ou wild card.
        
        ```haskell
        (&&) :: Bool -> Bool -> Bool
        True && True = True
        True && False = False
        False && True = False
        False && False = False
        ```
        
        Poderia ser definido de modo mais compacto usando os curingas.
        
        ```haskell
        True && True = True
        _ && _ = False
        ```
        
        Uma outra  forma seria:
        
        ```haskell
        True && b = b
        False && _ = False
        ```
        
- Funções recursivas
    - Aula básica sobre recursividade dada para uma disciplina de estrutura de dados.
        
        [https://pt.slideshare.net/skosta/aula-recursividade](https://pt.slideshare.net/skosta/aula-recursividade)
        
        [https://www.youtube.com/watch?v=3RTIzLCpJo0](https://www.youtube.com/watch?v=3RTIzLCpJo0)
        
    
    [https://youtu.be/g5cjphvkP5Q](https://youtu.be/g5cjphvkP5Q)
    
    - Exemplos clássicos
        
        Com a ausência de variáveis mutáveis, não é possível a utilização de estruturas de iteração. Usa-se nestes casos:
        
        - as funções de alta ordem ou
        - funções recursivas explicitamente.
        
        Para exemplificar uma função recursiva, vamos usar o clássico exemplo.
        
        ![](3%20Fun%C3%A7%C3%B5es/Untitled%201.png)
        
        ```haskell
        fat 0 = 1
        fat n = n * fat (n-1)
        ```
        
        O Haskell avalia as expressões por substituição:
        
        ```haskell
        > fat 4
              => 4 * fat 3
              => 4 * (3 * fat 2)
              => 4 * (3 * (2 * fat 1))
              => 4 * (3 * (2 * 1))
              => 4 * (3 * 2)
              => 4 * 6
              => 24
        ```
        
        O algoritmo de Euclides para encontrar o Máximo Divisor Comum (*greatest common divisor* - gcd) é definido matematicamente como:
        
        ```haskell
        gcd :: Int -> Int -> Int
        gcd a 0 = a
        gcd a b = gcd b (a `mod` b)
        
        ```
        
        ```haskell
        > gcd 48 18
            => gcd 18 12
            => gcd 12 6
            => gcd 6 0
            => 6
        
        ```
        
    - Eficiência
        
        As funções recursivas são muito criticadas na literatura. Em partes essa crítica é razoável, dado o consumo de memória que pode levar ao erro conhecido como “stack overflow”. Contudo, existem diversas técnicas que podem evitar esse tipo de erro, como por exemplo a recursão em cauda. O algorimo de fibonacci é muito usado como um exemplo ruim de recursividade. Essa implementação é bem simples, porém tem um custo alto, além de consumir muito tempo.
        
        ```haskell
        fib :: Integer -> Integer
        fib 0 = 1
        fib 1 = 1
        fib x = fib (x - 1) + fib (x - 2)
        ```
        
        Com algumas modificações, podemos fazer uma nova versão que é capaz de imprimir facilmente o milésimo fibonnacci.
        
        ```haskell
        fibTuple :: (Integer, Integer, Integer) -> (Integer, Integer, Integer)
        fibTuple (x, y, 0) = (x, y, 0)
        fibTuple (x, y, index) = fibTuple (y, x + y, index - 1)
        
        fibEf :: Integer -> Integer
        fibEf x =  r
          where
          (r,_,_) = fibTuple (0, 1, x) 
        
        main = print $ fibEf 1000
        ```
        
        A execução do código acima retornaria o seguinte número:
        
        ```
        4346655768693745643568852767504062580256466051737178040248172908953655541794
        90518904038798400792551692959225930803226347752096896232398733224711616429964409
        06533187938298969649928516003704476137795166849228875
        
        ```
        
        - For utilizada a técnica conhecida como tail recursion. Essa técnica é muito bem explicada   por Hutton nesse vídeo.
            
            [https://www.youtube.com/watch?v=_JtPhF8MshA](https://www.youtube.com/watch?v=_JtPhF8MshA)
            
        
- Expressões *λ (lambda)*
    
    [https://youtu.be/a7lKUy0gtPA](https://youtu.be/a7lKUy0gtPA)
    
    As expressões lambdas, também chamadas de funções anônimas, definem uma função sem nome para uso geral. Considerado um exemplo com strings:
    
    ```python
    s = "Ola Mundo"
    print (s) # string nomeada
    
    print ("ola mundo") # string anônima
    ```
    
    As expressões lambdas são muito úteis quando não queremos criar uma função, mas apenas passa-la para outra função. Pense nas expressões lambdas como equivalente a literais como `10`, ou `"Ola Mundo!"`. Nesse exemplo, a expressão lambda é passado para a função map, que irá retornar uma nova lista com os valores duplicados.
    
    ```haskell
    > map (\x-> 2 *x) [4,5,6]
    => [8,10,12]
    ```
    
    Veremos mais a frente sobre funções de alta ordem e lista. 
    
    - Vídeo de Hutton sobre cálculo lambda:
        
        [https://youtu.be/eis11j_iGMs](https://youtu.be/eis11j_iGMs)
        
- Funções e Operadores
    
    [https://youtu.be/E7Gn13iXZjo](https://youtu.be/E7Gn13iXZjo)
    
    Para definir um operador em Haskell, podemos criar na forma infixa ou na forma de função:
    
    ```haskell
    (<^>) :: Int -> Int -> Int
    a <^> b =  a + b
    ```
    
    ou
    
    ```haskell
    (<^>) :: Int -> Int -> Int
    (<^>) a b =  a + b
    ```
    
    Da mesma forma, uma função pode ser utilizada como operador se envolta de crases:
    
    ```haskell
    > mod 10 3
    1
    > 10 `mod` 3
    1
    ```
    
    - Seções
        
        Sendo `#` um operador, temos que `(#), (x #), (# y)` são chamados de seções, e definem:
        
        ```haskell
        (#)   = \x -> (\y -> x # y)
        (x #) = \y -> x # y
        (# y) = \x -> x # y
        ```
        
        Seções e aplicações parciais poderia ser usado como alternativa a expressão lambdas:
        
        ```haskell
        Prelude> map ((*) 2) [4,5,6]
        [8,10,12]
        ```