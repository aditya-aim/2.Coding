## 📄 **API Documentation**

**Project:** AI Coding Interviewer

**Framework:** Flask + Langchain + OpenAI

---

## 🚀 **How to Run**

### 1. **Create a Virtual Environment**

```bash
python -m venv venv
```

### 2. **Activate the Virtual Environment**

* **Windows:**

```bash
.\venv\Scripts\activate
```

* **MacOS/Linux:**

```bash
source venv/bin/activate
```

### 3. **Install Requirements**

```bash
pip install -r requirements.txt
```

### 4. **Create `.env` File**

Create a `.env` file in the root directory and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=sk-proj-...
```

### 5. **Run the App**

- **app.py :** AI generates a coding problem using a system prompt.

- **app2.py :** Loads coding questions from a JSON file and picks one randomly.

```bash
python app2.py
```

---

### ✅ **Python Version**

This project runs on **Python 3.12.7**

---

## 📌 **API Endpoints**

### 1. **Start Interview**

`POST /start`

**Description:**

Starts the coding interview by selecting a random question from `interview_questions.json` and initiating the session.

**Request:**

* **Body:** None

**Response:**

* **200 OK**

```json
{
  "message": "Hello! Let's start the coding interview. Your question is: How would you implement a binary search algorithm?"
}
```

* **500 Internal Server Error**

```json
{
  "error": "Error message"
}
```

---

### 2. **Ask Question**

`POST /ask`

**Description:**

Allows the user to ask a question about the coding problem. The AI will clarify the problem without providing a direct solution.

**Request:**

* **Body:**

```json
{
  "input": "Can I use recursion to solve this?"
}
```

**Response:**

* **200 OK**

```json
{
  "response": "Yes, recursion is a valid approach. You can try breaking down the problem into smaller parts."
}
```

* **400 Bad Request**

```json
{
  "error": "Input is required"
}
```

* **400 Bad Request** (if interview not started)

```json
{
  "error": "Interview has not started yet"
}
```

* **500 Internal Server Error**

```json
{
  "error": "Error message"
}
```

---

### 3. **Submit Code**

`POST /submit`

**Description:**

Submits the user's solution. The AI will evaluate the code for correctness, efficiency, and edge cases.

**Request:**

* **Body:**

```json
{
  "code": "def binary_search(arr, target):\n  left, right = 0, len(arr) - 1\n  while left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == target:\n      return mid\n    elif arr[mid] < target:\n      left = mid + 1\n    else:\n      right = mid - 1\n  return -1"
}
```

**Response:**

* **200 OK**

```json
{
  "feedback": "The solution is correct. However, you could improve efficiency by handling edge cases explicitly."
}
```

* **400 Bad Request**

```json
{
  "error": "Code is required"
}
```

* **400 Bad Request** (if interview not started)

```json
{
  "error": "No question has been asked yet"
}
```

* **500 Internal Server Error**

```json
{
  "error": "Error message"
}
```

---

### 4. **End Interview**

`POST /end`

**Description:**

Ends the interview session and saves the conversation to `coding_session_log.txt`.

**Request:**

* **Body:** None

**Response:**

* **200 OK**

```json
{
  "message": "Session ended. Log saved to 'coding_session_log.txt'"
}
```

* **500 Internal Server Error**

```json
{
  "error": "Error message"
}
```

---

## 🖥️ **Example Curl Commands**

### ✅ Start Interview

```bash
curl -X POST http://127.0.0.1:5000/start
```

### ✅ Ask for Clarification

```bash
curl -X POST http://127.0.0.1:5000/ask -H "Content-Type: application/json" -d '{
  "input": "Can I use recursion?"
}'
```

### ✅ Submit Code

```bash
curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{
  "code": "def binary_search(arr, target):\n  left, right = 0, len(arr) - 1\n  while left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == target:\n      return mid\n    elif arr[mid] < target:\n      left = mid + 1\n    else:\n      right = mid - 1\n  return -1"
}'
```

### ✅ End Interview

```bash
curl -X POST http://127.0.0.1:5000/end
```

---

## 📁 **Files**

| File Name                    | Description                                       |
| ---------------------------- | ------------------------------------------------- |
| `app.py`                   | Flask app with endpoints for the coding interview |
| `requirements.txt`         | Project dependencies                              |
| `interview_questions.json` | JSON file with coding questions                   |
| `coding_session_log.txt`   | Logs of the interview session                     |
| `.env`                     | Contains the OpenAI API key                       |

---

## 💡 **Notes**

* The AI will provide clarifications and hints but  **NOT direct solutions** .
* Make sure the `OPENAI_API_KEY` is set correctly in the `.env` file.
* The coding session log is saved to `coding_session_log.txt` after the interview ends.

---

### ✅ **Status Codes**

| Status Code | Description                                |
| ----------- | ------------------------------------------ |
| `200`     | Successful request                         |
| `400`     | Bad request (missing input, invalid state) |
| `500`     | Internal server error                      |
