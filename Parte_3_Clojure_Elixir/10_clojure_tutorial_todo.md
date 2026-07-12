# Tutorial: Clojure/ClojureScript ToDo List

Olá e bem-vindo(a) a este guia prático.

O objetivo aqui é construir juntos uma aplicação **Todo List completa** , indo de um repositório Git vazio até um **projeto full-stack funcional** , usando o ecossistema **Clojure** moderno.

Mais do que um simples tutorial de “copiar e colar”, este guia foi pensado para **ensinar arquitetura** — passo a passo, com atenção ao raciocínio funcional e à depuração de problemas reais.

Não vamos apenas construir uma aplicação: vamos entender **por que ela funciona** e **por que ela quebra** , explorando erros típicos (como CORS, formatos de dados incompatíveis e sincronização de estado) e aprendendo a corrigi-los com clareza.

Usaremos o clássico aplicativo **Todo List** como exemplo, pois sua simplicidade nos permite concentrar no que realmente importa: **a arquitetura e a interação entre as partes de um sistema reativo**.

* * *

### 🧱 O que Vamos Construir

  * **Backend:** Clojure, com **Ring** , **Reitit** e **next.jdbc** ;
  * **Frontend:** ClojureScript, com **Reagent 2.0 (React 19)** e **Shadow-CLJS** ;
  * **Banco de Dados:** **SQLite** , para persistência real.



Seguiremos uma jornada incremental:

  1. **Fundação:** verificação do ambiente, Git e `.gitignore`.
  2. **Backend mínimo:** um servidor “Hello World”.
  3. **Banco em memória:** criando e lendo tarefas com um `atom`.
  4. **Frontend reativo isolado:** interface dinâmica com Reagent.
  5. **Integração full-stack:** comunicação via API REST, lidando com CORS e formato de dados.
  6. **Banco real:** migrando para SQLite com `next.jdbc`.
  7. **CRUD completo:** marcar tarefas como concluídas (**Update**) e removê-las (**Delete**), com um visual melhorado.
  8. **Documentação:** um `README.md` profissional e a preparação para a entrega.



Ao final, você compreenderá **como os componentes de um sistema Clojure moderno se encaixam** , dominando o fluxo entre estado, renderização e persistência.

* * *

### 🗺️ A Arquitetura (Mapa Mental)

Durante quase todo o tutorial, você trabalhará com **dois terminais abertos ao mesmo tempo** :

Terminal | Comando | O que roda | Porta  
---|---|---|---  
**Terminal 1 (Backend)** | `clj -M:run` | A API REST (Jetty + Reitit) | `3000`  
**Terminal 2 (Frontend)** | `npx shadow-cljs watch app` | O compilador CLJS + servidor de desenvolvimento | `8000`  
  
O navegador acessa sempre o **frontend** (`http://localhost:8000`), e o frontend conversa com o **backend** (`http://localhost:3000/api/...`) via `fetch`.

💡 Guarde esta tabela. A confusão mais comum do tutorial é acessar a porta errada ou esquecer que um dos dois servidores precisa estar rodando (ou precisa ser **reiniciado** após mudar o `deps.edn`).

* * *

### 📌 Versões Utilizadas (Importante!)

Para garantir que o tutorial seja reprodutível, **fixamos todas as versões**. Use exatamente estas — misturar versões (principalmente do `shadow-cljs`) é a causa nº 1 de erros difíceis de diagnosticar.

Ferramenta / Biblioteca | Versão  
---|---  
Java (JDK) | 11 ou superior (17 ou 21 recomendado)  
Clojure CLI (`clj` / `clojure`) | 1.11+  
Node.js | 18 ou superior  
`shadow-cljs` (npm **e** `deps.edn`) |  `2.28.23` — **a mesma nos dois lugares!**  
`reagent/reagent` | `2.0.0`  
`react` / `react-dom` (npm) | `19.2.0`  
`ring` / `ring-jetty-adapter` | `1.12.2`  
`metosin/reitit-ring` | `0.7.0`  
`ring/ring-json` | `0.5.1`  
`ring-cors/ring-cors` | `0.1.13`  
`seancorfield/next.jdbc` | `1.2.659`  
`org.xerial/sqlite-jdbc` | `3.45.3.0`  
  
