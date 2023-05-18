from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from .exceptions import UploadFileException
from django.core.files.storage import default_storage
from secrets import token_hex


class ChunkUploadedFile():
    
    
    def __init__(self, file: TemporaryUploadedFile | InMemoryUploadedFile, chunk_size: int=2* 1024**2) -> None:
        if not isinstance(file, (InMemoryUploadedFile, TemporaryUploadedFile)):
            raise UploadFileException('file must be a instance of InMemoryUploadedFile or InMemoryUploadedFile')
        self.file = file
        self.chunk_size = chunk_size
        
    
    def _save_disk(self, file_path, file_read):
        with default_storage.open(file_path, 'wb+') as f_out:
            while True:
                chunk = file_read.read(self.chunk_size)
                if not chunk:
                    break
                f_out.write(chunk)
        return file_path


    def _create_base_file(self):
        return default_storage.save(f'{token_hex(16)}.mp4', ContentFile(''))   
    
    
    def _save_disk_tyny_file(self):
        file_path = self._create_base_file()
        return self._save_disk(file_path, self.file)
    
    
    def _save_disk_big_file(self):
        file_path = self._create_base_file()
        with open(self.file.temporary_file_path(), 'rb') as f_in:
            return self._save_disk(file_path, f_in)
        
        
    def save_disk(self):
        if isinstance(self.file, InMemoryUploadedFile):
            return self._save_disk_tyny_file()
        elif isinstance(self.file, TemporaryUploadedFile):
            return self._save_disk_big_file()
            