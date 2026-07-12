# Entrada/Saída (I/O) e Programação Interativa

Até este ponto, focamos puramente em expressões funcionais que recebem dados e computam saídas sem qualquer efeito colateral. No entanto, um programa útil na vida real precisa interagir com o mundo externo: ler dados do teclado, gravar arquivos em disco ou realizar requisições de rede. Neste capítulo, estudaremos como o Haskell resolve o paradoxo de interagir com o mundo impuro de forma segura através da **Monad de IO** e da **notação `do`**.

---

## 1. O Paradoxo do I/O na Programação Funcional Pura

Se o Haskell é uma linguagem funcional pura baseada em determinismo matemático (onde a mesma função com os mesmos argumentos sempre retorna o mesmo valor), como podemos implementar uma função como `lerTeclado`? Se o usuário digita coisas diferentes a cada execução, essa função seria impura e violaria as garantias de otimização e avaliação preguiçosa do compilador.

Para resolver este paradoxo, o Haskell separa rigorosamente o mundo das **expressões puras** do mundo das **ações de I/O**.

```text
  ┌────────────────────────────────┐
  │      Mundo Puro (Haskell)      │
  │  - Sem efeitos colaterais      │
  │  - Determinismo absoluto       │
  └───────────────┬────────────────┘
                  │  (Encapsulamento via Tipo IO)
                  ▼
  ┌────────────────────────────────┐
  │       Mundo Impuro (I/O)       │
  │  - Leitura/Escrita de Arquivos │
  │  - Interação com Teclado/Tela  │
  └────────────────────────────────┘
```

---

## 2. A Solução: O Tipo `IO a`

Em Haskell, uma ação que interage com o mundo externo tem o tipo **`IO a`**. Isso significa: *"uma receita/ação que, quando executada pelo sistema operacional, realizará efeitos colaterais e retornará um valor do tipo `a`"*.

* **`IO Char`**: Uma ação que realiza I/O e retorna um caractere (ex: `getChar`).
* **`IO ()`**: Uma ação que realiza I/O mas não retorna nenhum valor útil (representado pelo tipo unitário `()`, semelhante ao `void` de outras linguagens).

> [!IMPORTANT]
> Existe uma diferença crucial entre o tipo `String` e o tipo `IO String`. Um valor do tipo `String` é apenas texto puro que pode ser avaliado com segurança. Um valor do tipo `IO String` é uma **ação pendente** (como ler uma linha do teclado) que só produzirá a string quando for executada. Você nunca pode "extrair" um valor de `IO` para o mundo puro sem que a função inteira também se torne uma ação de `IO`.

---

## 3. Ações Básicas de I/O

A biblioteca padrão do Haskell fornece as seguintes ações primitivas de I/O:

* **`getChar :: IO Char`**: Lê um único caractere do teclado.
* **`putChar :: Char -> IO ()`**: Escreve um único caractere na tela.
* **`getLine :: IO String`**: Lê uma linha inteira de texto do teclado.
* **`putStrLn :: String -> IO ()`**: Escreve uma string na tela seguida por uma nova linha.

---

## 4. Sequenciando Ações com a Notação `do`

Para realizar várias ações de I/O em sequência, utilizamos o construtor sintático **`do`**. Ele nos permite encadear ações de forma linear, assemelhando-se à programação imperativa:

```haskell
interagir :: IO ()
interagir = do
  putStrLn "Qual eh o seu nome?"
  nome <- getLine
  putStrLn ("Bem-vindo ao Haskell, " ++ nome ++ "!")
```

### O Operador de Atribuição de I/O (`<-`)
Note o uso do símbolo **`<-`**. Ele serve para extrair o valor puro produzido por uma ação de `IO` e vinculá-lo a um nome local (neste caso, extraindo a `String` de dentro de `IO String` retornada por `getLine`).

### O Significado de `return` em Haskell
Diferentemente de linguagens imperativas, onde `return` é um comando de controle que interrompe a execução de uma função, em Haskell o **`return` é uma função comum**. 

A função `return :: a -> IO a` pega um valor puro de tipo `a` e o envelopa em uma ação de `IO` que não realiza nenhum efeito colateral:

```haskell
pedirConfirmacao :: IO Bool
pedirConfirmacao = do
  putStrLn "Deseja continuar? (s/n)"
  resposta <- getChar
  if resposta == 's' 
    then return True 
    else return False
```

---

## 5. Manipulação de Arquivos

Além de ler e escrever no console, o Haskell fornece ações básicas para ler e gravar arquivos em disco:

* **`readFile :: FilePath -> IO String`**: Abre e lê todo o conteúdo de um arquivo de forma preguiçosa.
* **`writeFile :: FilePath -> String -> IO ()`**: Grava uma string em um arquivo (sobrescrevendo o conteúdo existente).
* **`appendFile :: FilePath -> String -> IO ()`**: Anexa uma string no final de um arquivo existente.

Exemplo de um programa que lê um arquivo e grava seu conteúdo em maiúsculas em outro arquivo:

```haskell
converterArquivo :: FilePath -> FilePath -> IO ()
converterArquivo origem destino = do
  conteudo <- readFile origem
  let conteudoMaiusculo = map paraMaiuscula conteudo
  writeFile destino conteudoMaiusculo
  putStrLn "Arquivo processado com sucesso!"
  
paraMaiuscula :: Char -> Char
-- Função pura auxiliar (exemplo ilustrativo)
paraMaiuscula c = c -- lógica real usaria Data.Char.toUpper
```

No próximo capítulo, praticaremos esses conceitos avançados de Haskell através de uma coletânea de exercícios sobre tipos e entrada/saída.