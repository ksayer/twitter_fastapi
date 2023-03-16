from src import schemas
from src.core.exceptions import ValidationError
from src.crud.base import CreateSchemaType, CRUDBase
from src.models.user import Follow


class CRUDFollow(CRUDBase[Follow, CreateSchemaType]):
    async def follow_user(self, db, *, following_user_id: int, follower_user_id: int):
        """Creating a subscription from one user to another"""
        check_follow = await self.get_or_none(
            db, follower_id=follower_user_id, following_id=following_user_id
        )
        if check_follow or following_user_id == follower_user_id:
            raise ValidationError(self.model.__tablename__)
        follow_obj = schemas.FollowIn(
            follower_id=follower_user_id, following_id=following_user_id
        )
        await self.create(db, obj_in=follow_obj)  # type: ignore
        return True

    async def delete_follow(self, db, *, following_user_id: int, follower_user_id: int):
        """Stop following the given user"""
        check_follow = await self.get(
            db, follower_id=follower_user_id, following_id=following_user_id
        )
        await db.delete(check_follow)
        await db.commit()
        return True


follow: CRUDFollow = CRUDFollow(Follow)
