# Estrutura de Projetos com Stack e Haskell Moderno

No desenvolvimento industrial de Haskell, não compilamos arquivos avulsos usando `ghc` manualmente como no ambiente acadêmico. Em vez disso, utilizamos ferramentas de build modernas que gerenciam dependências, garantem reprodutibilidade e automatizam compilações e testes.

A ferramenta padrão da indústria hoje é o **Stack**.

---

## 🚀 O que é o Stack?

O **Stack** é um programa para gerenciar projetos Haskell. Ele se encarrega de:

1. Instalar a versão correta do compilador GHC automaticamente para cada projeto (isolando-a de outras no sistema).
2. Baixar e gerenciar dependências utilizando o **Stackage**, um repositório curado onde todas as bibliotecas são testadas juntas para garantir compatibilidade.
3. Compilar, rodar executáveis e executar suítes de testes de forma simples.

---

## 📁 Estrutura de um Projeto Stack

Quando criamos um projeto novo rodando `stack new hs2json`, o Stack gera a seguinte árvore de diretórios:

```text
hs2json/
├── app/
│   └── Main.hs             # Ponto de entrada executável (função main)
├── src/
│   └── Lib.hs              # Código-fonte da nossa biblioteca reutilizável
├── test/
│   └── Spec.hs             # Suíte de testes automatizados
├── package.yaml            # Configuração do projeto moderna (metadados e dependências)
├── stack.yaml              # Configuração do Stack (fixa a versão do compilador GHC)
└── hs2json.cabal           # Configuração gerada automaticamente (NÃO EDITAR)
```

### Arquivos Principais de Configuração:
* **`stack.yaml`**: Define o `resolver`, que especifica a versão do compilador GHC e a seleção compatível de pacotes do Stackage.
* **`package.yaml`**: A especificação moderna do seu pacote. Aqui você define:
    * Nome, autor, versão do projeto.
    * Dependências globais (ex: `base`, `text`, `containers`).
    * Módulos da **Library** (código em `src/`).
    * Dependências e módulos do **Executable** (código em `app/` que consome a library).
    * Configuração dos **Tests** (código em `test/` que testa a library).

---

## 🛠️ Comandos Essenciais do Stack

Dentro do diretório do projeto:

| Comando | Descrição |
| :--- | :--- |
| `stack setup` | Baixa e instala a versão necessária do GHC (se ainda não estiver instalada). |
| `stack build` | Compila todo o projeto (biblioteca, executáveis e testes). |
| `stack run` | Executa o binário principal do projeto. |
| `stack test` | Executa a suíte de testes do projeto. |
| `stack ghci` | Abre o REPL interativo carregando todos os módulos e dependências do projeto. |

---

## 🧩 Escrevendo um Módulo Haskell Moderno

Para que os arquivos se enxerguem, cada arquivo `.hs` dentro de `src/` deve declarar seu **nome de módulo** de forma correspondente ao seu caminho no sistema de arquivos.

Exemplo de um arquivo `src/SimpleJSON.hs`:
```haskell
module SimpleJSON
    ( JValue(..)
    , getString
    ) where

data JValue = JString String
            | JBool Bool
            deriving (Show, Eq)

getString :: JValue -> Maybe String
getString (JString s) = Just s
getString _           = Nothing
```

E para usá-lo em `app/Main.hs`:
```haskell
module Main where

import SimpleJSON (JValue(..), getString)

main :: IO ()
main = do
    let val = JString "Haskell Moderno"
    print (getString val)
```

---

## 🔗 Transição: Da Teoria Acadêmica para o Desenvolvimento Modular

Na Unidade 1, você trabalhou com arquivos soltos compilados pelo `ghc` ou carregados no `ghci`. Essa abordagem é ideal para focar na sintaxe e conceitos puros da linguagem (como casamento de padrões, listas e recursão). 

No entanto, no desenvolvimento real, lidamos com código dividido em múltiplos arquivos (módulos), dependências externas (como bibliotecas HTTP, bancos de dados ou frameworks de teste) e testes de unidade automatizados.

Nesta **Unidade 2**, usamos o **Stack** para unificar duas práticas fundamentais:

1. **Modelagem de Dados (SimpleJSON)**: Onde aplicamos os conceitos de tipos de dados algébricos e pattern matching para construir uma biblioteca de parsing e manipulação de objetos JSON reais (baseado no Capítulo 5 do *Real World Haskell*).
2. **Garantia de Qualidade (QuickCheck)**: Onde mostramos como testar propriedades matemáticas da nossa biblioteca de maneira automatizada (baseado no Capítulo 11 do *Real World Haskell*).

No próximo capítulo, iniciaremos a construção da nossa biblioteca `SimpleJSON`, aplicando as estruturas de projeto do Stack apresentadas aqui.
