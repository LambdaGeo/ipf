# Paradigmas de Programação e Introdução à Programação Funcional

Para entender a Programação Funcional (PF), é necessário primeiro compreender o conceito de **paradigma de programação** e a evolução histórica que nos trouxe até as linguagens modernas.

---

## 🧠 O que é um Paradigma de Programação?

Um paradigma de programação é um estilo ou uma forma de estruturar e organizar o raciocínio para resolver problemas através do código. Não se trata apenas de sintaxe, mas de um modelo mental sobre como os dados e as operações sobre esses dados devem se relacionar.

Os três paradigmas dominantes no desenvolvimento de software são:

### 1. Paradigma Imperativo
O modelo mental imperativo é focado em **como** fazer. O programa é visto como uma sequência de comandos que alteram o estado global da memória passo a passo.
* **Características**: Variáveis mutáveis, loops explicitos (`for`, `while`), estruturas condicionais e execução sequencial.
* **Analogia**: Uma receita de bolo passo a passo: *"Adicione 2 ovos, bata por 5 minutos, adicione farinha..."*

### 2. Paradigma Orientado a Objetos (POO)
Uma evolução do imperativo que agrupa estados (atributos) e comportamentos (métodos) em unidades conceituais chamadas **objetos**.
* **Características**: Encapsulamento, herança, polimorfismo. O estado do sistema é distribuído entre vários objetos que interagem enviando mensagens entre si.
* **Analogia**: Um teatro onde cada ator (objeto) tem seu próprio papel (método) e memória interna (atributos), conversando com outros atores.

### 3. Paradigma Declarativo / Funcional
O modelo mental funcional é focado em **o que** deve ser feito, e não em como. Os programas são construídos através da composição de funções matemáticas puras, sem alteração de estado global ou dados mutáveis.
* **Características**: Imutabilidade, funções como cidadãs de primeira classe, ausência de efeitos colaterais (*side effects*) e avaliação preguiçosa (*lazy evaluation*).
* **Analogia**: Uma linha de montagem matemática. Dados entram por um lado, passam por transformações (funções) e saem como novos dados do outro lado, sem alterar os dados originais.

---

## 📌 Histórico do Paradigma Funcional

A programação funcional baseia-se no **Cálculo Lambda (λ-cálculo)**, um formalismo matemático criado pelo lógico **Alonzo Church** na década de 1930 para estudar a computabilidade. Curiosamente, o cálculo lambda surgiu na mesma época em que **Alan Turing** criou a Máquina de Turing.

* **Máquina de Turing** (Base do Paradigma Imperativo): Baseada em transições de estado físicos e escrita/leitura em fitas magnéticas (memória).
* **Cálculo Lambda** (Base do Paradigma Funcional): Baseado em aplicações e definições de funções puras, substituição de variáveis e recursão.

Embora matematicamente equivalentes (Tese de Church-Turing), as duas abordagens levaram a caminhos diferentes na computação:
1. **Lisp (1958)**: Criada por John McCarthy, foi a primeira linguagem a implementar conceitos do cálculo lambda, utilizando S-expressions. Lisp é a ancestral comum do Clojure.
2. **Família ML (1970s)**: Linguagens como Standard ML e OCaml trouxeram sistemas de tipos estáticos fortes, polimorfismo e casamento de padrões.
3. **Haskell (1990)**: Surgiu como um padrão acadêmico para unificar pesquisas em linguagens funcionais puras e preguiçosas. Tornou-se a referência máxima em pureza e elegância matemática.

---

## 🛡️ Pilares da Programação Funcional

### 1. Pureza Funcional e Efeitos Colaterais
Uma função é dita **pura** se ela atende a dois requisitos básicos:
1. Retorna sempre o mesmo valor para os mesmos argumentos (determinismo).
2. Não causa efeitos colaterais visíveis (como modificar uma variável global, escrever em arquivos, alterar parâmetros recebidos ou imprimir texto na tela).

### 2. Imutabilidade
Uma vez que um valor é criado, ele nunca muda. Para "alterar" um dado, criamos uma nova versão dele aplicando uma função. Isso elimina completamente problemas de concorrência e condições de corrida (*race conditions*), pois múltiplos threads podem ler o mesmo dado sem medo de que ele seja modificado no meio do caminho.

### 3. Funções como Cidadãs de Primeira Classe
Em linguagens funcionais, funções são tratadas como qualquer outro tipo de dado:
* Podem ser passadas como argumentos para outras funções.
* Podem ser retornadas por outras funções.
* Podem ser armazenadas em variáveis ou coleções de dados.

Funções que recebem ou retornam outras funções são chamadas de **Funções de Alta Ordem** (*High-Order Functions*).
