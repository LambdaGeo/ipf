# Módulo 2 — Haskell Avançado e Qualidade de Código (20h)

## Identificação

| | |
|---|---|
| **Módulo** | 2 de 3 |
| **Carga horária** | 20 horas (10 aulas de 2h) |
| **Pré-requisitos** | Módulo 1 concluído (Haskell básico: funções, listas, alta ordem) |
| **Linguagem** | Haskell (projetos com Stack, QuickCheck, HSpec) |

## Objetivos de aprendizagem

Ao final deste módulo, o estudante deverá ser capaz de:

1. **Definir** tipos algébricos de dados (ADTs), tipos recursivos e instâncias de classes de tipos próprias.
2. **Construir** programas interativos compreendendo a separação entre código puro e ações `IO`.
3. **Estruturar** um projeto Haskell moderno com Stack, organizando biblioteca, executável e suíte de testes.
4. **Implementar** uma biblioteca completa de serialização JSON, aplicando ADTs e pretty-printing (adaptado de *Real World Haskell*, cap. 5).
5. **Garantir** a qualidade do código com testes baseados em propriedades usando QuickCheck (adaptado de *Real World Haskell*, cap. 11).

## Cronograma

| Aula | CH | Conteúdo | Capítulo |
|:---:|:---:|---|---|
| 1 | 2h | Declaração de tipos: `type`, `data`, tipos parametrizados e recursivos | [Declarando Custom Types](01_declarando_tipos_classes.md) |
| 2 | 2h | Classes de tipos próprias, instâncias e derivação | [Declarando Custom Types](01_declarando_tipos_classes.md) |
| 3 | 2h | Programas interativos: a monad `IO`, `do`-notation, entrada e saída | [Programas Interativos (IO)](02_programas_interativos.md) |
| 4 | 2h | Prática dirigida: exercícios avançados com ADTs e IO | [Exercícios Avançados](03_exercicios_avancados.md) |
| 5 | 2h | Haskell moderno: Stack, package.yaml, módulos e dependências | [Projetos Modernos com Stack](04_haskell_moderno.md) |
| 6 | 2h | Biblioteca JSON — parte 1: modelagem do tipo `JValue` e serialização | [Escrevendo a Biblioteca JSON](05_biblioteca_json.md) |
| 7 | 2h | Biblioteca JSON — parte 2: pretty-printing e refinamento da API | [Escrevendo a Biblioteca JSON](05_biblioteca_json.md) |
| 8 | 2h | Testes baseados em propriedades com QuickCheck e HSpec | [Testes com QuickCheck](06_testes_qualidade.md) |
| 9 | 2h | Laboratório orientado: desenvolvimento do trabalho prático | [Trabalho Prático](07_avaliacao.md) |
| 10 | 2h | Entrega, apresentação e defesa dos trabalhos | [Trabalho Prático](07_avaliacao.md) |

## Metodologia

O módulo é orientado a projeto: os conceitos das aulas 1–5 convergem para a construção incremental da biblioteca JSON (aulas 6–8), que é também o objeto da avaliação. As aulas 4, 9 e 10 são realizadas em laboratório.

## Avaliação

- **Trabalho prático (100%)** — desenvolvimento da biblioteca JSON estruturada com Stack e integrada com uma suíte de testes QuickCheck, conforme especificado no capítulo [Trabalho Prático](07_avaliacao.md). A nota considera: corretude e completude da biblioteca, qualidade e cobertura das propriedades testadas, organização do projeto e defesa individual na aula 10.

## Bibliografia do módulo

- O'SULLIVAN, Bryan; STEWART, Don; GOERZEN, John. *Real World Haskell* — capítulos 5 e 11 (código modernizado para os padrões atuais do GHC).
- LIPOVAČA, Miran. *Learn You a Haskell for Great Good!* — capítulos 7 a 9.
