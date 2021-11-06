Nesta tarefa, você irá fazer alterações na tarefa da prática passada para que seja usado GenericViews e, além disso, use autenticação em alguma view. Generic views são classes python que facilitam a criação de views que fazem as operações básicas de listar, inserir, remover e atualizar.

Antes de começar: não esqueça de executar o `makemigrations` e o `migrate` para atualizar o banco apropriadamente.

## Exercício 1 - Inserir/Atualizar Tesouros usando CreateView e UpdateView

**Inserir**
- Para usar Generics ao inserir, você deverá usar uma classe para inserir e outra para atualizar. Primeiramente, crie a classe `InserirTesouro`, a classe `CreateView` será superclasse de `InserirTesouro` ([relembre herança aqui](https://daniel-hasan.github.io/cefet-web-grad/classes/python3/)).

- A classe `CreateView` pertence ao módulo `django.views.generic.edit`. Faça o import apropriado.

- Dentro da classe InserirTesouro, você deverá criar os seguintes atributos estáticos:

	- `model`: Classe do modelo que se refere esta inserção (não esquecer de dar import)

	- `fields`: lista com o nome dos campos que serão usados no form (ao inserir um tesouro).

	- `template_name`: endereço do template a ser renderizado

	- `success_url`: URL que será redirecionada caso tenha sido inserido com sucesso. Use o comando `reverse_lazy` para obter a URL pelo nome. A função `reverse_lazy` tem a mesma funcionalidade que a `reverse`  mas, ela só é executada quando a variável `success_url` for lida (e não quando for atribuida) - por isso é lazy. Assim, evita-se que a URL seja resolvida antes do carregamento do arquivo `urls.py`. Essa função está no módulo `django.urls`.

- Altere no template `salvar_tesouro.html` o formulário que está sendo impresso. Agora o nome dele é `form`.

- Para que o nome do label de `img_tesouro` seja `Imagem`, defina esse nome no parametro `verbose_name`  da classe `ImageField` do atributo `img_tesouro` em `models.py`.

- Altere em `urls.py`, na URL de inserção, a view de `SalvarTesouro` para `InserirTesouro`. Rode o servidor e teste a inserção.

**Atualizar**
- Diferentemente da VIew que criamos uma para inserir e atualizar, para usar Generic View, você deverá usar uma classe para inserir e outra para atualizar. Assim, crie a classe `AtualizarTesouro`, a classe `UpdateView` será superclasse de `AtualizarTesouro`.

- A classe `UpdateView` pertence ao módulo `django.views.generic.edit`. Faça o import apropriado.

- Os atributos estáticos são os mesmos que você criou para a classe `InserirTesouro`

- Altere em `urls.py`, na URL de edição, a view de `SalvarTesouro` para `AtualizarTesouro`. Altere o parametro de `id` para `pk`, pois é o padrão das Generic views.  Agora, você pode excluir a classe `SalvarTesouro` e o `ModelForm` que você tinha criado. Execute o servidor teste e verifique se a classe funciona da mesma forma.


**Melhoria das classes**

Quando há repetição de código, da forma que deixamos os atributos estáticos de InserirTesouro e AtualizarTesouro, há alguma coisa que pode ser melhorada. Neste caso, você pode fazer uma classe `SalvarTesouro` ela que possuirá todos os atributos estáticos. `SalvarTesouro` não possuirá superclasses. Coloque `SalvarTesouro` como superclasse de `InserirTesouro` e `AtualizarTesouro`. Lembre-se que você pode fazer herança múltipla apenas separando as superclasses por vírgula, exemplo:
```python
class Funcionario(Pessoa,Pagavel):
	...
```
Significa que `Pessoa` e `Pagavel` são superclasses de Funcionario. Deixe o SalvarTesouro como a primeira classe a ser herdada (pois a seguinte necessita dos dados da SalvarTesouro já carregada).


Logo após, você pode eliminar todos os atributos das classes `InserirTesouro` e `AtualizarTesouro`. Deixe o comando `pass` no lugar dos atributos para que o código funcione sem erro de sintaxe. Rode o servidor e verifique se ainda a inserção e atualização está funcionando.

## Exercício 2 - Remover Tesouros usando DeleteView

- Exclua a classe antiga `RemoverTesouro` e crie uma nova com o mesmo nome. Essa nova classe deverá ser subclasse de `DeleteView`.

- `DeleteView` pertence também ao módulo `django.views.generic.edit` faça import apropriadamente.

- `RemoverTesouro` possuirá os atributos estáticos `model` e `success_url` com o mesmo funcionamento dos atributos do exercício anterior.

- Na URL de remover o tesouro, altere o parâmetro de `id` para `pk`.

- Não é uma boa prática de programação excluir via GET (ou seja, por meio da URL). Por isso, a forma indicada em fazer é criar um formulário com o botão de excluir. Por causa disso, a classe `DeleteView` exclui apenas se enviarmos via POST.  Se enviássemos via GET, iriamos ter que criar um página de confirmação para a exclusão ser sempre via POST.

Assim, no template de listar os tesouros, vamos implementar a primeira alternativa: crie um formulário para o botão de excluir na mesma célula que estava o link de excluir, mas, ao invés do link, colocariamos o seguinte:
```html
<form method="POST" action="<!-- URL de exclusão -->">
                 {% csrf_token %}
                 <button>
			<!-- imagem do botão -->
                  </button>
</form>
```
Veja que usamos o `csrf_token` por isso, temos mais segurança em excluir ao fazer desse jeito - em comparação ao usar GET, mesmo sendo um pouco mais verboso. O botão já foi estilizado em `estilos.css` para ficar como uma imagem sem bordas e cor de fundo.




## Execício 3 - Listar utilizando ListView

Primeiramente, iremos ver como é fácil fazer uma ListView. Depois, iremos complicar um pouco :-).

- Exclua todos os métodos da classe `ListarTesouro` (copie o codigo para um bloco de notas, você irá precisar dele). Agora, essa classe será superclasse de `ListView` e possuirá apenas os atributos estáticos `model` e `template_name` similar ao funcionamento dos exercícios anteriores. A classe ListView pertence ao módulo django.views.generic.list. 

- Agora, no template `lista_tesouros.html`, a variável da lista de tesouros se chama `object_list` faça a alteração apropriada para que a listagem funcione.

Execute o servidor e teste a alteração. Se tudo ocorreu bem, a listagem funcionou (se você inserir algum elemento). Porém, não é exibido o total geral nem o valor total por tesouro. Para isso, faça o seguinte:

- **Para obter o valor total por tesouro:** Crie, na classe `ListarTesouro`, o método `get_queryset`. Esse método é responsável para obter a consulta que será armazenada na variável `object_list`. Por isso, esse método deverá retornar a consulta feita na prática passada - para obter o valor total por tesouro.

- **Para obter o total geral:** Agora Você deverá criar o método `get_context_data` na classe `ListarTesouro`. Esse método prepara um dicionário com todas as variáveis usadas no template. Cada variável no template é uma chave deste dicionário. Veja como o esqueleto deste método:

```python
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
	#adicione aqui algo a mais no contexto
        return context

```
Nesse código, `context` é o dicionário que armazena as variáveis a serem usadas no template. Você pode adicionar mais variáveis. Ou seja, você pode criar o `context['total_geral']` e esse será a nossa variável `total_geral` no template. Note que `context['object_list']` possui a lista de tesouros. Assim, você deverá navegar na veriável `context['object_list']` para calcular o total geral e armazenar em `context['total_geral']`.




## Exercício 4 -  Autenticação

- Inicialmente, você deve criar um super usuário para seu sistema. Faça isso da seguinte forma:

```
python3 manage.py createsuperuser
```


- Existe um View já pronta para fazer o login. Assim, você dever configurar o template para que funcione com esta view. Para isso, altere `login.html` para ser a página de login. No conteúdo dessa página será exibido apenas um formulário com login e senha. O formulário de login é representado pela  variável de nome `form` no template. Você deve imprimir essa variável dentro de um formulário HTML (tag `form`). Esse formulário deve ser enviado por POST.

- Crie a URL respectiva ao login. Você deve vincular à view `LoginView`. Ao chamar o método `as_view` dessa view, passe como parâmetro o nome do template usando o parâmetro `template_name` (i.e. `template_name="endereço_do_template"`). A classe `LoginView` já existe e pertence ao módulo `django.contrib.auth.views`, faça o import apropriado.

- Em `settings.py`, você deverá criar duas variáveis: `LOGIN_REDIRECT_URL` e `LOGIN_URL`. `LOGIN_REDIRECT_URL` é a variável que armazena o nome da URL (ou URL) que será redirecionado após fazer o login. Mande redirecionar para a lista de tesouros. `LOGIN_URL` armazena o nome da URL (ou URL) da página de login. Em ambos os casos, opte sempre por usar o nome da URL.  

Agora, você pode testar o login.

- Você deve criar a URL de logout. Para isso, crie uma URL referenciando a view `LogoutView`. Ao chamar o método `as_view` especifique pelo parametro `next_page` o nome da URL que será redirecionado após logout. Você pode redirecionar para a página de login. A classe `LogoutView` pertence ao módulo `django.contrib.auth.views`, faça o import apropriado.

- Logo após, no template `lista_tesouros.html`, crie um link para efetuar o logout. Para que este link esteja estilizado apropriadamente, use o `id="logout"` na tag de link (`<a>`).

- Agora você deve especificar todas os locais que necessitam de login para acessar. Para isso, todas as views que necessitam que você esteja logado para acessá-la deve ser subclasse de `LoginRequiredMixin`. Assim, em nosso caso, deixe `LoginRequiredMixin` superclasse de todas as views. Por causa de harança múltipla e como `LoginRequiredMixin` possui os mesmos métodos que outras superclasses da view (como o `post`) você deve deixar o `LoginRequiredMixin` como a primeira superclasse da lista. Exemplo:

```python
class SalvarTesouroView(LoginRequiredMixin, ...):
	...
```

- Faça o import apropriado da classe LoginRequiredMixin que pertence ao módulo `django.contrib.auth.mixins`

## Desafio - filtrar a tabela pelo usuário autenticado

Crie um relacionamento da tabela `Tesouro` com o usuário. Para isso, crie uma chave estrangeira para a tabela `User` essa tabela já existe e deve ser importada do módulo `django.contrib.auth.models`. Logo após, nas views, altere o filtro da tabela: você pode acessar o usuário autenticado em uma GenericView em `self.request.user`.

Você deverá alterar a inserção/atualização do `Tesouro` apropriadamente. [Veja na documentação do Django](https://docs.djangoproject.com/pt-br/2.1/topics/class-based-views/generic-editing/).

Você deverá atualizar o banco de dados para que essa alteração funcione. Caso tenha dificuldades (pois já existem dados associados) faça o seguinte: (1) exclua o arquivo `db.sqlite3`; (2) exclua todos os arquivos `.py` (menos o `__init__.py`) da pasta `pirates/migrations` (3) execute o `makemigrations` e o `migrate` para atualizar o banco.
