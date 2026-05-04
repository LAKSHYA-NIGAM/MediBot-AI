from flask import Flask, render_template, jsonify, request, session
from src.helper import download_hugging_face_embeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
from auth import auth_bp, init_db, login_required, save_chat_message, get_chat_history
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from PIL import Image
import os
import io
import base64

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Register auth blueprint
app.register_blueprint(auth_bp)

# Initialize database
init_db()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai_client = genai.Client(api_key=GOOGLE_API_KEY) if GOOGLE_API_KEY else None

# Load embeddings and connect to ChromaDB
embeddings = download_hugging_face_embeddings()
CHROMA_DB_DIR = "./chroma_db"

docsearch = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings,
    collection_name="medical-chatbot"
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Use Gemini (fast, free tier)
chatModel = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    google_api_key=GOOGLE_API_KEY
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@login_required
def index():
    history = get_chat_history(session['user_id'])
    return render_template('chat.html', username=session.get('username'), chat_history=history)


@app.route("/get", methods=["GET", "POST"])
@login_required
def chat():
    msg = request.form.get("msg", "")
    if not msg.strip():
        return "Please enter a message."

    user_id = session['user_id']
    save_chat_message(user_id, "user", msg)

    try:
        response = rag_chain.invoke({"input": msg})
        answer = response["answer"]
    except Exception as e:
        answer = f"I'm sorry, I encountered an error. Please try again. ({str(e)[:100]})"

    save_chat_message(user_id, "bot", answer)
    return str(answer)


@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    msg = request.form.get("msg", "Analyze this file")

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Use PDF, images, or text files."}), 400

    ext = file.filename.rsplit('.', 1)[1].lower()
    user_id = session['user_id']

    try:
        if ext == 'pdf':
            file_bytes = file.read()
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            text = text[:3000]
            combined_query = f"Based on this document content: {text[:2000]}\n\nUser question: {msg}"
            save_chat_message(user_id, "user", f"[Uploaded PDF: {file.filename}] {msg}")
            response = rag_chain.invoke({"input": combined_query})
            answer = response["answer"]

        elif ext in {'png', 'jpg', 'jpeg', 'gif', 'webp'}:
            file_bytes = file.read()
            image = Image.open(io.BytesIO(file_bytes))
            # Use google.genai (new API) for vision
            if genai_client:
                vision_response = genai_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        f"You are a medical AI assistant. {msg}. Analyze this image from a medical perspective. "
                        "Provide helpful information but remind the user to consult a healthcare professional.",
                        image
                    ]
                )
                answer = vision_response.text
            else:
                answer = "Image analysis requires a valid GOOGLE_API_KEY in your .env file."
            save_chat_message(user_id, "user", f"[Uploaded Image: {file.filename}] {msg}")

        elif ext == 'txt':
            text = file.read().decode('utf-8', errors='ignore')[:3000]
            combined_query = f"Based on this text: {text[:2000]}\n\nUser question: {msg}"
            save_chat_message(user_id, "user", f"[Uploaded Text: {file.filename}] {msg}")
            response = rag_chain.invoke({"input": combined_query})
            answer = response["answer"]
        else:
            answer = "Unsupported file type."

    except Exception as e:
        answer = f"Error processing file: {str(e)[:200]}"

    save_chat_message(user_id, "bot", answer)
    return jsonify({"answer": answer})


@app.route("/history")
@login_required
def history():
    msgs = get_chat_history(session['user_id'])
    return jsonify(msgs)


@app.route("/clear_history", methods=["POST"])
@login_required
def clear_history():
    from auth import get_db
    conn = get_db()
    conn.execute('DELETE FROM chat_history WHERE user_id = ?', (session['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
