# Test Results

**Store Name:** Pet Store
**Author:** Ibrahim Nasr
**Total Passed:** 0
**Total Failed:** 6

## Summary
- **Total Test Cases Executed:** 6
- **Passed:** 0
- **Failed:** 6

### Don't worry, it's just testing!
It's not about how many times you fail, but how many times you get up! 🎉

## Detailed Results
### Test Case: **Test Case: Happy Path for GET https://petstore.swagger.io/v2/user/login**

**Request:**

**Endpoint:** https://petstore.swagger.io/v2/user/login
**Method:** GET
**Query Parameters:**
* username: test_user
* password: 12345

**Expected Response:**

**Status Code:** 200 OK
**Response Body:**
```json
{
  "code": 200,
  "type": "unknown",
  "message": "ok"
}
```

**Validation Steps:**

1. Assert that the status code is 200 OK.
2. Verify that the response body contains the "code" field with a value of 200.
3. Check that the response body includes the "type" field with a value of "unknown".
4. Ensure that the response body has a "message" field with a value of "ok".
- **Status:** FAILED
- **Error:** No error details available

### Test Case: **Test Case:**

**API Endpoint:** GET https://petstore.swagger.io/v2/user/login

**Request:**

**Method:** GET

**Query Parameters:**

* username: **invalid_username**
* password: **invalid_password**

**Expected Response:**

**Status Code:** 400 (Bad Request)

**Response Body:**

```json
{
  "code": 400,
  "message": "Invalid username/password supplied"
}
```
- **Status:** FAILED
- **Error:** No error details available

### Test Case: **Test Case for GET https://petstore.swagger.io/v2/pet/findByStatus**

**Mandatory Parameters:**

| Name | Location | Type | Description |
|---|---|---|---|
| status | query | array | Status values that need to be considered for filter |

**Request Payload:**

```json
{
  "status": [
    "available",
    "pending",
    "sold"
  ]
}
```

**Expected Response:**

```json
[
  {
    "id": 1,
    "category": {
      "id": 1,
      "name": "Dogs"
    },
    "name": "Doggie",
    "photoUrls": [
      "string"
    ],
    "tags": [
      {
        "id": 1,
        "name": "tag1"
      },
      {
        "id": 2,
        "name": "tag2"
      }
    ],
    "status": "available"
  },
  {
    "id": 2,
    "category": {
      "id": 1,
      "name": "Dogs"
    },
    "name": "Fluffy",
    "photoUrls": [
      "string"
    ],
    "tags": [
      {
        "id": 1,
        "name": "tag1"
      }
    ],
    "status": "sold"
  }
]
```

**Test Steps:**

1. Send a GET request to https://petstore.swagger.io/v2/pet/findByStatus with the following parameters in the query string:
   - status: available,pending,sold
2. Verify that the response status code is 200.
3. Verify that the response body matches the expected response.
- **Status:** FAILED
- **Error:** No error details available

### Test Case: **Test Case:** GET https://petstore.swagger.io/v2/pet/findByStatus with Invalid Value for 'status' Query Parameter

**Description:** This test case verifies the error path when an invalid value is provided for the `status` query parameter.

**Request:**

```
GET https://petstore.swagger.io/v2/pet/findByStatus?status=invalid_status
```

**Expected Response:**

* **Status Code:** 400 Bad Request
* **Response Body:**
```json
{
  "code": 400,
  "message": "Invalid status value"
}
```
- **Status:** FAILED
- **Error:** No error details available

### Test Case: **Test Case:**

**Test Case ID:** GET_Store_Inventory_001

**Test Case Name:** Verify GET https://petstore.swagger.io/v2/store/inventory

**Test Objective:** To verify that the GET https://petstore.swagger.io/v2/store/inventory endpoint is functioning as expected and returns the inventory of the store.

**Pre-Conditions:**

* The Petstore API is up and running.

**Test Procedure:**

1. **Request:**
   * **URL:** https://petstore.swagger.io/v2/store/inventory
   * **Method:** GET

2. **Expected Response:**
   * **Status Code:** 200 OK
   * **Response Body:** A JSON object with the following properties:
     * `id` (integer): the id of the pet
     * `name` (string): the name of the pet
     * `photoUrls` (array of strings): the photo URLs of the pet
     * `tags` (array of objects): the tags associated with the pet
     * `status` (string): the status of the pet

**Expected Results:**

* The API returns the inventory of the store in the expected JSON format.

**Post-Conditions:**

* The Petstore API is still running.
- **Status:** FAILED
- **Error:** No error details available

### Test Case: **Test Case for Error Path of GET https://petstore.swagger.io/v2/store/inventory**

**Request:**

* **Method:** GET
* **URL:** https://petstore.swagger.io/v2/store/inventory
* **Parameters:** None

**Expected Response:**

* **Status Code:** 500 (Internal Server Error)
* **Response Body:** An error message indicating that the server encountered an unexpected condition that prevented it from fulfilling the request.
* **Response Headers:**
    * **Content-Type:** application/json

**Test Case Details:**

**Purpose:**
To verify that the API returns an error when an unexpected server-side condition occurs during the execution of the request.

**Assumptions:**
* The server is experiencing an issue that prevents it from processing the request.

**Steps:**

1. Send a GET request to the API endpoint with no parameters.
2. Verify that the response status code is 500.
3. Examine the response body to confirm that it contains an error message.
4. Inspect the response headers to ensure that the Content-Type is set to application/json.
- **Status:** FAILED
- **Error:** No error details available

## Test Case Results Pie Chart
![Test Case Results](test_case_results_pie_chart.png)
---
Generated on: 2024-10-20 01:44:53
