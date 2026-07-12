# Desenvolvendo uma Biblioteca JSON em Haskell

Neste capítulo, desenvolveremos uma biblioteca completa para manipulação e serialização de dados em formato **JSON (JavaScript Object Notation)**, adaptando os conceitos apresentados no clássico *Real World Haskell* (Capítulo 5) para a estrutura de um projeto moderno gerenciado pelo **Stack**.

---

## 🧭 O Ecossistema e Estrutura do Projeto

Para começar, criamos um projeto novo chamado `hs2json` usando o Stack:

```bash
stack new hs2json
cd hs2json
```

A estrutura de código em `src` conterá os seguintes arquivos:
1. `SimpleJSON.hs`: Define a representação abstrata de valores JSON e accessors básicos.
2. `Prettify.hs`: Uma biblioteca genérica de "pretty printing" baseada em um tipo abstrato `Doc`.
3. `PrettyJSON.hs`: O renderizador que pega nossa representação JSON `JValue` e converte em um `Doc` estruturado.

Vamos implementar esses arquivos passo a passo.

---

## 1. Representando Dados JSON em Haskell (`SimpleJSON.hs`)

Para trabalhar com JSON em Haskell, utilizamos um tipo de dado algébrico (ADT) para representar os tipos possíveis do JSON.

Crie o arquivo `src/SimpleJSON.hs` e adicione o código abaixo:

```haskell
module SimpleJSON
    ( JValue(..)
    , getString
    , getInt
    , getDouble
    , getBool
    , getObject
    , getArray
    , isNull
    ) where

data JValue = JString String
            | JNumber Double
            | JBool Bool
            | JNull
            | JObject [(String, JValue)]
            | JArray [JValue]
            deriving (Eq, Ord, Show)

getString :: JValue -> Maybe String
getString (JString s) = Just s
getString _           = Nothing

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

---

## 2. A Anatomia do Pretty Printer (`Prettify.hs`)

Um *pretty printer* é uma biblioteca que renderiza estruturas de dados de forma formatada e organizada. Para manter nossa biblioteca modular, separamos a geração do formato da impressão em si. Usamos o tipo abstrato `Doc` para isso.

Crie o arquivo `src/Prettify.hs` com o código:

```haskell
module Prettify
    ( Doc
    , empty
    , char
    , text
    , line
    , union
    , (<<>>)
    , concatDoc
    , hcat
    , fcat
    , render
    , string
    , double
    ) where

import Prelude hiding (empty)

data Doc = Empty
         | Char Char
         | Text String
         | Line
         | Concat Doc Doc
         | Union Doc Doc
         deriving (Show, Eq)

empty :: Doc
empty = Empty

char :: Char -> Doc
char c = Char c

text :: String -> Doc
text "" = Empty
text s  = Text s

line :: Doc
line = Line

-- Concatena dois documentos
(<<>>) :: Doc -> Doc -> Doc
Empty <<>> y = y
x <<>> Empty = x
x <<>> y     = Concat x y

concatDoc :: [Doc] -> Doc
concatDoc = foldr (<<>>) empty

hcat :: [Doc] -> Doc
hcat = concatDoc

-- Representa alternativas de quebra de linha
union :: Doc -> Doc -> Doc
union = Union

fcat :: [Doc] -> Doc
fcat = foldr (\x y -> x <<>> union line empty <<>> y) empty

-- Renderizador simples para String
render :: Doc -> String
render d = toString d ""
  where
    toString Empty r        = r
    toString (Char c) r     = c : r
    toString (Text s) r     = s ++ r
    toString Line r         = '\n' : r
    toString (Concat a b) r = toString a (toString b r)
    toString (Union a b) r  = toString a r  -- Simplificação: pega a primeira alternativa

string :: String -> Doc
string = text

double :: Double -> Doc
double d = text (show d)
```

---

## 3. Renderizando JSON (`PrettyJSON.hs`)

Agora que temos as primitivas do pretty printer, criamos o renderizador de JSON que consome `JValue` e produz um `Doc`.

Crie `src/PrettyJSON.hs`:

```haskell
module PrettyJSON
    ( renderJValue
    ) where

import Numeric (showHex)
import Data.Char (ord)
import Prelude hiding (empty)
import SimpleJSON (JValue(..))
import Prettify (Doc, char, double, empty, string, text, (<<>>), hcat, fcat)

renderJValue :: JValue -> Doc
renderJValue (JBool True)  = text "true"
renderJValue (JBool False) = text "false"
renderJValue JNull         = text "null"
renderJValue (JNumber num) = double num
renderJValue (JString str) = string (escapeString str)
renderJValue (JArray ary)  = series '[' ']' renderJValue ary
renderJValue (JObject obj) = series '{' '}' field obj
  where
    field (name, val) = string (escapeString name)
                      <<>> text ": "
                      <<>> renderJValue val

series :: Char -> Char -> (a -> Doc) -> [a] -> Doc
series open close toDoc xs = char open
                           <<>> fcat (punctuate (char ',') (map toDoc xs))
                           <<>> char close

punctuate :: Doc -> [Doc] -> [Doc]
punctuate p []     = []
punctuate p [d]    = [d]
punctuate p (d:ds) = (d <<>> p) : punctuate p ds

escapeString :: String -> String
escapeString = concatMap escapeChar

escapeChar :: Char -> String
escapeChar c | c `elem` "\"\\\f\n\r\t" = '\\' : [c]
             | otherwise = if c >= ' ' && c <= '~'
                           then [c]
                           else hexEscape c

hexEscape :: Char -> String
hexEscape c | d < 0x10000 = "\\u" ++ showHex d ""
            | otherwise   = error "caractere invalido"
  where d = ord c
```

---

## 4. O Ponto de Entrada do Executável (`app/Main.hs`)

Para interagir com a nossa biblioteca dentro do Stack, atualizamos o arquivo `app/Main.hs`:

```haskell
module Main where

import SimpleJSON
import PrettyJSON
import Prettify (render)

main :: IO ()
main = do
    let json = JObject [("nome", JString "Antigravity"), ("versao", JNumber 2.0), ("linguagens", JArray [JString "Haskell", JString "Clojure", JString "Elixir"])]
    putStrLn "JSON Estruturado:"
    putStrLn (render (renderJValue json))
```

Para rodar o projeto e ver a saída formatada do JSON:

```bash
stack build
stack run
```
