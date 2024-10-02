from django.shortcuts import render

from django.views.generic import TemplateView

class ContatoView(TemplateView):
    template_name = 'contact.html'

    
    def get(self,request):
        context = {'titulo':'Contato'}
        return render(request, self.template_name, context)
    