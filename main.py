import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from google.adk.agents import Agent 

# Load environment variables from your .env file
load_dotenv()

app = Flask(__name__)

# 1. Define the Agent's Core Instructions
SYSTEM_PROMPT = """
You are the PhishGuard Zero-Trust text analyzer. 
Your only job is to analyze incoming messages for social engineering tactics, urgency triggers, and phishing attempts.
You must return ONLY a valid JSON object with no markdown formatting. The JSON must contain exactly two keys:
1. "Threat_Level": Choose "Low", "Medium", or "High".
2. "Red_Flag_Summary": A one-sentence explanation of the psychological manipulation used (or "No obvious manipulation detected" if safe).
"""

# 2. Initialize the ADK Agent
agent = Agent(
    name="phishguard_api_agent",
    model="gemini-2.5-flash",
    instruction=SYSTEM_PROMPT
)

# 3. Define the Web Endpoint
@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Ensure the incoming request contains JSON data
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request. Please provide a JSON payload with a 'message' key."}), 400
    
    user_message = data['message']
    
    try:
        # Pass the message to the AI agent
        ai_response = agent.run(user_message)
        
        # Clean the response to ensure it is strict JSON (removing potential ```json tags)
        clean_text = ai_response.text.strip().strip('```json').strip('```')
        result_dict = json.loads(clean_text)
        
        # Send the analysis back to the user
        return jsonify(result_dict), 200

    except Exception as e:
        return jsonify({"error": f"Failed to process the message: {str(e)}"}), 500

# 4. Run the Server
if __name__ == '__main__':
    # Cloud Run requires binding to 0.0.0.0 and defaults to port 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)