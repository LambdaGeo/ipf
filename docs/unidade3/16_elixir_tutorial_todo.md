# Tutorial: Elixir/Phoenix LiveView ToDo List

Este é um tutorial completo e guiado para construir uma aplicação de **Lista de Tarefas (Todo List)** do zero, usando a stack moderna de **Elixir com Phoenix LiveView** — um framework funcional e reativo para o desenvolvimento web full-stack.

Mas há um diferencial: este guia é o **segundo lado de uma mesma jornada**.

No outro tutorial — [Clojure/ClojureScript: Construindo uma Aplicação Persistente e Reativa](/blog/tutorial-clojure-clojurescript-todo-list/) — resolvemos o mesmo problema usando a stack **Clojure + Reagent + next.jdbc** , explorando o modelo de atualização reativa no navegador e a comunicação via API REST.

Aqui, faremos o mesmo **conceitualmente** , mas com **Elixir e LiveView** , onde **frontend e backend se fundem** em um único processo funcional e altamente performático.

* * *

### 🎯 Objetivo Pedagógico

O propósito deste tutorial não é apenas “fazer funcionar”, mas **entender o porquê**. Cada comando, cada função e cada módulo será explicado com contexto e analogia. Você aprenderá:

  * Como o Phoenix organiza um projeto web;
  * O que são **schemas** , **migrations** e **changesets** (e como se relacionam com os _models_ dos ORMs tradicionais);
  * Como o **LiveView** elimina a separação rígida entre frontend e backend, permitindo **interações em tempo real** sem escrever uma linha de JavaScript;
  * E, claro, como criar, listar, marcar e excluir tarefas com atualização instantânea na interface.



* * *

### ⚙️ A Stack que Vamos Usar

  * **Linguagem:** Elixir (baseada em Erlang, funcional e concorrente);
  * **Framework Web:** Phoenix 1.8 + LiveView 1.1;
  * **Banco de Dados:** SQLite (via Ecto);
  * **Estilo:** Tailwind CSS v4 + daisyUI (já integrados ao Phoenix).



### 📌 Versões Utilizadas (Importante!)

Para que o tutorial seja reprodutível, estas são as versões de referência:

Ferramenta / Biblioteca | Versão  
---|---  
Erlang/OTP | 26+  
Elixir | 1.17+  
Node.js | 18+ (LTS)  
Phoenix (`phx_new`) | 1.8.x  
Phoenix LiveView | 1.1.x  
`ecto_sql` | ~> 3.10  
`ecto_sqlite3` | ~> 0.12  
  
⚠️ **Atenção especial ao Phoenix 1.8.** Muitos tutoriais e respostas antigas na internet (e em IAs!) referem-se ao Phoenix **1.7** , que usava Tailwind v3 com `tailwind.config.js` e componentes ligeiramente diferentes. O Phoenix **1.8** mudou várias dessas coisas. Este tutorial está inteiramente alinhado ao 1.8 — se algo que você encontrar por aí divergir daqui, desconfie da versão.

* * *

### 🔁 Um Mesmo Problema, Dois Caminhos Funcionais

Aspecto | Clojure | Elixir  
---|---|---  
Paradigma | Funcional puro (imutabilidade explícita) | Funcional concorrente (processos leves)  
Renderização | Frontend reativo com Reagent (React) | LiveView (renderização no servidor em tempo real)  
Comunicação | API REST + JSON | Canal WebSocket interno (phx)  
Persistência | next.jdbc + SQLite | Ecto + SQLite  
Reatividade |  `r/atom` (frontend) | Estado do socket (`assigns`)  
  
Ambos ensinam o mesmo princípio:

> **como o estado flui em uma aplicação funcional e reativa.**

* * *

### 🧾 Os Marcos do Git (Seu Histórico Final)

