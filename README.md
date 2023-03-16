# My little Twitter API

Implemented functionality:

- API documentation (http://3.67.169.243/docs)
- Creating (deleting) twits
- Uploading media
- Followers
- Likes
- News feed with user's followings twits
- Get info about any user

Test coverage - 97%

### Usage

create .env in root project directory with this values:

```
PROJECT_NAME=TWITTER
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=twitter
POSTGRES_HOST=db
POSTGRES_PORT=5432
TEST_POSTGRES_DB=dbtest
API_PREFIX_V1=/api/v1
MEDIA_ROOT=media/
MEDIA_URL=/media/
DEBUG=False
```

run:
``docker-compose up -d``
