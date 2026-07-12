# Mapas Complexos e Threading em Clojure

## 1. Introdução

Embora estruturas de dados simples como vetores e mapas sejam poderosas, as aplicações do mundo real frequentemente lidam com dados mais complexos e aninhados. Para modelar entidades como perfis de usuário, configurações de sistema ou transações comerciais, precisamos de estruturas que reflitam sua natureza hierárquica.

Este guia explora as ferramentas essenciais que o Clojure oferece para manipular essas estruturas de forma elegante, eficiente e, acima de tudo, legível. Abordaremos os conceitos fundamentais de mapas aninhados, técnicas de acesso e atualização profundos, a extração de dados com desestruturação e o uso de macros de threading para transformar código complexo em fluxos lógicos e claros.

## 2. Estruturando Dados do Mundo Real: Mapas Aninhados

Um **mapa aninhado** é simplesmente um mapa que contém outros mapas como valores. Essa estrutura é a forma natural em Clojure para representar entidades do mundo real que possuem hierarquias ou agrupamentos lógicos de informação. Em vez de "achatar" os dados em uma única estrutura, o aninhamento preserva as relações e o contexto, tornando o modelo de dados mais intuitivo e fiel à sua contraparte real.

### Exemplo Prático

Considere a estrutura de dados de um perfil de usuário. Ele contém informações básicas, mas também um resumo de atividades que, por sua vez, detalha médias de valores. Modelar isso com mapas aninhados é direto e idiomático:

```clojure
(def usuario
  {:kyle {:nome-completo "Kyle XY"
          :data-ingresso "2009-01-01"
          :resumo {:pedidos 120
                   :media {:mensal 1000
                           :anual 12000}}}})

```

Na estrutura acima, temos uma hierarquia clara:

1. O mapa principal `usuario` contém informações sobre todos os usuários.
2. A chave `:kyle` aponta para um mapa com os dados específicos desse usuário.
3. Dentro dos dados de `:kyle`, a chave `:resumo` aponta para outro mapa, agrupando informações de atividade.
4. Finalmente, dentro do `:resumo`, a chave `:media` aponta para o mapa mais interno, com as médias de valores.

Essa abordagem de "dados como dados" é uma das grandes forças do Clojure, permitindo modelar domínios complexos de forma concisa e natural.

## 3. Acesso e Atualização em Estruturas Profundas

Agora que entendemos como estruturar dados complexos, vamos aprender as maneiras idiomáticas de acessar e modificar informações nesses mapas aninhados, sempre respeitando o princípio da imutabilidade.

### 2.1. Acesso por Composição de Keywords

Como *keywords* em Clojure podem atuar como funções que procuram a si mesmas dentro de um mapa, podemos encadear essas chamadas de função para navegar em estruturas aninhadas.

Para acessar a média mensal do usuário `kyle`, lemos a expressão "de dentro para fora":

```clojure
;; Acessando a média mensal do Kyle
(:mensal (:media (:resumo (:kyle usuario))))
;; => 1000

```

Embora seja uma abordagem direta, ela tem suas limitações. Fica verbosa para estruturas muito profundas e, mais importante, lançará um `NullPointerException` se qualquer nível intermediário no caminho não existir.

### 2.2. Acesso e Atualização Seguros com e

Clojure fornece funções robustas e idiomáticas para lidar com estruturas profundas: `get-in` e `update-in`. Ambas utilizam um vetor de chaves que especifica o "caminho" até o valor desejado, tornando o código mais legível e seguro.

- **`get-in` para Leitura Segura:** Esta função acessa um valor aninhado. Se o caminho for inválido ou algum nível intermediário não existir, ela retorna `nil` em vez de lançar um erro.
- **`update-in` para Atualização Funcional:** O verdadeiro poder está em `update-in`. Em vez de apenas fornecer um novo valor, você fornece uma **função** que será aplicada ao valor antigo. Isso cria uma nova estrutura de dados completamente nova com o valor atualizado, preservando a imutabilidade do mapa original.

No exemplo abaixo, usamos `update-in` para aplicar a função `+` ao valor da média mensal, aumentando-a em 500.

```clojure
;; Aumentando a média mensal em 500
(update-in usuario [:kyle :resumo :media :mensal] + 500)

;; Resultado:
;; {:kyle {:nome-completo "Kyle XY",
;;         :data-ingresso "2009-01-01",
;;         :resumo {:pedidos 120,
;;                  :media {:mensal 1500, :anual 12000}}}}

```

