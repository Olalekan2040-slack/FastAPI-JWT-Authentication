from fastapi import FastAPI, Body, Depends
from model import PostSchema, UserSchema, UserLoginSchema
from auth.jwt_handler import signJWT
import uvicorn
from auth.jwt_bearer import jwtBrearer


posts = [
{
    "id" : 1,
    "title" : "Animals",
    "content" : "A random post about animals"
},
{
    "id" : 2,
    "title" : "Birds",
    "content" : "A random post about Birds"
},
{
    "id" : 3,
    "title" : "Humans",
    "content" : "A random post about Humans"
}
]


users = []

app = FastAPI()



#1
@app.get("/")
def greetings():
    return {"Greet": "Hello"}



#2
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"Data": posts}


@app.get("/posts/{id}", tags = ["posts"])
def get_post_by_id(id : int):
    if id > len(posts):
        return {"Error": "Post not available"}
    
    for post in posts:
        if id == post["id"]:
            return {"Data": post}


@app.post("/posts", dependencies= [Depends(jwtBrearer)], tags=["posts"])
def post_content(post: PostSchema):
    post.id = len(posts) + 1

    posts.append(dict(post))
    return {"Data": "Post added successfully!"}
    





#User signup (Create a new user)
@app.post("/user/signup", tags=["user"])
def user_signup(user : UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@app.post("/user/login", tags=["user"])
def user_login(user : UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return{
            "error": "Invalid login details"
        }

    