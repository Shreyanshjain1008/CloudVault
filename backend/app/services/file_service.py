from app.models.file import File

def soft_delete_file(file: File):
    file.is_deleted = True

def restore_file(file: File):
    file.is_deleted = False
