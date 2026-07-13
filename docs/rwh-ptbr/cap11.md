# Capítulo 11. Testes e garantia de qualidade (v2 — Revisado e Validado)

> **Nota desta edição revisada.** Este capítulo é uma adaptação para o português do Capítulo 11 de *Real World Haskell* (Bryan O'Sullivan, Don Stewart e John Goerzen, 2008). Nesta revisão: (1) todo o código e todas as saídas foram **executados e conferidos** com GHC 9.4 e **QuickCheck 2.14.3** — as mensagens do QuickCheck mudaram de formato desde o livro original, e o texto mostra as atuais; (2) o QuickCheck moderno já traz instâncias que antes precisávamos escrever à mão (como a de `Char`); (3) a seção sobre `quickCheckAll` foi reescrita, incluindo uma correção importante no código de saída da suíte de testes; (4) a seção sobre **HPC** foi inteiramente reescrita para as ferramentas atuais, com um relatório real gerado sobre a nossa biblioteca — e a discussão do que ele revela; e (5) o capítulo pressupõe a biblioteca `hs2json` na forma do **Capítulo 5 revisado** (Stack + `package.yaml`).

Construir sistemas reais significa ter cuidado com controle de qualidade, robustez e corretude. Com os mecanismos certos de garantia de qualidade, código bem escrito pode parecer uma máquina precisa, com todas as funções executando suas tarefas de acordo com as especificações. Não há desleixo nas situações críticas, e o resultado é código autoexplicativo — e obviamente correto — do tipo que inspira confiança.

Em Haskell, existem diversas ferramentas à disposição para construir sistemas assim. A mais óbvia, embutida na própria linguagem, é o sistema de tipos expressivo, que permite impor restrições verificadas estaticamente — tornando impossível escrever código que as viole. Adicionalmente, pureza e polimorfismo promovem um estilo de código modular, refatorável e testável.

Os testes têm papel central em manter o código no caminho certo. Os principais mecanismos de teste em Haskell são o tradicional teste de unidade (por meio da biblioteca HUnit) e seu descendente mais poderoso: o **teste baseado em propriedades**, através do **QuickCheck**, um framework de testes de código aberto. Testes baseados em propriedades promovem uma abordagem de alto nível, na forma de **invariantes** que as funções devem satisfazer universalmente, com os dados de teste **gerados pela biblioteca** para o programador. Assim, o código pode ser martelado com milhares de testes que seriam inviáveis de escrever à mão, cobrindo casos-limite que dificilmente encontraríamos de outra forma.

Neste capítulo, veremos como usar o QuickCheck para estabelecer invariantes no código e então reexaminaremos o *pretty printer* desenvolvido no Capítulo 5, testando-o com o framework. Também veremos como acompanhar o processo com a ferramenta de cobertura de testes do GHC: o HPC.

## Preparando o projeto

Caso não tenha desenvolvido a biblioteca do Capítulo 5, clone-a:

```bash
git clone https://github.com/profsergiocosta/hs2json.git
cd hs2json
```

Após entrar na pasta, execute a suíte de testes:

```
$ stack test
```

Após a compilação, aparecerá a informação de que ainda não existem testes implementados:

```
hs2json> test (suite: hs2json-test)

Test suite not yet implemented

hs2json> Test suite hs2json-test passed
```

Podemos confirmar no código-fonte que nenhum teste foi implementado — este é o `test/Spec.hs` que o template do Stack gerou:

```haskell
-- test/Spec.hs
main :: IO ()
main = putStrLn "Test suite not yet implemented"
```

O objetivo deste capítulo é implementar esses testes.

> 💡 **Nota do professor:** a implementação final deste capítulo fica guardada em um repositório separado (`hs2json-test`), para que vocês possam usá-lo como referência se algo der errado. Porém, é importante que **executem os passos a seguir** a partir do repositório *sem* os testes — o aprendizado está no caminho, não no destino.

### Adicionando o QuickCheck às dependências

O QuickCheck não faz parte do `base`, então precisamos declará-lo no `package.yaml`:

```yaml
# package.yaml
dependencies:
- base >= 4.7 && < 5
- QuickCheck
```

No próximo `stack build` (ou `stack test`, ou `stack ghci`), o Stack baixa e compila o QuickCheck automaticamente — é a mágica das dependências explícitas que discutimos no Capítulo 5.

> 💡 Colocado nessa posição, o QuickCheck fica disponível para **todos** os componentes (biblioteca, executável e testes) — é o que queremos aqui, pois escreveremos propriedades também em `src/`. Em projetos reais, dependências usadas *só* nos testes costumam ser declaradas apenas no componente de testes (dentro de `tests:` no `package.yaml`), para não "vazar" para quem usa a biblioteca.

## QuickCheck: teste baseado em propriedades

Para ter uma ideia de como funcionam os testes baseados em propriedades, começaremos com um cenário simples: você escreveu uma função de ordenação e quer testar seu comportamento. Crie um novo módulo, `src/QuickTestes.hs`, já com as importações que usaremos ao longo da seção:

```haskell
-- src/QuickTestes.hs
module QuickTestes where

import Data.List (sort, (\\))
import Test.QuickCheck
```

E a função que queremos testar — uma rotina personalizada de ordenação:

```haskell
-- src/QuickTestes.hs
qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (x:xs) = qsort lhs ++ [x] ++ qsort rhs
    where lhs = filter  (< x) xs
          rhs = filter (>= x) xs
```

Esta é a clássica implementação de ordenação em Haskell: um estudo sobre elegância em programação funcional, não sobre eficiência (não é um algoritmo *in-place*). Queremos checar se essa função obedece às regras básicas que uma boa ordenação deve seguir.

Uma invariante útil para começar — e que aparece com frequência em código puramente funcional — é a **idempotência**: aplicar a função duas vezes deve dar o mesmo resultado que aplicá-la uma vez. Para uma rotina de ordenação, isso deve valer sempre, ou a situação vai ficar feia. A invariante pode ser codificada como uma simples propriedade:

```haskell
-- src/QuickTestes.hs
prop_idempotent xs = qsort (qsort xs) == qsort xs
```

Usaremos a convenção do QuickCheck de prefixar as propriedades com `prop_`, para diferenciá-las do código normal. A propriedade de idempotência é só uma função Haskell declarando uma igualdade que deve valer para qualquer entrada. Podemos checar manualmente que ela faz sentido para alguns casos:

```
$ stack ghci
ghci> prop_idempotent []
True
ghci> prop_idempotent [1,1,1,1]
True
ghci> prop_idempotent [1..100]
True
ghci> prop_idempotent [1,5,2,1,2,0,9]
True
```

Parece certo. Entretanto, escrever entradas à mão é tedioso e viola o código moral do programador funcional eficiente: **deixe a máquina fazer o trabalho!** Para automatizar isso, o QuickCheck traz geradores de dados para todos os tipos básicos do Haskell, usando a *typeclass* `Arbitrary` como interface uniforme para a geração pseudoaleatória — e o sistema de tipos para decidir qual gerador usar. O QuickCheck normalmente esconde a geração de dados, mas podemos executar os geradores à mão para espiar o que ele produz. Por exemplo, gerando uma lista aleatória de booleanos:

```
ghci> import Test.QuickCheck
ghci> generate arbitrary :: IO [Bool]
[True,True,True,True,False,True,False,True,False,False,True,True]
```

*(A saída varia a cada execução, claro — os dados são aleatórios.)*

O QuickCheck gera dados assim e os passa à propriedade da nossa escolha, por meio da função `quickCheck`. O tipo da propriedade determina qual gerador é usado; o `quickCheck` então verifica que a propriedade vale para todos os dados produzidos. Como nossa propriedade é **polimórfica** na lista, precisamos escolher um tipo concreto para o qual gerar os dados, o que escrevemos como uma restrição de tipo (caso contrário, o GHCi escolheria o desinteressante tipo `()` para os elementos):

```
ghci> quickCheck (prop_idempotent :: [Integer] -> Bool)
+++ OK, passed 100 tests.
```

Para 100 listas diferentes geradas, a propriedade foi satisfeita. Ao escrever testes, costuma ser útil ver os dados gerados em cada caso. Para isso, trocamos `quickCheck` pelo seu irmão verboso, `verboseCheck`. Mostrando só o começo da saída:

```
ghci> verboseCheck (prop_idempotent :: [Integer] -> Bool)
Passed:
[]

Passed:
[1]

Passed:
[-2,-2,3]

Passed:
[-2,0,2]

...
+++ OK, passed 100 tests.
```

Observe que os testes são aplicados a listas de tamanhos variados (o QuickCheck começa com entradas pequenas e vai crescendo). Agora, vamos a propriedades mais sofisticadas.

### Testes de propriedade

Boas bibliotecas consistem em um conjunto de primitivas ortogonais com relações sensatas entre si. Podemos usar o QuickCheck para **especificar essas relações**, o que nos ajuda inclusive a desenhar uma boa interface: o QuickCheck age como uma ferramenta de "lint" da consistência da biblioteca.

Nossa função de ordenação certamente se relaciona com outras operações de lista. Por exemplo: o primeiro elemento de uma lista ordenada deve ser o **menor** elemento da entrada. Ficamos tentados a expressar essa intuição usando a função `minimum`:

```haskell
-- src/QuickTestes.hs
prop_minimum xs = head (qsort xs) == minimum xs
```

Ao recarregar o módulo (`:r`) e testar a nova propriedade, encontraremos um erro:

```
ghci> :r
ghci> quickCheck (prop_minimum :: [Integer] -> Bool)
*** Failed! (after 1 test):
Exception:
  Prelude.head: empty list
  ...
  head, called at src/QuickTestes.hs:15:19 in main:QuickTestes
[]
```

*(No livro original a mensagem era uma linha só; o QuickCheck moderno mostra a exceção com o *call stack*, apontando a linha exata do `head` culpado — bem mais útil. A última linha, `[]`, é o **contraexemplo**: a entrada que quebrou a propriedade.)*

A propriedade falhou ao ordenar a lista **vazia** — para a qual `head` e `minimum` não estão definidas, como vemos nas suas definições:

```haskell
-- definidas no Prelude
head :: [a] -> a
head (x:_) = x
head []    = error "Prelude.head: empty list"

minimum :: (Ord a) => [a] -> a
minimum [] = error "Prelude.minimum: empty list"
minimum xs = foldl1 min xs
```

Portanto, a propriedade só faz sentido para listas não vazias. Felizmente, o QuickCheck vem com uma pequena linguagem de propriedades que nos permite ser mais precisos sobre as invariantes, descartando entradas que não queremos considerar. Para o caso da lista vazia, o que queremos dizer é: **se** a lista não é vazia, **então** o primeiro elemento da ordenação é o mínimo. A função de implicação `(==>)` descarta os dados inválidos antes de testar:

```haskell
-- src/QuickTestes.hs
prop_minimum' xs = not (null xs) ==> head (qsort xs) == minimum xs
```

Removido o caso da lista vazia, confirmamos que a propriedade de fato vale:

```
ghci> quickCheck (prop_minimum' :: [Integer] -> Property)
+++ OK, passed 100 tests; 14 discarded.
```

*(O número de descartados — as listas vazias geradas e ignoradas — varia a cada execução.)*

Note que tivemos que mudar o **tipo** da propriedade: de um simples `Bool` para o tipo mais geral `Property` (a propriedade agora é um valor que filtra as entradas antes de testar, e não uma constante booleana).

Podemos completar o conjunto básico com outras invariantes que a ordenação deve satisfazer: a saída deve estar **ordenada** (cada elemento menor ou igual ao sucessor); a saída deve ser uma **permutação** da entrada (via a diferença de listas, `(\\)`); o último elemento deve ser o **máximo**; e o mínimo de duas listas concatenadas e ordenadas deve ser o menor dos mínimos delas:

```haskell
-- src/QuickTestes.hs
prop_ordered xs = ordered (qsort xs)
    where ordered []       = True
          ordered [x]      = True
          ordered (x:y:ys) = x <= y && ordered (y:ys)

prop_permutation xs = permutation xs (qsort xs)
    where permutation as bs = null (as \\ bs) && null (bs \\ as)

prop_maximum xs =
    not (null xs) ==>
        last (qsort xs) == maximum xs

prop_append xs ys =
    not (null xs) ==>
    not (null ys) ==>
        head (qsort (xs ++ ys)) == min (minimum xs) (minimum ys)
```

### Testando sobre um modelo

Outra técnica para ganhar confiança no código é testar contra uma **implementação-modelo**. Podemos relacionar a nossa ordenação com a função `sort` da biblioteca padrão: se elas se comportam igual, ganhamos confiança de que a nossa faz a coisa certa.

```haskell
-- src/QuickTestes.hs
prop_sort_model xs = sort xs == qsort xs
```

```
ghci> quickCheck (prop_sort_model :: [Integer] -> Bool)
+++ OK, passed 100 tests.
```

Esse tipo de teste baseado em modelo é extremamente poderoso. Frequentemente, desenvolvedores têm uma implementação de referência ou protótipo que, embora ineficiente, é correta. Ela pode ser mantida por perto para assegurar que o código de produção otimizado continua de acordo com a referência. Construindo uma grande suíte desses testes e executando-a regularmente (a cada commit, por exemplo), garantimos baratíssimo a precisão do código. Grandes projetos Haskell costumam ter suítes de propriedades de tamanho comparável ao do próprio projeto, com milhares de invariantes testadas a cada mudança.

## Estudo de caso: especificando um pretty printer

Testar propriedades naturais de funções individuais é uma das abordagens mais básicas que guiam o desenvolvimento de grandes sistemas em Haskell. Veremos agora um cenário mais complicado: construir uma suíte de testes para a biblioteca de *pretty printing*\* do Capítulo 5.

\**N. do T.: pretty printing é o nome que se dá à apresentação de um conteúdo de maneira que a estrutura da apresentação reforce o sentido do próprio conteúdo.*

### Gerando dados de teste

Lembre-se de que o pretty printer é construído em torno do `Doc`, um tipo de dados algébrico que representa documentos bem estruturados:

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

A biblioteca em si é implementada como um conjunto de funções que criam e transformam valores desse tipo, antes de finalmente produzir sua representação como string.

O QuickCheck encoraja uma abordagem em que o desenvolvedor especifica invariantes que devem valer para **quaisquer** dados consumidos pelo código. Para testar a biblioteca, então, precisamos de uma fonte de valores `Doc` aleatórios. Para isso, usamos a pequena suíte de combinadores que o QuickCheck fornece via a classe `Arbitrary`:

```haskell
-- definida em Test.QuickCheck
class Arbitrary a where
  arbitrary :: Gen a
```

Note que os geradores executam em um ambiente `Gen`, indicado pelo tipo. Trata-se de um *monad* simples de passagem de estado, usado para esconder o estado do gerador de números aleatórios que fica espalhado pelo código. Examinaremos monads minuciosamente nos próximos capítulos; por ora, basta saber que, como `Gen` é um monad, podemos usar a sintaxe `do` para escrever geradores que acessam implicitamente os números aleatórios. Para escrever geradores dos nossos próprios tipos, combinamos as funções que a biblioteca oferece — as principais são:

```haskell
-- definidas em Test.QuickCheck.Gen
elements :: [a] -> Gen a
choose   :: Random a => (a, a) -> Gen a
oneof    :: [Gen a] -> Gen a
```

A função `elements` recebe uma lista de valores e retorna um gerador que escolhe aleatoriamente um deles. Usaremos `choose` e `oneof` em seguida. Com isso, podemos escrever geradores para tipos simples. Para praticar, adicionaremos ao módulo `QuickTestes` um tipo novo, para lógica ternária:

```haskell
-- src/QuickTestes.hs
data Ternary
    = Yes
    | No
    | Unknown
    deriving (Eq, Show)
```

Escrevemos uma instância de `Arbitrary` para `Ternary` escolhendo um elemento da lista dos valores possíveis:

```haskell
-- src/QuickTestes.hs
instance Arbitrary Ternary where
    arbitrary = elements [Yes, No, Unknown]
```

Com isso, já é possível gerar dados aleatórios para o tipo:

```
ghci> :r
ghci> generate arbitrary :: IO [Ternary]
[Unknown,Unknown,No,Yes,Yes,No,Yes,No,Unknown,No,No,Unknown,Yes]
```

Outra abordagem é gerar valores de um tipo básico e **traduzi-los** para o tipo que nos interessa. Poderíamos ter escrito a instância de `Ternary` gerando inteiros de 0 a 2 com `choose` e mapeando-os para os construtores:

```haskell
instance Arbitrary Ternary where
    arbitrary = do
        n <- choose (0, 2) :: Gen Int
        return $ case n of
                      0 -> Yes
                      1 -> No
                      _ -> Unknown
```

Para tipos enumerados, as duas abordagens funcionam bem. Para tipos-produto (como registros e tuplas), geramos cada componente separadamente (e recursivamente, se aninhados) e depois os combinamos. É assim que a própria biblioteca define o gerador de pares:

```haskell
-- definida em Test.QuickCheck.Arbitrary
instance (Arbitrary a, Arbitrary b) => Arbitrary (a, b) where
  arbitrary = do
      x <- arbitrary
      y <- arbitrary
      return (x, y)
```

Por exemplo, gerando tuplas de inteiros:

```
ghci> generate arbitrary :: IO [(Int,Int)]
[(-1,18),(-25,7),(-24,-15),(20,-8),(20,3),(-29,-3),(-19,6),(-13,17)]
```

> 💡 **E os caracteres?** Quando o livro foi escrito, o QuickCheck **não tinha** uma instância padrão para `Char` — havia dúvidas sobre qual codificação usar —, e era preciso escrever uma à mão. Nas versões atuais essa instância **já existe** em `Test.QuickCheck`, e é bem mais rica que a gambiarra da época: ela gera todo o espectro Unicode, com viés para caracteres ASCII comuns e caracteres de controle (justamente os que costumam revelar bugs de escape — repare neles nas saídas a seguir). Ou seja: **não defina uma instância de `Char`**; apenas use `arbitrary`.

Vamos então ao gerador para todas as variantes do tipo `Doc`. Quebramos o problema: escolhemos aleatoriamente um construtor e, dependendo dele, geramos seus campos — recursivamente, nos casos de concatenação e união. Escreveremos o código diretamente no `test/Spec.hs`, com um `main` provisório que só imprime alguns documentos gerados:

```haskell
-- test/Spec.hs
import Test.QuickCheck
import Prettify

instance Arbitrary Doc where
    arbitrary = do
        n <- choose (1,6) :: Gen Int
        case n of
             1 -> return Empty

             2 -> do x <- arbitrary
                     return (Char x)

             3 -> do x <- arbitrary
                     return (Text x)

             4 -> return Line

             5 -> do x <- arbitrary
                     y <- arbitrary
                     return (Concat x y)

             6 -> do x <- arbitrary
                     y <- arbitrary
                     return (Union x y)

main :: IO ()
main = do
    docs <- generate arbitrary :: IO [Doc]
    print docs
```

> ⚠️ **Isso ainda não compila — e o erro é instrutivo.** No Capítulo 5, exportamos `Doc` como um tipo **abstrato** (`Doc`, sem os construtores) — exatamente para que ninguém de fora pudesse construir ou inspecionar documentos na mão. Mas é **isso** que o nosso gerador e as nossas propriedades precisam fazer! Há uma tensão real aqui entre encapsulamento e testabilidade. A solução mais simples, que adotaremos, é passar a exportar os construtores: no `src/Prettify.hs`, troque `Doc` por `Doc(..)` na lista de exportação. (Em bibliotecas de verdade, o padrão comum é um módulo `*.Internal` que exporta tudo — os testes importam o Internal, e os usuários, a fachada abstrata.)

Feito o ajuste, execute:

```
$ stack test
hs2json> test (suite: hs2json-test)

[Text "o\38884\DC3R\201400?\EOT#;;/\\Gk_y\1061091\178450\&7(4'\174004-A",Text "8\986417\&7",Concat Line (Union Empty (Char '4')),Char '\NUL',Text "\68902\ACKQTA\SOH^Q\200597h\SIh\36934"]
```

*(Saída ilustrativa, encurtada — a sua será diferente.)* Examinando-a, vemos uma boa mistura: casos básicos, textos cheios de caracteres Unicode e de controle, e documentos aninhados. A cada execução de teste, centenas desses serão gerados.

Essa abordagem foi bem direta, e podemos melhorá-la usando a função `oneof` (cujo tipo vimos acima) para escolher entre geradores de uma lista — e o combinador monádico `liftM` (do módulo `Control.Monad`) para evitar nomear os resultados intermediários:

```haskell
-- test/Spec.hs
instance Arbitrary Doc where
    arbitrary =
        oneof [ return Empty
              , liftM  Char   arbitrary
              , liftM  Text   arbitrary
              , return Line
              , liftM2 Concat arbitrary arbitrary
              , liftM2 Union  arbitrary arbitrary ]
```

Esta versão é mais concisa — apenas escolhe de uma lista de geradores —, mas ambas descrevem os mesmos dados.

### Testando a construção de documentos

Duas das funções básicas sobre documentos são o documento nulo, `empty`, e o operador de concatenação. Revendo suas definições:

```haskell
-- src/Prettify.hs
empty :: Doc
empty = Empty

(<>) :: Doc -> Doc -> Doc
Empty <> y = y
x <> Empty = x
x <> y = x `Concat` y
```

Juntas, elas devem satisfazer uma propriedade razoável: concatenar um documento com o vazio — de qualquer lado — deve deixá-lo inalterado. (É a propriedade de **identidade** que anunciamos no "momento matemático" do Capítulo 5.) Podemos afirmar a invariante assim:

```haskell
-- test/Spec.hs
prop_empty_id x =
    empty <> x == x
  &&
    x <> empty == x
```

E confirmar que ela vale, direto no GHCi (`stack ghci --test` carrega também o componente de testes):

```
ghci> quickCheck prop_empty_id
+++ OK, passed 100 tests.
```

*(Repare que aqui não precisamos de anotação de tipo: o `<>` do Prettify força `x :: Doc`, e a nossa instância `Arbitrary Doc` faz o resto.)*

### Executando tudo com o `stack test`: `quickCheckAll`

*(Esta seção foi reescrita nesta edição.)*

Rodar `quickCheck` propriedade por propriedade no GHCi é ótimo para explorar, mas queremos que o **`stack test`** execute todas de uma vez. O QuickCheck traz um utilitário para isso: `quickCheckAll`, que usa **Template Haskell** — o mecanismo de metaprogramação do GHC — para localizar, em tempo de compilação, todas as funções do módulo cujo nome começa com `prop_`, e gerar o código que as executa.

Três detalhes fazem tudo funcionar:

1. O pragma `{-# LANGUAGE TemplateHaskell #-}` no topo do arquivo, habilitando a extensão;
2. A linha `return []` antes da definição — um truque necessário para que o Template Haskell "enxergue" todas as definições que vieram acima dela no arquivo;
3. A invocação `$quickCheckAll` (o `$` executa a metafunção em tempo de compilação), que produz uma ação `IO Bool`: `True` se todas as propriedades passaram.

Há ainda um detalhe que o livro original deixou passar, e que vale corrigir: **o processo de testes precisa terminar com código de saída de erro quando algo falha**. É só o código de saída que o `stack test` (e qualquer ferramenta de integração contínua) olha — sem isso, a suíte imprime "falhou" mas o Stack alegremente reporta `Test suite passed`. Resolvemos com `exitFailure`, do módulo `System.Exit`.

O `test/Spec.hs` completo até aqui:

```haskell
-- test/Spec.hs
{-# LANGUAGE TemplateHaskell #-}

import Prelude hiding ((<>))

import Test.QuickCheck
import Data.List (intersperse)
import Control.Monad (liftM, liftM2)
import System.Exit (exitFailure)

import Prettify

instance Arbitrary Doc where
    arbitrary =
        oneof [ return Empty
              , liftM  Char   arbitrary
              , liftM  Text   arbitrary
              , return Line
              , liftM2 Concat arbitrary arbitrary
              , liftM2 Union  arbitrary arbitrary ]

prop_empty_id x =
    empty <> x == x
  &&
    x <> empty == x

return []
runTests = $quickCheckAll

main :: IO ()
main = do
    passed <- runTests
    if passed
        then putStrLn "Passou em todos os testes."
        else do putStrLn "Alguns testes falharam."
                exitFailure
```

*(Note o `import Prelude hiding ((<>))` — o mesmo ajuste dos módulos do Capítulo 5, pois usamos aqui o `<>` do Prettify, não o do Prelude.)*

Executando:

```
$ stack test
hs2json> test (suite: hs2json-test)

=== prop_empty_id from test/Spec.hs:22 ===
+++ OK, passed 100 tests.

Passou em todos os testes.

hs2json> Test suite hs2json-test passed
```

Outras funções da API são simples o suficiente para terem o comportamento **completamente** descrito por propriedades. Revendo suas definições no `Prettify`:

```haskell
-- src/Prettify.hs
char :: Char -> Doc
char c = Char c

text :: String -> Doc
text "" = Empty
text s  = Text s

double :: Double -> Doc
double d = text (show d)

line :: Doc
line = Line
```

Escrevemos, então, os testes correspondentes — assim, modificações futuras não quebrarão estas invariantes básicas sem que a suíte grite:

```haskell
-- test/Spec.hs
prop_char c   = char c   == Char c
prop_text s   = text s   == if null s then Empty else Text s
prop_line     = line     == Line
prop_double d = double d == text (show d)
```

Essas propriedades bastam para testar completamente a estrutura retornada pelos operadores básicos de documentos.

### Usando listas como modelos

Funções de alta ordem são a base de programas reutilizáveis, e nossa biblioteca não é exceção: um `fold` customizado é usado internamente para implementar tanto a concatenação quanto a intercalação de separadores:

```haskell
-- src/Prettify.hs
fold :: (Doc -> Doc -> Doc) -> [Doc] -> Doc
fold f = foldr f empty

hcat :: [Doc] -> Doc
hcat = fold (<>)
```

Podemos testar instâncias específicas do `fold` isoladamente. A concatenação horizontal, por exemplo, é fácil de especificar escrevendo uma implementação de referência sobre listas:

```haskell
-- test/Spec.hs
prop_hcat xs = hcat xs == glue xs
    where
        glue []     = empty
        glue (d:ds) = d <> glue ds
```

História parecida com `punctuate`, cuja inserção de pontuação parece se modelar com a intercalação de listas (`intersperse`, de `Data.List`, recebe um elemento e o intercala entre os elementos de uma lista):

```haskell
-- test/Spec.hs
prop_punctuate s xs = punctuate s xs == intersperse s xs
```

Embora pareça correta, a execução revela uma falha na nossa lógica:

```
$ stack test

=== prop_punctuate from test/Spec.hs:37 ===
*** Failed! Falsified (after 6 tests):
Char '}'
[Text "\DC3v\DEL~w",Concat Empty (Text "\199132\NAK")]

Alguns testes falharam.
```

*(O QuickCheck moderno diz `Falsified` onde o antigo dizia `Falsifiable`. As duas linhas após o cabeçalho são os argumentos do contraexemplo: o separador `s` e a lista `xs` — repare no `Empty` dentro de um `Concat`, a pista do problema. E, graças ao nosso `exitFailure`, desta vez o `stack test` termina, corretamente, reportando a falha da suíte.)*

A biblioteca **otimiza fora os documentos vazios redundantes** (lembre-se dos casos `Empty` do `<>`), algo que o modelo de lista não faz — então precisamos enriquecer o modelo para casar com a realidade. Primeiro intercalamos a pontuação e depois eliminamos os `Empty` espalhados, assim:

```haskell
-- test/Spec.hs
prop_punctuate' s xs = punctuate s xs == combine (intersperse s xs)
    where
        combine []           = []
        combine [x]          = [x]
        combine (x:Empty:ys) = x : combine ys
        combine (Empty:y:ys) = y : combine ys
        combine (x:y:ys)     = x `Concat` y : combine ys
```

Executando (e removendo a versão ingênua, `prop_punctuate`), confirmamos o resultado. É reconfortante que o framework localize falhas na lógica que expressamos — é exatamente para isso que ele existe:

```
$ stack test

=== prop_empty_id from test/Spec.hs:22 ===
+++ OK, passed 100 tests.

=== prop_char from test/Spec.hs:27 ===
+++ OK, passed 100 tests.

=== prop_text from test/Spec.hs:28 ===
+++ OK, passed 100 tests.

=== prop_line from test/Spec.hs:29 ===
+++ OK, passed 1 test.

=== prop_double from test/Spec.hs:30 ===
+++ OK, passed 100 tests.

=== prop_hcat from test/Spec.hs:32 ===
+++ OK, passed 100 tests.

=== prop_punctuate' from test/Spec.hs:37 ===
+++ OK, passed 100 tests.

Passou em todos os testes.

hs2json> Test suite hs2json-test passed
```

*(Curiosidade: `prop_line` não recebe argumentos, então não há o que gerar — o QuickCheck a trata como um teste único: `passed 1 test`.)*

> 💡 **Sobre o encolhimento (shrinking):** quando uma propriedade falha, o QuickCheck tenta **encolher** o contraexemplo — remover elementos, diminuir números — até achar o menor caso que ainda falha, o que facilita muito a depuração (você verá mensagens como `Failed! ... and 3 shrinks`). Isso funciona automaticamente para os tipos embutidos; para o nosso `Doc`, não definimos o método `shrink` da classe `Arbitrary`, então os contraexemplos vêm "crus". Implementá-lo (dica: `genericShrink`) fica como exercício.

## Medindo a cobertura de testes com HPC

*(Esta seção foi inteiramente reescrita para as ferramentas atuais, e o relatório abaixo foi gerado de verdade sobre a nossa biblioteca.)*

Nossa suíte passa em todos os testes. Mas... ela testa **o quê**, exatamente? Essa pergunta tem uma resposta objetiva.

O **HPC** (*Haskell Program Coverage*) é um recurso do GHC que instrumenta o código para observar quais partes dele foram **realmente executadas** durante uma execução do programa. No contexto de testes, isso nos permite ver com precisão quais funções, ramos e expressões foram avaliados pela suíte — e, mais importante, quais **não** foram. O resultado é um conhecimento exato do percentual de código coberto, e o HPC ainda gera páginas HTML com o código-fonte colorido, facilitando localizar os pontos fracos da suíte.

Com o Stack, obter os dados de cobertura é um parâmetro a mais:

```
$ stack test --coverage
```

A suíte executa normalmente (todas as propriedades passando, como antes) e, ao final, o Stack imprime o relatório e os caminhos dos arquivos HTML gerados:

```
Generating coverage report for hs2json's test-suite "hs2json-test"

 19% expressions used (30/154)
  0% boolean coverage (0/3)
       0% guards (0/3), 3 unevaluated
     100% 'if' conditions (0/0)
     100% qualifiers (0/0)
 23% alternatives used (8/34)
  0% local declarations used (0/4)
 45% top-level declarations used (10/22)

The coverage report for hs2json's test-suite "hs2json-test" is available at
.../.stack-work/install/.../hpc/hs2json/hs2json-test/hpc_index.html
```

*(Os números referem-se ao módulo `Prettify`; por padrão, o Stack reporta a cobertura do código do **pacote** exercido pelos testes. Abra o `hpc_index.html` indicado no navegador para a versão visual.)*

> 💡 **Sem o Stack:** o HPC é do próprio GHC, então o fluxo manual equivalente é compilar com o flag `-fhpc`, executar o programa (o que gera um arquivo `.tix` com as contagens) e então usar o utilitário `hpc`: `hpc report` para o resumo textual e `hpc markup` para as páginas HTML. O `stack test --coverage` faz exatamente isso por você.

### Lendo o relatório

Aprender a ler essas linhas é o que dá valor à ferramenta:

| Métrica | O que mede | Nosso resultado |
| --- | --- | --- |
| `expressions used` | Quantas expressões do código foram avaliadas ao menos uma vez. É a métrica mais fina. | **19%** (30 de 154) |
| `boolean coverage` / `guards` | Dos pontos de decisão booleanos (guardas, `if`), quantos foram avaliados — e para os dois lados. | **0%** (0 de 3) |
| `alternatives used` | Das alternativas de casamento de padrões (equações de função, ramos de `case`), quantas foram exercitadas. | **23%** (8 de 34) |
| `local declarations` | Definições em `where`/`let` executadas. | **0%** (0 de 4) |
| `top-level declarations` | Funções de topo do módulo executadas. | **45%** (10 de 22) |

À primeira vista, os números parecem contraditórios: como uma suíte que "passa em tudo" cobre só 19% das expressões? A resposta está na visão por declaração. Abrindo o `hpc_index_fun.html` (ou o fonte anotado `Prettify.hs.html`, onde o código nunca executado aparece **destacado em amarelo**), o padrão salta aos olhos — as funções jamais tocadas pela suíte são:

```
fsep, (</>), softline, group, flatten, fits, compact, pretty
```

Ou seja: testamos completamente a metade **de construção** da biblioteca (`empty`, `char`, `text`, `double`, `line`, `<>`, `hcat`, `fold`, `punctuate`), mas **zero** da metade de **renderização** — justamente as funções mais complexas, `compact` e `pretty`, com seus `where` internos (eis os `local declarations 0%`: `transform`, `best`, `nicest`...) e suas guardas (eis o `boolean coverage 0%`: as guardas de `fits` e `nicest`). A suíte verde estava nos contando só metade da história — e o HPC expôs isso em uma linha. *(Curiosidade: as 22 declarações de topo contadas incluem os métodos gerados pelo `deriving` — `show`, `showsPrec`... —, que o HPC também rastreia.)*

### Fechando o ciclo: da lacuna à propriedade

O relatório não é um fim; é o começo da próxima iteração. Vamos escrever uma propriedade que exercite a renderização — um teste baseado em modelo minúsculo para a `compact`: renderizar compactamente um documento de texto puro deve devolver a própria string:

```haskell
-- test/Spec.hs
prop_compact_text s = compact (text s) == s
```

Rodando de novo com cobertura:

```
$ stack test --coverage

=== prop_compact_text from test/Spec.hs:45 ===
+++ OK, passed 100 tests.

Passou em todos os testes.

 27% expressions used (42/154)
 ...
 35% alternatives used (12/34)
 25% local declarations used (1/4)
 50% top-level declarations used (11/22)
```

Uma propriedade de uma linha: expressões cobertas de 19% para **27%**, alternativas de 23% para **35%**, e a `transform` interna da `compact` saiu do zero. É esse o ritmo do desenvolvimento guiado por propriedades **e** cobertura: a suíte diz *"o que testei está correto"*; o HPC diz *"eis o que você ainda não testou"*; e cada lacuna vira a próxima invariante.

> ⚠️ Cobertura alta **não** prova corretude — mede apenas o que foi *executado*, não o que foi *verificado*. Uma propriedade frouxa pode executar tudo e não conferir nada. Use os dois sinais juntos: propriedades fortes para a corretude, cobertura para achar os pontos cegos.

## Exercícios

**1.** Escreva propriedades para a metade ainda descoberta da biblioteca e acompanhe a cobertura subindo. Sugestões, em dificuldade crescente:

- `pretty` de um documento sem `softline` não depende da largura: `pretty w (text s)` deve ser igual a `s` para qualquer `w`;
- toda linha de `pretty w d` "cabe" — relacione com a intuição da função `fits` (cuidado: quando um pedaço **não cabe** de jeito nenhum, a linha pode estourar `w`; a propriedade precisa levar isso em conta);
- um teste baseado em modelo relacionando `compact` e `pretty`: os dois devem produzir o **mesmo texto**, a menos de espaços em branco e quebras de linha (comece definindo essa noção de equivalência!).

**2.** Implemente o método `shrink` na instância `Arbitrary Doc` (investigue `genericShrink`, que exige `deriving (Generic)` no tipo) e provoque uma falha de propósito para ver o QuickCheck reduzir o contraexemplo ao mínimo.

**3.** Nosso gerador de `Doc` escolhe entre os seis construtores com igual probabilidade, e os casos recursivos podem, ocasionalmente, gerar árvores enormes. Investigue as funções `sized` e `frequency` do QuickCheck e reescreva o gerador limitando a profundidade da árvore pelo "tamanho" do teste.

---

*Baseado no Capítulo 11 de **Real World Haskell**, copyright 2007, 2008 Bryan O'Sullivan, Don Stewart e John Goerzen, sob licença Creative Commons Attribution-Noncommercial 3.0. Tradução do projeto rwh-ptbr; revisão, atualização para GHC 9.x/QuickCheck 2.14/Stack e validação de todo o código nesta edição v2.*
