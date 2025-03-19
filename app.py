import random
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load questions from JSON file
with open('interview_questions.json', 'r') as file:
    questions = json.load(file)["questions"]

# Initialize GPT-4o model
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    openai_api_key=api_key
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
@app.route('/start', methods=['POST', 'OPTIONS'])
def start_interview():
    if request.method == 'OPTIONS':
        return '', 200

    global current_question

    try:
        # ✅ Get Role and Skill from Headers
        role = request.headers.get('Role')
        skill = request.headers.get('Skill')

        if not role or not skill:
            return jsonify({"error": "Missing Role or Skill in headers"}), 400

        # ✅ Filter questions based on Role and Skill
        filtered_questions = [
            q for q in questions if q["role"].lower() == role.lower() and skill.lower() in [s.lower() for s in q["skills"]]
        ]

        if filtered_questions:
            # ✅ Select a random question from the filtered list
            current_question = random.choice(filtered_questions)["question"]
        else:
            # ✅ If no questions are found, generate one using LLM
            prompt = f"""
            You are an expert AI interviewer. Generate a challenging coding question for a {role} position 
            that requires expertise in {skill}. The question should be clear, concise, and relevant to the skill.
            """
            current_question = conversation.predict(input=prompt)

        # ✅ SYSTEM PROMPT: Start the interview and present the question
        initial_prompt = f"""
        You are an AI interviewer. Start the coding interview session.
        - Greet the candidate.
        - Mention the role: **{role}**
        - Mention the key skill: **{skill}**
        - Present the following coding question:
        - Do not add extra details to the question by your own
        
        **Question:** {current_question}
        """

        # ✅ Get response from LLM
        response = conversation.predict(input=initial_prompt)
        return jsonify({"message": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route 2: Ask Clarification (No direct answers)
@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.json
        user_input = data.get('input')
        user_code = data.get('code')

        if not user_input:
            return jsonify({"error": "Input is required"}), 400

        if not current_question:
            return jsonify({"error": "Interview has not started yet"}), 400

        if not user_code:
            return jsonify({"error": "Please attach your code for evaluation and analysis."}), 400


        # SYSTEM PROMPT: Help with clarifying the question, not solving it
        clarification_prompt = f"""
        You are an AI coding interviewer. The candidate has submitted the following solution for the coding question:

        **Question:** {current_question}  
        **Candidate's Query:** {user_input}  
        **Submitted Code:**\n{user_code}

        Your task:
        1. **AI-Powered Hints & Explanations:**  
            - Provide hints or explanations if the candidate is stuck.  
            - Offer guidance to help the candidate understand the problem better without giving the solution directly.  
            - Keep your responses clear and professional without stating that you are giving a hint.  

        2. **Performance Analytics:**  
            - Analyze the code's **accuracy** and **efficiency**.  
            - Provide insights into how the code performs under different input sizes.  
            - Highlight potential bottlenecks or inefficiencies.  

        3. **Code Complexity Analysis:**  
            - Analyze the time complexity and space complexity in **Big-O notation**.  
            - If possible, suggest how to improve the complexity.  
            - Ensure the complexity analysis is accurate and easy to understand.  

        4. **Feedback:**  
            - Provide feedback on the solution.  
            - Highlight strengths, such as clean code, edge cases handled, and algorithmic approach.  
            - Point out areas for improvement, including performance, edge cases, and coding style.  
            - Keep the tone professional and supportive.  

        5. **Debugging Assistance:**  
            - Identify and explain any **syntax errors** or **logical errors** in the code.  
            - Suggest how to fix the issues without providing direct code solutions.  
            - Offer practical debugging strategies to help the candidate troubleshoot their code effectively.  

        **Rules:**  
        - Do **NOT** solve the coding problem directly.  
        - Avoid speculative or ambiguous responses.  
        - Keep responses straightforward, precise, and actionable.
        - Include less details in your response
        - Your response should be a direct answer to Candidate's Query 
        - Also be clear that you are not here to tell Candidate that code is according to Question or not
        your job is to assist pretending your dont know the answer and the final analysis report based on the questions goal will be
        given on clicking on submit button at the end of the interview 
        """


        response = conversation.predict(input=clarification_prompt)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Route 3: Submit Code for Evaluation
@app.route('/submit', methods=['POST', 'OPTIONS'])
def submit_code():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.json
        code = data.get('code')
        expected_duration = data.get('expected_duration') 
        candidates_duration = data.get('candidates_duration') 

        if not code:
            return jsonify({"error": "Code is required"}), 400

        if not current_question:
            return jsonify({"error": "No question has been asked yet"}), 400
        
        if expected_duration is None:
            return jsonify({"error": "expected_duration is required"}), 400
        
        if candidates_duration is None:
            return jsonify({"error": "candidates_duration is required"}), 400


        evaluation_prompt = f"""
        You are an AI coding interviewer. The candidate has submitted the following solution for the question:

        **Question:** {current_question}  
        **Submitted Code:**\n{code}  
        **Time Taken:** {candidates_duration} minutes  
        **Expected Duration:** {expected_duration} minutes  

        ### 🔍 **Your Task:**
        You are tasked with generating a detailed **performance report** based on the submitted solution. 
        You have to be careful that the Submitted Code is solving the Question
        Your report should cover the following aspects:

        1. **Code Quality,Efficiency and style:**  
        - Evaluate the overall quality of the code — is it clean, well-structured, and readable?  
        - Analyze the time and space complexity of the code in **Big-O notation**.  
        - Assess the efficiency of the solution and whether it meets industry standards.  
        - Also Assess the coding style of the candidate

        2. **Accuracy and Correctness:**  
        - Does the code solve the problem correctly?  
        - Are edge cases and boundary conditions handled properly?  
        - Highlight any potential logical flaws or missed cases.  

        3. **Performance Analysis:**  
        - Compare the time taken by the candidate with the expected duration:  
            - If the candidate finished too quickly, assess whether they may have overlooked edge cases or used shortcuts.  
            - If they took too long, identify potential inefficiencies or overcomplications.  

        4. **Strengths and Weaknesses:**  
        - Highlight what the candidate did well (e.g., clear logic, handling edge cases, good coding practices).  
        - Point out areas for improvement (e.g., better algorithm choice, cleaner code, improved complexity).  

        5. **Final Performance Summary:**  
        - Provide an overall assessment of the candidate's performance based on their coding style, efficiency, accuracy, and problem-solving approach.  
        - Offer professional, clear, and actionable feedback to help the candidate improve.  

        ### 🚫 **Rules:**  
        - Do **NOT** execute the code.  
        - Keep the report objective and professional — avoid overly harsh or overly positive language.  
        - Focus on factual, actionable insights rather than vague statements.  
        """

        response = conversation.predict(input=evaluation_prompt)
        return jsonify({"feedback": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Route 4: End the Interview
@app.route('/end', methods=['POST', 'OPTIONS'])
def end_interview():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        with open("coding_session_log.txt", "w", encoding="utf-8") as file:
            file.write(memory.load_memory_variables({})['history'])

        # Clear the conversation memory
        memory.clear()
        return jsonify({"message": "Session ended. Log saved to 'coding_session_log.txt'"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
