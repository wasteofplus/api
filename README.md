# wasteof.plus api

This is the API (application programming interface) that powers wasteof.plus, the browser extension for the wasteof.money social media.

# API Docs

## Base URL

The base url for all API endpoints is: `https://wasteofplus.radi8.dev`.

## Authentication

Most requests should be authenticated. When authenticating, send two parameters, `token`, being your wasteof2 API token, and `username`, your wasteof.money username. All tokens are discared after use and are never stored, as we care about privacy of your account. The only use of tokens is so we can verify who you are.

## Endpoints

### Polls
#### `POST /polls/create`

Creates a poll.

**Request**

```http
POST /polls/create HTTP/1.1
Host: wasteofplus.radi8.dev
Content-Type: application/json

{
    "username": str, # Your wasteof.money username
    "token": str # Your wasteof2 API token
    "postID": str # The post you would like to create a poll for
    "polloptions": str # A list of poll options seperated by commas (eg. bananas,apples,kiwis)
}
```

**Responses**

For poll creation success:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "ok": "poll created",
  "_id_": "63cdfb95040f988e1c71cc32" # The ID of the created poll
}
```

For poll creation failure, when post is not found:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "post not found",
}
```

For poll creation failure, when not authorized:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "not authorized",
}
```

For poll creation failure, when poll with post ID already created:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": "poll with post ID already created",
}
```

#### `GET /polls/get/{pollID}`

Get a poll by poll ID.

**Request**

```http
GET /polls/get/{pollID} HTTP/1.1
Host: wasteofplus.radi8.dev
```

**Responses**

For success on retrieving poll:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "postID": "63cdfb95040f988e1c71cc32",
  "user": "6185cd269dd808c2c76fa070",
  "options": [
    "apple",
    "banana",
    "dadaasdasds"
  ],
  # Each key will contain a list of users by ID that voted for that option
  "votes": { 
    "apple": [
      "6185cd269dd808c2c76fa070"
    ],
    "banana": [],
    "dadaasdasds": []
}
```

For failure, when poll is not found:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "poll not found",
}
```

#### `GET /polls/get/post/{postID}`

Get a poll by post ID.

**Request**

```http
GET /polls/get/post/{postID} HTTP/1.1
Host: wasteofplus.radi8.dev
```

**Responses**

For success on retrieving poll:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "postID": "63cdfb95040f988e1c71cc32",
  "user": "6185cd269dd808c2c76fa070",
  "options": [
    "apple",
    "banana",
    "dadaasdasds"
  ],
  # Each key will contain a list of users by ID that voted for that option
  "votes": { 
    "apple": [
      "6185cd269dd808c2c76fa070"
    ],
    "banana": [],
    "dadaasdasds": []
}
```

For failure, when poll is not found:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "poll not found",
}
```

#### `PUT /polls/vote/{pollID}`

Votes on a poll.

**Request**

```http
GET /polls/vote/{pollID} HTTP/1.1
Host: wasteofplus.radi8.dev
Content-Type: application/json

{
    "username": str, # Your wasteof.money username
    "token": str # Your wasteof2 API token
    "pollID": str # The poll you would like to vote on
    "pollOption": str # The poll option you would like to vote
}
```

**Responses**

For voting success:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "ok": "voted",
}
```

For voting failure, when you have already voted:

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "error": "already voted",
}
```

For voting failure, when option not found:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "option not found",
}
```

For voting failure, when poll not found:

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "error": "poll not found",
}
```

For voting failure, when not authorized:

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "not authorized",
}
```

### Reactions

#### `POST /reactions/react`

Reacts to a post. (Or remove a reaction)

**Request**

```http
GET /reactions/react HTTP/1.1
Host: wasteofplus.radi8.dev
Content-Type: application/json

{
    "username": str, # Your wasteof.money username
    "token": str # Your wasteof2 API token
    "pollID": str # The post you would like to react to
    "emoji": str # The emoji you are reacting with (or removing)
}
```

**Responses**

For voting success:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "ok": "added reaction",
}

# Another response could also be:

{
  "ok": "removed reaction" # If a reaction is being removed
}
```

For reaction failure, when emoji is not allowed:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "reaction not allowed",
}
```

For reaction failure, when the post you want to react to is not found:

```http
HTTP/1.1 409 Unauthorized
Content-Type: application/json

{
  "error": "post not found",
}
```