# Tutorial 4 - Written Answers

Name: Rhys Brown

## Results of each request in Postman
| Request  | Status Code | Number of devices after request |
|-------|-----|------------|
| **POST /devices** for the first probe | 201  | 5   |
| **POST /devices** for the second probe    | 201  | 6   |
| **GET /devices/probe**  | 200  | 6 |
| **PUT /devices/attic** for first time  | 200  | 6 |
| **PUT /devices/attic** again for second time | 200  | 6 |
| **DELETE /devices/fridge** for first time | 200  | 5 |
| **DELETE /devices/fridge** for second time | 404  | 5 |

## Sever-side changes from each request

The server remained in the same whether the request was sent once or twice for the DELETE and PUT requests; however, the same was not true for the POST request as the second probe was added after the second request was sent. Idempotency is a property of a web requests where the server is left in the same state if the request is sent once vs multiple times. Therefore, DELETE and PUT requests are idempotent but POST requests are not.