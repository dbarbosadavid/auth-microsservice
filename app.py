import token
from fastapi import FastAPI
from routers.roles_routes import roles
from routers.user_routes import user
from routers.token_routes import token

app = FastAPI(title='AuthAPI', version='1.0.0')


app.include_router(token)
app.include_router(user)
app.include_router(roles)