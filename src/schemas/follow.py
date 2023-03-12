from pydantic import BaseModel


class FollowIn(BaseModel):
    follower_id: int
    following_id: int
