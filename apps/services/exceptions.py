class UploadFileException(Exception):
    
    
    def __init__(self, message) -> None:
        super().__init__(message)
        self.message = message
        
    def __str__(self) -> str:
        return f'{type(self).__name__}: {self.message}'