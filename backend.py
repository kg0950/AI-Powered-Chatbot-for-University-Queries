from flask import Flask, request, jsonify
import openai
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Database connection
conn = psycopg2.connect(
    database="university_chatbot",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS query_logs (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255),
        question TEXT,
        answer TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get("user_id", "guest")
    question = data.get("message", "")
    
    if not question:
        return jsonify({"error": "Empty message"}), 400
    
    # Get AI-generated response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful university chatbot."},
                  {"role": "user", "content": question}]
    )
    answer = response["choices"][0]["message"]["content"]
    
    # Store in DB
    cursor.execute("INSERT INTO query_logs (user_id, question, answer) VALUES (%s, %s, %s)",
                   (user_id, question, answer))
    conn.commit()
    
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(debug=True)
