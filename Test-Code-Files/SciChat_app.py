import os
import atexit
from flask import Flask, render_template, request, jsonify
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
import pinecone

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

llm = Ollama(model="mistral")
lang_llm = Ollama(model="mistral", verbose=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
PINECONE_API_KEY = "<PINECONE-KEY>"
PINECONE_API_ENV = "<PINECONE-ENV-NAME>"
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
INDEX_NAME = "scichat"

def pdf_embedding():
    file = open("./embed-file-list.txt", "r+")
    text = file.read().splitlines()
    file.close()

    file_list = os.listdir("./uploads")

    for i in file_list:
        if i not in text:
            text.append(i)

            loader = PyPDFLoader("./uploads/" + i)
            data = loader.load()
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=25)
            docs = text_splitter.split_documents(data)
            Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=INDEX_NAME)

    
    write_content = "\n".join(text)

    file = open("./embed-file-list.txt", "w+")
    file.write(write_content)
    file.close()

@app.route("/")
def index():
    uploaded_files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", uploaded_files=uploaded_files)

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    files = os.listdir("./uploads")
    if files == []:
        bot_response = llm.invoke(user_message)
    else:
        pdf_embedding()
        docsearch = Pinecone.from_existing_index(INDEX_NAME, embeddings)
        semantic_indices = docsearch.similarity_search(user_message)
        chain = load_qa_chain(lang_llm, chain_type="stuff")
        bot_response = chain.run(input_documents=semantic_indices, question=user_message)

    return jsonify({"bot_response": bot_response})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    files = request.files.getlist("file")

    uploaded_files = []
    for file in files:
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file:
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            uploaded_files.append(filename)

    return jsonify({"uploaded_files": uploaded_files}), 200

@app.route("/remove", methods=["POST"])
def remove_file():
    filename = request.form["filename"]
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    try:
        os.remove(file_path)
        return jsonify({"success": "File removed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

def empty_directory(directory="./uploads"):
    files = os.listdir("./uploads")
    if files != []:
        for root, dirs, files in os.walk(directory):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        print("Upload directory cleaned!")


if __name__ == "__main__":
    atexit.register(empty_directory)
    app.run(debug=True)
