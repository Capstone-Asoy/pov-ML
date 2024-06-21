from fastapi import FastAPI, HTTPException, Request
import tensorflow as tf # type: ignore
import numpy as np
from numpy.linalg import norm
import os
import json

# ------------------------------ data init and load --------------------------------------
BASE_DIR = "/data"
model = tf.keras.models.load_model(os.path.join(BASE_DIR, 'user_model.h5'))
emb_user = np.load(os.path.join(BASE_DIR, 'user_data.npy'))
emb_book = np.load(os.path.join(BASE_DIR, 'book_data.npy'))

with open(os.path.join(BASE_DIR, 'genre_index.json'), 'r') as json_file:
    word_index = json.load(json_file)
    
genre_tokenizer = tf.keras.preprocessing.text.Tokenizer()
genre_tokenizer.word_index = word_index

books_data = np.array([norm(embedding) for embedding in emb_book])
users_data = np.array([norm(embedding) for embedding in emb_user])

app = FastAPI()

# ------------------------------------- func declaration --------------------------------
def book_recommendation(book_id: int):
    book_data = books_data[book_id - 1]
    dot_products = np.dot(books_data, book_data)
    similarities = dot_products / (books_data * book_data)
    indices = np.argsort(similarities)[::-1] + 1
    return indices[1:21]

def user_recommendation(user_id: int):
    user_data = users_data[user_id - 1]
    dot_products = np.dot(books_data, user_data)
    similarities = dot_products / (books_data * user_data)
    indices = np.argsort(similarities)[::-1] + 1
    return indices[1:51]

# -------------------------------------- end point --------------------------------------
@app.post("/user_recommend")
async def user_recommend_endpoint(request: Request):
    data = await request.json()
    user_id = data.get("user")

    if user_id is None:
        raise HTTPException(status_code=400, detail="User ID is required")

    return {"data": [int(a) for a in list(user_recommendation(user_id).flatten())]}

@app.post("/book_recommend")
async def book_recommend_endpoint(request: Request):
    data = await request.json()
    books = data.get("books")

    if books is None or not isinstance(books, list):
        raise HTTPException(status_code=400, detail="Books list is required")

    recommend = []
    for book in books:
        recommend += list(book_recommendation(book).flatten())

    return {"data": [int(a) for a in list(set(recommend))]}

@app.get("/update")
def update():
    global model, emb_user, emb_book, books_data, users_data
    model = tf.keras.models.load_model(os.path.join(BASE_DIR, 'user_model.h5'))
    emb_user = np.load(os.path.join(BASE_DIR, 'user_data.npy'))
    emb_book = np.load(os.path.join(BASE_DIR, 'book_data.npy'))
    books_data = np.array([norm(embedding) for embedding in emb_book])
    users_data = np.array([norm(embedding) for embedding in emb_user])

@app.post("/add_user")
async def add_user(request: Request):
    global emb_user, users_data
    data = await request.json()
    genre = data.get("genre")

    if genre is None:
        raise HTTPException(status_code=400, detail="Genre is required")

    genre_data = genre_tokenizer.texts_to_sequences([genre])
    new_user = np.array(model.predict(genre_data))

    emb_user = np.vstack([emb_user, new_user])
    users_data = np.append(users_data, norm(new_user))

    np.save(os.path.join(BASE_DIR, 'user_data.npy'), emb_user)

    return {"User_id": len(emb_user)}

