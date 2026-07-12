# Testes e Garantia de Qualidade com QuickCheck

Neste capítulo, aprenderemos como realizar **Garantia de Qualidade (QA)** e testes automatizados em Haskell usando a metodologia de **Testes Baseados em Propriedades (Property-Based Testing)**, adaptando os conceitos originais do clássico *Real World Haskell* (Capítulo 11) para o ambiente de testes de um projeto **Stack** moderno com a biblioteca **QuickCheck**.

---

## 🧪 Por que Testar Propriedades?

Os testes unitários tradicionais baseiam-se em fornecer entradas específicas e checar se o resultado bate com a saída esperada (ex: `soma 2 3 == 5`). Embora úteis, eles exigem que o desenvolvedor pense manualmente em todos os casos especiais (como listas vazias, números negativos, limites de tipos).

Os **Testes Baseados em Propriedades** invertem essa lógica:
1. Em vez de testar casos individuais, definimos **propriedades universais** (invariantes) que nosso código deve obedecer para *qualquer* entrada.
2. A biblioteca **QuickCheck** gera automaticamente centenas ou milhares de dados de entrada aleatórios e testa essas invariantes.
3. Se ela encontrar alguma entrada que falha, ela realiza o processo de **encolhimento (shrinking)** para encontrar o menor caso de teste possível que reproduz o erro.

---

## 1. Configurando o QuickCheck no Projeto Stack

Para utilizar o QuickCheck em nosso projeto modernizado `hs2json`, editamos o arquivo `package.yaml` para adicionar o pacote `QuickCheck` como dependência na seção de testes (`tests`):

```yaml
tests:
  hs2json-test:
    main:                Spec.hs
    source-dirs:         test
    dependencies:
      - hs2json
      - QuickCheck
```

Sempre que rodarmos `stack test`, o Stack compilará e executará os testes definidos nessa suíte.

---

## 2. Escrevendo Invariantes Básicas

Vamos implementar e testar um algoritmo clássico de ordenação (*quicksort*) e definir suas propriedades.

Crie o arquivo `test/Spec.hs` com o código:

```haskell
module Main where

import Test.QuickCheck
import Data.List (sort, (\\))

-- Algoritmo Quicksort didatico (nao in-place)
qsort :: Ord a => [a] -> [a]
qsort []     = []
qsort (x:xs) = qsort lhs ++ [x] ++ qsort rhs
  where lhs = filter (< x) xs
        rhs = filter (>= x) xs

-- Propriedade 1: Idempotência (ordenar duas vezes dá o mesmo resultado)
prop_idempotent :: [Int] -> Bool
prop_idempotent xs = qsort (qsort xs) == qsort xs

-- Propriedade 2: O menor elemento da entrada deve estar no início da saída
-- Usamos a implicação (==>) para ignorar listas vazias
prop_minimum :: [Int] -> Property
prop_minimum xs = not (null xs) ==> head (qsort xs) == minimum xs

-- Propriedade 3: A lista final deve estar de fato ordenada
prop_ordered :: [Int] -> Bool
prop_ordered xs = ordered (qsort xs)
  where ordered []       = True
        ordered [_]      = True
        ordered (x:y:ys) = x <= y && ordered (y:ys)

-- Propriedade 4: A saída deve ser uma permutação da entrada
prop_permutation :: [Int] -> Bool
prop_permutation xs = null (xs \\ qsort xs) && null (qsort xs \\ xs)

-- Propriedade 5: Modelo de Teste (deve ser idêntico à ordenação padrão do Haskell)
prop_sort_model :: [Int] -> Bool
prop_sort_model xs = qsort xs == sort xs

main :: IO ()
main = do
    putStrLn "Executando Testes de Propriedades com QuickCheck:"
    quickCheck prop_idempotent
    quickCheck prop_minimum
    quickCheck prop_ordered
    quickCheck prop_permutation
    quickCheck prop_sort_model
```

Para rodar os testes:

```bash
stack test
```

A saída mostrará o sucesso das propriedades:

```text
Executando Testes de Propriedades com QuickCheck:
+++ OK, passed 100 tests.
+++ OK, passed 100 tests (exposing 13% empty lists).
+++ OK, passed 100 tests.
+++ OK, passed 100 tests.
+++ OK, passed 100 tests.
```

---

## 3. Gerando Dados de Teste Customizados (`Arbitrary`)

Para testar estruturas de dados complexas criadas por nós (como o `JValue` da nossa biblioteca JSON), precisamos ensinar o QuickCheck a gerar instâncias aleatórias dessa estrutura. Fazemos isso implementando a classe de tipo **`Arbitrary`**.

Para evitar recursão infinita e estruturas gigantescas que consomem toda a memória, utilizamos o combinador `sized` do QuickCheck para controlar a profundidade do dado gerado de forma recursiva.

Crie um novo arquivo de teste chamado `test/JSONSpec.hs` e implemente a geração aleatória de JSON:

```haskell
{-# LANGUAGE OverloadedStrings #-}
module JSONSpec where

import Test.QuickCheck
import SimpleJSON

-- Geradores auxiliares para JValue
instance Arbitrary JValue where
  arbitrary = sized genJValue

genJValue :: Int -> Gen JValue
genJValue 0 = oneof
    [ JBool <$> arbitrary
    , return JNull
    , JNumber <$> arbitrary
    , JString <$> arbitrary
    ]
genJValue n = oneof
    [ JBool <$> arbitrary
    , return JNull
    , JNumber <$> arbitrary
    , JString <$> arbitrary
    -- Casos recursivos (reduzem a profundidade por 2)
    , JArray <$> resize (n `div` 2) (listOf (genJValue (n `div` 2)))
    , JObject <$> resize (n `div` 2) (listOf genPair)
    ]
  where
    genPair = do
      key <- arbitrary
      val <- genJValue (n `div` 2)
      return (key, val)

-- Propriedade Exemplo: Ler e depois extrair string
prop_jvalue_string :: String -> Bool
prop_jvalue_string s = getString (JString s) == Just s
```

O QuickCheck usará esses geradores para passar objetos JSON extremamente profundos e variados para as nossas funções, validando nossa biblioteca sob estresse!
