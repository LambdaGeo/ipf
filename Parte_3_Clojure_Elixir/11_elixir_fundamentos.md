# Fundamentos da Linguagem

**⏱️ Duração:** 1h40m

**📚 Tópicos:** Sintaxe, IEx, tipos, pipe, coleções básicas

## 🎯 **Objetivos de Aprendizagem**

- Instalar e configurar o ambiente Elixir
- Dominar o uso do IEx (Interactive Elixir)
- Compreender tipos básicos e imutabilidade
- Aplicar o operador pipe (`|>`)
- Manipular coleções básicas com `Enum`

---

## 🔸 **1.1 Instalação e Ambiente (15 min)**

Exisitem diversas maneiras de instalar o elixir, veja mais detalhes em  https://elixir-lang.org/install.html

---

## 🔸 **1.2 Tipos Básicos (25 min)**

### **Inteiros e Operações Aritméticas**

```elixir
42
0x1F  # hexadecimal -> 31
0b1010  # binário -> 10
1_000_000  # separador visual -> 1000000

1 + 2  # 3
10 / 2  # 5.0 (float)
div(10, 2)  # 5 (divisão inteira)
rem(10, 3)  # 1 (resto)

```

> Inteiros podem ser representados em diferentes bases e suportam operações básicas.
> 

---

### **Pontos Flutuantes**

```elixir
3.14
1.0e-10

```

> Usados para valores decimais ou muito pequenos/grandes, sempre em precisão dupla (64 bits).
> 

---

### **Booleanos e Valores de Verdade**

```elixir
true
false
nil  # também considerado "falsy"

!!1    # true
!!nil  # false

```

> Em Elixir, apenas false e nil são falsos. Todo o resto é verdadeiro.
> 

---

### **Átomos**

```elixir
:ok
:error
:admin
:"átomo com espaços"

```

> Átomos são constantes nomeadas, cujo nome é o próprio valor.
> 
> 
> Servem para:
> 
- Representar **estados** (`:ok`, `:error`)
- Rótulos simbólicos e flags
- Identificadores em estruturas de dados

```elixir
File.read("dados.txt")
# {:ok, "conteúdo"} ou {:error, :enoent}

```

---

### **Strings**

```elixir
"Hello World"
"interpolação #{1 + 1}"  # => "interpolação 2"
String.length("Olá")      # 3

```

> Strings são binários UTF-8, suportando acentos e emojis.
> 
> 
> Suportam **interpolação** e funções do módulo `String`.
> 

---

## 🔸 **1.3 Imutabilidade**

```elixir
x = [1, 2, 3]
y = [0 | x]  # x não é modificado
x  # => [1, 2, 3]
y  # => [0, 1, 2, 3]

```

> Todos os valores em Elixir são imutáveis. Alterar dados cria novas estruturas, preservando as originais.
> 

---

## 🔸 **1.4 Coleções Básicas**

### **Listas (`[ ]`)**

```elixir
list = [1, 2, 3, 4]
[head | tail] = list
# head: 1, tail: [2, 3, 4]
[0 | list]  # [0, 1, 2, 3, 4]

```

> Sequências ordenadas, boas para iterações e transformações.
> 
> 
> Acesso rápido no início, lento no final.
> 

---

### **Tuplas (`{ }`)**

```elixir
person = {"João", 25, :engineer}
elem(person, 0)  # "João"
put_elem(person, 1, 26)  # {"João", 26, :engineer"}

```

> Estrutura fixa de tamanho conhecido.
> 
> 
> Ideal para **retornar múltiplos valores** ou **representar estados**.
> 

---

### **Mapas (`%{ }`)**

```elixir
user = %{name: "Maria", age: 30}
user.name       # "Maria"
user[:name]     # "Maria"
Map.get(user, :age)  # 30

```

> Coleção de pares chave-valor, ótima para representar entidades.
> 
> 
> Atualizações geram **novos mapas**.
> 

---

### **Keyword Lists (`[chave: valor]`)**

```elixir
config = [host: "localhost", port: 4000]
config[:host]  # "localhost"

```

> Lista de tuplas com chaves átomos, preservando ordem.
> 
> 
> Muito usada para **configurações e opções de funções**.
> 

<aside>
💡

**Mapas vs Keyword Lists**

Em Elixir, **mapas** e **keyword lists** são coleções de pares chave-valor, mas têm diferenças importantes:

| Característica | Mapas (`%{}`) | Keyword Lists (`[key: value]`) |
| --- | --- | --- |
| **Sintaxe** | `%{chave => valor}` | `[chave: valor]` |
| **Chaves** | Qualquer tipo | Sempre átomos (`:chave`) |
| **Ordem** | Não garantida | Mantida (útil quando a ordem importa) |
| **Chaves duplicadas** | Não permitidas | Permitidas |
| **Acesso** | `map[:chave]` ou `map.chave` | `kw[:chave]` |
| **Uso típico** | Dados estruturados complexos | Opções de funções, configurações simples |

💡 **Resumo:**

- Use **mapas** para representar dados estruturados e mutáveis (como registros de pessoas, produtos, etc.).
- Use **keyword lists** para passar **opções ou parâmetros de funções**, especialmente quando a ordem importa.

Exemplo:

```elixir
# Mapa
user = %{name: "Ana", age: 30}
user[:name]
# "Ana"

# Keyword List
opts = [host: "localhost", port: 4000]
opts[:host]
# "localhost"

```

> Apesar de parecerem similares, a escolha depende do contexto e da necessidade de ordem ou chaves duplicadas.
> 
</aside>

---

## 🔸 **1.5 Operador Pipe (`|>`)**

```elixir
"  hello world  "
|> String.trim()
|> String.upcase()
# "HELLO WORLD"

[1, 2, 3, 4, 5]
|> Enum.filter(&(&1 > 2))
|> Enum.map(&(&1 * 2))
|> Enum.sum()
# 18

```

> Encadeia funções de forma sequencial e legível.
> 

---

## 🔸 **1.6 Introdução ao Enum**

```elixir
Enum.count([1, 2, 3])         # 3
Enum.empty?([])               # true
Enum.member?([1, 2, 3], 2)   # true

Enum.map([1, 2, 3], fn x -> x * 2 end)       # [2,4,6]
Enum.filter([1, 2, 3, 4], fn x -> rem(x,2)==0 end)  # [2,4]

```

> Enum oferece funções de ordem superior para manipular coleções de forma funcional.
> 

---

## 🔸 **Exercícios em Sala**

1. Criar uma lista com números de 1 a 5, usar pipe para **dobrar cada número** e filtrar apenas pares.
2. Criar um mapa representando uma pessoa, **adicionar nova chave** usando `Map.put`.

---

## 🔸 **Tarefa para Casa**

1. Ler as lições “Basics” do Elixir School em português.
2. Fazer exercícios do Exercism: "Hello World", "Two Fer", "Reverse String".
3. Praticar no IEx: criar **10 pipelines diferentes** usando `Enum`.

---

## 🔸 **Material de Apoio**

- [📘 Elixir School - Básico](https://elixirschool.com/pt/lessons/basics/basics)
- [📘 HexDocs - Getting Started](https://hexdocs.pm/elixir/introduction.html)
- [🧪 Exercism - Trilha Elixir](https://exercism.org/tracks/elixir)

---