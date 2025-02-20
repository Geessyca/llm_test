from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import sys
import os
import logging


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model import TestingGenerator
from database import Database

load_dotenv()


HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")

database = Database(host=HOST,
                    user=USER,
                    password=PASSWORD,
                    database=DATABASE,
                    port=PORT)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
AUDIO_TRANSCRIBER = os.getenv("AUDIO_TRANSCRIBER")

model = TestingGenerator(api_key = OPENAI_API_KEY,
                         llm_model = LLM_MODEL)

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler() 
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "methods": ["POST", "OPTIONS"]}})

@app.route('/api/code', methods=['POST'])
def upload_text():
    logger.info("Received request to upload code.")

    data = request.get_json()
    if not data or 'code' not in data:
        logger.warning("No code provided in the request.")
        return jsonify({"error": "No code provided"}), 400

    code = data['code']
    if not code.strip():
        logger.warning("Code cannot be empty.")
        return jsonify({"error": "Code cannot be empty"}), 400

    logger.info("Text received and returned successfully.")
    llm_response=model.generate(code)
    code_id = database.insert_data(code, llm_response)
    return jsonify({"testing": str(llm_response), "id_response": code_id})

@app.route('/api/feedback', methods=['POST'])
def upload_feedback():
    logger.info("Received request to upload code.")

    data = request.get_json()
    if not data or 'code_id' not in data or 'feedback' not in data:
        logger.warning("No body provided in the request.")
        return jsonify({"error": "No body provided"}), 400

    code_id = data['code_id']
    feedback = data['feedback']
    if not code_id or not feedback:
        logger.warning("Code cannot be empty.")
        return jsonify({"error": "Code cannot be empty"}), 400

    logger.info("Text received and returned successfully.")
    db_response=database.update_feedback(code_id,feedback)
    return jsonify({"response": str(db_response)})


if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
