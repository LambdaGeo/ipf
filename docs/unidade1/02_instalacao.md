# Instalação e Configuração do Ambiente Haskell

A abordagem moderna e padrão recomendada hoje pela comunidade Haskell para instalar e gerenciar o compilador e suas ferramentas de build é o **GHCup** (Haskell Toolchain Installer). O GHCup gerencia a instalação do compilador GHC, do gerenciador de pacotes Cabal, do servidor de linguagem HLS (Haskell Language Server) e do **Stack**.

Neste livro, utilizaremos o **Stack** como a nossa ferramenta de build e gerenciamento de projetos devido à sua confiabilidade com os *Resolvers* (snapshots compatíveis de pacotes que garantem compilação livre de erros de versão).

---

## 💻 Como Instalar o Haskell com GHCup

### 1. No Linux e macOS
Abra o seu terminal e execute o comando oficial do GHCup:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```
Durante a instalação interativa:
* Pressione **Enter** para aceitar os caminhos padrão do diretório de instalação.
* Quando perguntado se deseja adicionar os caminhos ao seu `PATH` (no arquivo `.bashrc` ou `.zshrc`), responda **Yes (Y)**.
* Quando perguntado se deseja instalar o **Stack** (nossa ferramenta de build), responda **Yes (Y)**.
* Quando perguntado se deseja instalar o **HLS** (Haskell Language Server, essencial para autocompletar e linting no VS Code), responda **Yes (Y)**.

Após a conclusão da instalação, reinicie o seu terminal ou execute `source ~/.bashrc` (ou seu equivalente) para carregar os caminhos de execução.

### 2. No Windows
Abra o console do PowerShell (de preferência como Administrador) e execute o script oficial:
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://get-ghcup.haskell.org/install_haskell.ps1'))
```
Siga as instruções exibidas na tela e selecione as opções para instalar o **Stack** e o **HLS**.

---

## 🛠️ O que é o Stack e como usá-lo?

O **Stack** é um gerenciador de projetos que isola as dependências de cada projeto Haskell. A primeira vez que você rodar um comando do Stack, ele baixará a versão correspondente do compilador GHC automaticamente na sua pasta pessoal de usuário, sem interferir com outras instalações do seu sistema.

Para testar a instalação e abrir o interpretador interativo (REPL) do Haskell gerenciado pelo Stack, execute:
```bash
stack ghci
```
*Na primeira vez, esse comando pode demorar alguns minutos pois o Stack baixará o compilador GHC e as bibliotecas base para o diretório de cache do usuário.*

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

O funcionamento dessa biblioteca será estudado em detalhes na Unidade 2 (capítulo de [Testes com QuickCheck](../unidade2/06_testes_qualidade.md)); a referência original é o capítulo 11 de [*Real World Haskell*](http://book.realworldhaskell.org/read/testing-and-quality-assurance.html). O objetivo deste tutorial é apresentar o `stack`. Então, por aqui, assuma que vamos precisar atualizar o arquivo `test/Spec.hs` como a seguir:

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