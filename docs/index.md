# Introdução à Programação Funcional

Bem-vindo ao livro didático de **Introdução à Programação Funcional**! Este material foi estruturado para servir como guia completo da disciplina, dividida em três unidades que abordam desde conceitos básicos até o desenvolvimento de aplicações modernas e reativas usando paradigmas funcionais.

---

## 🎯 Estrutura do Curso

O livro é organizado em três partes principais:

### 📘 Parte 1: Fundamentos e Paradigmas com Haskell (Unidade 1)
Nesta primeira unidade, exploramos os fundamentos teóricos do paradigma funcional em comparação aos paradigmas imperativo e orientado a objetos. Utilizando a linguagem **Haskell**, uma linguagem funcional pura com tipagem estática forte, estudamos os conceitos essenciais:
* Fundamentos da sintaxe e ambiente de desenvolvimento (GHCUp, Stack, REPL/GHCi)
* Funções puras, casamento de padrões (*pattern matching*) e guardas
* Manipulação e compreensão de listas, e recursão
* Funções de Alta Ordem (*High-Order Functions*: `map`, `filter`, `fold`)
* Definição de novos tipos algébricos (ADTs) e Typeclasses
* Programação interativa usando a Monad de Entrada/Saída (`IO`)

*A avaliação desta unidade será teórica/escrita focando em conceitos e exercícios de codificação Haskell básica.*

### 📙 Parte 2: Haskell Avançado e Qualidade de Código (Unidade 2)
Na segunda unidade, avançamos para tópicos do ecossistema de produção em Haskell, adaptados às práticas do Haskell moderno:
* Estrutura de projetos industriais com **Stack** e gerenciamento de dependências com Cabal/package.yaml
* Construção de uma biblioteca de manipulação e serialização de dados JSON (adaptado do clássico *Real World Haskell*, Capítulo 5)
* Testes baseados em propriedades com **QuickCheck** e garantia de qualidade de software (adaptado do *Real World Haskell*, Capítulo 11)

*A avaliação desta unidade será o desenvolvimento prático da biblioteca JSON integrada com uma suíte de testes robusta usando QuickCheck.*

### 📗 Parte 3: Clojure e Elixir (Unidade 3)
Na última unidade, exploramos a diversidade do paradigma funcional através de duas linguagens modernas focadas na indústria:
1. **Clojure**: Um dialeto Lisp moderno e pragmático rodando sobre a Máquina Virtual Java (JVM), que traz forte ênfase em imutabilidade e metaprogramação.
2. **Elixir**: Uma linguagem funcional concorrente que roda sobre a BEAM (Erlang VM), famosa por sua escalabilidade, tolerância a falhas e reatividade em tempo real.

*A avaliação desta unidade consiste em dois projetos práticos detalhados:*
* **Clojure/ClojureScript ToDo List**: Uma aplicação full-stack com backend Jetty/Reitit, banco SQLite (next.jdbc) e frontend reativo com ClojureScript e Reagent (React 19).
* **Elixir/Phoenix LiveView ToDo List**: Uma aplicação de tempo real concorrente onde o frontend e o backend se integram nativamente via WebSockets e LiveView, utilizando Ecto e SQLite.

---

## 📚 Bibliografia e Referências

* **Haskell**: Lipovača, Miran. *Learn You a Haskell for Great Good!*
* **Real World Haskell**: O'Sullivan, Bryan; Stewart, Don; Goerzen, John. *Real World Haskell* (com código modernizado para os padrões atuais do GHC).
* **Clojure**: Miller, Alex. *Programming Clojure*.
* **Elixir**: Thomas, Dave. *Programming Elixir*.
* **Materiais e Tutoriais Complementares**: [LambdaGEO Research Lab](https://lambdageo.github.io).
