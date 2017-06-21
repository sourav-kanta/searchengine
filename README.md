Created a django app and added Koushik's crawler in it without any modifications.

Steps to run :

Set up elasticsearch and MongoDB.
I am using mongo-connector module to sync the two. Its very easy just refer too the link that I and Koushik shared previously.

then do      

    cd elasticsearch   
    python manage.py runserver 0.0.0.0:8000

Then open http://localhost:8000 in your browser
