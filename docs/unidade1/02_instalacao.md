# Instalando via stack

O guia rápido a instalação do stack pode ser encontrado em:

[https://docs.haskellstack.org/en/stable/README/](https://docs.haskellstack.org/en/stable/README/)

e com mais detalhes em:

[https://docs.haskellstack.org/en/stable/GUIDE/](https://docs.haskellstack.org/en/stable/GUIDE/)

A seguir farei um resumo de alguns pontos que considerei importantes para ajudar fazerem o trabalho da terceira unidade.

[https://youtu.be/SosFv3ME9zs](https://youtu.be/SosFv3ME9zs)

## Como instalar ?

No Linux basta:

```haskell
curl -sSL https://get.haskellstack.org/ | sh
```

Então, será pedido a sua senha de administrador para baixar e depois para copiar o `stack` para o sistema. 

No caso do windows, após baixar o [executável](https://get.haskellstack.org/stable/windows-x86_64-installer.exe), basta seguir o processo "next, next ..."

![](Instalando%20via%20stack/Untitled.png)

![](Instalando%20via%20stack/Untitled%201.png)

Depois de instalado, ao criar um projeto ou acessar o ghci, o stack irá baixar o ghc. Então, para instalar o stack, execute o seguinte comando em um terminal:

```bash
stack ghci
```

Na primeira vez esse processo irá demorar, pois irá baixar o ghc e diversas bibliotecas.

![](Instalando%20via%20stack/Untitled%202.png)

No termino desse processo, você  já poderá interagir  com o GHCI.

![](Instalando%20via%20stack/Untitled%203.png)

## Criando um projeto

Para a atividade, crie o projeto hs2json

```jsx
stack new hs2json
```

Esse comando irá criar uma pasta, nesse caso com o nome hs2json, com alguns arquivos básicos.

![](Instalando%20via%20stack/Untitled%204.png)

Abrindo a pasta no VisualStudio code, observe uma pasta src, que poderá ter módulos, e outros arquivo do projeto. Em app tem o programa principal, que é o Main.hs nesse caso. 

```bash
stack build
```

ele gera um executável com o nome do projeto e o sufixo "-exe". Podemos rodar explicitamente com:

```bash
stack exec hs2json-exe
```

Ou simplesmente:

```bash
stack run
```

Para instalar o executável, basta executar `stack install` e o nome do projeto.

```bash
stack install hs2json
```

No linux, o executável será copiado para a pasta ~/.local/bin:

```bash
Copied executables to /home/sergio/.local/bin:
- hs2json-exe
```

### Teste

Aqui iremos ver como adicionar uma biblioteca, e consequentemente como rodar os teste em seu projeto usando o QuickCheck. Antes de mais nada, vamos precisar de uma função mais útil. Então em lib, adiciona a função qsort:

```haskell
module Lib
    ( 
				someFunc,
        qsort
    ) where

qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (x:xs) = qsort lhs ++ [x] ++ qsort lhs
    where lhs = filter  (< x) xs
          rhs = filter (>= x) xs

someFunc :: IO ()
someFunc = putStrLn "someFunc"
```

Para testar essa função,  vamos adicionar a biblioteca Quickcheck com o seguinte import:

```haskell
import Test.QuickCheck

main :: IO ()
main = putStrLn "Test suite not yet implemented"
```

Agora vamos executar o teste:

```haskell
> stack test
/home/sergio/dev/hs2json/test/Spec.hs:1:1: error:
    Could not find module ‘Test.QuickCheck’
    Use -v to see a list of the files searched for.
  |         
1 | import Test.QuickCheck
```

Isso significa que o import não está disponível. Para poder usar o Quickcheck é necessário adicionar essa dependencia no package.yaml:

```yaml
dependencies:
- base >= 4.7 && < 5
- QuickCheck # adicionado aqui
```

Agora podemos testar novamente:

```bash
> stack test
....
hs2json   > test (suite: hs2json-test)
                     
Test suite not yet implemented

hs2json   > Test suite hs2json-test passed
Completed 5 action(s).
```

Agora vamos implementar um teste para a função quicksort.  Se esta função obedece às regras básicas que uma boa ordenação deveria seguir. Uma invariante útil para começar e uma que aparece com frequência em códigos puramente funcionais, é a idempotência – uma função aplicada duas vezes deve ter o mesmo resultado quando aplicada apenas uma vez. Para a nossa rotina de ordenação – um algoritmo estável de ordenação – isso deve ser sempre verdadeiro. A invariante pode ser codificada como uma simples propriedade, da seguinte maneira

```haskell
prop_idempotent xs = qsort (qsort xs) == qsort xs
```

Em [https://lambda-ma.github.io/rwh-ptbr/cap11](https://lambda-ma.github.io/rwh-ptbr/cap11) é explicado o funcionamento dessa biblioteca. O objetivo desse tutorial é apresentar o `stack`.  Então, por aqui, assuma que vamos precisar atualizar o arquivo `test/Spec.hs`  como a seguir:

```haskell
{-# LANGUAGE TemplateHaskell #-}

import Test.QuickCheck
import Lib

prop_idempotent xs = qsort (qsort xs) == qsort xs

return []
runTests = $quickCheckAll

main :: IO ()
main = runTests >>= \passed -> if passed then putStrLn "Passou em todos testes."
                                             else putStrLn "Alguns testes falharam"
```

Agora podemos rodar os testes:

```bash
> stack test
...
hs2json> test (suite: hs2json-test)
            
Progress 1/2: hs2json=== prop_idempotent from test/Spec.hs:6 ===
*** Failed! Falsified (after 5 tests and 2 shrinks):    
[0,-1]

Alguns testes falharam
```

Verificamos aqui que após 5 tests, ocorreu uma falha. Ao voltarmos ao código encontramos o erro.

```haskell
qsort lhs ++ [x] ++ qsort lhs
```

Deveria ser:

```haskell
qsort lhs ++ [x] ++ qsort rhs
```

O codigo completo deveria ser então:

```haskell
qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (x:xs) = qsort lhs ++ [x] ++ qsort rhs
    where lhs = filter  (< x) xs
          rhs = filter (>= x) xs
```

Então podemos rodar os testes novamente:

```bash
> stack test

...

=== prop_idempotent from test/Spec.hs:6 ===
+++ OK, passed 100 tests.

Passou em todos testes.

hs2json> Test suite hs2json-test passed
Completed 2 action(s).
```