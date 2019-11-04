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
 - 400: Bad Request
 - 404: Resource Not Found
 - 422: Not Processable
 - 405: Method Not Allowed

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

- If there are no questions in the database for the requested page, a `404` error response
  will be returned. Checkout the section on error handling above for the structure of the response.