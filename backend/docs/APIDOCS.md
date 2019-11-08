# API Reference Document

## Introduction

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game. This API forms the backend of that 
application.

## Getting Started
- Base url: This API is not currently hosted byt can be accessed in a local environment on the following url.
```
http://localhost:5000/api/v1
```
- The API in its current version does not use any authentication mechanisms.
 
 ## Error Handling
 Errors are returned as JSON objects in the following format:
 ```
 {
    "success": False,
    "error": 404,
    "message": "resource not found"
 }
 ```
 The API will return the following error types when requests fail:
 - 400: bad request
 - 404: resource not found
 - 422: unable to process request 
 - 405: method not allowed

## Resource endpoint library
```
GET /questions
```
- General
     - Returns a list of question objects, success value, total number of questions
    in the database, a list of category objects and the value of the current category
    - Results are paginated in groups of 10 by default. Include a **page** request argument to choose
    a page number, starting from 1. If no argument is supplied the default page is page 1.
    - You can also optionally specify a **limit** request argument to change the number or returned questions
    in the pagination group.

- Request Arguments: 
    - `page` integer [optional - defaults to 1]
    - `limit` integer [optional - defaults to 10]

- Sample: ``` curl http://localhost:5000/api/v1/questions?page=2&limit=3 ```
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
- Response Codes
  - success: 200
  - error: 404
- If there are no questions in the database for the requested page, a `404` error response
  will be returned. Checkout the section on error handling above for the structure of the response.

```
POST /questions
```
- General
     - Takes a json object contaning question, answer, difficulty and category values as the request
       body.
     - These fields are all `required`. A 400 error response is returned if there are any validation errors in these fields and if any is missing. 

- Request Arguments: 
    - None
- Request Body:
  ```
    {
        'question': 'Which is the longest river in Africa?',
        'answer': 'River Nile',
        'difficulty': 2,
        'category': 3
    }
  ```

- Sample: `curl -X POST http://localhost:5000/api/v1/questions -d' {"question": "Which is the longest river in Africa?", "answer": "River Nile", "category": 3, "difficulty": 2}' -H "Content-Type: application/json"`
```
{
  "data": {
    "answer": "River Nile", 
    "category": 3, 
    "difficulty": 2, 
    "id": 25, 
    "question": "Which is the longest river in Africa?"
  }, 
  "success": true
}
```
- Response Codes
  - success: 201
  - error: 400 


```
DELETE /questions/<int:id>
```
- General
     - deletes the question with the given ID from the database.
     - returns a 422 error response if a question with the ID
       supplied is not found in the database.
     - returns a 404 error response if the ID supplied is not an integer.

- Request Arguments: 
    - None

- Sample: `curl -X DELETE http://localhost:5000/api/v1/questions/21`
```
{
  "message": "Question with ID: 21 deleted", 
  "success": true
}
```
- Response Codes
  - success: 200
  - error: 422, 404  


```
GET /categories
```
- General
  - Returns a list of category objects and a success value.
- Request Arguments
  - No arguments
- Sample: `curl http://localhost:5000/api/v1/categories`

```                                                                                                                  
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
```
- Response Codes
  - success: 200
  - error: 404
- If there are no categories in the database, a `404` error response will be returned. Checkout the section on error handling above for the structure of the response.

```
GET /categories/<int:id>/questions
```
- General
  - Returns a list of question objects, a success value, the current category object and the total
    number of questions for the category with the given **id**
  - Results are paginated in groups of 10 by default. Include a **page** request argument to choose
    a page number, starting from 1. If no argument is supplied the default page is page 1.
    - You can also optionally specify a **limit** request argument to change the number or returned questions
    in the pagination group.

- Request Arguments: 
    - `page` integer [optional - defaults to 1]
    - `limit` integer [optional - defaults to 10]

- Sample: `curl http://localhost:5000/api/v1/categories/1/questions?page=1&limit=2`

```                                                                                                                  
{
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```
- Response Codes
  - success: 200
  - error: 404
- If there are no categories in the database with the supplied ID, a `404` error response will be returned. Checkout the section on error handling above for the structure of the response.