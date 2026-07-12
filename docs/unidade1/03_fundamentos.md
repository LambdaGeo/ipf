# 1. Fundamentos

- **Por quê estudar o paradigma funcional ?**
    
    [https://www.youtube.com/watch?v=PuiwBS_CoPY](https://www.youtube.com/watch?v=PuiwBS_CoPY)
    
    - Mudança de paradigma
        
        Como  a seguinte expressão seria avaliada em Python ? e em Haskell ? 
        
        ```haskell
        x = x + 1
        ```
        
        - Avaliação no Haskell
            
            Irá substituir indefenidamente `x` por `x+1`
            
            ```haskell
            x = (x+1) + 1
            x = ((x+1)+1) + 1
            ...
            ```
            
        
        E agora esse:
        
        ```haskell
        x = 0
        x = x + 1
        ```
        
        - Avaliação em Haskell
            
            Levará um erro, pois tem duas definições diferentes para `x`
            
        
        ![](1%20Fundamentos/Untitled.png)
        
    - Conceitos já estão presentes em diversas linguagens e frameworks.
        - Linguagens mais recentes já foram criadas com diversos conceitos de programação funcional como Kotlin, Swift, Rust, Golang ...
        - Outras nem tão novas já tinham alguns recursos, e tem adicionado outros, como Python e JavaScript (arrow functions, react)
        - Outras como Java e C++ também tem incorporado esses conceitos.
    - Melhoria na capacidade de expresar idéias
        
        Segundo diversos autores, aprender novas linguagens melhora a nossa capacidade de expressar idéias. O que pode ser potencializado quando as linguagens são de diferentes paradigmas.
        
    - **Programação funcional é difícil ?**
        
        No início, quando descobre que não tem variáveis, você pode se sentir assim :
        
        ![](1%20Fundamentos/Untitled%201.png)
        
        Mas depois, basta abrir a cabeça e tentar aceitar que se trata de um novo paradigma
        
        ![](1%20Fundamentos/Untitled%202.png)
        
- **Linguagens e Paradigmas de programação**
    
    [https://www.youtube.com/watch?v=iyX0Lzt-ANk](https://www.youtube.com/watch?v=iyX0Lzt-ANk)
    
    - Linguagens de programação
        
        > “*A program is a sequence of symbols that specifies a computation. A programming language is a set of rules that specify which sequences of symbols constitute a program, and what computation the program describes.*”
        > 
        
        > “*A programming language is an artificial formalism in which algorithms can be expressed*”. (Gabbrielli, Maurizio, Martini, Simone - Programming Languages: Principles and Paradigms)
        > 
    - Paradigmas de programação
        - Entre tantas linguagens, podemos identificar diferenças e similaridades
        - As linguagens dentro de um mesmo paradigma, tendem a ter mais similaridades.
        - Definição:
            
            > “A paradigm is a distinctive style of programming. Each paradigm is characterized by the predominance of certain key concepts”. (David Watt - Programming Language Design Concepts)
            > 
            
            ![](1%20Fundamentos/Untitled%203.png)
            
        
        - O 4 principais paradigmas
            
            Um programa em assembly é uma sequência de operações do processador.
            
            Um programa em uma linguagem de alto nível depende do paradigma de programação. Por exemplo
            
            ![](1%20Fundamentos/Untitled%204.png)
            
            - Imperativo
                - Estruturado (ou procedural),  uma coleção de subrotinas ou procedimentos: C, Ada, Pascal
                - Orientado a objeto, uma coleção de objetos que se relacionam e se comunicam através de mensagens: Smalltalk, C++, Java, Python, Ruby, Kotlin, C#
            - Declarativo
                - Funcional, uma composição e aplicações de funções: Haskell, Lisp, Clojure, Elixir ..
                - Lógico,  uma coleção de fatos e regras: Prolog, Mercury
    - Paradigma Funcional
        - Definição
            
            Nos últimos anos a programação funcional tem ganhado um destaque maior, e é fácil ouvir falar sobre esse paradigma em palestras de tecnologia. Porém, é importante distinguir a programação funcional, das linguagens funcionais. De acordo com Hutton: 
            
            > "*Functional programming is style of programming in which the basic method of computation is the application of functions to arguments*;"
            > 
            
            > "*A functional language is one that supports and encourages the functional style*".
            > 
        
        Martin Odersky o criador da linguagem Scala, destaca duas visões, uma mais restrita e outra mais ampla.
        
        - Wider sense, programar com **foco nas funções**, e nas suas composições
            - As funções como **valores de primeira classe,** que significa que elas podem:
                - Ser entrada para outras funções
                - Ser saída de outras funções.
                - Fazer parte de outras estruturas de dados
                - Ser tratada como literais, não precisam estar associadas a um nome, ou seja, elas podem ser anônimas.
                
                Como as funções são valores como qualquer outro, pode-se declarar uma função como se fosse um valor literal. Não é necessário "amarrar" esse valor a um nome. Esse tipo de função é normalmente denominada de funções anônimas, ou expressões lambdas.
                
                ```haskell
                Prelude> map (\x->2 * x) [4,5,6]
                [8,10,12]
                ```
                
            - Sintaxe simplificada
                
                Programar com foco nas funções, elas são usualmente escritas através de uma sintaxe simples. Por exemplo, uma função dobro em Haskell seria definido da seguinte maneira:
                
                ```haskell
                dobro x = 2 * x
                ```
                
                Compare essa definição de função com outras linguagens, como Ada, Pascal, C e até mesmo com linguagens dinâmicas e modernas como Python.
                
                ```python
                def dobro (x) :    
                    return 2 * x
                ```
                
                A chamada de uma função também é simples, basta passar o nome da função e os parâmetros de entrada sem usar parênteses e nem virgulas. Por exemplo, acessando o *repl.it* podemos entrar no terminal com ( [https://repl.it/@profsergiocosta/haskellexemplo1](https://repl.it/@profsergiocosta/haskellexemplo1)) :
                
                ```haskell
                > dobro 2
                4
                ```
                
        - Restricted sense, programar sem **efeitos colaterais (funções puras).**
            
            Programas escritos em linguagens imperativas (estruturadas)  lidam com alteração de estados, onde uma mesma variável pode assumir diferentes valores durante a execução. Por exemplo, a somatoria é usualmente resolvido da seguinte maneira:
            
            ```c
            total = 0;
            for (i = 1; i < 10; ++i)
               total = total+i;
            ```
            
            O mesmo problema poderia ser escrito da seguinte maneira em Haskell:
            
            ```haskell
            sum [1..10]
            ```
            
            - Uma visão mais restrita, define que em um programa funcional é definido por funções que aplicadas a **valores imutáveis** produzem novos valores.
            - As funções não deveriam causar nenhum **efeito colateral**, como uma operação de entrada e saída ou alteração de valores de uma variável.
            - Quando uma função tem um efeito colateral ela deixa de ser uma **função pura** e perde a **transparência referenci~~a~~l**. [Texto no medium que explico melhor esse conceito, e as vantanges.](https://medium.com/@sergiocosta/princ%C3%ADpios-e-padr%C3%B5es-de-programa%C3%A7%C3%A3o-funcional-parte-1-fa3bff0d6d2d)
            - Mesmo em linguagens imperativas é possível escrever funções puras, por exemplo:
                
                ```c
                double dobra(double x) {
                  return 2*x;
                }
                ```
                
                A função abaixo é pura ou impura ?
                
                ```c
                double i = 0;
                
                double dobraMaisI(double x) {
                  i += 1;
                  return 2*x + i;
                }
                
                ```
                
                E essa ?
                
                ```c
                double media (int *valores, int n) {
                    double soma = 0;
                    int i;
                    for (i = 0; i < n; i++)
                        soma_valor(&soma, valores[i]);
                    return soma / n;
                }
                
                void soma_valor (double *soma, int valor) {
                    *soma += valor;
                }
                ```
                
- **Breve histórico da programação funcional**
    
    
    ### Vídeos
    
    - Vídeo aula do Erick Meijer (a partir do minuto 8:00)
        
        [https://youtu.be/UIUlFQH4Cvo](https://youtu.be/UIUlFQH4Cvo)
        
    - Talk do John Hughes
        
        [https://youtu.be/XrNdvWqxBvA](https://youtu.be/XrNdvWqxBvA)
        
    
    ### Timeline
    
    - 1930s: Alonzo Church develops the lambda calculus, a simple but powerful theory of functions.
        
        ![](1%20Fundamentos/Untitled%205.png)
        
    - 1950s: John McCarthy develops Lisp, the first functional language, with some influences from the lambda calculus, but retaining variable assignments.
        
        ![](1%20Fundamentos/Untitled%206.png)
        
    - 1960s: Peter Landin develops ISWIM, the first pure functional language, based strongly on the lambda calculus, with no assignments.
        
        ![](1%20Fundamentos/Untitled%207.png)
        
    - 1970s: John Backus develops FP, a functional language that emphasizes higher-order functions and reasoning about programs.
        
        ![](1%20Fundamentos/Untitled%208.png)
        
    - 1970s: Robin Milner and others develop ML, the first modern functional language, which introduced type inference and polymorphic types.
        
        ![](1%20Fundamentos/Untitled%209.png)
        
    - 1970-1980: David Turner develops a number of lazy functional languages, culminating in the Miranda system.
        
        ![](1%20Fundamentos/Untitled%2010.png)
        
    - 1986: Joseph Leslie Armstrong, na Ericsson, desenvolve a linguage, Erlang.
        
        ![](1%20Fundamentos/Untitled%2011.png)
        
    - 1987:An international committee of researchers initiates the development of Haskell, a standard lazy functional language.
        
        ![](1%20Fundamentos/Untitled%2012.png)
        
    - 2000: Jacques Garrigue extended Objective Caml with several new features, which he had been experimenting with for a few years in the Objective Label dialect of Objective Caml. Among these features were polymorphic methods, labeled and optional function arguments, and polymorphic variants.
        
        ![](1%20Fundamentos/Untitled%2013.png)
        
    - 2003:The committee publishes the Haskell 98 report, defining a stable version of the language.
        
        ![](1%20Fundamentos/Untitled%2014.png)
        
    - 2001-2003 The design of Scala started in 2001 at the [École Polytechnique Fédérale de Lausanne](https://en.wikipedia.org/wiki/%C3%89cole_Polytechnique_F%C3%A9d%C3%A9rale_de_Lausanne) (EPFL) (in [Lausanne](https://en.wikipedia.org/wiki/Lausanne), [Switzerland](https://en.wikipedia.org/wiki/Switzerland)) by [Martin Odersky](https://en.wikipedia.org/wiki/Martin_Odersky). It followed on from work on Funnel, a programming language combining ideas from functional programming and [Petri nets](https://en.wikipedia.org/wiki/Petri_net).[[12]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-history-of-scala-12) Odersky formerly worked on [Generic Java](https://en.wikipedia.org/wiki/Generic_Java), and [javac](https://en.wikipedia.org/wiki/Javac), Sun's Java compiler.[[12]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-history-of-scala-12) After an internal release in late 2003, Scala was released publicly in early 2004 on the [Java platform](https://en.wikipedia.org/wiki/Java_(software_platform)),[[13]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-cacm-13)[[6]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-overview-6)[[12]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-history-of-scala-12)[[14]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-spec-14) A second version (v2.0) followed in March 2006.[[6]](https://en.wikipedia.org/wiki/Scala_(programming_language)#cite_note-overview-6)
        
        ![](1%20Fundamentos/Untitled%2015.png)
        
    - 2005: O post: [The Free Lunch Is Over: A Fundamental Turn Toward Concurrency in Software](http://www.gotw.ca/publications/concurrency-ddj.htm) chama bastante atenção da comunidade.
    - 2005 F#, uma linguagem funcional do dialeto ML, que compila para a máquina virtual CLR, da Microsoft
    - 2007 Clojure, uma linguagem funcional do dialeto Lisp que compila para a máquina virtual do java
    - 2010: O comitê publica Haskell 2010 report.
    - 2011 José Valim lança a linguagem Elixir, que compila para a máquina virtual Erlang.
        
        ![](1%20Fundamentos/Untitled%2016.png)
        
    
- **Primeiros passos com a linguagem Haskell**
    - Vídeo do professor Hugues
        
        [https://youtu.be/LnX3B9oaKzw](https://youtu.be/LnX3B9oaKzw)
        
    
    [https://www.youtube.com/watch?v=3J-Ou955QRE](https://www.youtube.com/watch?v=3J-Ou955QRE)
    
    - Surgiu em 1990 com o objetivo de ser a primeira linguagem puramente funcional.
    - Por muito tempo considerada uma linguagem acadêmica.
    - Atualmente é utilizada em diversas empresas (totalmente ou em parte de projetos).
    - Principais características
        - **Criada por um comitê**
            
            Por ter sido criada por um comitê de estudiosos de linguagem de programação funcional e com a mentalidade de mantê-la útil para o ensino e pesquisa de linguagem de programação, assim como uso em empresas, a linguagem adquiriu diversas características distintas e interessantes não observadas em outras linguagens.
            
        - **Códigos concisos e declarativos**
            
            o programador *declara* o que ele quer ao invés de escrever um passo-a-passo. Programas em Haskell chegam a ser dezenas de vezes menores que em outras linguagens.
            
            ```haskell
            take 100 [x | x <- N, primo x]
            ```
            
        - **Puramente funcional (imutabilidade)**
            - Haskell é considerada uma linguagem puramente funcional, ou seja, ela não possui elementos de programação imperativa, como em Clojure, Lisp, Elixir entre outras.
            - Em Haskell os efeitos colaterais são isolados e assim ela consegue manter as funções puras.
            - A grande maioria das linguagens são impuras, como F#, Clojure, Ocaml, Elixir entre outras. Nessas linguagens os efeitos colaterais são apenas reduzidos, porém existem diversos elementos de programação imperativa.
            - Não existe nem o conceito de variável, apenas nomes e declarações. Uma vez que um nome é declarado com um valor, ele não pode sofrer alterações.
            
            ```haskell
            x = 1.0
            x = 2.0 -- Erro, pois existe duas definições para x
            
            ```
            
        - **Funções Recursivas**
            
            Com a imutabilidade, o conceito de laços de repetição também não existe em linguagens funcionais. Eles são implementados através de funções recursivas.
            
            ```haskell
            f 0 = 1
            f n = 2 * f (n-1)
            
            print (f 10)
            ```
            
        - **Tipos polimórficos**
            
            Permite definir funções genéricas que funcionam para classes de tipos. Por exemplo, o operador de soma *+* pode ser utilizado para qualquer tipo numérico.
            
            ```haskell
            1 + 2         -- 3
            1.0 + 3.0     -- 4.0
            (2%3) + (3%6) -- (7%6)
            
            ```
            
        - **Avaliação preguiçosa**
            - Algumas linguagens funcionais implementam o conceito de avaliação preguiçosa (avaliação não estrita).
            - Quando uma expressão é gerada, ela gera uma promessa de execução. Se e quando necessário, ela é avaliada.
            - Exemplo de avaliação estrita
                
                ```c
                int main () {
                    int x = 2;
                    f(x*x, 4*x + 3);
                    return 0;
                }
                
                int f(int x, int y) {
                    return 2*x;
                }
                
                ```
                
                Passo 1
                
                ```
                int main () {
                    int x = 2;
                    f(2*2, 4*2 + 3);
                    return 0;
                }
                
                int f(int x, int y) {
                    return 2*x;
                }
                
                ```
                
                Passo 2
                
                ```
                int main () {
                    int x = 2;
                    f(4, 4*x + 3);
                    return 0;
                }
                
                int f(int x, int y) {
                    return 2*x;
                }
                
                ```
                
                Passo 3
                
                ```
                int main () {
                    int x = 2;
                    f(4, 11);
                    return 0;
                }
                
                int f(int x, int y) {
                    return 2*x;
                }
                
                ```
                
                Passo 4
                
                ```
                int main () {
                    int x = 2;
                    8;
                    return 0;
                }
                
                int f(int x, int y) {
                    return 2*x;
                }
                
                ```
                
            - Exemplo de avaliação preguiçosa
                
                ```haskell
                f x y = 2*x
                
                main = do
                  let z = 2
                  print (f (z*z) (4*z + 3))
                
                ```
                
                ```haskell
                f x y = 2*x
                
                main = do
                  let z = 2
                  print (2 * (z*z))
                
                ```
                
                ```haskell
                f x y = 2*x
                
                main = do
                  let z = 2
                  print (8)
                
                ```
                
                A expressão 4*z + 3 nunca foi avaliada!
                
                - A avaliação preguiçosa que permite a criação de listas infinitas.
                
                ```haskell
                take 10 [2*i | i <-[1..]]
                ```
                
            
        - **Estaticamente tipada**
            - Algumas linguagens funcionais possuem sistemas de tipos dinâmicos, sendo mais flexíveis, porém mais suscetíveis a erros em tempo de execução.
                - Exemplos de linguagens funcionais dinâmicas incluem Lisp, Clojure e Elixir.
            - Haskell é uma linguagem com um sistema de tipos estático, sendo mais rígida e segura, checando os erros em tempo de compilação e evitando erros em tempo de execução.  Por exemplo, uma implementação simples de uma turma em Haskell poderia ser:
            
            ```haskell
            -- tipos
            data Disciplina = Disciplina {
                sigla::String, 
                nome::String, 
                ch::Int
            } deriving (Show)
            
            data Turma = Turma {
                disciplina::Disciplina, 
                inicio:: String,
                alunos ::[String] 
            } deriving (Show)
            
            -- valores
            pp = Disciplina {
                  sigla ="pp", 
                  nome = "Paradigmas de Programacao",
                  ch = 60 
            }
            
            turma = Turma {
              disciplina = pp,
              inicio = "07/01/2019",
              alunos = ["Marcos", "Ana", "Eva", "Lucas", "Joao"]
            }
            ```
            
            - Em linguagens dinâmicas como Clojure, usa-se as estruturas de dados já existentes, como listas, vetores e maps para representar os dados. Neste caso nenhum tipo de dado é definido, apenas os valores.
            
            ```clojure
            (def pp
              {:disciplina/sigla "pp"
               :disciplina/nome "Paradigmas de Programação"
               :disciplina/ch 60})
            
            (def turma {
                        :turma/disciplina pp
                        :turma/inicio #inst "2018-02-10"
                        :turma/alunos ["Marcos" "Ana" "Eva", "Lucas" "Joao"]})
            ```
            
        - **Sistema de tipagem forte**
            
            Ao contrário de linguagens como *Java* e *C*, as declarações de tipo no Haskell são simplificadas (e muitas vezes podem ser ignoradas), porém, seu sistema rigoroso permite que muitos erros comuns sejam detectados em tempo de **compilação**.
            
            ```java
            int x    = 10;
            double y = 5.1;
            System.out.println("Resultado:  " + (x*y)); // ok
            
            ```
            
            Ser estativamente tipado, não significa ser fortemente tipado. Em Haskell o seguinte código não compila:
            
            ```haskell
            x = 10  :: Int
            y = 5.1 :: Double
            print ("Resultado: " + (x*y) ) -- não compila
            ```
            
            OCaml poderia ser considerada mais fortemente tipada do que Haskell
            
        - **ML-like**
            - Tem a sintaxe influenciada pela linguagem ML como SML, OCaml , F#, Scala e Elixir .
                - Estas linguagens são bem distintas das linguagens da família Lisp que são conhecidas pelo grande quantidade de uso de parenteses.
                    
                    Nas linguagens que são dialetos de Lisp, todo programa é uma coleção de listas, que são processadas por uma “máquina”. Toda lista tem seus valores entre a abertura e fechamento de parênteses. Deste modo, não existe distinção entre código e dado. As linguagens dessa família inclui: Scheme, Racket e Clojure.
                    
            - Para comparação, considere a função fatorial implementado usando case expression em Haskell:
            
            ```haskell
            fat n = case n of
              0 -> 1
              _ -> n * fat (n-1)
            ```
            
            - Agora uma implementação equivalente em F#:
            
            ```fsharp
            let rec fat n = 
                match n with
                | 0 -> 1
                | _ ->  n * fat (n - 1)
            ```
            
        - **Uso de parenteses reduzido**
            
            
            Na matemática a aplicação de funções em seus argumentos é definido pelo nome da função e os parâmetros entre parênteses. A expressão `f(a,b) + c*d` representa a aplicação de `f` nos parâmetros `a,b` e, em seguida, a soma do resultado com o resultado do produto entre `c,d`.
            
            No Haskell, a aplicação de função é definida como o nome da função seguido dos parâmetros separados por espaço com a maior prioridade na aplicação da função. O exemplo anterior ficaria:
            
            ```haskell
            f a b + c*d
            ```
            
            A tabela abaixo contém alguns contrastes entre a notação matemática e o Haskell:
            
            [Aplicação de funções](1%20Fundamentos/Aplica%C3%A7%C3%A3o%20de%20fun%C3%A7%C3%B5es%205b14dfd2cbb14a5280cbfdde7bbba349.csv)
            
        - **Número reduzido de palavas reservadas**
            
            Os únicos nomes que não podem ser utilizados são:
            
            > case, class, data, default, deriving do, else, foreign, if, import, in infix, infixl, infixr, instance, let module, newtype, of, then, type, where
            > 
    - Um Hello World !
        
        Programas escritos em Haskell usa por concenção a extensao .hs. Abaixo um classico Hello World!
        
        ```haskell
        module Main where   -- indica que é o módulo principal
        
        main :: IO ()
        main = do                  -- início da função principal
          putStrLn "hello world"   -- imprime hello world
        ```
        
        Você pode ver esse programa rodando em :[https://repl.it/@SergioSouza1/haskellhelloworld](https://repl.it/@SergioSouza1/haskellhelloworld)
        
        ### Regra de layout
        
        O layout dos códigos em Haskell é similar ao do Python, em que os blocos lógicos são definidos pela indentação.
        
        ```haskell
        f x = a*x + b
             where
               a = 1
               b = 3
        z = f 2 + 3 
        
        ```
        
        A palavra-chave *where* faz parte da definição de *f*, da mesma forma, as definições de *a, b* fazem parte da cláusula *where*. A definição de *z* não faz parte de *f*.
        
        A definição de tabulação varia de editor para editor. Como o espaço é importante no Haskell, **usem espaço ao invés de tab.**
        
        Comentários em uma linha são demarcados pela sequência **--**, comentários em múltiplas linhas são demarcados por **{-** e **-}**:
        
        ```haskell
        -- função que dobra o valor de x
        dobra x = x + x
        
        {-
        dobra recebe uma variável numérica
        e retorna seu valor em dobro.
        -}
        
        ```
        
    - Uma função Haskell um pouco mais complexa 😃
        
        O que está sendo feito pela função abaixo ? 
        
        ```haskell
        f []     = []
        f (x:xs) = f ys ++ [x] ++ f zs
                   where
                      ys = [a | a <- xs, a <= x]
                      zs = [b | b <- xs, b > x]
        ```
        
        - Resposta:
            
            Esse é um algoritmo clássico de ordenação denominado de quicksort. Considerando `q` no lugar de `f`:
            
            ![](1%20Fundamentos/Untitled%2017.png)
            
            Pode experimentar essa função no [repl.it](http://repl.it) [https://repl.it/@SergioSouza1/icognito](https://repl.it/@SergioSouza1/icognito)
            
        
    - **Primeiros passos**
        
        ![](1%20Fundamentos/Untitled%2018.png)
        
        **Glasgow Haskell Compiler**: compilador de código aberto para a linguagem Haskell.
        
        Possui um modo interativo **ghci,** normalmente chamado de REPL (Read Evaluate Print Loop). 
        
        ### Repl.it
        
        Para as aulas e laboratório, iremos usar apenas o repl.it. Ele utiliza o GHC, porém de modo transparente já que não será necessário instalar nada no seu computador.
        
        Muito do curso será acompanhado através de uma turma criada lá. 
        
        <aside>
        📖 Para aprendermos um pouco sobre expressões em Haskell, faça o seguinte laboratorio. As atividade de 1.1 a 2.1:
        
        </aside>
        
        [Sign Up](https://repl.it/classroom/invite/rOFcESf)
        
        <aside>
        📌 Esse laboratório foi criado como base nos [Capítulo 2 do livro Real World Haskell](http://book.realworldhaskell.org/read/getting-started.html) e no Capítulo 2 do livro Programming in Haskell (Graham Hutton)
        
        </aside>
        
        - **Instalação do Stack**
            
            A instalação do Stack e de um editor de texto é opcional, mas pode ser bem aproveitoso, principalmente a partir da terceira semana.
            
            Mas nessa semana, aproveite bem o [repl.it](http://repl.it) 😃
            
            Atualmente é mais utilizado um gerenciador de projeto Stack. Ele mesmo baixa e "instala" o GHC. No terminal de uma distribuição Linux:
            
            ```bash
            curl -sSL https://get.haskellstack.org/ | sh
            ```
            
            ou
            
            ```bash
            wget -qO- https://get.haskellstack.org/ | sh
            ```
            
            ### Interpretador
            
            Depois de instalado o stack, basta:
            
            ```haskell
            $ stack ghci
            > 2+3*4
            14
            
            > (2+3)*4
            20
            
            > sqrt (3^2 + 4^2)
            5.0
            ```
            
            ### Criando projetos
            
            Para criar projetos, utilizaremos a ferramenta stack. Essa ferramenta cria um ambiente isolado
            
            ```haskell
            $ stack new primeiro-projeto simple
            $ cd primeiro-projeto
            $ stack setup
            $ stack build
            $ stack exec primeiro-projeto
            ```
            
            Os dois últimos comandos são referentes a compilação do projeto e execução.
            
            Obs: No inicio desse curso, não é obrigatório trabalhar com o stack, principalmente criar projetos. 
            
            O stack cria a seguinte estrutura de diretório:
            
            - **LICENSE:** informação sobre a licença de uso do software.
            - **README.md:** informações sobre o projeto em formato Markdown.
            - **Setup.hs:** retrocompatibilidade com o sistema cabal.
            - **primeiro-projeto.cabal:** informações das dependências do projeto.
            - **stack.yaml:** parâmetros do projeto
            - **package.yaml:** configurações de compilação e dependências de bibliotecas externas.
            - **src/Main.hs:** arquivo principal do projeto.
            
            Nesse caso, um Hello World 😃
            
            ```haskell
            module Main where   -- indica que é o módulo principal
            
            main :: IO ()
            main = do                  -- início da função principal
              putStrLn "hello world"   -- imprime hello world
            ```
            
        - **Editor de texto**
            
            [Visual Studio Code](http://pesquisa.ufabc.edu.br/haskell/posts/basico/01-Compilador.html) com os pacotes:
            
            - Haskell Syntax Highlighting
            - Haskero
            - hoogle-vscode