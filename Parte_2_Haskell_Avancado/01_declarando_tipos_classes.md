# Declaração de Tipos Algébricos e Classes de Tipos (ADTs)

No desenvolvimento de sistemas complexos, a capacidade de modelar o domínio do problema por meio de tipos precisos é uma das maiores vantagens do Haskell. Neste capítulo, estudaremos como estender o sistema de tipos definindo **Sinônimos de Tipos**, **Tipos Algébricos de Dados (ADTs)**, **Sintaxe de Registro (Records)** e como criar ou estender **Classes de Tipos** (Typeclasses).

---

## 1. Sinônimos de Tipos: Criando Apelidos (`type`)

A forma mais simples de definir um novo tipo em Haskell é por meio de um **Sinônimo de Tipo** utilizando a palavra-chave `type`. Um sinônimo funciona apenas como um apelido legível para um tipo existente, facilitando a documentação e legibilidade do código:

```haskell
type Coordenada = (Double, Double)
type ID = Int
type Pessoa = (ID, String, Coordenada)
```

Os sinônimos de tipo podem aceitar parâmetros de tipo, funcionando de forma genérica:

```haskell
type Par a = (a, a)
type ListaAssoc k v = [(k, v)]
```

> [!WARNING]
> Como os sinônimos de tipo são apenas "apelidos", o compilador não impede que você passe um par comum `(Double, Double)` para uma função que espera uma `Coordenada`. Para obter isolamento completo e segurança de tipos em tempo de compilação, devemos utilizar `newtype` ou `data`.
>
> Além disso, sinônimos de tipo **não podem ser recursivos** (por exemplo, tentar declarar `type Arvore = (Int, [Arvore])` resultará em erro).

---

## 2. Tipos Algébricos de Dados (ADTs) (`data`)

Para criar tipos de dados inteiramente novos com seus próprios construtores de valor, utilizamos a palavra-chave **`data`**. Um **Tipo Algébrico de Dados** é composto por uma combinação de dois padrões matemáticos: **Tipos Soma** (alternativas) e **Tipos Produto** (combinações).

```text
               ┌────────────────────────┐
               │    Tipos Algébricos    │
               │      de Dados          │
               └──────────┬─────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
       [Tipo Soma]                [Tipo Produto]
      (Alternativas)              (Combinações)
  Vermelho | Verde | Azul       Circulo Float | Retangulo Float Float
```

### 1. Tipos Soma (Enumerações)
Representam valores que podem assumir uma entre várias alternativas distintas:

```haskell
data Cor = Vermelho | Verde | Azul | Amarelo
data Resposta = Sim | Nao | Talvez
```

Aqui, `Vermelho`, `Verde`, `Sim` e `Nao` são chamados de **Construtores de Valor**. Eles funcionam como constantes que representam os dados concretos do tipo.

### 2. Tipos Produto
Representam valores compostos por múltiplos campos de dados combinados:

```haskell
data Forma = Circulo Float
           | Retangulo Float Float
           | Quadrado Float
```

O tipo `Forma` possui três construtores de valor. O construtor `Circulo` carrega um `Float` (o raio). O construtor `Retangulo` carrega dois valores `Float` (largura e altura). Podemos usar casamento de padrões para inspecionar e extrair esses valores:

```haskell
area :: Forma -> Float
area (Circulo r)       = pi * r ^ 2
area (Retangulo l a)   = l * a
area (Quadrado l)      = l ^ 2
```

---

## 3. Sintaxe de Registro (Record Syntax)

Quando definimos tipos produto com muitos campos, acessar os valores por posição em casamento de padrões torna-se confuso e propenso a erros. Para resolver isso, Haskell fornece a **Sintaxe de Registro** (*Record Syntax*), que permite nomear os campos:

```haskell
data Usuario = Usuario 
  { nome    :: String
  , idade   :: Int
  , ativo   :: Bool
  } deriving (Show, Eq)
```

### Vantagens da Sintaxe de Registro:
1. **Funções Seletoras Automáticas**: O compilador cria automaticamente funções com o nome de cada campo para extrair o valor de um registro. Ex: `nome meuUsuario` retorna a `String` do nome.
2. **Atualização Prática de Registros**: Podemos atualizar campos facilmente por meio de uma sintaxe de cópia imutável:
   ```haskell
   aniversario :: Usuario -> Usuario
   aniversario u = u { idade = idade u + 1 }
   ```

---

## 4. Tipos Recursivos: Modelando Estruturas de Dados

Os tipos declarados com `data` podem ser recursivos, ou seja, conter referências a si mesmos em seus campos. Isso nos permite modelar estruturas de dados complexas, como árvores binárias:

```haskell
data Arvore a = Folha
              | No a (Arvore a) (Arvore a)
              deriving (Show, Eq)
```

Podemos processar essa árvore utilizando recursão sobre sua estrutura:

```haskell
altura :: Arvore a -> Int
altura Folha      = 0
altura (No _ e d) = 1 + max (altura e) (altura d)
```

---

## 5. Implementando Classes de Tipos Personalizadas

Vimos na Unidade 1 que classes de tipos (como `Eq` e `Ord`) governam comportamentos comuns. Haskell nos permite declarar novas classes de tipos por meio da palavra-chave `class`:

```haskell
class Serializavel a where
  serializar :: a -> String
```

Aqui, declaramos uma classe `Serializavel` que exige que qualquer tipo participante implemente a função `serializar`.

### Declarando Instâncias (`instance`)
Para fazer um tipo de dados fazer parte de uma classe de tipos, escrevemos uma declaração de **`instance`**:

```haskell
instance Serializavel Cor where
  serializar Vermelho = "#FF0000"
  serializar Verde    = "#00FF00"
  serializar Azul     = "#0000FF"
  serializar Amarelo  = "#FFFF00"
```

### Derivação Automática (`deriving`)
Para classes de tipos muito comuns da biblioteca padrão (`Show`, `Read`, `Eq`, `Ord`), o compilador do Haskell é inteligente o bastante para gerar as implementações de instância automaticamente. Basta adicionar a cláusula `deriving` no final da declaração do tipo:

```haskell
data Ponto = Ponto Double Double
  deriving (Show, Eq)
```

No próximo capítulo, veremos como utilizar o encapsulamento de tipos algébricos para lidar com a manipulação de Entrada/Saída de forma segura através da Monad de IO.