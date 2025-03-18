import random
import json
from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load questions from JSON file
with open('interview_questions.json', 'r') as file:
    questions = json.load(file)["questions"]

# Initialize GPT-4o model
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-4o"
)
# Initialize Conversation Memory
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

current_question = None


# ✅ Route 1: Start the Interview
@app.route('/start', methods=['POST'])
def start_interview():
    global current_question

    try:
        # Select a random question
        current_question = random.choice(questions)["question"]

        # SYSTEM PROMPT: Greet the user and present the question
        initial_prompt = f"""
        You are an AI interviewer. Start the coding interview session.
        - Greet the candidate.
        - Present the following coding question:
        
        **Question:** {current_question}
        """

        # Get response from LLM
        response = conversation.predict(input=initial_prompt)
        return jsonify({"message": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route 2: Ask Clarification (No direct answers)
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_input = data.get('input')

        if not user_input:
            return jsonify({"error": "Input is required"}), 400

        if not current_question:
            return jsonify({"error": "Interview has not started yet"}), 400

        # SYSTEM PROMPT: Help with clarifying the question, not solving it
        clarification_prompt = f"""
        You are an AI coding interviewer. The candidate has asked the following question about the coding problem:
        
        **Question:** {current_question}
        **Candidate's Query:** {user_input}
        
        Your task:
        - DO NOT answer the coding question directly.
        - Only help the candidate clarify the problem or provide hints if needed.
        - dont say i am here to clarify and all...you respond to what asked.
        """

        response = conversation.predict(input=clarification_prompt)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route 3: Submit Code for Evaluation
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        code = data.get('code')

        if not code:
            return jsonify({"error": "Code is required"}), 400

        if not current_question:
            return jsonify({"error": "No question has been asked yet"}), 400

        # SYSTEM PROMPT: Evaluate the submitted code
        evaluation_prompt = f"""
        You are an AI coding interviewer. The candidate has submitted the following solution for the question:
        
        **Question:** {current_question}
        **Submitted Code:**\n{code}
        
        Your task:
        - Evaluate the submitted code.
        - Provide detailed feedback, including strengths and areas for improvement.
        - Do NOT execute the code.
        """

        response = conversation.predict(input=evaluation_prompt)
        return jsonify({"feedback": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route 4: End the Interview
@app.route('/end', methods=['POST'])
def end_interview():
    try:
        with open("coding_session_log.txt", "w", encoding="utf-8") as file:
            file.write(memory.load_memory_variables({})['history'])

        return jsonify({"message": "Session ended. Log saved to 'coding_session_log.txt'"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
