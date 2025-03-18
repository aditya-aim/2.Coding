from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Initialize GPT-4o model
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-4o"
)

# Initialize Conversation Memory
memory = ConversationBufferMemory()

# Initialize Conversation Chain with Memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Generate coding question on start
@app.route('/start', methods=['POST'])
def start():
    try:
        initial_prompt = """
        You are an AI coding interviewer. Generate a coding problem for the user.
        The user will write code to solve the problem.
        If the user asks questions, help with debugging and clarification, but DO NOT give the solution directly.
        Start by greeting and generating a coding question.
        The question that you asked,the coe should be relevant to that
        """
        # Start the conversation
        response = conversation.predict(input=initial_prompt)
        return jsonify({"question": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User asks questions or sends partial code
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_input = data.get('input')
        
        if not user_input:
            return jsonify({"error": "Input is required"}), 400
        
        prompt = f"""
        The user is working on the coding problem you generated.
        They have asked the following question or shared partial code:
        {user_input}
        
        DO NOT give the solution directly.
        Only help with debugging, clarifications, or hints.
        """
        response = conversation.predict(input=prompt)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User submits the complete code
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        final_code = data.get('code')
        
        if not final_code:
            return jsonify({"error": "Code is required"}), 400
        
        prompt = f"""
        The user has submitted the following code:
        ```python
        {final_code}
        ```

        Provide constructive feedback on the code.
        Check for correctness, efficiency, edge cases, and suggest improvements.
        """
        response = conversation.predict(input=prompt)
        return jsonify({"feedback": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Save the conversation and end the session
@app.route('/end', methods=['POST'])
def end():
    try:
        # Save the conversation
        with open("coding_session_log.txt", "w", encoding="utf-8") as file:
            file.write(memory.load_memory_variables({})['history'])
        
        return jsonify({"message": "Session ended. Log saved to 'coding_session_log.txt'"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
