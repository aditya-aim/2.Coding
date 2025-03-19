# AI Coding Interview Platform

A modern web application that conducts AI-powered coding interviews with real-time feedback, code analysis, and text-to-speech capabilities.

## 🌟 Features

- **Interactive Code Editor**: Monaco Editor integration for a professional coding experience
- **AI-Powered Interview**: Dynamic questions based on role and skill selection
- **Real-time Feedback**: Instant analysis of code and responses
- **Text-to-Speech**: AI responses are automatically spoken
- **Multiple Language Support**: Support for Python, JavaScript, Java, C++, and React
- **Role-Based Questions**: Questions tailored to different developer roles
- **Code Analysis**: Detailed feedback on code quality, efficiency, and best practices

## 🛠️ Tech Stack

### Backend
- Python 3.x
- Flask
- LangChain
- OpenAI GPT-4
- SQLAlchemy
- Flask-CORS

### Frontend
- HTML5
- CSS3
- JavaScript
- Monaco Editor
- Web Speech API

## 📋 Prerequisites

- Python 3.x
- OpenAI API Key
- Modern web browser with JavaScript enabled

## 🔧 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Running the Application

1. Start the Flask backend server:
```bash
python app.py
```

2. In a new terminal, start the frontend server:
```bash
cd frontend-html
python -m http.server 8000
```

3. Open your browser and navigate to:
```
http://localhost:8000
```

## 💻 Usage

1. **Start Interview**:
   - Select your role (e.g., Backend Developer)
   - Choose your primary skill (e.g., Python)
   - Click "Start Interview"

2. **During Interview**:
   - Write your code in the Monaco Editor
   - Ask questions using the chat interface
   - AI responses will be automatically spoken
   - Toggle text-to-speech using the speaker icon

3. **Submit Code**:
   - Click "Submit Code" when ready
   - Receive detailed analysis of your solution
   - Get feedback on code quality and efficiency

## 📁 Project Structure

```
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── interview_questions.json  # Interview questions database
├── frontend-html/        # Frontend files
│   ├── index.html       # Main HTML file
│   ├── styles.css       # CSS styles
│   └── script.js        # Frontend JavaScript
└── venv/                # Python virtual environment
```

## 🔒 Security

- API keys are stored in environment variables
- CORS is enabled for local development
- Input validation on both frontend and backend
- Secure password handling in interview questions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Monaco Editor for the code editor
- Flask team for the web framework
- All contributors and users of the platform

## 📞 Support

For support, please open an issue in the repository or contact the maintainers.

## 🔄 Updates

- Regular updates to interview questions
- New features and improvements
- Bug fixes and security patches

---

Made with ❤️ by [Your Name/Organization]

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
