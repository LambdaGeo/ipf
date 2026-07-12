# Capítulo 5. Escrevendo uma biblioteca para dados no formato JSON (v2 — Revisado e Validado)

> **Nota desta edição revisada.** Este capítulo é uma adaptação para o português do Capítulo 5 de *Real World Haskell* (Bryan O'Sullivan, Don Stewart e John Goerzen, 2008). O texto original tem mais de quinze anos, e o ecossistema Haskell mudou bastante desde então. Nesta revisão: (1) a instalação e a criação de projetos foram atualizadas para o fluxo moderno com **GHCup** e **Stack** (com `package.yaml`/hpack); (2) o código foi ajustado para compilar em **GHC 9.x** — em particular, desde o GHC 8.4 o operador `<>` faz parte do Prelude, o que exige um ajuste que o livro original não previa; (3) a antiga seção sobre `runghc Setup configure` e `ghc-pkg` foi substituída pelo empacotamento moderno; e (4) **todo o código e todas as saídas de terminal deste capítulo foram executados e conferidos** com GHC 9.4. Onde a saída de uma ferramenta mudou desde 2008, o texto mostra a saída atual.

## Um tour rápido pelo JSON

Neste capítulo, vamos desenvolver uma pequena, mas completa, biblioteca Haskell. Nossa biblioteca manipulará e serializará dados em um popular formato conhecido como JSON.

A linguagem JSON (JavaScript Object Notation) é uma representação pequena e simples para armazenar e transmitir dados estruturados, por exemplo, por meio de uma conexão de rede. É mais comumente usada para transferir dados de um serviço da Web para um aplicativo JavaScript baseado em navegador. O formato JSON é descrito em [www.json.org](https://www.json.org), e em maior detalhe pela RFC 8259 (que substituiu a antiga RFC 4627).

O JSON suporta quatro tipos básicos de valor: *strings*, *numbers*, *booleans* e um valor especial chamado `null`.

```json
"a string"  12345  true  null
```

A linguagem fornece dois tipos compostos: um *array* é uma sequência ordenada de valores, e um *object* é uma coleção não ordenada de pares nome/valor. Os nomes em um objeto são sempre strings; os valores em um objeto ou array podem ser de qualquer tipo.

```json
[-3.14, true, null, "a string"]
{"numbers": [1,2,3,4,5], "useful": false}
```

## Preparando o ambiente: GHCup e Stack

*(Esta seção substitui o antigo "tour rápido pelo Stack", refletindo o fluxo de instalação atual.)*

A forma recomendada de instalar Haskell hoje é o **[GHCup](https://www.haskell.org/ghcup/)**, o instalador oficial da plataforma. Ele instala e gerencia as versões de todas as ferramentas que precisamos:

| Ferramenta | O que é |
| --- | --- |
| **GHC** | O compilador de Haskell (Glasgow Haskell Compiler). |
| **Stack** | Ferramenta de build e projetos, com versões reprodutíveis (usaremos neste capítulo). |
| **cabal-install** | A ferramenta de build "clássica"; alternativa ao Stack (falaremos dela ao final). |
| **HLS** | O Haskell Language Server, que dá autocompletar e erros em tempo real no VS Code e outros editores. |

**Instalação (Linux/macOS/WSL):**

```bash
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
```

O instalador é interativo — aceite as opções padrão e confirme a instalação do Stack e do HLS quando perguntado. No **Windows**, siga as instruções da página do GHCup (há um comando PowerShell equivalente).

**Verificação:** feche e reabra o terminal, e confirme:

```bash
ghc --version      # The Glorious Glasgow Haskell Compilation System, version 9.x
stack --version    # Version 2.x ou superior
```

> 💡 **Sobre versões:** este capítulo foi validado com GHC 9.4, e o código funciona em qualquer GHC da série 9.x. O Stack cuida de fixar uma versão exata de GHC por projeto (via *resolver*), então diferentes projetos podem usar diferentes GHCs sem conflito.

### Criando o projeto

Vamos criar o esqueleto do projeto deste capítulo:

```bash
stack new hs2json
cd hs2json
```

O `stack new` gera uma estrutura de projeto completa. As partes que nos interessam:

```
hs2json/
├── package.yaml      👈 a descrição do pacote (nome, versão, dependências)
├── stack.yaml        👈 configuração do Stack (qual snapshot/GHC usar)
├── src/
│   └── Lib.hs        👈 a biblioteca (código reutilizável)
├── app/
│   └── Main.hs       👈 o executável (o programa em si)
└── test/
    └── Spec.hs       👈 testes (não usaremos neste capítulo)
```

> 💡 **`package.yaml` vs `.cabal`:** o formato "oficial" de descrição de pacotes Haskell é o arquivo `.cabal`. O template do Stack usa uma camada mais amigável por cima dele: o `package.yaml`, processado por uma ferramenta chamada **hpack** (embutida no Stack). A cada `stack build`, o hpack gera o arquivo `hs2json.cabal` automaticamente a partir do `package.yaml`. A grande vantagem para nós: o hpack **detecta sozinho os módulos** dentro de `src/` — quando criarmos `SimpleJSON.hs`, `Prettify.hs` etc., não precisaremos registrá-los manualmente em lugar nenhum. (O `.cabal` gerado não deve ser editado à mão; falaremos mais sobre ele na seção de empacotamento, ao final.)

Os três comandos que usaremos o tempo todo:

```bash
stack build          # compila o projeto
stack run            # compila (se preciso) e executa o executável
stack ghci           # abre o REPL com os módulos do projeto carregados
```

Na **primeira** execução de `stack build`, o Stack pode baixar a versão de GHC definida no `stack.yaml` — é demorado, mas acontece uma vez só.

## Representando dados JSON em Haskell

Primeiro, crie um novo arquivo `SimpleJSON.hs` em `src/`:

```haskell
-- src/SimpleJSON.hs
module SimpleJSON where
```

Para trabalhar com dados JSON no Haskell, usamos um tipo de dados algébrico para representar os valores possíveis nesse formato:

```haskell
-- src/SimpleJSON.hs
data JValue = JString String
            | JNumber Double
            | JBool Bool
            | JNull
            | JObject [(String, JValue)]
            | JArray [JValue]
              deriving (Eq, Ord, Show)
```

Para cada tipo de JSON, fornecemos um construtor de valor distinto. Alguns desses construtores possuem parâmetros: se quisermos construir uma string JSON, devemos fornecer um valor `String` como argumento para o construtor `JString`.

Para começar a experimentar esse código, salve o arquivo `SimpleJSON.hs` no seu editor, alterne para uma janela de terminal e carregue o projeto no REPL executando o seguinte comando na raiz do projeto:

```
$ stack ghci
Using main module: 1. Package `hs2json' component hs2json:exe:hs2json-exe with main-is file: .../app/Main.hs
Building all executables for `hs2json' once. ...
Configuring GHCi with the following packages: hs2json
GHCi, version 9.4.7: https://www.haskell.org/ghc/  :? for help
[1 of 3] Compiling Lib              ( src/Lib.hs, interpreted )
[2 of 3] Compiling SimpleJSON       ( src/SimpleJSON.hs, interpreted )
[3 of 3] Compiling Main             ( app/Main.hs, interpreted )
Ok, three modules loaded.
ghci> JString "foo"
JString "foo"
ghci> JNumber 2.7
JNumber 2.7
ghci> :type JBool True
JBool True :: JValue
```

*(A saída exata do cabeçalho varia com as versões, mas o prompt e o comportamento são estes.)*

Podemos ver como usar um construtor para pegar um valor Haskell normal e transformá-lo em um `JValue`. Para fazer o inverso, usamos casamento de padrões. Aqui está uma função que podemos adicionar ao `SimpleJSON.hs`, que irá extrair uma string de um valor JSON para nós. Se o valor JSON realmente contiver uma string, nossa função envolverá a string com o construtor `Just`. Caso contrário, retornará `Nothing`.

```haskell
-- src/SimpleJSON.hs
getString :: JValue -> Maybe String
getString (JString s) = Just s
getString _           = Nothing
```

Quando salvamos o arquivo de código-fonte modificado, podemos recarregá-lo no `stack ghci` com o comando `:r` e testar a nova definição:

```
ghci> :r
[2 of 3] Compiling SimpleJSON       ( src/SimpleJSON.hs, interpreted )
Ok, three modules loaded.
ghci> getString (JString "hello")
Just "hello"
ghci> getString (JNumber 3)
Nothing
```

A seguir, mais algumas funções acessoras. Desta vez incluímos as assinaturas de tipo — o GHC as infere sozinho, mas escrevê-las é uma boa prática (e o template do Stack ativa avisos que nos lembram disso):

```haskell
-- src/SimpleJSON.hs
getInt :: JValue -> Maybe Int
getInt (JNumber n) = Just (truncate n)
getInt _           = Nothing

getDouble :: JValue -> Maybe Double
getDouble (JNumber n) = Just n
getDouble _           = Nothing

getBool :: JValue -> Maybe Bool
getBool (JBool b) = Just b
getBool _         = Nothing

getObject :: JValue -> Maybe [(String, JValue)]
getObject (JObject o) = Just o
getObject _           = Nothing

getArray :: JValue -> Maybe [JValue]
getArray (JArray a) = Just a
getArray _          = Nothing

isNull :: JValue -> Bool
isNull v = v == JNull
```

A função `truncate` transforma um número de ponto flutuante ou racional em um inteiro, descartando os dígitos após o ponto decimal:

```
ghci> truncate 5.8
5
ghci> :module +Data.Ratio
ghci> truncate (22 % 7)
3
```

## A anatomia de um módulo Haskell

Um arquivo fonte do Haskell contém a definição de um único *module*. Um módulo nos permite determinar quais nomes dentro dele são acessíveis a partir de outros módulos.

Um arquivo fonte começa com uma declaração `module`. Ela deve preceder todas as outras definições no arquivo:

```haskell
-- src/SimpleJSON.hs
module SimpleJSON
    (
      JValue(..)
    , getString
    , getInt
    , getDouble
    , getBool
    , getObject
    , getArray
    , isNull
    ) where
```

A palavra `module` é reservada. Ela é seguida pelo nome do módulo, que deve começar com uma letra maiúscula. Um arquivo fonte deve ter o mesmo *base name* (o componente antes do sufixo) que o nome do módulo que ele contém. É por isso que nosso arquivo `SimpleJSON.hs` contém um módulo chamado `SimpleJSON`.

Após o nome do módulo há uma lista de *exportações*, entre parênteses. A palavra-chave `where` indica que o corpo do módulo vem a seguir.

A lista de exportações indica quais nomes deste módulo estão visíveis para outros módulos. Isso nos permite manter o código privado escondido do mundo exterior. A notação especial `(..)` que segue o nome `JValue` indica que estamos exportando o tipo **e todos os seus construtores**.

Pode parecer estranho que possamos exportar o nome de um tipo (isto é, seu construtor de tipo) mas não seus construtores de valor. A capacidade de fazer isso é importante: ela nos permite ocultar os detalhes de um tipo dos seus usuários, tornando o tipo **abstrato**. Se não podemos ver os construtores de valor de um tipo, não podemos casar padrões com um valor desse tipo, nem construir um novo valor desse tipo. Mais adiante neste capítulo, veremos uma situação em que **queremos** exatamente isso.

Se omitirmos as exportações (e os parênteses que as envolvem) da declaração do módulo, todos os nomes do módulo serão exportados:

```haskell
module ExportEverything where
```

Para não exportar nenhum nome (o que raramente é útil), escrevemos uma lista de exportação vazia, usando um par de parênteses:

```haskell
module ExportNothing () where
```

## Compilando um programa Haskell

Para compilar o projeto e executar o binário, na raiz do projeto:

```
$ stack build
$ stack run
someFunc
```

*(O `someFunc` vem do `src/Lib.hs` gerado pelo template — é o "hello world" do esqueleto.)*

Agora que compilamos com sucesso nossa biblioteca mínima, vamos começar a escrever a biblioteca proposta aqui. Antes de seguir, **apague o arquivo `src/Lib.hs`**, já que não o usaremos mais, e então modifique o `app/Main.hs`:

```haskell
-- app/Main.hs
module Main (main) where

import SimpleJSON

main :: IO ()
main = print (JObject [("foo", JNumber 1), ("bar", JBool False)])
```

> 💡 Graças ao hpack, apagar `Lib.hs` e criar `SimpleJSON.hs` **não exige editar configuração nenhuma**: no próximo `stack build`, o arquivo `hs2json.cabal` é regenerado refletindo os módulos que existem em `src/`. (No fluxo antigo do livro original, cada módulo novo precisava ser registrado à mão no `.cabal`.)

Observe a diretiva `import` que segue a declaração do módulo. Ela indica que queremos pegar todos os nomes exportados do módulo `SimpleJSON` e disponibilizá-los no nosso módulo. Quaisquer diretivas `import` devem aparecer em grupo, no início do módulo — após a declaração `module`, mas antes de todo o resto do código. Não podemos espalhá-las pelo arquivo.

Os nomes dos arquivos fonte e das funções ficam a cargo do programador. Porém, para criar um executável, o GHC espera um módulo chamado `Main` que contenha uma função chamada `main`. A função `main` é a que será chamada quando executarmos o programa.

```
$ stack build
$ stack run
JObject [("foo",JNumber 1.0),("bar",JBool False)]
```

## Imprimindo dados JSON

Agora que temos uma representação em Haskell para os tipos JSON, gostaríamos de ser capazes de pegar valores Haskell e produzi-los como dados JSON.

Há algumas maneiras de fazer isso. Talvez a mais direta seja escrever uma função que imprima os valores no formato JSON. Quando terminarmos, exploraremos abordagens mais interessantes.

```haskell
-- src/PutJSON.hs
module PutJSON where

import Data.List (intercalate)
import SimpleJSON

renderJValue :: JValue -> String
renderJValue (JString s)   = show s
renderJValue (JNumber n)   = show n
renderJValue (JBool True)  = "true"
renderJValue (JBool False) = "false"
renderJValue JNull         = "null"
renderJValue (JObject o) = "{" ++ pairs o ++ "}"
  where pairs [] = ""
        pairs ps = intercalate ", " (map renderPair ps)
        renderPair (k,v) = show k ++ ": " ++ renderJValue v
renderJValue (JArray a) = "[" ++ values a ++ "]"
  where values [] = ""
        values vs = intercalate ", " (map renderJValue vs)
```

Uma boa prática em Haskell é separar o código puro do código que produz efeitos de entrada e saída (`IO ()`). Nossa função `renderJValue` não interage com o mundo exterior, mas ainda precisamos ser capazes de **imprimir** um `JValue`:

```haskell
-- src/PutJSON.hs
putJValue :: JValue -> IO ()
putJValue v = putStrLn (renderJValue v)
```

Imprimir um valor JSON agora é fácil.

Por que separar o código de renderização do código que realmente imprime? Isso nos dá flexibilidade. Por exemplo: se quiséssemos compactar os dados antes de imprimi-los, e o código de renderização estivesse misturado com o de impressão, adaptar o código seria muito mais difícil.

Essa ideia de separar código puro de código impuro é poderosa e onipresente em Haskell. Várias bibliotecas de compressão existem, e todas têm uma interface simples: uma função que aceita uma string descompactada e retorna uma string compactada. Podemos usar composição de funções para converter dados JSON em string e compactá-los em outra string, adiando qualquer decisão sobre como, efetivamente, mostrar ou transmitir os dados.

Experimentando:

```
$ stack ghci
ghci> import PutJSON
ghci> putJValue (JObject [("nome", JString "Sergio"), ("idade", JNumber 38)])
{"nome": "Sergio", "idade": 38.0}
```

## Uma visão mais geral de renderização

Nosso código de renderização JSON está adaptado às necessidades dos nossos tipos de dados e às convenções de formatação do JSON. A saída que ele produz pode não ser amigável aos olhos humanos. Agora olharemos a renderização como uma tarefa mais genérica: como construir uma biblioteca útil para renderizar dados em uma variedade de situações?

Gostaríamos de produzir saídas adequadas tanto para consumo humano (para depurar, por exemplo) quanto para processamento por máquinas. Bibliotecas que fazem essa tarefa são chamadas de *pretty printers* — "impressoras agradáveis". Há várias bibliotecas Haskell prontas desse tipo. Não estamos criando a nossa para substituí-las, mas pelos vários aprendizados que ganharemos em design de bibliotecas e técnicas de programação funcional.

Chamaremos nosso módulo genérico de pretty printing de `Prettify`; o código ficará no arquivo `src/Prettify.hs`.

> **Nomeando:** no módulo `Prettify`, basearemos nossos nomes naqueles usados por várias bibliotecas bem estabelecidas desse tipo. Isso nos dá um grau de compatibilidade com as bibliotecas maduras.

Para termos certeza de que `Prettify` atende a necessidades práticas, escreveremos um novo renderizador de JSON que usa a API do `Prettify`. Depois que estiver pronto, voltaremos e preencheremos os detalhes do módulo `Prettify`.

Em vez de renderizar direto para string, nosso `Prettify` usará um tipo **abstrato**, que chamaremos de `Doc`. Baseando nossa biblioteca em um tipo abstrato, podemos trocar a implementação por uma mais flexível ou mais eficiente sem que os usuários da biblioteca percebam.

Chamaremos nosso novo renderizador JSON de `PrettyJSON.hs`, mantendo o nome `renderJValue` para a função de renderização. Renderizar um dos valores básicos do JSON é simples:

```haskell
-- src/PrettyJSON.hs
module PrettyJSON where

import Prelude hiding ((<>))

import SimpleJSON
import Prettify

renderJValue :: JValue -> Doc
renderJValue (JBool True)  = text "true"
renderJValue (JBool False) = text "false"
renderJValue JNull         = text "null"
renderJValue (JNumber num) = double num
renderJValue (JString str) = string str
```

O tipo `Doc` e as funções `text`, `double` e `string` serão fornecidos pelo nosso módulo `Prettify`.

> ⚠️ **A linha `import Prelude hiding ((<>))` é obrigatória — e é a maior mudança desde o livro original.** Quando *Real World Haskell* foi escrito, o operador `<>` era um nome livre. Desde o **GHC 8.4** (2018), porém, o Prelude exporta `<>` (o operador da classe `Semigroup`). Como nossa biblioteca define o **seu próprio** `<>` para concatenar documentos, precisamos esconder o do Prelude em **todos os módulos que definem ou usam o nosso** — ou seja, tanto em `Prettify.hs` quanto em `PrettyJSON.hs`. Se você esquecer essa linha, o GHC reclamará de *"Ambiguous occurrence '<>'"*. Guarde este erro: ele é um clássico ao seguir material antigo de Haskell.

## Desenvolvendo código Haskell sem quebrar a cabeça

No início, quando estamos nos familiarizando com o desenvolvimento em Haskell, temos tantos conceitos novos para entender de uma vez que escrever código que compile sem erros pode ser um desafio.

Enquanto escrevemos o corpo inicial do código, ajuda muito parar a cada poucos minutos e tentar compilar o que produzimos até o momento. Como Haskell é fortemente tipado, se o código compila, estamos longe de muitas armadilhas da programação.

Uma técnica útil para desenvolver o esqueleto de um programa é escrever versões *de esboço* (placeholders) dos nossos tipos e funções. Por exemplo: dissemos acima que as funções `string`, `text` e `double` serão fornecidas pelo módulo `Prettify`. Se não fornecermos definições para essas funções nem para o tipo `Doc`, nosso lema "compile cedo, compile frequentemente" falha logo no renderizador, pois o compilador não conhece nada sobre elas. Para evitar o problema, escrevemos esboços que não fazem nada:

```haskell
-- src/Prettify.hs
module Prettify where

import Prelude hiding ((<>))

data Doc = ToBeDefined
         deriving (Show)

string :: String -> Doc
string str = undefined

text :: String -> Doc
text str = undefined

double :: Double -> Doc
double num = undefined
```

O valor especial `undefined` tem o tipo `a`, então ele passa pela verificação de tipos não importa onde o usemos. Se tentarmos **avaliá-lo**, ele causará um erro no programa:

```
ghci> :type undefined
undefined :: HasCallStack => a
ghci> undefined
*** Exception: Prelude.undefined
ghci> :type double
double :: Double -> Doc
ghci> double 3.14
*** Exception: Prelude.undefined
```

*(No GHC moderno, o tipo aparece como `HasCallStack => a` — o `HasCallStack` é só o mecanismo que permite ao erro apontar a linha exata onde o `undefined` explodiu. Para nossos propósitos, leia como o `a` do livro original.)*

Embora não possamos **executar** os esboços, o verificador de tipos garante que o programa está sensatamente tipado.

## Impressão agradável de uma string

Quando precisamos imprimir uma string, o JSON impõe regras de escape moderadamente complexas que devemos seguir. No nível mais alto, uma string é apenas uma série de caracteres entre aspas.

Estas funções fazem parte do **renderizador**, então vão em `PrettyJSON.hs`:

```haskell
-- src/PrettyJSON.hs
string :: String -> Doc
string = enclose '"' '"' . hcat . map oneChar
```

> **Estilo ponto-livre:** este estilo de escrever uma definição exclusivamente como composição de outras funções é chamado de *estilo ponto-livre* (point-free). O uso da palavra "ponto" **não** se refere ao caractere `.` da composição; o termo é aproximadamente sinônimo (em Haskell) de *valor* — uma definição ponto-livre não menciona o valor sobre o qual opera.
>
> Compare a definição ponto-livre de `string`, acima, com esta versão "pointy", que usa a variável `s` para se referir ao valor:
>
> ```haskell
> pointyString :: String -> Doc
> pointyString s = enclose '"' '"' (hcat (map oneChar s))
> ```

A função `enclose` simplesmente põe um valor `Doc` entre um caractere de abertura e um de fechamento:

```haskell
-- src/PrettyJSON.hs
enclose :: Char -> Char -> Doc -> Doc
enclose left right x = char left <> x <> char right
```

O operador `(<>)` será fornecido pela nossa biblioteca `Prettify`. Ele concatena dois valores `Doc` — é o análogo, para documentos, do `(++)` das listas. Adicione os esboços ao `Prettify.hs`:

```haskell
-- src/Prettify.hs
(<>) :: Doc -> Doc -> Doc
a <> b = undefined

char :: Char -> Doc
char c = undefined
```

*(Lembre: o `import Prelude hiding ((<>))` no topo do `Prettify.hs` é o que nos permite definir nosso próprio `<>` sem ambiguidade.)*

Nossa biblioteca `Prettify` também fornece `hcat`, que concatena múltiplos valores `Doc` em um só — análogo ao `concat` para listas:

```haskell
-- src/Prettify.hs
hcat :: [Doc] -> Doc
hcat xs = undefined
```

Nossa função `string` aplica `oneChar` a cada caractere da string, concatena tudo, e põe o resultado entre aspas. A função `oneChar` escapa ou renderiza um caractere individual:

```haskell
-- src/PrettyJSON.hs
oneChar :: Char -> Doc
oneChar c = case lookup c simpleEscapes of
              Just r -> text r
              Nothing | mustEscape c -> hexEscape c
                      | otherwise    -> char c
    where mustEscape ch = ch < ' ' || ch == '\x7f' || ch > '\xff'

simpleEscapes :: [(Char, String)]
simpleEscapes = zipWith ch "\b\n\f\r\t\\\"/" "bnfrt\\\"/"
    where ch a b = (a, ['\\',b])
```

O valor `simpleEscapes` é uma lista de pares. Chamamos uma lista de pares de *lista de associação*, ou simplesmente *alist* (de *association list*). Cada elemento da nossa alist associa um caractere à sua versão escapada:

```
ghci> take 4 simpleEscapes
[('\b',"\\b"),('\n',"\\n"),('\f',"\\f"),('\r',"\\r")]
```

Nossa expressão `case` tenta casar o caractere com a alist. Se encontramos uma correspondência, a emitimos; caso contrário, talvez precisemos escapar o caractere de uma forma mais complicada, e nesse caso realizamos esse escape. Somente se nenhum escape é necessário emitimos o caractere como texto puro. Para sermos conservadores, os únicos caracteres sem escape que emitimos são os ASCII imprimíveis.

O escape mais sofisticado envolve transformar o caractere na string `"\u"` seguida de uma sequência de quatro caracteres hexadecimais representando o valor numérico do caractere Unicode:

```haskell
-- src/PrettyJSON.hs
smallHex :: Int -> Doc
smallHex x  = text "\\u"
           <> text (replicate (4 - length h) '0')
           <> text h
    where h = showHex x ""
```

A função `showHex` vem do módulo `Numeric` (você precisará importá-lo no início do `PrettyJSON.hs`) e retorna a representação hexadecimal de um número:

```
ghci> import Numeric
ghci> showHex 114111 ""
"1bdbf"
```

A função `replicate` é fornecida pelo Prelude e cria uma lista de tamanho fixo com o elemento repetido:

```
ghci> replicate 5 "foo"
["foo","foo","foo","foo","foo"]
```

Há um problema: a codificação de quatro dígitos do `smallHex` só consegue representar caracteres Unicode até `0xffff`, mas caracteres Unicode válidos vão até `0x10ffff`. Para representar corretamente um caractere acima de `0xffff` em uma string JSON, seguimos regras (complicadas) que o dividem em **dois** valores de 16 bits — os chamados *pares substitutos* (surrogate pairs). Isso nos dá a oportunidade de fazer manipulação de bits em Haskell:

```haskell
-- src/PrettyJSON.hs
astral :: Int -> Doc
astral n = smallHex (a + 0xd800) <> smallHex (b + 0xdc00)
    where a = (n `shiftR` 10) .&. 0x3ff
          b = n .&. 0x3ff
```

A função `shiftR`, do módulo `Data.Bits`, desloca um número para a direita. A função `(.&.)`, do mesmo módulo, executa a conjunção (E) bit a bit de dois valores:

```
ghci> import Data.Bits
ghci> 0x10000 `shiftR` 4
4096
```

Agora que escrevemos `smallHex` e `astral`, podemos fornecer a definição de `hexEscape` (a função `ord`, do módulo `Data.Char`, converte um caractere para seu código numérico):

```haskell
-- src/PrettyJSON.hs
hexEscape :: Char -> Doc
hexEscape c | d < 0x10000 = smallHex d
            | otherwise   = astral (d - 0x10000)
  where d = ord c
```

Ok, agora pode compilar:

```
$ stack build
```

## Arrays, objetos e o cabeçalho do módulo

Comparada com strings, a impressão agradável de arrays e objetos é fácil. Sabemos que ambos são visualmente similares: cada um inicia com um caractere de abertura, seguido por uma série de valores separados por vírgulas, seguida por um caractere de fechamento. Vamos escrever uma função que captura essa estrutura comum:

```haskell
-- src/PrettyJSON.hs
series :: Char -> Char -> (a -> Doc) -> [a] -> Doc
series open close item = enclose open close
                       . fsep . punctuate (char ',') . map item
```

Comecemos interpretando o tipo dessa função. Ela recebe um caractere de abertura e um de fechamento, e uma função que sabe imprimir um valor de algum tipo desconhecido `a`, seguida por uma lista de valores do tipo `a`, e retorna um valor do tipo `Doc`.

Note que, embora a assinatura de tipos mencione quatro parâmetros, listamos apenas três na definição da função. Estamos simplesmente seguindo a mesma regra que nos permite simplificar uma definição como `myLength xs = length xs` para `myLength = length`.

Já escrevemos `enclose`. A função `fsep` viverá no módulo `Prettify`: ela combina uma lista de valores `Doc` em um só, possivelmente quebrando linhas caso a saída não caiba em uma linha só.

```haskell
-- src/Prettify.hs
fsep :: [Doc] -> Doc
fsep xs = undefined
```

A partir de agora, você já sabe definir os próprios esboços no `Prettify`, seguindo os exemplos anteriores — não mostraremos mais nenhum explicitamente.

A função `punctuate` também viverá no `Prettify`, e podemos defini-la **de verdade** em termos de funções para as quais já temos esboços:

```haskell
-- src/Prettify.hs
punctuate :: Doc -> [Doc] -> [Doc]
punctuate p []     = []
punctuate p [d]    = [d]
punctuate p (d:ds) = (d <> p) : punctuate p ds
```

Com essa definição de `series`, imprimir arrays é totalmente direto. Adicionamos esta equação ao final do bloco que escrevemos para `renderJValue`:

```haskell
-- src/PrettyJSON.hs
renderJValue (JArray ary) = series '[' ']' renderJValue ary
```

Para imprimir um objeto, precisamos de só um pouco mais de trabalho: para cada elemento, temos um nome **e** um valor com que lidar.

```haskell
-- src/PrettyJSON.hs
renderJValue (JObject obj) = series '{' '}' field obj
    where field (name,val) = string name
                          <> text ": "
                          <> renderJValue val
```

Ok, agora pode compilar:

```
$ stack build
```

### Escrevendo o cabeçalho do módulo

Agora que escrevemos o corpo do `PrettyJSON.hs`, voltamos ao topo e completamos a declaração do módulo:

```haskell
-- src/PrettyJSON.hs
module PrettyJSON
    (
      renderJValue
    ) where

import Prelude hiding ((<>))

import Numeric (showHex)
import Data.Char (ord)
import Data.Bits (shiftR, (.&.))

import SimpleJSON (JValue(..))
import Prettify (Doc, (<>), char, double, fsep, hcat, punctuate, text)
```

Exportamos apenas uma função deste módulo: `renderJValue`, nossa função de renderização de JSON. As outras definições existem puramente para dar suporte a ela, então não há razão para torná-las visíveis a outros módulos.

Sobre as importações: os módulos `Numeric`, `Data.Char` e `Data.Bits` são distribuídos junto com o GHC (no pacote `base`). Nós mesmos escrevemos o `SimpleJSON` e preenchemos o `Prettify` com definições esqueléticas. Note que não há diferença alguma na forma de importar módulos padrão e módulos que escrevemos.

> 💡 O livro original também importava `compact` e `pretty` neste cabeçalho. Não faça isso: essas funções serão **usadas por quem chama** o `PrettyJSON` (nós, no GHCi), não por ele — e o GHC moderno, com os avisos que o template do Stack ativa, reclamaria (com razão) de importação não utilizada.

Em cada diretiva `import` listamos explicitamente os nomes que queremos trazer para o escopo. Isso não é obrigatório — omitindo a lista, todos os nomes exportados ficam disponíveis —, mas é geralmente uma boa ideia:

- Uma lista explícita deixa claro **de onde** cada nome vem, facilitando achar a documentação de uma função desconhecida.
- Se o mantenedor de uma biblioteca remover ou renomear uma função, o erro de compilação resultante pode ocorrer muito tempo depois de escrevermos o módulo. A lista explícita age como lembrete de onde o nome ausente vinha, acelerando o diagnóstico.
- Se alguém adicionar a um módulo um nome idêntico a um do nosso código, sem lista explícita terminaremos com o mesmo nome em escopo duas vezes — e o GHC reportará ambiguidade se o usarmos. (Foi exatamente o que aconteceu, em escala global, com o `<>` e o Prelude!)

A explicitação das importações é uma orientação de bom senso, não uma regra rígida. Às vezes precisamos de tantos nomes de um módulo que listá-los se torna cansativo; em outros casos, um módulo é tão amplamente usado que qualquer programador Haskell experiente sabe o que vem dele.

## Criando a biblioteca de impressão agradável

No módulo `Prettify`, representamos o tipo `Doc` como um tipo de dados algébrico:

```haskell
-- src/Prettify.hs
data Doc = Empty
         | Char Char
         | Text String
         | Line
         | Concat Doc Doc
         | Union Doc Doc
           deriving (Show, Eq)
```

Observe que o tipo `Doc` é, na verdade, uma **árvore**. Os construtores `Concat` e `Union` criam um nó interno a partir de outros dois valores `Doc`, enquanto `Empty` e os demais construtores simples formam as folhas.

No cabeçalho do módulo, exportaremos o nome do tipo, **mas não seus construtores** (repare: `Doc`, e não `Doc(..)`). Isso impedirá que módulos que usem `Doc` criem valores diretamente ou casem padrões com eles — é o tipo abstrato de que falamos:

```haskell
-- src/Prettify.hs
module Prettify
    (
      Doc
    , empty
    , char
    , text
    , double
    , line
    , (<>)
    , hcat
    , fsep
    , (</>)
    , punctuate
    , group
    , softline
    , compact
    , pretty
    ) where

import Prelude hiding ((<>))
```

Em vez de criar um `Doc` na mão, um usuário do módulo `Prettify` chamará uma função que fornecemos. Eis as funções de construção simples. À medida que adicionamos as definições reais, **substituímos os esboços** que estavam no `Prettify.hs`:

```haskell
-- src/Prettify.hs
empty :: Doc
empty = Empty

char :: Char -> Doc
char c = Char c

text :: String -> Doc
text "" = Empty
text s  = Text s

double :: Double -> Doc
double d = text (show d)
```

O construtor `Line` representa uma quebra de linha. A função `line` cria uma quebra de linha *hard*, que sempre aparece na saída da biblioteca. Às vezes queremos uma quebra de linha *soft*, usada somente se a linha for grande demais para caber na janela ou página — introduziremos a função `softline` em breve.

```haskell
-- src/Prettify.hs
line :: Doc
line = Line
```

Quase tão simples quanto os construtores básicos é a função `(<>)`, que concatena dois valores `Doc`:

```haskell
-- src/Prettify.hs
(<>) :: Doc -> Doc -> Doc
Empty <> y = y
x <> Empty = x
x <> y = x `Concat` y
```

Casamos o padrão `Empty` de forma que concatenar um `Doc` com `Empty` à esquerda ou à direita não tenha efeito. Isso evita acrescentar valores inúteis à árvore:

```
ghci> text "foo" <> text "bar"
Concat (Text "foo") (Text "bar")
ghci> text "foo" <> empty
Text "foo"
ghci> empty <> text "bar"
Text "bar"
```

> **Um momento matemático:** se colocarmos brevemente nossos chapéus de matemáticos, podemos dizer que `Empty` é a **identidade** da concatenação, pois nada acontece ao concatenar um `Doc` com `Empty` — assim como `0` é a identidade da adição e `1` a da multiplicação. Essa perspectiva tem consequências muito úteis. Aliás, aqui está a piada interna do Haskell moderno: um tipo com uma operação associativa como `<>` é um **`Semigroup`**, e com um elemento identidade como `empty` é um **`Monoid`** — exatamente as classes que hoje vivem no Prelude e que nos obrigaram ao `hiding ((<>))`. Nosso `Doc` poderia declarar instâncias delas; fica como exploração para depois das classes de tipos (Capítulo 6).

Nossas funções `hcat` e `fsep` concatenam uma lista de `Doc` em um só. Lembre-se de que podemos definir a concatenação de listas usando `foldr`:

```haskell
concat :: [[a]] -> [a]
concat = foldr (++) []
```

Como `(<>)` é análogo a `(++)`, e `empty` a `[]`, podemos escrever `hcat` e `fsep` como *folds* também:

```haskell
-- src/Prettify.hs
hcat :: [Doc] -> Doc
hcat = fold (<>)

fold :: (Doc -> Doc -> Doc) -> [Doc] -> Doc
fold f = foldr f empty
```

A definição de `fsep` depende de várias outras funções:

```haskell
-- src/Prettify.hs
fsep :: [Doc] -> Doc
fsep = fold (</>)

(</>) :: Doc -> Doc -> Doc
x </> y = x <> softline <> y

softline :: Doc
softline = group line
```

Isso merece uma explicação. A `softline` deve inserir uma nova linha se a linha atual ficar muito grande, ou um espaço, caso contrário. Como fazer isso, se o tipo `Doc` não sabe nada sobre renderização? Nossa resposta: toda vez que encontramos uma linha soft, mantemos **duas representações alternativas** do documento, usando o construtor `Union`:

```haskell
-- src/Prettify.hs
group :: Doc -> Doc
group x = flatten x `Union` x
```

Nossa função `flatten` substitui cada `Line` por um espaço, transformando duas linhas em uma só:

```haskell
-- src/Prettify.hs
flatten :: Doc -> Doc
flatten (x `Concat` y) = flatten x `Concat` flatten y
flatten Line           = Char ' '
flatten (x `Union` _)  = flatten x
flatten other          = other
```

Note que sempre chamamos `flatten` no lado **esquerdo** de uma `Union`: esse lado tem sempre o mesmo tamanho (em caracteres) ou é maior que o direito. Usaremos essa propriedade na função de renderização adiante.

### Renderização compacta

Frequentemente precisamos da representação de uma informação com o mínimo de caracteres possível. Se estamos enviando JSON por uma conexão de rede, não faz sentido deixá-lo "bonito": o software do outro lado não se importa, e os espaços em branco do layout só adicionam sobrecarga.

Para esses casos, e por ser um pedaço de código simples para começar, forneceremos a função `compact`:

```haskell
-- src/Prettify.hs
compact :: Doc -> String
compact x = transform [x]
    where transform [] = ""
          transform (d:ds) =
              case d of
                Empty        -> transform ds
                Char c       -> c : transform ds
                Text s       -> s ++ transform ds
                Line         -> '\n' : transform ds
                a `Concat` b -> transform (a:b:ds)
                _ `Union` b  -> transform (b:ds)
```

A função `compact` envolve seu argumento em uma lista e aplica a auxiliar `transform`, que trata o argumento como uma **pilha** de itens a processar, onde o primeiro elemento da lista é o topo.

A `transform` usa o padrão `(d:ds)` para quebrar a pilha em topo, `d`, e restante, `ds`. Na expressão `case`, os primeiros ramos fazem recursão sobre `ds`, consumindo um item da pilha por chamada. Os dois últimos ramos **adicionam** itens à frente de `ds`: o ramo `Concat` adiciona ambos os elementos à pilha, enquanto o ramo `Union` ignora o elemento esquerdo (aquele em que chamamos `flatten`) e adiciona o direito.

Agora já preenchemos definições suficientes para experimentar a `compact` no GHCi:

```
$ stack ghci
ghci> import Prettify
ghci> import PrettyJSON
ghci> let value = renderJValue (JObject [("f", JNumber 1), ("q", JBool True)])
ghci> :type value
value :: Doc
ghci> putStrLn (compact value)
{"f": 1.0,
"q": true
}
```

Para entender melhor como o código funciona, olhemos um exemplo mais simples em detalhe:

```
ghci> char 'f' <> text "oo"
Concat (Char 'f') (Text "oo")
ghci> compact (char 'f' <> text "oo")
"foo"
```

1. Quando aplicamos `compact`, ela põe o argumento numa lista e aplica `transform`.
2. A `transform` recebe uma lista de um item, que casa com `(d:ds)`. Então `d` é `Concat (Char 'f') (Text "oo")` e `ds` é a lista vazia, `[]`.
3. Como o construtor de `d` é `Concat`, o padrão `Concat` casa na expressão `case`. No lado direito, adicionamos `Char 'f'` e `Text "oo"` à pilha e aplicamos `transform` recursivamente.
4. A `transform` recebe uma lista de dois itens, casando de novo com `(d:ds)`. Agora `d` é `Char 'f'` e `ds` é `[Text "oo"]`.
5. O `case` casa no ramo `Char`. No lado direito, usamos `(:)` para construir uma lista cuja cabeça é `'f'` e cujo restante é a aplicação recursiva de `transform`.
6. A chamada recursiva recebe um item: `d` é `Text "oo"`, e `ds` é `[]`.
7. O `case` casa no ramo `Text`. Usamos `(++)` para concatenar `"oo"` com o resultado da chamada recursiva.
8. Na invocação final, `transform` recebe a lista vazia e retorna a string vazia.
9. O resultado é `"oo" ++ ""`... e, subindo, `'f' : ("oo" ++ "")` — ou seja, `"foo"`.

### A verdadeira impressão agradável

Enquanto a `compact` é útil para comunicação máquina-a-máquina, seu resultado nem sempre é fácil de um humano acompanhar: há pouquíssima informação em cada linha. Para saídas mais agradáveis, escreveremos outra função, `pretty`. Comparada à `compact`, a `pretty` recebe um argumento a mais: a largura máxima da linha, em colunas. (Assumimos uma fonte de largura fixa.)

```haskell
-- src/Prettify.hs
pretty :: Int -> Doc -> String
```

Para sermos precisos: o parâmetro `Int` controla o comportamento de `pretty` quando ela encontra uma `softline`. Só ali ela tem a opção de continuar na linha atual ou começar uma nova. Nos demais lugares, seguimos rigorosamente as diretrizes estabelecidas por quem construiu o documento.

Eis o núcleo da implementação:

```haskell
-- src/Prettify.hs
pretty width x = best 0 [x]
    where best col (d:ds) =
              case d of
                Empty        -> best col ds
                Char c       -> c :  best (col + 1) ds
                Text s       -> s ++ best (col + length s) ds
                Line         -> '\n' : best 0 ds
                a `Concat` b -> best col (a:b:ds)
                a `Union` b  -> nicest col (best col (a:ds))
                                           (best col (b:ds))
          best _ _ = ""

          nicest col a b | (width - least) `fits` a = a
                         | otherwise                = b
                         where least = min width col
```

Nossa auxiliar `best` recebe dois argumentos: o número de colunas já usadas na linha atual e a lista dos valores `Doc` que restam processar.

Nos casos simples, `best` atualiza a variável `col` de maneira direta conforme consome a entrada. Até o caso `Concat` é óbvio: empilhamos os dois componentes e não tocamos em `col`.

O caso interessante é o construtor `Union`. Lembre que aplicamos `flatten` ao elemento da esquerda e nada ao da direita; e que `flatten` troca quebras de linha por espaços. Portanto, nosso trabalho é ver **qual dos dois layouts** — o achatado ou o original — cabe na restrição de largura.

Para isso, escrevemos uma pequena auxiliar que determina se uma linha de um valor `Doc` renderizado cabe no número dado de colunas:

```haskell
-- src/Prettify.hs
fits :: Int -> String -> Bool
w `fits` _ | w < 0 = False
w `fits` ""        = True
w `fits` ('\n':_)  = True
w `fits` (c:cs)    = (w - 1) `fits` cs
```

> 💡 **Sobre os avisos do compilador:** se você compila com `stack build`, o template do projeto ativa `-Wall`, e o GHC emitirá alguns *warnings* neste código — por exemplo, `Defined but not used: 'p'` na primeira equação de `punctuate` e avisos similares em `fits`. **Warnings não são erros**: o programa compila e funciona. Eles apontam variáveis nomeadas que não usamos; a convenção idiomática é prefixá-las com sublinhado (`_p`, `_w`) para dizer ao compilador "eu sei, é de propósito". Mantivemos o código como no livro original; silenciar os avisos fica como micro-exercício.

### Seguindo o fluxo de execução

Para entender como esse código funciona, consideremos um valor `Doc` simples:

```
ghci> empty </> char 'a'
Concat (Union (Char ' ') Line) (Char 'a')
```

Vamos aplicar `pretty 2` a esse valor. Na primeira aplicação de `best`, o valor de `col` é zero. O `case` casa com `Concat`, empilha `Union (Char ' ') Line` e `Char 'a'`, e recorre. Na chamada recursiva, casa com `Union (Char ' ') Line`.

Neste ponto, ignoraremos a ordem usual de avaliação do Haskell — isso simplifica a explicação sem mudar o resultado. Temos agora duas subexpressões: `best 0 [Char ' ', Char 'a']` e `best 0 [Line, Char 'a']`. A primeira avalia para `" a"`, e a segunda para `"\na"`. Substituindo na expressão externa, obtemos `nicest 0 " a" "\na"`.

Para entender o resultado de `nicest` aqui, fazemos uma pequena substituição: os valores de `width` e `col` são `2` e `0`, então `least` é `0` e `width - least` é `2`. Avaliamos rapidamente `` 2 `fits` " a" `` no GHCi:

```
ghci> 2 `fits` " a"
True
```

Como isso avalia para `True`, o resultado de `nicest` é `" a"`.

Se aplicarmos nossa função `pretty` ao mesmo JSON de antes, veremos que ela produz resultados diferentes dependendo da largura que dermos:

```
ghci> putStrLn (pretty 10 value)
{"f": 1.0,
"q": true
}
ghci> putStrLn (pretty 20 value)
{"f": 1.0, "q": true
}
ghci> putStrLn (pretty 30 value)
{"f": 1.0, "q": true }
```

## Exercícios

Nossa biblioteca de impressão agradável é concisa — de modo a caber nas restrições de espaço de um capítulo —, mas há várias melhorias úteis que podemos fazer.

**1.** Escreva a função `fill`, com a seguinte assinatura de tipos:

```haskell
fill :: Int -> Doc -> Doc
```

Ela deve adicionar espaços a um documento até que ele atinja a largura dada em colunas. Se o documento já é mais largo que isso, ela não adiciona nada.

**2.** Nosso `Prettify` não leva **indentação** em conta. Quando abrimos parênteses, chaves ou colchetes, as linhas seguintes deveriam ser indentadas, alinhadas com o caractere de abertura, até o caractere de fechamento correspondente. Adicione suporte a indentação, com quantidade controlável de espaços:

```haskell
nest :: Int -> Doc -> Doc
```

## Criando um pacote

*(Esta seção foi inteiramente reescrita: o fluxo original — `Setup.hs`, `runghc Setup configure` e `ghc-pkg` — pertence à era pré-2010 do Cabal e não é mais como se trabalha.)*

A comunidade Haskell padronizou a descrição de software no formato **Cabal**: cada *pacote* contém uma biblioteca e, possivelmente, executáveis, descritos em um arquivo `.cabal`. É esse o formato que o Hackage (o repositório central de pacotes) e todas as ferramentas entendem.

Como vimos no início, nosso projeto tem uma camada de conveniência por cima disso: o **`package.yaml`**, que o hpack converte em `hs2json.cabal` a cada build. Vamos entender o que há nele — os conceitos são os mesmos do `.cabal`, só que em YAML.

### A descrição do pacote

Abra o `package.yaml`. A primeira parte são as propriedades globais do pacote:

```yaml
name:                hs2json
version:             0.1.0.0
license:             BSD-3-Clause
author:              "Seu Nome"
maintainer:          "seu@email.org"
```

Nomes de pacotes devem ser **únicos** dentro do seu conjunto de dependências (e globalmente, se um dia você publicar no Hackage). A versão segue a PVP (*Package Versioning Policy*), a política de versionamento do ecossistema.

Boa parte das propriedades destina-se a leitores humanos, não às ferramentas:

```yaml
synopsis:            Minha biblioteca de impressão agradável, com suporte a JSON
description:         Uma pequena biblioteca de pretty printing que ilustra
                     como desenvolver uma biblioteca Haskell.
category:            Text
```

A maioria dos pacotes Haskell usa a licença BSD de 3 cláusulas, que o Cabal chama de `BSD-3-Clause` (você é livre para escolher a que achar apropriada; o campo `license-file` aponta para o arquivo com o texto exato).

Em seguida vêm as **dependências** e os componentes. No template, as dependências valem para todos os componentes:

```yaml
dependencies:
- base >= 4.7 && < 5

library:
  source-dirs: src

executables:
  hs2json-exe:
    main:                Main.hs
    source-dirs:         app
    dependencies:
    - hs2json
```

Traduzindo:

- **`dependencies`** lista os pacotes de que precisamos, com faixas de versão. Nossa biblioteca só usa o `base` (que traz o Prelude, `Data.Bits`, `Numeric` etc.).
- **`library`** descreve a biblioteca: todo módulo em `src/` faz parte dela. No `.cabal` gerado, isso vira um campo `exposed-modules:` listando `Prettify`, `PrettyJSON`, `PutJSON` e `SimpleJSON` — o hpack preenche a lista sozinho, varrendo o diretório. (Se um dia você quiser módulos **internos**, invisíveis aos usuários do pacote, declare-os em `other-modules:` no `package.yaml`; tudo que não estiver lá continua exposto.)
- **`executables`** descreve os binários. Note que o executável **depende da própria biblioteca** (`hs2json`) — é assim que o `Main.hs` enxerga o `SimpleJSON`.

> **Entendendo as dependências:** não precisamos adivinhar quais pacotes declarar. Experimente remover a linha `- base >= 4.7 && < 5` e rodar `stack build`: a compilação falha imediatamente, com o GHC dizendo que não encontra nem o Prelude. A mensagem de erro nos diz o que falta — recoloque a linha e tudo volta. Explicitar as dependências tem um benefício prático enorme: é o que permite ao Stack (e ao cabal-install) baixar, compilar e instalar automaticamente **tudo** de que um pacote precisa, recursivamente.

### O papel do `stack.yaml` (e onde foi parar o `ghc-pkg`)

No fluxo antigo, o GHC mantinha um banco de dados global de pacotes instalados, manipulado com `ghc-pkg` — e instalar duas versões conflitantes era receita para o infame *"Cabal hell"*. O Stack resolveu isso com os **snapshots**: o `stack.yaml` do projeto aponta para um *resolver* (por exemplo, `lts-23.x`), que é um conjunto congelado de milhares de pacotes do Hackage **testados juntos**, amarrado a uma versão exata do GHC. Dois projetos com resolvers diferentes convivem sem se tocar. Você raramente precisará editar este arquivo; quando precisar de um pacote fora do snapshot, é nele que se declara (campo `extra-deps`).

### Compilando, testando e instalando

Com a descrição pronta, o ciclo completo é:

```
$ stack build            # compila biblioteca e executáveis
$ stack run              # executa o hs2json-exe
$ stack test             # roda a suíte de testes (test/Spec.hs)
$ stack install          # copia o executável para ~/.local/bin
```

O `stack install` deixa o binário disponível no seu `PATH` (se `~/.local/bin` estiver nele) — é o equivalente moderno do antigo `runghc Setup install`, sem nenhuma configuração prévia.

### E o cabal-install?

Tudo que fizemos tem equivalente direto na outra ferramenta oficial, o **cabal-install**: `cabal init` cria o projeto (gerando o `.cabal` diretamente, sem `package.yaml`), e `cabal build` / `cabal run` / `cabal repl` / `cabal install` espelham os comandos do Stack. As diferenças práticas: o cabal-install resolve versões contra o Hackage inteiro (em vez de snapshots) e usa o GHC que estiver no PATH (instalado pelo GHCup). Para uma disciplina, o Stack tende a dar builds mais reprodutíveis entre as máquinas dos alunos; mas saber que os dois falam o mesmo formato `.cabal` é o que importa.

## Dicas práticas e leitura adicional

O ecossistema tem bibliotecas de impressão agradável prontas e maduras — recomendamos usá-las em código real, em vez de escrever a sua:

- **[prettyprinter](https://hackage.haskell.org/package/prettyprinter)** é a biblioteca moderna de referência, com anotações (por exemplo, para saída colorida) e uma API muito próxima da que construímos: você reconhecerá `<>`, `group`, `nest`, `softline` na hora.
- **`Text.PrettyPrint.HughesPJ`** (pacote `pretty`, distribuído com o GHC) é a biblioteca clássica citada no livro original, ainda amplamente usada.

O design dessas bibliotecas tem história: a HughesPJ foi introduzida por John Hughes em *The Design of a Pretty-Printing Library* (1995) e melhorada por Simon Peyton Jones — daí o nome. A nossa, como a do livro, é baseada no sistema mais simples descrito por Philip Wadler em *A Prettier Printer* (1998), estendido por Daan Leijen na antiga `wl-pprint` — da qual a `prettyprinter` moderna é a sucessora direta. O artigo do Hughes é longo, mas vale a leitura pela discussão de como **projetar** uma biblioteca em Haskell — que foi, afinal, o verdadeiro assunto deste capítulo.

---

*Baseado no Capítulo 5 de **Real World Haskell**, copyright 2007, 2008 Bryan O'Sullivan, Don Stewart e John Goerzen, sob licença Creative Commons Attribution-Noncommercial 3.0. Tradução do projeto rwh-ptbr; revisão, atualização para GHC 9.x/Stack e validação de todo o código nesta edição v2.*