### Tabela Comparativa de Métodos de Acesso

| Método | Caso de Uso Principal | Vantagem Principal |
| --- | --- | --- |
| Composição de Keywords | Leitura rápida de dados que você tem certeza que existem. | Sintaxe concisa para acesso simples. |
| `get-in` | Leitura segura de dados em qualquer profundidade. | Retorna `nil` em vez de erro se o caminho for inválido. |
| `update-in` | Atualização funcional de dados em qualquer profundidade. | Forma idiomática e segura de modificar estruturas aninhadas. |

## 4. Extraindo Dados com Desestruturação de Mapas

Manipular a estrutura inteira é útil, mas muitas vezes queremos extrair e trabalhar com partes específicas dela. A **desestruturação** é uma forma declarativa de extrair valores de uma estrutura de dados (como um mapa ou vetor) e associá-los a nomes locais, tudo em uma única etapa, reduzindo drasticamente o código repetitivo.

### Iterando sobre Pares Chave-Valor

Quando um mapa é tratado como uma sequência (por exemplo, dentro de uma função `map`), ele se torna uma sequência de vetores de dois elementos: `[chave valor]`. Podemos usar a desestruturação de vetores para dar nomes significativos a cada parte.

```clojure
(def despesas [[:livros 49.95] [:cafe 4.95]])

;; Usando desestruturação para nomear cada parte do vetor
(map (fn [[categoria valor]]
       (println (str "Categoria: " (name categoria) ", Valor: " valor)))
     despesas)

```

Se quiséssemos processar apenas os valores, poderíamos usar o `_` para ignorar a categoria, deixando nossa intenção mais clara:

```clojure
(map (fn [[_ valor]]
       (println (str "Valor: " valor)))
     despesas)

```

### Desestruturação Direta de Mapas

A forma mais comum de desestruturação é extrair valores de um *único* mapa diretamente para nomes locais usando a diretiva `:keys`. Isso é extremamente útil em conjunto com `let` ou em listas de parâmetros de funções.

```clojure
(let [resumo-kyle (:resumo (:kyle usuario))
      {:keys [pedidos media]} resumo-kyle]
  (println (str "Pedidos: " pedidos))
  (println (str "Média: " media)))
;; Imprime:
;; Pedidos: 120
;; Média: {:mensal 1000, :anual 12000}

```

Às vezes, queremos desestruturar um mapa, mas também manter uma referência ao mapa inteiro. A diretiva `:as` permite nomear o mapa completo:

```clojure
(let [{:keys [pedidos] :as resumo-completo} (:resumo (:kyle usuario))]
  (println (str "Total de pedidos: " pedidos))
  (println (str "Resumo completo: " resumo-completo)))

```

### Focando em Chaves ou Valores

Se precisarmos apenas das chaves ou dos valores de um mapa, podemos usar as funções `keys` e `vals` para obter uma sequência contendo apenas esses elementos, simplificando o processamento.

```clojure
(keys (:kyle usuario))
;; => (:nome-completo :data-ingresso :resumo)

```

## 5. Melhorando a Legibilidade com Macros de Threading

A forma como escrevemos o código é tão crucial quanto sua funcionalidade. Chamadas de função aninhadas, embora corretas, podem ser difíceis de seguir. As macros de threading do Clojure nos permitem transformar código aninhado em um **pipeline de processamento de dados** claro e legível.

Considere este exemplo, que calcula o fatorial de 5. Para entendê-lo, você precisa lê-lo de dentro para fora:

```clojure
(apply * (range 1 (+ 1 5)))

```

Clojure oferece as macros de threading (`->>` e `->`) para transformar esse código em um fluxo de operações linear e legível, de cima para baixo.

### 4.1. A Macro Thread-Last ()

A macro `->>` (lê-se "thread-last") pega o resultado de uma expressão e o insere como o **último** argumento da próxima expressão.

Vamos reescrever o cálculo do fatorial com `->>` para ver a clareza que ganhamos:

**Antes (Aninhado):**

```clojure
(apply * (range 1 (+ 1 5)))

```

**Depois (Com `->>`):**

```clojure
(->> 5
     (+ 1)
     (range 1)
     (apply *))

```

A versão com `->>` lê-se como um pipeline de transformações ou uma receita passo a passo: comece com 5, some 1, crie um intervalo a partir do resultado, e por fim, aplique a multiplicação.

