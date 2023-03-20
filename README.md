# Twitter Clone

Implemented functionality:

- API documentation (https://ksayer.info/api/docs)
- Creating (deleting) twits
- Uploading media
- Followers
- Likes
- News feed with user's followings twits
- Get info about any user

### Technologies

- API based on FastAPI
- SQLAlchemy 2.0 (__async engine__)
- PostgreSQL
- Pytest __(coverage - 96%)__
- Gitlab CI

### Usage

create .env in root project directory with values:

```
PROJECT_NAME=TWITTER
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=twitter
POSTGRES_HOST=db
POSTGRES_PORT=5432
TEST_POSTGRES_DB=dbtest
API_PREFIX_V1=/api
MEDIA_ROOT_HOST=
MEDIA_URL=/media/
DEBUG=True
INSTALL_DEV=True
```

run:
``docker-compose up -d``
