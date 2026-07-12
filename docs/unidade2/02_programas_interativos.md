# 6. Programas interativos

Conforme discutimos anteriormente, funções de **entrada e saída** de dados são **impuras** pois alteram o estado atual do sistema.

- Aula gravada
    
    [https://www.youtube.com/watch?v=SDCR6fYF5Hg](https://www.youtube.com/watch?v=SDCR6fYF5Hg)
    
- Então temos um problema:
    - Um programa em Haskell consiste num conjunto de funções, sem
    efeitos colaterais.
    - O objetivo de executar qualquer programa é ter algum efeito colateral
    
    Como usar o Haskell para escrever programas interativos que leem do teclado e gravam na tela enquanto estão em execução
    
    ![](6%20Programas%20interativos/Untitled.png)
    
- Solução
    
    Escrever programas interativos em Haskell usando tipos que fazem distinção entre expressões funcionais “puras” de ações “impuras” que podem envolver efeitos colaterais
    
    Um valor do tipo (`IO a`) é uma ação que, quando realizada, pode fazer alguma forma de IO antes de devolver um resultado do tipo `a`.
    
    ```haskell
    type IO a = World -> (a, World)
    ```
    
    ![](6%20Programas%20interativos/Untitled%201.png)
    
    Por exemplo:
    
    - IO Char: O tipo das ações de IO que retornam um caracter
    - IO (): O tipo das ações que não tem valor de retorno
    
    A função `getChar` captura um caracter do teclado. Se eu executar tal função duas vezes, a saída não necessariamente será igual.
    
    A função `putChar` escreve um caracter na saída padarão (ex.: monitor). Se eu executar duas vezes seguidas com a mesma entrada, a saída será diferente.
    
    ```haskell
    getchar :: IO Char
    putChar :: Char -> IO ()
    
    ```
    
    Aqui entraria o conceito de mônadas, mas para esse curso, vamos usar IO de forma mais transparente
    
    Para saber mais, o grupo da UFABC tem esse material [http://pesquisa.ufabc.edu.br/haskell/monads.html](http://pesquisa.ufabc.edu.br/haskell/monads.html)
    
    Podem entrar em contato comigo, caso queiram tirar mais dúvidas.
    
- Entrada e Saída - Ação
    
    No Haskell chamamos as funções de entrada e saída como **ações de IO** (**IO actions**).
    
    As funções básicas são implementadas internamente de acordo com o Sistema Operacional
    
    Vamos trabalhar inicialmente com três ações básicas:
    
    ```haskell
    -- recebe um caracter da entrada padrão
    getChar :: IO Char
    
    -- escreve um caracter na saída padrão
    putChar :: Char -> IO ()
    
    -- retorna um valor puro envolvido de uma ação IO
    return :: a -> IO a
    ```
    
    Compondo as ações básicas para criar outras funções.
    
    - O Haskell tem uma notação (do notation) que facilita combinar as ações, que leva a lembrar um estilo imperativo.
        
        ```haskell
        do
           <comando 1>
           <comando 2>
           ...
           <comando n>
        ```
        
        onde cada comando é da forma
        
        ```haskell
        v <- <ação>
        ```
        
        ou apenas
        
        ```haskell
        <ação>
        ```
        
        - Um pouco mais sobre a do notation
            
            
            Para ser tratado como um monada, um tipo de dadoas Haskell precisa implementar a classe de tipos monada.
            
            ```haskell
            class Monad m where  
                return :: a -> m a  
              
                (>>=) :: m a -> (a -> m b) -> m b  
              
                (>>) :: m a -> m b -> m b  
                x >> y = x >>= \_ -> y  
              
                fail :: String -> m a  
                fail msg = error msg
            ```
            
            Sem a notação do, teríamos que usar os operadores (>≥= ) ou (>>) para combinar as ações. Por exemplo, caso quiséssemos ler uma mensagem e logo imprimir ela na tela, basta combina-las da seguinte mainira:
            
            ```haskell
            main = getLine >>= putStrLn
            ```
            
            Lembrando que:
            
            ```haskell
            getLine :: IO String
            putStrLn :: String -> IO ()
            ```
            
            Agora, se fosse necessário fazer alguma operação com essa entrada, tipo concatenar com outro valor:
            
            ```haskell
            main = getLine >>= (\s -> return ("ola "++ s) ) >>= putStrLn
            ```
            
            Onde o tipo da expressão lambda é:
            
            ```haskell
            (\s -> return ("ola "++ s) ) :: String -> IO String
            ```
            
            Usando a notação do ficaria:
            
            ```haskell
            main = do
              s <- getLine
              putStrLn ("ola "++ s)
            ```
            
            Existem implementações para diversos tipos de dados. Por exemplo para o tipo de dados Maybe
            
            ```haskell
            instance Monad Maybe where  
                return x = Just x  
                Nothing >>= f = Nothing  
                Just x >>= f  = f x  
                fail _ = Nothing
            ```
            
            Ou mesmo para lista:
            
            ```haskell
            instance Monad [] where
                return x = [x]
                xs >>= f = concatMap f xs
                fail _ = []
            ```
            
            Excelente vídeo Graham Hutton sobre monad:
            
            [https://www.youtube.com/watch?v=t1e8gqXLbsU&t=17s](https://www.youtube.com/watch?v=t1e8gqXLbsU&t=17s)
            
        
    - Exemplos
        
        Capturar apenas um caracter pode não ser tão interessante quanto capturar uma linha inteira de informação. Podemos escrever uma função `getLine` da seguinte maneira:
        
        ```haskell
        getLine :: IO String
        getLine = do x <- getChar
                     if x == '\n' then
                        return []
                     else
                        do xs <- getLine
                           return (x:xs)
        ```
        
        A função inversa, que escreve uma `String` na saída padrão:
        
        ```haskell
        putStr :: String -> IO ()
        putStr []     = return ()
        putStr (x:xs) = do putChar x
                           putStr  xs
                           
        putStrLn :: String -> IO ()
        putStrLn xs = do putStr xs
                         putChar 'n'
        ```
        
    
- Podemos tentar entender melhor agora um Hello World
    
    ```haskell
    ask :: String -> IO String
    ask question = do
      putStrLn question
      getLine
    
    main :: IO ()
    main = do
      nome <- ask "Qual eh o seu nome?"
      putStrLn ("Bem vindo "++ nome ++ "!")
    ```
    
    Pode experimentar esse codigo em: [https://repl.it/@SergioSouza1/hellohaskell](https://repl.it/@SergioSouza1/hellohaskell)
    
- Um programa um pouco mais elaborado
    
    O programa a seguir remove stopword de um dado texto de entrada, e salva em um novo arquivo.
    
    ```haskell
    import Data.Char
    
    ignore = ["OF","THE","TO","A","AN","AND","OR","FOR"]
    
    textFilter text = 
      filter  (flip notElem ignore ) 
      $ words 
      $ map toUpper text
    
    main = do
      text <- readFile "entrada.txt"
      writeFile "saida.txt" $ unwords $ textFilter text
    ```
    
    Um exemplo de arquivo de entrada seria:
    
    ```
    Of all the adaptations that allow our animal brethren to soar through the air or endure the darkness and crushing pressure  ...
    ```
    
    Ao executar o programa acima a saída será:
    
    ```
    ALL ADAPTATIONS THAT ALLOW OUR ANIMAL BRETHREN SOAR THROUGH AIR ENDURE DARKNESS CRUSHING PRESSURE ...
    ```
    
    Esse programa pode ser acessado em [https://repl.it/@SergioSouza1/haskellremovestopwords#main.hs](https://repl.it/@SergioSouza1/haskellremovestopwords#main.hs)