**Caso de Uso Ideal:** A `->>` é perfeita para operações de coleções e sequências (`map`, `filter`, `reduce`), pois essas funções esperam a coleção como seu último argumento.

### 4.2. A Macro Thread-First ()

A macro `->` (lê-se "thread-first") é a contraparte da `->>`. Ela pega o resultado de cada expressão e o insere como o **primeiro** argumento da próxima.

**Caso de Uso Ideal:** É extremamente útil para encadear operações no estilo de programação orientada a objetos ou ao interagir com código Java, onde o objeto (a instância) é tipicamente o primeiro argumento de um método.

```clojure
;; Equivalente em Java: "hello".toUpperCase().substring(0, 3)

;; Com a macro -> em Clojure
(-> "hello"
    .toUpperCase
    (.substring 0 3))
;; => "HEL"

```

Este exemplo de aplicação irá ilustrar os conceitos de **Mapas Complexos** e **Threading** (*Encadeamento*) em Clojure, conforme abordado no Encontro 6 da estrutura curricular.

O cenário baseia-se no processamento de pedidos em um sistema de loja, um domínio que naturalmente exige o uso de estruturas de dados aninhadas e transformações sequenciais complexas.

<aside>
💡

Se você já trabalhou com Elixir, vai notar uma semelhança interessante: o macro `->` (thread-first) de Clojure é conceitualmente equivalente ao operador `|>` (pipe) em Elixir. Ambos facilitam a leitura encadeando transformações de dados de forma clara e funcional — um ótimo exemplo de como ideias poderosas se espalham entre linguagens funcionais!

</aside>

## 6. Juntando tudo em um exemplo de Pedidos em uma Loja

Imagine que estamos trabalhando com uma coleção de pedidos. Cada pedido é um mapa complexo que contém dados aninhados para descrever os itens (como quantidade e preço).

Um mapa complexo é uma estrutura de dados (tipicamente um mapa) cujos valores são outros mapas. Usamos essas estruturas para agrupar dados e funções de forma padronizada.

Primeiro, definimos a estrutura aninhada de um pedido:

```
(def pedido-exemplo
  {:cliente "Alice"
   :id-pedido 1234
   :itens {:mochila  {:quantidade 2, :preco-unitario 80.00}
           :camiseta {:quantidade 3, :preco-unitario 40.00}}})

```

### Acessando Valores Aninhados

Em Clojure, as *keywords* (palavras-chave) funcionam como funções, permitindo encadear chamadas para "navegar" em mapas aninhados.

Para obter a quantidade de mochilas no pedido:

```
;; Acesso encadeado (navegando por camadas)
(:quantidade (:mochila (:itens pedido-exemplo)))
;; => 2

```

### Atualizando Valores Aninhados (`update-in`)

Como os dados são **imutáveis**, qualquer "alteração" resulta em um novo mapa. Para modificar valores em níveis mais profundos, utilizamos a função `update-in`:

```
;; Aumenta a quantidade de mochilas em 1
(def novo-pedido-exemplo
  (update-in pedido-exemplo [:itens :mochila :quantidade] inc))

;; O caminho de navegação é um vetor: [:itens :mochila :quantidade]
(:quantidade (:mochila (:itens novo-pedido-exemplo)))
;; => 3

```

Aqui, `inc` é aplicado ao valor atual, e o resultado substitui o valor na estrutura, retornando um novo mapa.

### Threading Macros: `>` e `>>`

Os *threading macros* (ou macros de encadeamento) são essenciais para melhorar a legibilidade do código funcional em Clojure, permitindo que as transformações sejam lidas sequencialmente, de cima para baixo (como uma "pipeline"). Isso contrasta com a leitura "de dentro para fora" das expressões aninhadas.

**`>` (Thread First)**

O macro `->` (Thread First) insere o resultado da expressão anterior como o **primeiro argumento** da próxima expressão. É útil para navegações e encadeamentos lineares, como acessos a estruturas de dados:

**Tarefa:** Extrair a quantidade de certificados de um cliente em um mapa aninhado.

```
(def clientes-map {:15 {:nome "Guilherme"
                         :certificados ["Clojure" "Java"]}})

;; Forma tradicional (aninhada):
(count (:certificados (:15 clientes-map)))

;; Forma Thread First (->):
(-> clientes-map
  :15
  :certificados
  count)
;; => 2

```

A leitura de `->` (Thread First) imita a sintaxe de orientação a objetos (`objeto.metodo1().metodo2()`).

