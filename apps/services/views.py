from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .uploaded_file import ChunkUploadedFile
from .utils import is_video


def request_budget(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'request_budget.html')
    
    elif request.method == 'POST':
        file = request.FILES.get('file')

        if not is_video(file):
            messages.add_message(request, constants.ERROR, 'O arquivo enviado deve ser um vídeo.')
            print('passei aqui')
            return redirect('request_budget')
        
        file_upload = ChunkUploadedFile(file)
        file_upload.save_disk()
            
        return HttpResponse('teste')