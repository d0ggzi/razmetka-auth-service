class ResourceNotFound(Exception):
    """Сущность не найдена в БД"""


class ResourceAlreadyExist(Exception):
    """Сущность уже есть в БД"""