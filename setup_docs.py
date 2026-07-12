# -*- coding: utf-8 -*-
import os
import shutil

BASE_DIR = "/home/sergio/dev/github/introducao_programacao_funcional"
DOCS_DIR = os.path.join(BASE_DIR, "docs")
U1_DIR = os.path.join(DOCS_DIR, "unidade1")
U2_DIR = os.path.join(DOCS_DIR, "unidade2")
U3_DIR = os.path.join(DOCS_DIR, "unidade3")

# Ensure target directories exist
for d in [DOCS_DIR, U1_DIR, U2_DIR, U3_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# Source directories at root
p1_source = os.path.join(BASE_DIR, "Parte_1_Haskell_Basico")
p2_source = os.path.join(BASE_DIR, "Parte_2_Haskell_Avancado")
p3_source = os.path.join(BASE_DIR, "Parte_3_Clojure_Elixir")

# Copy contents recursively from root folders to docs/
def copy_contents(src, dest):
    if not os.path.exists(src):
        print(f"Warning: Source folder {src} does not exist!")
        return
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for item in os.listdir(src):
        s_item = os.path.join(src, item)
        d_item = os.path.join(dest, item)
        if os.path.isdir(s_item):
            shutil.copytree(s_item, d_item)
        else:
            shutil.copy2(s_item, d_item)
    print(f"Synchronized {os.path.basename(src)} to {os.path.basename(dest)}")

copy_contents(p1_source, U1_DIR)
copy_contents(p2_source, U2_DIR)
copy_contents(p3_source, U3_DIR)

# 1. Create docs/index.md
index_content = """# Introdução à Programação Funcional

Bem-vindo ao material didático da disciplina de **Introdução à Programação Funcional**! Este livro serve como guia completo da disciplina, organizada em **três módulos de 20 horas cada (60 horas totais)**, que percorrem desde os fundamentos do paradigma funcional até o desenvolvimento de aplicações modernas e reativas.

---

## 📋 Plano da Disciplina

| | |
|---|---|
| **Carga horária total** | 60 horas |
| **Estrutura** | 3 módulos de 20 horas (10 aulas de 2h por módulo) |
| **Linguagens** | Haskell, Clojure/ClojureScript e Elixir |
| **Pré-requisitos** | Lógica de programação e experiência com alguma linguagem imperativa |

**Ementa:** Paradigmas de programação. Funções puras, imutabilidade e transparência referencial. Tipos algébricos e classes de tipos. Recursão, listas e funções de alta ordem. Programas interativos e efeitos. Testes baseados em propriedades. Linguagens funcionais na indústria: Clojure (JVM) e Elixir (BEAM). Concorrência com o modelo de atores. Desenvolvimento de aplicações web funcionais.

Cada módulo possui um **plano detalhado** com objetivos de aprendizagem, cronograma aula a aula, metodologia e critérios de avaliação — consulte a primeira página de cada módulo no menu.

---

## 🎯 Estrutura do Curso

### 📘 Módulo 1: Paradigmas e Haskell Básico (20h)
Exploramos os fundamentos teóricos do paradigma funcional em comparação aos paradigmas imperativo e orientado a objetos. Utilizando a linguagem **Haskell**, uma linguagem funcional pura com tipagem estática forte, estudamos os conceitos essenciais:
* Fundamentos da sintaxe e ambiente de desenvolvimento (GHCUp, Stack, REPL/GHCi)
* Funções puras, casamento de padrões (*pattern matching*) e guardas
* Manipulação e compreensão de listas, e recursão
* Funções de Alta Ordem (*High-Order Functions*: `map`, `filter`, `fold`)

*Avaliação: prova escrita individual (70%) e listas de exercícios (30%). Veja o [plano completo do módulo](unidade1/00_plano_modulo1.md).*

### 📙 Módulo 2: Haskell Avançado e Qualidade de Código (20h)
Avançamos para tópicos do ecossistema de produção em Haskell, adaptados às práticas do Haskell moderno:
* Definição de novos tipos algébricos (ADTs) e Typeclasses
* Programação interativa usando a Monad de Entrada/Saída (`IO`)
* Estrutura de projetos industriais com **Stack** e gerenciamento de dependências com Cabal/package.yaml
* Construção de uma biblioteca de manipulação e serialização de dados JSON (adaptado do clássico *Real World Haskell*, Capítulo 5)
* Testes baseados em propriedades com **QuickCheck** e garantia de qualidade de software (adaptado do *Real World Haskell*, Capítulo 11)

*Avaliação: desenvolvimento prático da biblioteca JSON integrada com uma suíte de testes QuickCheck (100%). Veja o [plano completo do módulo](unidade2/00_plano_modulo2.md).*

### 📗 Módulo 3: Clojure e Elixir (20h)
No último módulo, exploramos a diversidade do paradigma funcional através de duas linguagens modernas focadas na indústria:
1. **Clojure**: Um dialeto Lisp moderno e pragmático rodando sobre a Máquina Virtual Java (JVM), que traz forte ênfase em imutabilidade e metaprogramação.
2. **Elixir**: Uma linguagem funcional concorrente que roda sobre a BEAM (Erlang VM), famosa por sua escalabilidade, tolerância a falhas e reatividade em tempo real.

*Avaliação: dois projetos práticos com peso igual (veja o [plano completo do módulo](unidade3/00_plano_modulo3.md)):*
* **Clojure/ClojureScript ToDo List (50%)**: Uma aplicação full-stack com backend Jetty/Reitit, banco SQLite (next.jdbc) e frontend reativo com ClojureScript e Reagent (React 19).
* **Elixir/Phoenix LiveView ToDo List (50%)**: Uma aplicação de tempo real concorrente onde o frontend e o backend se integram nativamente via WebSockets e LiveView, utilizando Ecto e SQLite.

---

## 📚 Bibliografia e Referências

* **Haskell**: Lipovača, Miran. *Learn You a Haskell for Great Good!*
* **Real World Haskell**: O'Sullivan, Bryan; Stewart, Don; Goerzen, John. *Real World Haskell* (com código modernizado para os padrões atuais do GHC).
* **Clojure**: Miller, Alex. *Programming Clojure*.
* **Elixir**: Thomas, Dave. *Programming Elixir*.
* **Materiais e Tutoriais Complementares**: [LambdaGEO Research Lab](https://lambdageo.github.io).
"""

with open(os.path.join(DOCS_DIR, "index.md"), "w", encoding="utf-8") as f:
    f.write(index_content)

# 2. Create mkdocs.yml
mkdocs_config = """site_name: Introdução à Programação Funcional
site_description: >
  Livro didático da disciplina de Introdução à Programação Funcional:
  Haskell, Clojure e Elixir em três módulos de 20 horas.
site_author: "Sergio Souza Costa"

docs_dir: docs
site_dir: site

theme:
  name: material
  language: pt
  features:
    - navigation.top
    - navigation.sections
    - toc.integrate
    - content.code.annotate
    - content.code.copy
  palette:
    - scheme: default
      primary: teal
      accent: green

plugins:
  - search

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.superfences
  - tables
  - toc:
      permalink: true

extra_javascript:
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Apresentação: index.md

  - Módulo 1 — Paradigmas e Haskell Básico (20h):
    - "Plano do Módulo 1":                         unidade1/00_plano_modulo1.md
    - "Cap 1: Introdução aos Paradigmas":          unidade1/01_paradigmas.md
    - "Cap 2: Instalação do Ambiente":             unidade1/02_instalacao.md
    - "Cap 3: Fundamentos e o GHCi":               unidade1/03_fundamentos.md
    - "Cap 4: Tipos e Classes":                    unidade1/04_tipos_classes.md
    - "Cap 5: Funções e Pattern Matching":         unidade1/05_funcoes.md
    - "Cap 6: Listas, Recursão e Compreensão":     unidade1/06_listas.md
    - "Cap 7: Funções de Alta Ordem":              unidade1/07_alta_ordem.md
    - "Cap 8: Exercícios Resolvidos":              unidade1/08_exercicios.md

  - Módulo 2 — Haskell Avançado e Qualidade (20h):
    - "Plano do Módulo 2":                         unidade2/00_plano_modulo2.md
    - "Cap 9: Tipos Algébricos e Typeclasses":     unidade2/01_declarando_tipos_classes.md
    - "Cap 10: Programas Interativos (IO)":        unidade2/02_programas_interativos.md
    - "Cap 11: Exercícios Avançados":              unidade2/03_exercicios_avancados.md
    - "Cap 12: Projetos Modernos com Stack":       unidade2/04_haskell_moderno.md
    - "Cap 13: A Biblioteca JSON":                 unidade2/05_biblioteca_json.md
    - "Cap 14: Testes com QuickCheck":             unidade2/06_testes_qualidade.md
    - "Trabalho Prático: hs2json":                 unidade2/07_avaliacao.md

  - Módulo 3 — Clojure e Elixir (20h):
    - "Plano do Módulo 3":                         unidade3/00_plano_modulo3.md
    - "Cap 15: Clojure — Fundamentos":             unidade3/01_clojure_fundamentos.md
    - "Cap 16: Clojure — Vetores e Mapas":         unidade3/02_clojure_colecoes.md
    - "Cap 17: Clojure — Alta Ordem":              unidade3/03_clojure_alta_ordem.md
    - "Cap 18: Clojure — Threading Macros":        unidade3/04_clojure_threading_mapas_complexos.md
    - "Cap 19: Clojure — Lazy Sequences":          unidade3/05_clojure_lazy_sequences.md
    - "Cap 20: Clojure — Macros":                  unidade3/06_clojure_metaprogramacao.md
    - "Cap 21: Clojure — Interop com Java":        unidade3/07_clojure_interop.md
    - "Cap 22: Clojure — Revisão de Pilares":      unidade3/08_clojure_revisao.md
    - "Cap 23: Clojure — Exercícios Resolvidos":   unidade3/09_clojure_exercicios.md
    - "Trabalho Clojure: ToDo Full-Stack":         unidade3/10_clojure_tutorial_todo.md
    - "Cap 24: Elixir — Fundamentos":              unidade3/11_elixir_fundamentos.md
    - "Cap 25: Elixir — Pattern Matching":         unidade3/12_elixir_colecoes_pattern_matching.md
    - "Cap 26: Elixir — Módulos e Testes":         unidade3/13_elixir_modulos_funcoes_testes.md
    - "Cap 27: Elixir — Processos e Concorrência": unidade3/14_elixir_processos.md
    - "Cap 28: Elixir — Metaprogramação":          unidade3/15_elixir_metaprogramacao.md
    - "Trabalho Elixir: ToDo com LiveView":        unidade3/16_elixir_tutorial_todo.md
"""

with open(os.path.join(BASE_DIR, "mkdocs.yml"), "w", encoding="utf-8") as f:
    f.write(mkdocs_config)
print("Created mkdocs.yml configuration.")
print("All tasks completed successfully!")
