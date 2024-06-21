# pov-ML
Repository Bookmate Project from Machine Learning Team.<br>
[Link to our drive](https://drive.google.com/drive/folders/1z_TP4Jd-4EGid9W9dweU6Yg84ha_RC_k?usp=sharing)

<br>
ML Team: <br>
- M004D4KY2565 | Ariq Maulana Tazakka | Sepuluh Nopember Institute of Technology | [Active] <br>
- M010D4KX2387 | Nadira Maysa Dyandra | University of Indonesia | [Active]  <br>
- M010D4KX1490 | Amanda Nadhifah Zahra Andini | University of Indonesia | [Active]

### BookMate
BookMate is a mobile application built natively for Android that provides book recommendations. Whether you're an avid reader looking for your next book or just curious about what's trending, BookMate helps you find the perfect read.

### Features
Personalized Recommendations: Get book recommendations tailored to your preferences.
Search Functionality: Search for books by title, author, or genre.
Book Details: View detailed information about books including summaries, ratings, and reviews.
Favorites: Save your favorite books for quick access later.
User Reviews: Read and write reviews for books.
Installation
To get started with BookMate, follow these steps:

### How to start ?

clone and change directory to docker image
```
git clone https://github.com/Capstone-Asoy/pov-ML
cd capstone_docker
```

if you want to run it locally first build the docker image
```
docker build -t {your account}/{your image name}:{your docker tag} .
```

the run it
```
docker run -d -p 80:8080 -v "$(pwd)/data:data" {your account}/{your image name}:{your docker tag}
```

andyou can access it in localhost:80