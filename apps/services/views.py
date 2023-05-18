from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.views import View

from tinymce.widgets import TinyMCE
from datetime import datetime

from .uploaded_file import ChunkUploadedFile
from .utils import is_video
from .choices import ServiceTags
from .models import Budget


class BudgetRequestView(View):
    def get(self, request):
        html_field = TinyMCE().render(name='descricao', value='', attrs={'id': 'id_descricao'})
        return render(request, 'request_budget.html', {'html_field': html_field, 'services': ServiceTags.choices})


    def post(self, request):
        file = request.FILES.get('file')
        service = request.POST.get('service')
        descricao = request.POST.get('descricao')

        if not is_video(file):
            messages.add_message(request, constants.ERROR, 'O arquivo enviado deve ser um vídeo.')
            print('passei aqui')
            return redirect('request_budget')
        
        file_upload = ChunkUploadedFile(file)
        file_path = file_upload.save_disk()
            
        budget = Budget(
            client = request.user,
            service_tag = service,
            descricao = descricao,
            file_path = file_path,
            data = datetime.now(),

        )
        
        budget.save()
        
        messages.add_message(request, constants.SUCCESS, mark_safe(
            # Redirecionar pra visualização do status
            f'Solitação de orçamento realizada com sucesso. <a href="{reverse("request_budget")}">Clique aqui</a> para ver o status.'
            ))
            
        return redirect('request_budget')
