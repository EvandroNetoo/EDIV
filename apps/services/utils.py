import magic


def is_video(file):
    if not file:  # USUÁRIO ENVIOU UMA PASTA
        return False
    
    mime = magic.Magic(mime=True)
    file_tipe = mime.from_buffer(file.read(1024))
    return file_tipe.startswith('video/')
    