> [!NOTE] Em sistemas operacionais onde a ferramenta `rlwrap` não estiver instalada, o comando de atalho `clj` pode falhar com o erro: `Please install rlwrap for command editing or use "clojure" instead.` Se isso acontecer no seu ambiente, basta substituir todas as chamadas a `clj` do tutorial pela palavra `clojure` (ex: use `clojure -M:run` em vez de `clj -M:run`, e `clojure` para abrir o REPL). Ambos executam exatamente a mesma engine Clojure CLI, mas o comando `clojure` funciona sem depender do editor de linha de comando `rlwrap`.

* * *

### 🧾 Os Marcos do Git (Seu Histórico Final)

Este tutorial é também um exercício de **desenvolvimento incremental com Git**. Ao final, seu `git log --oneline` deve contar esta história (do mais recente para o mais antigo):
    
    
    docs: adiciona README com instruções de execução
    feat(crud): implementa funcionalidades de toggle e delete
    refactor(db): substitui banco em memória por persistência SQLite
    feat: conecta frontend com API do backend (CORS corrigido)
    feat: implementa UI do frontend com estado local (sem API)
    feat: implementa API REST de 'todos' com banco em memória
    feat: implementa servidor 'Hello World' com Jetty e Reitit
    feat: setup inicial do projeto com .gitignore
    

Cada fase termina com um **Git Checkpoint** que gera exatamente um desses commits.

* * *

### 📚 Índice das Fases

  * **Fase 0:** A Fundação (Ambiente, Setup e Git)
  * **Fase 1:** O Backend Mínimo (Servidor “Hello World”)
  * **Fase 2:** O Backend Funcional (API com Banco em Memória)
  * **Fase 3:** Introdução ao Frontend (Reagent e Shadow-CLJS)
  * **Fase 4:** Conectando o Frontend ao Backend (CORS e `fetch`)
  * **Fase 5:** Persistência Real (SQLite com `next.jdbc`)
  * **Fase 6:** 🏆 CRUD Completo — “Marcar como Feito”, “Deletar” e o Visual Final
  * **Fase 7:** README e Entrega



Boa jornada! 🚀

* * *

# Fase 0: A Fundação (Ambiente, Setup e Git)

**Objetivo:** Garantir que sua máquina tem todas as ferramentas necessárias, criar a pasta do projeto e iniciar o controle de versão com um `.gitignore` correto.

### Passo 0.1: Verificar o Ambiente (Pré-requisitos)

**Por que fazemos isso?** Nada é mais frustrante do que descobrir, no meio da Fase 3, que o Node.js não está instalado. Vamos verificar tudo **agora** , em 30 segundos.

**Ação:** Abra seu terminal e execute os comandos abaixo, um por um:
    
    
    java -version         # Precisa ser 11 ou superior (17 ou 21 recomendado)
    clj --version         # O Clojure CLI (qualquer versão 1.11+).
                          # Se falhar reclamando de rlwrap, use: clojure --version
    node -v               # Precisa ser 18 ou superior
    git --version         # Qualquer versão recente
    

> [!NOTE] **Sobre o clj vs. clojure:** O utilitário `clj` é apenas um script wrapper que tenta executar o Clojure em conjunto com a ferramenta de edição de linha de comando `rlwrap`. Em alguns sistemas, se o `rlwrap` não estiver instalado, rodar `clj` resultará em um erro como: `Please install rlwrap for command editing or use "clojure" instead.` Se for o seu caso, não se preocupe! Você não precisa instalar nada a mais. Basta usar o comando `clojure` no lugar de `clj` em todo este tutorial (ex: `clojure --version` para testar a versão, `clojure -M:run` para rodar o backend e `clojure` para REPL). Ambos executam exatamente o mesmo compilador.