**`>>` (Thread Last)**

O macro `->>` (Thread Last) insere o resultado da expressão anterior como o **último argumento** da próxima expressão. Isso o torna ideal para a tríade de funções de coleção (`map`, `filter`, `reduce`), onde a coleção processada é tradicionalmente o último argumento.

**Tarefa: Calcular o Valor Total de um Pedido.**

Vamos definir uma função que calcula o valor de um item (preço * quantidade) e, em seguida, uma pipeline que soma todos os itens do pedido.

1. **Função Auxiliar (Map Entry Destructuring):**
Ao iterar sobre um mapa, a função `map` retorna uma sequência de `MapEntry` (par [chave, valor]). Precisamos desestruturar esse par para acessar os dados.
    
    ```
    (defn preco-do-item [[_ item-detalhes]]
      "Calcula o preço total de um item, ignorando a chave do produto (com _)."
      (* (:quantidade item-detalhes)
         (:preco-unitario item-detalhes)))
    
    ```
    
2. **Pipeline de Processamento (Usando `>>`):**
A função `total-do-pedido` pega o mapa de pedidos, extrai a sequência de itens, mapeia o preço de cada item e, finalmente, reduz essa sequência a um único valor (a soma).
    
    ```
    (defn total-do-pedido [pedido]
      (->> pedido
           :itens        ; Pega o mapa de itens
           vals         ; Transforma o mapa em uma sequência dos valores dos itens (mapas aninhados)
           (map preco-do-item) ; Aplica a função de preço a cada item (MapEntry)
           (reduce +)))   ; Soma todos os valores mapeados
    
    (total-do-pedido pedido-exemplo)
    ;; => 400.0 (2 * 80.00 + 3 * 40.00)
    
    ```
    

### Exemplo de Agregação Complexa (Agrupamento)

Para ilustrar o poder da composição de coleções e *threading*, o Clojure frequentemente usa o `group-by` seguido de `map` e redução.

**Tarefa:** Dado um vetor de pedidos, agrupar por usuário e calcular o total de cada usuário.

Para este exemplo, assumimos que temos a função `todos-os-pedidos` que retorna um vetor de mapas de pedidos e uma função auxiliar `total-dos-pedidos` (que poderia ser a `total-do-pedido` definida acima, mas que no código fonte original aceita um vetor de pedidos).

A transformação completa, utilizando `->>` para encadear as etapas do processamento de dados:

```
;; Estrutura de Mapas Complexos: Mapas de Pedidos (usando a convenção de namespace l.db)
(->> (l.db/todos-os-pedidos) ; 1. Pega todos os pedidos (vetor de mapas)
     (group-by :usuario)      ; 2. Agrupa os pedidos pelo keyword :usuario, gerando um mapa (usuario-id -> [pedidos])
     (map quantia-de-pedidos-e-gasto-total-por-usuario)
     ;; 3. Mapeia cada entrada (que é um MapEntry [usuario pedidos]) para um resumo de gastos
     println)                ; 4. Imprime o resultado

```

Este é um exemplo clássico de como o `->>` permite criar uma sequência de transformações lógica e legível para processar mapas complexos e realizar agregações de dados.

**Conceitos Ilustrados:**

- **Mapas Complexos:** A estrutura de `pedido-exemplo` demonstra mapas aninhados.
- **Acesso Profundo:** Uso de *keywords* como funções e `update-in`.
- **Threading (`>` e `>>`):** O `>>` facilita a leitura de pipelines de processamento de coleções (`vals`, `map`, `reduce`).
- **Processamento de Mapas:** O uso de `vals` e a desestruturação `[_ item-detalhes]` lida com a iteração sobre `MapEntry` ao aplicar `map` a um mapa.

### 7. Conclusão

Ao final desta exploração, você agora possui um conjunto de ferramentas poderoso e idiomático para trabalhar com dados complexos em Clojure. Você aprendeu a:

1. Modelar dados complexos do mundo real com **mapas aninhados**.
2. Manipulá-los de forma segura e eficiente usando **`update-in`** para atualizações imutáveis e **desestruturação** para extração concisa de valores.
3. Escrever código de transformação de dados que seja não apenas funcional, mas também altamente legível, utilizando as **macros de threading** para converter aninhamentos confusos em fluxos de trabalho claros.

O domínio dessas técnicas é um passo fundamental para escrever código Clojure que seja claro, conciso e profissional, aproveitando ao máximo a filosofia da linguagem.