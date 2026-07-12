# Estrutura de Funções: Condicionais, Guardas e Pattern Matching

Na programação funcional, as funções são os blocos de construção primários. Neste capítulo, exploraremos a fundo como declarar e estruturar funções em Haskell. Analisaremos mecanismos para controle de fluxo e tomada de decisão: desde condicionais básicas até a elegância matemática de guardas e o poder do casamento de padrões (*pattern matching*).

---

## 1. Declaração de Funções e Assinaturas de Tipos

Em Haskell, é uma boa prática declarar a **assinatura de tipo** da função logo acima de sua implementação. Isso funciona como documentação para o programador e como uma especificação que o compilador validará estritamente.

```haskell
-- Assinatura de tipo: recebe dois números inteiros e retorna outro
soma :: Int -> Int -> Int
soma x y = x + y
```

### Funções com Múltiplos Parâmetros (Currying)
Como você deve ter notado, a assinatura de tipo utiliza setas (`->`) para separar os argumentos e o retorno. Em Haskell, sob o capô, **toda função recebe exatamente um único argumento** e retorna uma nova função que espera o próximo. Esse conceito matemático é conhecido como **Currying** (em homenagem ao matemático Haskell Curry) e será detalhado no capítulo de funções de alta ordem.

---

## 2. Expressões Condicionais: `if-then-else`

Ao contrário das linguagens imperativas, onde o `if` é uma estrutura de controle (um comando), em Haskell o `if` é uma **expressão**. Isso significa que ele **obrigatoriamente deve retornar um valor**.

```haskell
sinal :: Int -> Int
sinal n = if n < 0 then -1 else if n == 0 then 0 else 1
```

### Regras do `if` em Haskell:
1. **O bloco `else` é obrigatório**: Como uma expressão precisa avaliar para algum valor em qualquer cenário, não podemos omitir o `else`.
2. **Tipos idênticos**: Os blocos `then` e `else` devem retornar valores do **mesmo tipo**.

---

## 3. Guardas (Guards)

Quando lidamos com múltiplos caminhos condicionais, encadear vários blocos `if-then-else` torna o código poluído e difícil de ler. Para resolver isso, Haskell fornece os **Guardas** (representados por barras verticais `|`), que testam predicados booleanos sequencialmente.

Reescrevendo a função `sinal` com guardas:

```haskell
sinal :: Int -> Int
sinal n | n < 0     = -1
        | n == 0    = 0
        | otherwise = 1
```

### Detalhes Sintáticos:
* O símbolo `=` é colocado apenas após a condição do guarda para ligá-la à sua expressão de retorno.
* A palavra-chave **`otherwise`** é equivalente a `True` e serve como a ramificação padrão (o equivalente ao `else` final).

---

## 4. Casamento de Padrões (Pattern Matching)

O **Casamento de Padrões** (*Pattern Matching*) é o mecanismo mais expressivo para tomada de decisões em linguagens funcionais. Em vez de testarmos condições lógicas gerais, definimos equações separadas para diferentes formatos ou valores de dados que a função pode receber.

Considere a negação lógica:

```haskell
negar :: Bool -> Bool
negar True  = False
negar False = True
```

O compilador analisa a chamada da função de cima para baixo. Se passarmos `True`, ele seleciona a primeira linha; se passarmos `False`, seleciona a segunda.

### O Padrão Curinga (Wildcard)
Podemos usar o caractere sublinhado (`_`) como um curinga para casar com "qualquer valor", descartando-o se não formos utilizá-lo. Isso é muito comum para definir casos padrão:

```haskell
ehDificil :: String -> Bool
ehDificil "Haskell" = False
ehDificil "Clojure" = False
ehDificil _         = True  -- Qualquer outra linguagem é considerada difícil por padrão
```

### Pattern Matching em Tuplas
Podemos desestruturar estruturas de dados complexas, como tuplas, diretamente nos argumentos da função:

```haskell
somarPares :: (Int, Int) -> (Int, Int) -> (Int, Int)
somarPares (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)
```

---

## 5. Expressões `case`

O casamento de padrões que vimos acima é aplicado na própria definição das equações da função. Contudo, às vezes precisamos realizar um casamento de padrões dentro de uma expressão no meio da implementação. Para isso, utilizamos a construção **`case ... of`**:

```haskell
descreverNumero :: Int -> String
descreverNumero n = "O numero fornecido eh: " ++ case n of
    0 -> "Zero"
    1 -> "Um"
    _ -> "Muitos"
```

A estrutura `case` avalia a expressão e executa o casamento de padrões de cima para baixo, retornando o valor associado ao primeiro padrão compatível.

No próximo capítulo, veremos como aplicar recursão e casamento de padrões sobre estruturas de dados recursivas como **Listas**.