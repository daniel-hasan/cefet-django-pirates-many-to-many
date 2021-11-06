from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ModelForm
from django.urls import reverse

from .models import Tesouro
# Create your views here.
class ListarTesouros(View):
    def get(self,request):
        lst_tesouros = Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    )\
                            )
        valor_total = 0
        for tesouro in lst_tesouros:
            valor_total += tesouro.valor_total
        return render(request,"lista_tesouros.html",{"lista_tesouros":lst_tesouros,
                                                     "total_geral":valor_total})
class TesouroForm(ModelForm):
    class Meta:
        model = Tesouro
        fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
        labels = {
            "img_tesouro": "Imagem"
        }

class SalvarTesouro(View):
    def get_tesouro(self,id):
        if id:
            return Tesouro.objects.get(id=id)
        return None

    def get(self,request,id=None):
        return render(request,"salvar_tesouro.html",{"tesouroForm":TesouroForm(instance=self.get_tesouro(id))})

    def post(self,request,id=None):
        form = TesouroForm(request.POST,request.FILES, instance=self.get_tesouro(id))

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('lista_tesouros') )
        else:
            return render(request,"salvar_tesouro.html",{"tesouroForm":form})

class SalvarResponsavel(View):

    #get está em lista resposavel
    def get(self,request,tesouro_id):
        responsaveis = Tesouro.objects.get(id=tesouro_id).responsaveis_guarda_set.all()
        return render(request,"salvar_responsavel.html",{"responsavel_insert_form":ResponsavelForm(),
                                                         "resposavel":responsaveis})

    def post(self,request,tesouro_id):
        tesouro = Tesouro.objects.get(id=tesouro_id)
        
        #se foi uma insercao
        responsavel = None
        if "responsavel_add" in request.POST:
            form = ResponsavelForm(request.POST,request.FILES, instance=self.get_tesouro(id))

            if form.is_valid():
                form.save()
            responsavel = form.instance
        else:
            #caso nao seja, obtem o id a ser adicionado
            #id_responsavel pode ser um hidden field criado manualmente (sem usar form)
            id_responsavel = request.POST["id_responsavel"]
            responsavel = Responsavel.get(id=id_responsavel)
        #salva o responsavel e adiciona ele 
        tesouro.responsaveis_guarda.add(responsavel)
        tesouro.save()
        return HttpResponseRedirect(reverse('lista_responsavel') )
        """
        TODO: many-to-many
        veja mais a view "class SalvarResponsavel" e os models
        Eu não fiz tudo....eh só pra te dar ideia... Faltou:
            - template (com dois fórmularios HTML um feito pelo Django para inserir novo responsavel e outro feito "na mão" com o autocomplete -por ex - procurando responsável)
            - a classe ResponsavelForm
            - retornar erro caso o form não ser valido ao inserir novo responsavel no post da view salvarResponsavel (ver o exemplo emSalvarTesouro ) 
            Faltou testar kkkk então, talvez tenha erro de execução - eh mais para vc ter uma ideia
        
        """

class RemoverTesouro(View):
    def get(self,request,id):
        Tesouro.objects.get(id=id).delete()
        return HttpResponseRedirect(reverse('lista_tesouros') )
