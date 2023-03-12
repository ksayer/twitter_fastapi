from src.crud.base import CreateSchemaType, CRUDBase
from src.models import Like


class CRUDLike(CRUDBase[Like, CreateSchemaType]):
    ...


like: CRUDLike = CRUDLike(Like)