Este tutorial também é um exercício de **desenvolvimento incremental com Git**. Cada fase termina em um commit; ao final, seu `git log --oneline` deve contar esta história (do mais recente para o mais antigo):
    
    
    Fase 8: Atualiza README com instruções de execução
    Fase 7: Ajusta o tema e personaliza o visual (Tailwind/daisyUI)
    Fase 6: Implementa conclusão de tarefas (toggle_complete)
    Fase 5: Implementa exclusão de tarefas (delete)
    Fase 4: Refatora TodoLive para usar Ecto, Repo e to_form()
    Fase 3: Persistência - Configura Ecto, Repo, Migrations e Task Schema
    Fase 2: Lógica em Memória - Implementa adição de tarefas
    Fase 1: Prova de Vida - Substitui a rota raiz por TodoLive
    Fase 0: Gera o esqueleto do Phoenix com LiveView (sem Ecto)
    Fase 0: Inicializa o repositório e .gitignore
    

* * *

### 📚 Índice das Fases

  * **⚙️ Fase 0:** Setup (Ambiente, Git e o Esqueleto do Projeto)
  * **🏃 Fase 1:** “Hello World” — Prova de Vida
  * **🧠 Fase 2:** Lógica em Memória
  * **🧱 Fase 3:** Persistência — A Camada de Dados (Ecto, Repo, Migration e Schema)
  * **🫀 Fase 4:** O “Transplante” — Conectando o LiveView ao Banco
  * **🗑️ Fase 5:** Refinamento — Excluindo Tarefas
  * **✅ Fase 6:** Refinamento — Concluindo Tarefas (Toggle)
  * **🎨 Fase 7:** Personalizando o Design (Tailwind CSS v4 e daisyUI)
  * **📄 Fase 8:** README e Entrega



* * *

### 💡 Um Tutorial a Duas Mãos

Assim como o tutorial em Clojure, este também é fruto de uma construção colaborativa — unindo clareza didática com profundidade técnica.

Prepare seu ambiente, abra o terminal e venha ver como **Elixir + LiveView** transforma o jeito de pensar aplicações web. 🚀

* * *

# ⚙️ Fase 0: Setup (Ambiente, Git e o Esqueleto do Projeto)

**Objetivo:** Preparar o ambiente, instalar as ferramentas e gerar o esqueleto do projeto. Mas antes, vamos entender o que é essa stack.

### A Stack: Phoenix LiveView

Antes de começar, é crucial entender por que o **LiveView** é uma abordagem diferente — e por que ela vem ganhando tanto destaque entre desenvolvedores acostumados a React, Vue ou Next.js.

### O Modo Tradicional (React / Next.js)

Em um modelo tradicional baseado em frameworks JavaScript, a aplicação é dividida em **duas camadas independentes** :

  1. **Backend (API)** — armazena e serve dados, geralmente em **JSON**.
  2. **Frontend (SPA ou SSR)** — construído em JavaScript, responsável pela interface, pelo estado e pela renderização dos componentes.



No **React puro** , o navegador recebe um HTML básico e depois baixa e executa o JavaScript que monta toda a interface (renderização no cliente). O **Next.js** otimiza isso com **SSR/SSG** , renderizando o HTML inicial no servidor — mas, após o carregamento, o React ainda assume o controle no cliente, “reidratando” a página.

Apesar de eficiente, esse modelo **mantém o estado do aplicativo no navegador** , exigindo sincronização constante com o backend via AJAX ou GraphQL. Isso significa **duas fontes de verdade** (cliente e servidor), **gerenciamento de estado complexo** e **múltiplas camadas de código** para manter tudo sincronizado.

### O Modo LiveView (Estado no Servidor)

O **Phoenix LiveView** propõe algo radicalmente diferente:

👉 **toda a lógica de estado e renderização vive no servidor.**

O navegador abre uma **conexão WebSocket** — um “túnel” bidirecional e contínuo — com o servidor Phoenix. A partir daí, toda interação do usuário (como clicar em “Adicionar Tarefa”) envia apenas uma **mensagem leve** para o servidor: `"o evento 'save_task' aconteceu"`.

O **servidor Elixir** processa o evento, atualiza o estado (a lista de tarefas) e re-renderiza o HTML **no próprio servidor**. Em seguida, calcula o que mudou (o _diff_) e envia apenas os fragmentos atualizados de volta. Um **JavaScript minúsculo** , incluído automaticamente pelo LiveView, faz o “remendo” na página — sem recarregar, sem sincronizar estados, sem React Hooks, sem Redux.

