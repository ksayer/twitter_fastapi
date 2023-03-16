from src import schemas
from src.crud.base import CRUDBase
from src.models.user import User


class CRUDUser(CRUDBase[User, schemas.UserIn]):
    ...


user = CRUDUser(User)