**Resultado Esperado:** Cada comando deve imprimir uma versão. Se algum deles der `command not found`:

  * **Java:** instale um JDK (ex: [Adoptium/Temurin](https://adoptium.net/)).
  * **Clojure CLI:** siga o guia oficial em [clojure.org/guides/install_clojure](https://clojure.org/guides/install_clojure).
  * **Node.js:** instale a versão LTS em [nodejs.org](https://nodejs.org/).
  * **Git:** [git-scm.com](https://git-scm.com/).



💡 O `npm` (gerenciador de pacotes do Node) vem junto com o Node.js. Você pode confirmar com `npm -v`.

### Passo 0.2: Criar a Estrutura de Pastas

Primeiro, vamos criar um diretório principal para o projeto e navegar para dentro dele.

**Ação:** No seu terminal, execute:
    
    
    mkdir todo-app
    cd todo-app
    

Agora, você deve estar dentro da pasta `todo-app/`. Esta será a “raiz” (root) de todo o nosso projeto, onde colocaremos o `deps.edn`, o `.gitignore` e tudo mais.

⚠️ **Todos os comandos deste tutorial são executados a partir desta pasta raiz** (`todo-app/`), a menos que digamos o contrário. Se um comando falhar com “arquivo não encontrado”, a primeira coisa a verificar é: _estou na pasta certa?_ (use `pwd` para conferir).

### Passo 0.3: Iniciar o Git

**Por que fazemos isso?** O Git é nosso sistema de controle de versão. Pense nele como uma “máquina do tempo” para o nosso código. Ele nos permite salvar “fotos” (chamadas _commits_) do nosso projeto à medida que avançamos. Se algo quebrar, podemos facilmente voltar para uma versão que funcionava.

**Ação:** Dentro da pasta `todo-app/`, execute:
    
    
    git init
    git branch -m main
    

**O que vai acontecer?** Você verá uma resposta parecida com: `Initialized empty Git repository in /path/to/your/todo-app/.git/`

O Git criou um subdiretório oculto chamado `.git`. É ali que ele armazena todo o histórico. Você não precisa (e geralmente não deve) mexer nesse diretório diretamente. O segundo comando apenas renomeia a branch principal para `main` (o padrão moderno).

### Passo 0.4: Criar o `.gitignore`

**Por que fazemos isso?** O Git agora está observando _tudo_ em sua pasta. Mas não queremos salvar tudo. Existem arquivos que **não** devem ir para o controle de versão:

  1. **Dependências:** pastas como `node_modules/` podem ter milhares de arquivos. Elas podem ser reinstaladas a qualquer momento.
  2. **Arquivos compilados:** o Clojure e o shadow-cljs criam pastas de “saída” (como `target/` ou `resources/public/js/`). Nosso código-fonte é o que importa; o código compilado é apenas um resultado.
  3. **Arquivos de sistema/IDE:** seu sistema operacional ou sua IDE podem criar “lixo” (como `.DS_Store` ou `.calva/`).
  4. **Dados gerados pela aplicação:** na Fase 5, nossa aplicação criará um arquivo de banco de dados (`prod.db`). Ele é _resultado_ da aplicação rodando, não código-fonte — já vamos deixá-lo ignorado desde agora.
  5. **Segredos:** se um dia você tiver uma chave de API ou senha, ela também iria para o `.gitignore` para _nunca_ ser enviada ao GitHub.



**Ação:** Crie um novo arquivo na raiz do projeto chamado `.gitignore` (começando com um ponto) e cole o seguinte conteúdo:
    
    
    # --- Geral ---
    # Arquivos de sistema operacional
    .DS_Store
    Thumbs.db
    *.log
    
    # --- Dependências ---
    # Dependências do Node.js (para shadow-cljs)
    /node_modules/
    
    # --- Clojure & Java ---
    # Pasta de build padrão
    /target/
    
    # Cache de dependências do Clojure CLI
    .cpcache/
    .clj-kondo/
    .cider-repl-history
    
    # --- shadow-cljs (Frontend) ---
    # Saída do build do frontend
    /resources/public/js/
    
    # Cache do shadow-cljs
    .shadow-cljs/
    
    # --- IDEs ---
    # VS Code
    .vscode/
    
    # Emacs
    *~
    \#*\#
    
    # Calva (VS Code Clojure)
    .calva/
    
    # --- Banco de Dados (usado a partir da Fase 5) ---
    *.db
    *.sqlite
    *.sqlite3
    

### O que fizemos?

Instruímos o Git a ignorar as pastas e arquivos mais comuns de um projeto Clojure/ClojureScript — **incluindo, desde já, o arquivo do banco de dados** que só aparecerá na Fase 5. Assim ninguém commita o `prod.db` por acidente.

Agora, quando você executar `git status`, verá seu novo arquivo `.gitignore`, mas não verá nenhuma das pastas listadas (mesmo que elas existam).

### Passo 0.5: O Primeiro Commit

**Por que fazemos isso?** Até agora, criamos um arquivo (`.gitignore`) e o Git sabe que ele existe, mas ele não foi “salvo” na nossa linha do tempo.

O processo no Git é sempre em duas etapas:

  1. **Stage (Preparar):** você diz ao Git quais arquivos quer incluir na próxima “foto”. O comando é `git add`.
  2. **Commit (Salvar):** você tira a “foto” de todos os arquivos preparados e anexa uma mensagem. O comando é `git commit`.



**Ação:** Execute estes dois comandos, um após o outro:
    
    
    # 1. Adiciona TODOS os arquivos novos ou modificados na área de "Stage"
    #    (neste caso, apenas o .gitignore)
    git add .
    
    # 2. Salva (faz o commit) os arquivos que estão em "Stage"
    #    -m "..." é a mensagem que descreve o que fizemos
    git commit -m "feat: setup inicial do projeto com .gitignore"
    

**Resultado Esperado:**
    
    
    [main (root-commit) a1b2c3d] feat: setup inicial do projeto com .gitignore
     1 file changed, 40 insertions(+)
     create mode 100644 .gitignore
    

💡 **Se o Git reclamar de identidade** (`Please tell me who you are`), configure uma vez:
    
    
    git config --global user.name "Seu Nome"
    git config --global user.email "seu@email.com"
    

e repita o `git commit`.

### O que fizemos?

Salvamos a “Versão Zero” do nosso projeto. Você pode executar `git log` a qualquer momento para ver o histórico.

**Sobre a Mensagem de Commit (`feat: ...`):** A mensagem `feat: setup inicial...` segue uma convenção chamada **Conventional Commits** :

  * `feat:` significa _feature_ (uma nova funcionalidade — neste caso, o próprio setup).
  * Outros prefixos comuns: `fix:` (corrige um bug), `docs:` (documentação), `refactor:` (muda o código sem mudar o comportamento) e `style:` (formatação/visual).
  * Usar isso torna seu histórico Git muito fácil de ler — e é **exatamente o que será avaliado** no seu repositório.



* * *

**Fim da Fase 0!** 🏁

Temos uma fundação sólida: ambiente verificado, uma pasta de projeto limpa, um repositório Git rastreando nossas mudanças e um `.gitignore` para manter o “lixo” do lado de fora.

* * *

# Fase 1: O Backend Mínimo (Servidor “Hello World”)

**Objetivo:** Fazer um servidor web subir, rodar na sua máquina e responder “Hello, World!” quando acessado por uma URL. Isso prova que nossa configuração base está correta.

### Passo 1.1: O `deps.edn` (A “Lista de Compras” do Backend)

**O que é o`deps.edn`?** Pense neste arquivo como a “lista de compras” do seu projeto. Ele diz ao Clojure (`clj`) quais bibliotecas (dependências) ele precisa baixar da internet para o projeto funcionar.

Ele também define “apelidos” (_aliases_), que são atalhos para comandos que usamos com frequência, como “rodar o servidor”.

**Ação:** Crie o arquivo `deps.edn` na raiz do projeto (`todo-app/`) e cole o seguinte conteúdo:
    
    
    {:paths ["src" "resources"] ;; 1. Onde nosso código-fonte vai ficar
    
     :deps ;; 2. Nossa "lista de compras" de bibliotecas
     {;; O próprio Clojure
      org.clojure/clojure {:mvn/version "1.11.1"}
    
      ;; --- Dependências do Backend (API REST) ---
      ;; O "motor" do servidor web (Jetty) e as bibliotecas base do Ring
      ring/ring-core          {:mvn/version "1.12.2"}
      ring/ring-jetty-adapter {:mvn/version "1.12.2"}
    
      ;; A biblioteca de roteamento (para definir as URLs)
      metosin/reitit-ring     {:mvn/version "0.7.0"}}
    
     :aliases ;; 3. Nossos "atalhos" de comando
     {;; O alias que usaremos para iniciar o servidor
      :run
      {:main-opts ["-m" "todo.backend.core"]}}}
    

### O que fizemos?

  1. **`:paths`** : dissemos ao Clojure para procurar nosso código nas pastas `src` e `resources` (que ainda vamos criar).
  2. **`:deps`** : pedimos _apenas_ as bibliotecas essenciais do backend: 
     * `ring/ring-jetty-adapter`: o servidor web que vai “ouvir” na `localhost:3000`.
     * `metosin/reitit-ring`: o “roteador” que olha a URL (ex: `/api/hello`) e decide qual função Clojure deve ser chamada.
     * **Nota:** ainda _não_ adicionamos `shadow-cljs` ou `reagent`. Faremos isso só na Fase 3, para manter o backend limpo.
  3. **`:aliases`** : criamos o atalho `:run`. Quando rodarmos `clj -M:run`, ele executará a função principal (`-main`) do namespace `todo.backend.core` (que vamos criar a seguir).



### Passo 1.2: O Handler Mínimo (`handler.clj`)

**O que é um “Handler”?** No mundo do **Ring** (a biblioteca base da web em Clojure), um _handler_ é simplesmente uma **função** que segue um contrato:

  1. Ela recebe **um** argumento: um mapa `request` (com todos os dados da requisição HTTP que chegou).
  2. Ela retorna **um** valor: um mapa `response` (que descreve a resposta que queremos enviar de volta).



Nosso objetivo é criar a `hello-handler` mais simples possível.

**Ação 1: Criar os diretórios**

O `deps.edn` diz ao Clojure para procurar código na pasta `src/`. Em Clojure, os namespaces são mapeados diretamente para a estrutura de pastas: `todo.backend.handler` deve viver no arquivo `src/todo/backend/handler.clj`.

No seu terminal (dentro de `todo-app/`), execute:
    
    
    mkdir -p src/todo/backend
    

  * `mkdir` cria diretórios; a flag `-p` cria todos os “diretórios pais” necessários no caminho, sem dar erro.



💡 **O que é um Namespace (`ns`)?**

Em Clojure, não “importamos arquivos”, nós “requeremos namespaces”. Um namespace é um nome para um grupo de códigos, diretamente ligado à estrutura de pastas e ao nome do arquivo:

**Caminho do Arquivo** | **Declaração de Namespace (no topo do arquivo)**  
---|---  
`src/todo/backend/db.clj` | `(ns todo.backend.db ...)`  
`src/todo/backend/handler.clj` | `(ns todo.backend.handler ...)`  
  
Quando, em outro arquivo, quisermos usar as funções do `db.clj`, vamos “requerer” o namespace `todo.backend.db`, geralmente com um apelido (_alias_):
    
    
    (ns todo.backend.handler
      (:require [todo.backend.db :as db])) ;; "db" agora é o apelido
    

⚠️ **Atenção a um detalhe que pega muita gente:** se o namespace tem um hífen no nome (ex: `db-config`), o **arquivo** usa _underscore_ (`db_config.clj`). Hífen no `ns`, underscore no nome do arquivo.

**Ação 2: Criar o arquivo do handler**

Crie o arquivo `src/todo/backend/handler.clj` e cole o seguinte código:
    
    
    (ns todo.backend.handler
      "Este namespace define nossas 'funções de resposta' (Handlers).")
    
    (defn hello-handler
      "Nosso primeiro handler. Ele apenas diz 'Olá, Mundo!'"
    
      [_request] ;; 1. O handler recebe a 'request' como argumento.
                 ;;    Usamos '_' para sinalizar que, nesta função,
                 ;;    vamos ignorar esse argumento.
    
      ;; 2. O handler retorna um mapa de 'response'.
      {:status 200            ;; :status 200 é o código HTTP para "OK"
       :body "Hello, World!"}) ;; :body é o conteúdo enviado ao navegador
    

### O que fizemos?

Criamos nossa primeira peça de lógica: uma função pura e simples que atende ao contrato do Ring — ignora a entrada e retorna um mapa de resposta com status `200` e o texto “Hello, World!”.

No entanto, essa função não faz nada sozinha. Precisamos de duas coisas:

  1. Um **Servidor** (Jetty) para “ouvir” na `localhost:3000`.
  2. Um **Roteador** (Reitit) para dizer: “quando chegar um `GET` em `/api/hello`, execute a `hello-handler`”.



### Passo 1.3: O Servidor e o Roteador (`core.clj`)

O `core.clj` é o “cérebro” que junta todas as peças:

  1. **Inicia o servidor** (Jetty), que escuta na porta `3000`.
  2. **Define o roteador** (Reitit), que mapeia URLs para handlers.
  3. É o **ponto de entrada** que o comando `clj -M:run` (definido no `deps.edn`) executa.



**Ação:** Crie o arquivo `src/todo/backend/core.clj` (na mesma pasta do `handler.clj`) e cole:
    
    
    (ns todo.backend.core
      (:require [ring.adapter.jetty :as jetty]       ;; 1. O software do Servidor (Jetty)
                [reitit.ring :as ring]               ;; 2. O Roteador (Reitit)
                [todo.backend.handler :as handler])  ;; 3. Nossas funções (handler.clj)
      (:gen-class))
    
    ;; --- 1. Definição das Rotas ---
    ;; A URL "/api/hello", quando acessada com o método :get,
    ;; deve executar nossa função handler/hello-handler.
    (def app-routes
      (ring/router
       [["/api/hello" {:get {:handler handler/hello-handler}}]]))
    
    ;; --- 2. Definição da Aplicação (App) ---
    ;; O 'app' final é a função Ring principal.
    (def app
      (ring/ring-handler
       app-routes                     ;; Nossas rotas
       (ring/create-default-handler))) ;; Um handler padrão para 404 (Not Found)
    
    ;; --- 3. Função para Iniciar o Servidor ---
    (defn start-server [port]
      (println (str "Servidor iniciado na porta " port))
      ;; #'app passa a "var" da nossa app para o Jetty (útil no desenvolvimento)
      ;; :join? false evita que o servidor bloqueie a thread principal.
      (jetty/run-jetty #'app {:port port :join? false}))
    
    ;; --- 4. Ponto de Entrada Principal (-main) ---
    ;; Esta é a função que o alias :run (do deps.edn) procura.
    (defn -main [& args]
      ;; Permite passar a porta como argumento (ex: clj -M:run 8080)
      ;; ou usa "3000" como padrão.
      (let [port (Integer/parseInt (or (first args) "3000"))]
        (start-server port)))
    

### O que fizemos?

  1. **`(:require ...)`** : importamos nossas “ferramentas”: Jetty, Reitit e nosso próprio `handler.clj`.
  2. **`(:gen-class)`** : prepara este namespace para ser compilado como uma classe Java. Não é estritamente obrigatório para rodar com `clj -M:run`, mas é a convenção para namespaces com `-main` e será necessário se um dia você quiser empacotar a aplicação em um `.jar` executável. Vamos mantê-lo como boa prática.
  3. **`app-routes`** : nosso “mapa do site”. Por enquanto, com uma única rota.
  4. **`app`** : a aplicação Ring principal, que “entrega” nossas rotas ao Jetty.
  5. **`-main`** : a função que o `deps.edn` chama; pega a porta (ou usa `3000`) e chama `start-server`.



Neste ponto, temos as três peças: `deps.edn` (1.1), `handler.clj` (1.2) e `core.clj` (1.3). Vamos ver a mágica acontecer.

### Passo 1.4: Teste (Navegador e Terminal)

**Ação 1: Inicie o servidor**

No terminal, na raiz do projeto (onde está o `deps.edn`), execute:
    
    
    clj -M:run
    

**Resultado Esperado:** Na primeira vez, o Clojure vai **baixar todas as dependências** (pode demorar um pouco — várias linhas de download aparecerão). Em seguida:
    
    
    Servidor iniciado na porta 3000
    

**Importante:** este terminal agora está “ocupado” rodando o servidor. Deixe-o rodando.

**Ação 2: Teste no navegador**

  1. Abra o navegador.
  2. Digite a URL exata da nossa rota: `http://localhost:3000/api/hello`
  3. Pressione Enter.



**Resultado Esperado:** a página deve mostrar apenas o texto do `:body` do nosso handler:
    
    
    Hello, World!
    

**Ação 3: Teste no terminal com`curl`**

Para o restante do tutorial, usaremos bastante o `curl`, pois ele nos permite testar _todos_ os métodos HTTP (`GET`, `POST`, `DELETE`, etc.).

  1. Abra um **novo** terminal (deixe o servidor rodando no primeiro).
  2. Execute:


    
    
    curl http://localhost:3000/api/hello
    

**Resultado Esperado:** o `curl` imprime o `:body` diretamente no terminal:
    
    
    Hello, World!
    

### Se algo deu errado…

Sintoma | Causa provável  
---|---  
`Connection refused` | O servidor não está rodando no Terminal 1 (ou caiu com erro).  
`404 Not Found` | Erro de digitação na URL ou na rota do `core.clj` (`/api/hello`).  
`Could not locate todo/backend/core...` | O caminho do arquivo não bate com o namespace (confira `src/todo/backend/core.clj`) ou você não está na raiz do projeto.  
Erro de sintaxe ao iniciar | Algum parêntese a mais/menos ao colar. Compare com o código acima com calma.  
  
### Passo 1.5: Git Checkpoint (“Hello World”)

**Por que fazemos isso?** Se, na próxima fase, ao adicionar a lógica do banco, quebrarmos tudo acidentalmente, teremos um “ponto seguro” para o qual podemos voltar.

**Ação 1:** No terminal do servidor, pare-o (`Ctrl+C`). Agora, veja o que o Git enxerga:
    
    
    git status
    

**Resultado Esperado:** o Git mostrará os arquivos novos (“Untracked files”): `deps.edn` e `src/`.

**Ação 2:** Prepare e salve:
    
    
    git add .
    git commit -m "feat: implementa servidor 'Hello World' com Jetty e Reitit"
    

**Resultado Esperado:**
    
    
    [main 1a2b3c4] feat: implementa servidor 'Hello World' com Jetty e Reitit
     3 files changed, ...
     create mode 100644 deps.edn
     create mode 100644 src/todo/backend/core.clj
     create mode 100644 src/todo/backend/handler.clj
    

* * *

**Fim da Fase 1!** 🏁

Temos um projeto Git limpo, com um servidor web “Hello World” totalmente funcional e testado. Agora estamos prontos para construir a lógica de negócios real: a API, começando pelo “banco de dados em memória” (`atom`).

* * *