### A Vantagem

  * O **estado vive em um só lugar** — no servidor.
  * Você escreve **quase zero JavaScript**.
  * A interface é **reativa em tempo real** por padrão.
  * A performance surpreende: o Elixir lida com **milhares de conexões simultâneas** graças ao modelo de concorrência leve da **BEAM VM**.



O LiveView traz a **simplicidade do desenvolvimento tradicional (HTML + servidor)** com a **interatividade do front moderno (SPA)** — sem manter duas aplicações separadas.

* * *

### 🧰 Passo 0.1: Instalar as Ferramentas

Precisamos de três coisas:

  1. **Node.js** — o Phoenix o usa para compilar assets (CSS/JS);
  2. **Erlang** — a máquina virtual (BEAM) sobre a qual o Elixir roda;
  3. **Elixir** — a linguagem de programação.



**1\. Node.js:** baixe e instale a versão **LTS** no [site oficial](https://nodejs.org/).

**2\. Elixir e Erlang (via script oficial):** a maneira mais confiável, com controle exato das versões.

  * **Linux/macOS (Bash):**
        
        # Baixa e executa o script, fixando as versões
        curl -fsSO https://elixir-lang.org/install.sh
        sh install.sh elixir@1.17.2 otp@26.2.2 installs_dir=$HOME/.elixir-install/installs
        
        # Adicione ao seu PATH (ex: no ~/.bashrc ou ~/.zshrc)
        # export PATH=$HOME/.elixir-install/installs/otp/26.2.2/bin:$PATH
        # export PATH=$HOME/.elixir-install/installs/elixir/1.17.2-otp-26/bin:$PATH
        

  * **Windows (PowerShell):**
        
        # Baixa e executa o script
        curl.exe -fsSO https://elixir-lang.org/install.bat
        .\install.bat elixir@1.17.2 otp@26.2.2
        
        # Adicione os diretórios ao seu PATH de Ambiente de Usuário
        # (ex: %USERPROFILE%\.elixir-install\installs\otp\26.2.2\bin)
        # (ex: %USERPROFILE%\.elixir-install\installs\elixir\1.17.2-otp-26\bin)
        




**Verificação:** feche e reabra o terminal, e confirme que tudo respondeu com uma versão:
    
    
    elixir --version   # Elixir 1.17.x (compiled with Erlang/OTP 26)
    node -v            # v18 ou superior
    git --version
    

_(Se`elixir` não for encontrado, o `PATH` não foi configurado permanentemente — revise o passo acima antes de prosseguir.)_

### 🧱 Passo 0.2: Instalar o Hex e o Gerador do Phoenix

O **Mix** é a ferramenta de build do Elixir — algo como o **npm** (Node.js), o **pip** (Python) ou o **Maven** (Java). Com ele, gerenciamos dependências, rodamos tarefas, executamos testes e criamos projetos. Ele já vem instalado junto com o Elixir.

**O que é o Hex?** O **Hex** é o **gerenciador de pacotes oficial do Elixir** — o papel que o npm faz para o JavaScript. Quando usarmos bibliotecas externas (como o Ecto), é o Hex quem as baixa. Instale-o com:
    
    
    mix local.hex
    

**O que é o Phoenix?** O **Phoenix** é o principal **framework web** do ecossistema Elixir — comparável ao **Django** (Python), **Rails** (Ruby) ou **Express** (Node.js), mas construído para aproveitar ao máximo a **concorrência** e o **tempo real** da BEAM VM. Ele vem com o **LiveView** , que permite construir interfaces reativas **sem JavaScript manual**.

Instale o gerador de projetos:
    
    
    mix archive.install hex phx_new
    

✅ **Resumo:**

  * **Mix** → ferramenta de build e tarefas (como `npm` ou `pip`);
  * **Hex** → gerenciador de pacotes (como o registro do `npm`);
  * **Phoenix** → framework web completo, com foco em performance e tempo real.



### 📁 Passo 0.3: O Diretório e o Git

O `Git` é nosso sistema de controle de versão. Vamos usá-lo desde o início para salvar o progresso em “checkpoints” (commits).

**1\. Crie o diretório do projeto:**
    
    
    mkdir elixir_todo_list
    cd elixir_todo_list
    

⚠️ **O nome da pasta importa!** O Phoenix vai derivar o nome da aplicação (`:elixir_todo_list`) e o prefixo de **todos os módulos** (`ElixirTodoList...`) do nome desta pasta. Se você usar outro nome, terá que adaptar todos os nomes de módulo do tutorial. Recomendamos usar exatamente `elixir_todo_list`.

**2\. Inicialize o Git:**
    
    
    git init
    git branch -m main
    

**3\. Crie um`.gitignore` inicial.**

Antes de gerar qualquer código, vamos garantir que o repositório só contenha o que é realmente necessário. O `.gitignore` diz ao Git o que **não** versionar — dependências, arquivos compilados, configurações locais e **o arquivo do banco de dados** (que criaremos na Fase 3: ele é _resultado_ da aplicação, não código-fonte).

Crie o arquivo `.gitignore` (atenção à grafia: **ponto + gitignore** , sem letras faltando!) com o conteúdo:
    
    
    /_build
    /deps
    /priv/static/assets
    /node_modules
    /assets/node_modules
    *.log
    /config/dev.secret.exs
    .DS_Store
    .vscode/
    
    # --- Banco de Dados (SQLite, usado a partir da Fase 3) ---
    *.db
    *.db-shm
    *.db-wal
    

### 💾 Passo 0.4: O Commit Inicial
    
    
    git add .
    git commit -m "Fase 0: Inicializa o repositório e .gitignore"
    

💡 **Se o Git reclamar de identidade** (`Please tell me who you are`), configure uma vez:
    
    
    git config --global user.name "Seu Nome"
    git config --global user.email "seu@email.com"
    

e repita o commit.

### 🧩 Passo 0.5: Gerar o Esqueleto do Projeto

Com o Mix e o gerador Phoenix instalados, vamos criar a estrutura da aplicação **dentro do diretório atual** :
    
    
    mix phx.new . --no-ecto
    

**🔍 Analisando o comando:**

  * `.` → o projeto será criado **no diretório atual**. (Se quiséssemos uma pasta nova, seria `mix phx.new minha_app`.)
  * `--no-ecto` → evita instalar o **Ecto** (a camada de banco de dados) por enquanto. Vamos **adiar essa parte** para a Fase 3, pois queremos primeiro entender o funcionamento **“em memória”** do LiveView.



💡 E o LiveView? Desde o Phoenix 1.7, o **LiveView já vem incluído por padrão** — não é preciso nenhuma flag para ativá-lo (existe apenas `--no-live` para quem quiser removê-lo, o que não é o nosso caso).

**💡 Comparando com outras stacks:**

  * No **Django** : `django-admin startproject nome_do_projeto`.
  * No **Rails** : `rails new nome_do_projeto`.
  * No **Node.js** : `npx create-next-app` ou `express-generator`.



Assim como nesses casos, o Phoenix gera **um esqueleto completo** de aplicação web, com pastas organizadas para templates, rotas, assets e (opcionalmente) banco de dados.

**⚠️ Atenção às perguntas do gerador!** Como a pasta não está vazia, o Phoenix fará algumas perguntas:

  1. `The directory ... already exists. Are you sure you want to continue?` → responda **Y**.
  2. `.gitignore already exists, overwrite?` → responda **Y** (sim!). O `.gitignore` do Phoenix é mais completo que o nosso — vamos aceitá-lo e **recolocar nossas regras do banco em seguida**.
  3. `Fetch and install dependencies? [Yn]` → responda **Y**.



O Phoenix irá baixar todas as **dependências Elixir** (pelo Hex) e configurar os **assets** (Tailwind/esbuild), deixando o projeto pronto para rodar.

### ✂️ Passo 0.6: Reaplicar as Regras do Banco no `.gitignore`

Como aceitamos o `.gitignore` do Phoenix (que não conhece nosso futuro banco SQLite), abra o `.gitignore` e **acrescente ao final** :
    
    
    # --- Banco de Dados (SQLite, usado a partir da Fase 3) ---
    *.db
    *.db-shm
    *.db-wal
    

⚠️ **Por que os três padrões?** O SQLite, no modo padrão do Ecto, cria três arquivos: o banco em si (`.db`) e dois auxiliares de escrita (`.db-shm` e `.db-wal` — este último pode crescer para centenas de KB!). Nenhum deles deve ir para o GitHub. Esquecer isso é um dos erros mais comuns — e mais feios — em repositórios de alunos.

### 💾 Passo 0.7: O Commit do Esqueleto

Agora que temos a estrutura gerada (e o `.gitignore` completo), vamos versionar o ponto de partida:
    
    
    git add .
    git commit -m "Fase 0: Gera o esqueleto do Phoenix com LiveView (sem Ecto)"
    

Esse commit marca o início oficial do projeto: um esqueleto Phoenix totalmente funcional, com LiveView configurado, mas sem banco de dados — perfeito para explorar a lógica do LiveView em tempo real.

* * *

**Fim da Fase 0!** 🏁

* * *

# 🏃 Fase 1: “Hello World” — Prova de Vida

**Objetivo:** ligar o servidor Phoenix e verificar se tudo está funcionando — o primeiro “sinal de vida” do projeto. Em seguida, substituir a página padrão pelo **nosso** LiveView.

### 🔌 Passo 1.1: Ligar o Servidor
    
    
    mix phx.server
    

O servidor será iniciado e exibirá mensagens no terminal. Na primeira execução, o projeto será compilado — pode demorar um pouco.

Abra o navegador e visite: 👉 **http://localhost:4000**

Se tudo deu certo, você verá a **página de boas-vindas do Phoenix** (com o logo e links para a documentação).

⚠️ **Aviso comum no Linux:** se aparecer uma mensagem mencionando **inotify-tools** , o _live reload_ (atualização automática do navegador quando os arquivos mudam) não está funcionando. Pare o servidor (`Ctrl+C` duas vezes) e instale:
    
    
    sudo apt-get install inotify-tools
    

Depois rode `mix phx.server` novamente.

💡 **Deixe este terminal rodando.** Diferente do tutorial de Clojure (que precisava de dois servidores), aqui **um único processo** cuida de tudo: backend, frontend e a compilação dos assets. Abra um **segundo terminal** para os comandos de Git e Mix daqui em diante.

### 🧭 Passo 1.2: Alterar o Roteador

O Phoenix está exibindo a página padrão (controlada pelo `PageController`). Vamos trocá-la pelo nosso próprio **LiveView** , que será o coração da aplicação.

Abra o arquivo:
    
    
    lib/elixir_todo_list_web/router.ex
    

Encontre o escopo principal e substitua a rota raiz `/`.

_De:_
    
    
    scope "/", ElixirTodoListWeb do
      pipe_through :browser
    
      get "/", PageController, :home
    end
    

_Para:_
    
    
    scope "/", ElixirTodoListWeb do
      pipe_through :browser
    
      live "/", TodoLive, :index
    end
    

A diferença está na palavra-chave **`live`** :

  * `get` → responde com uma página renderizada **uma única vez** por um controller tradicional.
  * `live` → mantém uma **conexão em tempo real** (WebSocket), capaz de atualizar o conteúdo dinamicamente.



### 💥 Passo 1.3: O Primeiro Erro (e por que ele é bom)

Salve o arquivo e recarregue a página no navegador. Você verá um erro como:
    
    
    ** (UndefinedFunctionError) ... ElixirTodoListWeb.TodoLive ... is undefined
       (module ElixirTodoListWeb.TodoLive is not available)
    

Excelente! 🎉 Isso significa que o Phoenix **entendeu a nova rota** , mas não encontrou o módulo `TodoLive`. Ou seja: a configuração está correta — só falta criarmos o módulo. Esse tipo de erro é um ótimo sinal no Phoenix: o compilador está te guiando sobre o que precisa existir.

### 🧱 Passo 1.4: Criar o LiveView

⚠️ **Atenção — nomes de módulos no Elixir**

O Elixir segue uma convenção rígida: o **nome dos módulos** deve corresponder à **estrutura de diretórios** do projeto. Como nosso projeto foi criado na pasta `elixir_todo_list`, o prefixo dos módulos é `ElixirTodoList` (e, para a camada web, `ElixirTodoListWeb`).

Diretório | Arquivo | Módulo  
---|---|---  
`lib/elixir_todo_list_web/live/` | `todo_live.ex` | `ElixirTodoListWeb.TodoLive`  
  
Se o nome for diferente (por exemplo, `TodoListWeb.TodoLive`), o compilador **não encontrará o módulo** e você verá exatamente o erro do passo anterior — só que dessa vez sem solução à vista. Em resumo: **use o nome do diretório raiz do projeto como base** para os módulos.

Crie o arquivo:
    
    
    lib/elixir_todo_list_web/live/todo_live.ex
    

E adicione o seguinte código:
    
    
    defmodule ElixirTodoListWeb.TodoLive do
      use ElixirTodoListWeb, :live_view
    
      # mount/3 é o "construtor" do LiveView — chamado quando a página é carregada
      @impl true
      def mount(_params, _session, socket) do
        {:ok, socket}
      end
    
      # render/1 define o HTML que será exibido
      @impl true
      def render(assigns) do
        ~H"""
        <div class="p-12">
          <h1 class="text-3xl font-bold">Meu Todo List (Hello LiveView!)</h1>
        </div>
        """
      end
    end
    

O que está acontecendo aqui:

  * `use ElixirTodoListWeb, :live_view` → diz ao Phoenix que este módulo é um **LiveView** (e já traz, de brinde, os componentes de UI e helpers que usaremos nas próximas fases).
  * `mount/3` → chamado quando a página é carregada; é o ponto de inicialização do “estado”.
  * `render/1` → retorna o HTML a ser exibido.
  * `~H""" ... """` → é o **HEEx** (HTML + Embedded Elixir), uma versão do HTML com suporte a expressões Elixir — similar ao JSX do React, mas processado **no servidor** e **verificado em tempo de compilação**.



Salve o arquivo e observe: o servidor recompila automaticamente, o erro desaparece e o navegador atualiza sozinho mostrando:

> **Meu Todo List (Hello LiveView!)**

Isso confirma que o LiveView está funcionando: você acabou de renderizar sua primeira página dinâmica em tempo real, **sem escrever uma linha de JavaScript**.

### 💾 Passo 1.5: Commit

No **segundo terminal** (deixe o servidor rodando no primeiro):
    
    
    git add .
    git commit -m "Fase 1: Prova de Vida - Substitui a rota raiz por TodoLive"
    

Pronto! 🎯 Nosso projeto Phoenix com LiveView está oficialmente “vivo”.

* * *

## 🧠 Pausa Didática — Entendendo `use`, `@impl true`, `mount` e `render`

### 1\. O que faz o `use`

A linha:
    
    
    use ElixirTodoListWeb, :live_view
    

é uma forma especial de **trazer comportamentos e configurações** para o módulo atual — uma **injeção de código** feita durante a compilação.

💡 **Em termos simples:** o `use` importa automaticamente todas as funções, macros e configurações necessárias para que o módulo se comporte como um LiveView.

Linguagem | Equivalente aproximado | O que faz  
---|---|---  
**Java** | `extends BaseView` | Herda métodos e atributos de uma classe base  
**Python** | `class MyView(BaseView):` | Cria uma subclasse com comportamento herdado  
**Elixir** | `use ElixirTodoListWeb, :live_view` | Injeta código e comportamentos no módulo atual  
  
➡️ O `use` **não é herança** , mas **geração de código** : ele deixa o módulo pronto para o ecossistema Phoenix. No nosso projeto, ele também já **importa os componentes de UI** (`<.form>`, `<.input>`, `<.button>`) e disponibiliza o alias `Layouts` — vamos usá-los a partir da Fase 4.

### 2\. O papel do `@impl true`

O marcador `@impl true` vem antes de funções que **implementam callbacks** de um **comportamento** (_behaviour_). Um _behaviour_ em Elixir é parecido com uma **interface** em linguagens orientadas a objetos: ele define **quais funções um módulo deve implementar**.

O LiveView espera que cada módulo tenha, no mínimo, `mount/3` e `render/1`. Quando você escreve `@impl true`, está dizendo ao compilador: _“esta função é a implementação esperada pelo comportamento do LiveView”_.

Linguagem | Anotação equivalente | Finalidade  
---|---|---  
**Java** | `@Override` | Indica que o método sobrescreve outro da interface/classe pai  
**Elixir** | `@impl true` | Indica que a função implementa um callback de um comportamento  
  
Isso ajuda o compilador a verificar se o nome da função, a quantidade de parâmetros e o contrato do 
