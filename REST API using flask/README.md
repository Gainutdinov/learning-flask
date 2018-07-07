# A basic REST API on Flask

A REST API using Flask

## Getting Started

Please copy the repo

### Prerequisites

SQLAlchemy==1.2.9

Flask==1.0.2

Flask-SQLAlchemy==2.3.2

PyJWT==1.6.4

### Usage

run app.py
```
python app.py
```


In order to add more users who allowed to obtain token:

```
    from UserModel import *
    User.getAllUsers()
    User.createUser('username', 'password')
    exit()
```

If you want create db from scratch inside python interpreter

```
from MovieModel import db
db.create_all()

from UserModel import *
db.create_all()
exit()

User.getAllUsers()
User.createUser('user1', 'password')
User.getAllUsers()
exit()

```

## Running the REST API quries

avaliable http request types:


*GET*
```
URL: 
    http://127.0.0.1:5000/movies?token=<token_code>
```

*POST*
```
URL: 
    http://127.0.0.1:5000/movies
Headers
    Content-Type: application/json
Body
    {
        "name": "movie_name",
        "price": 8.88,
        "identity": 1233
    }
```

*DELETE*
```
URL:
    http://127.0.0.1:5000/movies/<identity>
```

*PATCH*
```
URL: 
    http://127.0.0.1:5000/books/<identity>
Headers
    Content-Type: application/json
Body
    {
        "name": "movie_name"
    }
```

*PUT*
```
URL: 
    http://127.0.0.1:5000/books/<identity>

Headers
    Content-Type: application/json
Body
    {
        "name": "movie_name",
        "price": 55.55
    }
```


*POST*
```
URL:
    http://127.0.0.1:5000/login
Headers
    Content-Type: application/json
Body
    {
        "username":"user1",
        "password":"password"
    }
```
