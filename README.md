# Vocabulary App
- Vocabulary-app is a web application developed to help users remember 
English words by adding them to their own personalized dictionary and then 
practicing them through repetition.
- The app allows users to register accounts, log in, add words to their 
  dictionary, view their entire word collection, edit and delete words, and 
  mark words that will be accessed for repetition. The app's main functionality is the word repetition feature, which displays English words and prompts users to enter their Ukrainian translations.
## Tech stack
Backend: Python, FastAPI, SQLAlchemy, websockets \
DB: PostgreSQL \
Frontend: JavaScript, React, HTML, CSS
## Installation
1. Clone the repository using the command:
```
git clone https://github.com/K1SKEE/vocabulary-app
```
2. Navigate to the cloned repository using the command:
```
cd vocabulary-app
```
3. Start the application using Docker Compose:
```
docker-compose up
```
4. In new terminal tab check the backend container ID for the running 
   application:
```
docker ps
```
5. Enter the backend container's shell using the following command, replacing 
   `<backend_container_id>` with the actual ID from the previous step:
```
docker exec -it <backend_container_id> bash
```
6. Apply database migrations using Alembic:
```
alembic upgrade heads
```
7. Exit the container's shell using the command:
```
exit
```
## Usage
To start the application in the future, simply run the command:
```
docker-compose up
```
