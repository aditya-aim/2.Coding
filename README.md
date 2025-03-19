
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

* **app.py :** AI generates a coding problem using a system prompt.
* **app2.py :** Loads coding questions from a JSON file and picks one randomly.

```bash
python app.py
```

---

### ✅ **Python Version**

This project runs on **Python 3.12.7**

---

## 📌 **API Endpoints**

### 1. **Start Interview**

`POST /start`

**Description:**

Starts the coding interview by selecting a random question based on the candidate's role and skill. If no question is found, the AI will generate one.

**Headers:**

| Key   | Type   | Description                   | Required |
| ----- | ------ | ----------------------------- | -------- |
| Role  | String | The job role of the candidate | ✅       |
| Skill | String | The key skill being evaluated | ✅       |

**Request:**

* **Body:** None

**Response:**

* **200 OK**

```json
{
  "message": "Hello! Let's start the coding interview for the role of Backend Developer focusing on Python. Your question is: How would you implement a binary search algorithm?"
}
```

* **400 Bad Request** (Missing role or skill)

```json
{
  "error": "Missing Role or Skill in headers"
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

Allows the candidate to ask for clarification or hints about the coding question. The AI will provide professional guidance without giving direct solutions.

**Request:**

* **Body:**

```json
{
  "input": "Can I use recursion?",
  "code": "def binary_search(arr, target):\n  left, right = 0, len(arr) - 1\n  while left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == target:\n      return mid\n    elif arr[mid] < target:\n      left = mid + 1\n    else:\n      right = mid - 1\n  return -1"
}
```

**Response:**

* **200 OK**

```json
{
  "response": "Yes, recursion is a valid approach. You could try breaking down the problem into smaller parts."
}
```

* **400 Bad Request** (Missing input)

```json
{
  "error": "Input is required"
}
```

* **400 Bad Request** (No active session)

```json
{
  "error": "Interview has not started yet"
}
```

* **400 Bad Request** (Missing code)

```json
{
  "error": "Please attach your code for evaluation and analysis."
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

Submits the candidate's solution for evaluation. The AI will analyze correctness, efficiency, and performance.

**Request:**

* **Body:**

```json
{
  "code": "def binary_search(arr, target):\n  left, right = 0, len(arr) - 1\n  while left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == target:\n      return mid\n    elif arr[mid] < target:\n      left = mid + 1\n    else:\n      right = mid - 1\n  return -1",
  "expected_duration": 10,
  "candidates_duration": 8
}
```

**Response:**

* **200 OK**

```json
{
  "feedback": "The solution is correct. However, you could improve efficiency by handling edge cases explicitly."
}
```

* **400 Bad Request** (Missing code)

```json
{
  "error": "Code is required"
}
```

* **400 Bad Request** (No active session)

```json
{
  "error": "No question has been asked yet"
}
```

* **400 Bad Request** (Missing expected duration)

```json
{
  "error": "expected_duration is required"
}
```

* **400 Bad Request** (Missing candidate's duration)

```json
{
  "error": "candidates_duration is required"
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
curl -X POST http://127.0.0.1:5000/start -H "Role: Backend Developer" -H "Skill: Python"
```

### ✅ Ask for Clarification

```bash
curl -X POST http://127.0.0.1:5000/ask -H "Content-Type: application/json" -d '{
  "input": "Can I use recursion?",
  "code": "def binary_search(arr, target):\n  left, right = 0, len(arr) - 1\n  while left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == target:\n      return mid\n    elif arr[mid] < target:\n      left = mid + 1\n    else:\n      right = mid - 1\n  return -1"
}'
```

### ✅ Submit Code

```bash
curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{
  "code": "def binary_search(arr, target):\n  left, right = 0, len(arr) - 1\n  while left <= right:\n    mid = (left + right) // 2\n    if arr[mid] == target:\n      return mid\n    elif arr[mid] < target:\n      left = mid + 1\n    else:\n      right = mid - 1\n  return -1",
  "expected_duration": 10,
  "candidates_duration": 8
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

## ✅ **Status Codes**

| Status Code | Description                                |
| ----------- | ------------------------------------------ |
| `200`     | Successful request                         |
| `400`     | Bad request (missing input, invalid state) |
| `500`     | Internal server error                      |
