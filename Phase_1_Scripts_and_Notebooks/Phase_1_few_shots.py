few_shots = {}

few_shots["python"] = [
"""
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
""",
"""
{
    "programming_language": "Python",
    "components": [
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "import os",
            "component_code": "import os",
            "component_description": "Imports Python's built-in os module, which provides functions for interacting with the operating system. This is used throughout the application for file system operations like listing directory contents, joining file paths, and removing files."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "import atexit",
            "component_code": "import atexit",
            "component_description": "Imports the atexit module which allows registering functions to be called when the Python interpreter terminates. In this application, it's used to clean up uploaded files when the server shuts down."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from flask import Flask, render_template, request, jsonify",
            "component_code": "from flask import Flask, render_template, request, jsonify",
            "component_description": "Imports core Flask components: Flask for creating the web application, render_template for serving HTML templates, request for handling HTTP requests, and jsonify for returning JSON responses. These form the foundation of the web interface."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain_community.embeddings import HuggingFaceEmbeddings",
            "component_code": "from langchain_community.embeddings import HuggingFaceEmbeddings",
            "component_description": "Imports HuggingFaceEmbeddings from LangChain, which provides access to Hugging Face's sentence transformer models. This is used to convert text from PDFs into numerical embeddings that can be stored and searched in Pinecone."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain_community.llms import Ollama",
            "component_code": "from langchain_community.llms import Ollama",
            "component_description": "Imports the Ollama interface from LangChain, which allows interacting with Ollama's local LLM models. In this application, it's configured to use the 'mistral' model for generating responses to user queries."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain.callbacks.manager import CallbackManager",
            "component_code": "from langchain.callbacks.manager import CallbackManager",
            "component_description": "Imports CallbackManager from LangChain, which provides a way to handle callbacks during LLM operations. This is used to manage the streaming output callback handler for the Ollama LLM."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler",
            "component_code": "from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler",
            "component_description": "Imports StreamingStdOutCallbackHandler which enables streaming LLM outputs to stdout in real-time. This provides immediate feedback during LLM operations rather than waiting for complete responses."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain_community.document_loads import PyPDFLoader",
            "component_code": "from langchain_community.document_loads import PyPDFLoader",
            "component_description": "Imports PyPDFLoader from LangChain, a document loader specifically for PDF files. This is used to extract text content from user-uploaded PDFs that will be processed and stored in Pinecone."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain.text_splitter import RecursiveCharacterTextSplitter",
            "component_code": "from langchain.text_splitter import RecursiveCharacterTextSplitter",
            "component_description": "Imports RecursiveCharacterTextSplitter which intelligently splits large documents into smaller chunks. This is crucial for processing PDFs as LLMs have context window limits, and it helps create manageable pieces for embedding."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain_community.vectorstores import Pinecone",
            "component_code": "from langchain_community.vectorstores import Pinecone",
            "component_description": "Imports the Pinecone integration from LangChain, which provides a high-performance vector database for storing and searching document embeddings. This enables semantic search capabilities over the uploaded PDF content."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "from langchain.chains.question_answering import load_qa_chain",
            "component_code": "from langchain.chains.question_answering import load_qa_chain",
            "component_description": "Imports load_qa_chain which provides a pre-configured question-answering pipeline. This chain combines document retrieval with LLM processing to answer questions based on the uploaded PDF content."
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "import pinecone",
            "component_code": "import pinecone",
            "component_description": "Imports the Pinecone client library directly, which is used to initialize and interact with the Pinecone vector database service where document embeddings are stored and retrieved."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "__init__",
            "component_code": "app = Flask(__name__)",
            "component_description": "Initializes the Flask application instance. The __name__ argument helps Flask determine where to look for templates and static files. This creates the core WSGI application that will handle all web requests."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "UPLOAD_FOLDER",
            "component_code": "UPLOAD_FOLDER = \\\"uploads\\\"",
            "component_description": "Defines a constant specifying the directory where user-uploaded PDF files will be stored. This local directory is used as temporary storage before files are processed into Pinecone embeddings."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "app.config",
            "component_code": "app.config[\\\"UPLOAD_FOLDER\\\"] = UPLOAD_FOLDER",
            "component_description": "Configures the Flask application to store the upload folder path in its configuration dictionary. This makes the upload path easily accessible throughout the application via Flask's config system."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "llm",
            "component_code": "llm = Ollama(model=\\\"mistral\\\")",
            "component_description": "Creates an instance of the Ollama language model configured to use the 'mistral' model. This simpler instance is used for general queries when no PDFs are uploaded, providing basic LLM functionality."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "lang_llm",
            "component_code": "lang_llm = Ollama(model=\\\"mistral\\\", verbose=True, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))",
            "component_description": "Creates an enhanced Ollama instance with verbose logging and streaming output capabilities. This instance is used for question-answering over documents, where streaming provides better user feedback during potentially longer operations."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "embeddings",
            "component_code": "embeddings = HuggingFaceEmbeddings(model_name=\\\"sentence-transformers/all-MiniLM-L6-v2\\\")",
            "component_description": "Initializes the HuggingFace embeddings model using the 'all-MiniLM-L6-v2' sentence transformer. This specific model is chosen for its balance between performance and accuracy in creating semantic embeddings of text chunks."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "PINECONE_API_KEY",
            "component_code": "PINECONE_API_KEY = \\\"<PINECONE-KEY>\\\"",
            "component_description": "Stores the API key required to authenticate with the Pinecone vector database service. In a production environment, this would typically be stored securely in environment variables rather than hardcoded."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "PINECONE_API_ENV",
            "component_code": "PINECONE_API_ENV = \\\"<PINECONE-ENV-NAME>\\\"",
            "component_description": "Specifies the Pinecone environment/region where the vector database is hosted. Different environments might have different performance characteristics or geographic locations."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "pinecone.init",
            "component_code": "pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)",
            "component_description": "Initializes the Pinecone client with the provided API credentials. This global initialization is required before any operations can be performed with the Pinecone vector database."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "INDEX_NAME",
            "component_code": "INDEX_NAME = \\\"scichat\\\"",
            "component_description": "Defines the name of the Pinecone index where document embeddings will be stored and retrieved. This name must match an existing index in your Pinecone project configured with appropriate dimensions for the embeddings model."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "pdf_embedding",
            "component_code": "def pdf_embedding():\\n    file = open(\\\"./embed-file-list.txt\\\", \\\"r+\\\")\\n    text = file.read().splitlines()\\n    file.close()\\n\\n    file_list = os.listdir(\\\"./uploads\\\")\\n\\n    for i in file_list:\\n        if i not in text:\\n            text.append(i)\\n\\n            loader = PyPDFLoader(\\\"./uploads/\\\" + i)\\n            data = loader.load()\\n            text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=25)\\n            docs = text_splitter.split_documents(data)\\n            Pinecone.from_texts([t.page_content for t in docs], embeddings, index_name=INDEX_NAME)\\n\\n\\n    write_content = \\\"\\n\\\".join(text)\\n\\n    file = open(\\\"./embed-file-list.txt\\\", \\\"w+\\\")\\n    file.write(write_content)\\n    file.close()",
            "component_description": "Defines the core PDF processing pipeline that: 1) Tracks processed files to avoid duplicate work, 2) Loads new PDFs using PyPDFLoader, 3) Splits documents into chunks with overlap for context preservation, 4) Generates embeddings using HuggingFace, and 5) Stores them in Pinecone. The text file acts as a simple persistence mechanism to track which files have been processed."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "index",
            "component_code": "@app.route(\\\"/\\\")\\ndef index():\\n    uploaded_files = os.listdir(app.config[\\\"UPLOAD_FOLDER\\\"])\\n    return render_template(\\\"index.html\\\", uploaded_files=uploaded_files)",
            "component_description": "Defines the root route that serves the main application interface. It lists all currently uploaded PDF files from the upload directory and passes them to the index.html template for rendering. This provides users with visibility of available documents."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "get_response",
            "component_code": "@app.route(\\\"/get_response\\\", methods=[\\\"POST\\\"])\\ndef get_response():\\n    user_message = request.form[\\\"user_message\\\"]\\n    files = os.listdir(\\\"./uploads\\\")\\n    if files == []:\\n        bot_response = llm.invoke(user_message)\\n    else:\\n        pdf_embedding()\\n        docsearch = Pinecone.from_existing_index(INDEX_NAME, embeddings)\\n        semantic_indices = docsearch.similarity_search(user_message)\\n        chain = load_qa_chain(lang_llm, chain_type=\\\"stuff\\\")\\n        bot_response = chain.run(input_documents=semantic_indices, question=user_message)\\n\\n    return jsonify({\\\"bot_response\\\": bot_response})",
            "component_description": "Handles user queries with two modes: 1) Direct LLM responses when no PDFs are uploaded, or 2) Document-enhanced responses using Pinecone semantic search to find relevant PDF chunks which are then processed by the LLM. The 'stuff' chain type simply combines all relevant chunks into the LLM context."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "upload_file",
            "component_code": "@app.route(\\\"/upload\\\", methods=[\\\"POST\\\"])\\ndef upload_file():\\n    if \\\"file\\\" not in request.files:\\n        return jsonify({\\\"error\\\": \\\"No file part\\\"}), 400\\n\\n    files = request.files.getlist(\\\"file\\\")\\n\\n    uploaded_files = []\\n    for file in files:\\n        if file.filename == \\\"\\\":\\n            return jsonify({\\\"error\\\": \\\"No selected file\\\"}), 400\\n\\n        if file:\\n            filename = file.filename\\n            file.save(os.path.join(app.config[\\\"UPLOAD_FOLDER\\\"], filename))\\n            uploaded_files.append(filename)\\n\\n    return jsonify({\\\"uploaded_files\\\": uploaded_files}), 200",
            "component_description": "Handles PDF file uploads via multipart form data. Supports multiple file uploads in one request, validates presence of files, saves them to the upload directory, and returns the list of successfully processed filenames. Includes proper error handling for missing files."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "remove_file",
            "component_code": "@app.route(\\\"/remove\\\", methods=[\\\"POST\\\"])\\ndef remove_file():\\n    filename = request.form[\\\"filename\\\"]\\n    file_path = os.path.join(app.config[\\\"UPLOAD_FOLDER\\\"], filename)\\n    try:\\n        os.remove(file_path)\\n        return jsonify({\\\"success\\\": \\\"File removed successfully\\\"})\\n    except Exception as e:\\n        return jsonify({\\\"error\\\": str(e)})",
            "component_description": "Provides an endpoint for removing specific uploaded files. Constructs the full file path safely using os.path.join, attempts deletion, and returns appropriate success/error responses. Note that this doesn't remove the file's embeddings from Pinecone."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "empty_directory",
            "component_code": "def empty_directory(directory=\\\"./uploads\\\"):\\n    files = os.listdir(\\\"./uploads\\\")\\n    if files != []:\\n        for root, dirs, files in os.walk(directory):\\n            for file in files:\\n                os.remove(os.path.join(root, file))\\n            for dir in dirs:\\n                os.rmdir(os.path.join(root, dir))\\n        print(\\\"Upload directory cleaned!\\\")",
            "component_description": "Utility function that recursively cleans the upload directory by removing all files and subdirectories. This is registered with atexit to run when the application terminates, serving as a cleanup mechanism for temporary uploads. Uses os.walk for comprehensive directory traversal."
        },
        {
            "component_type": "METHOD_DEFINITION",
            "component_name": "__name__ == '__main__'",
            "component_code": "if __name__ == \\\"__main__\\\":\\n    atexit.register(empty_directory)\\n    app.run(debug=True)",
            "component_description": "Standard Python idiom to ensure code only runs when executed directly (not when imported). Registers the cleanup function with atexit and starts the Flask development server with debug mode enabled, which provides automatic reloading and detailed error pages."
        }
    ],
    "overall_description": "This Python Flask application implements a document-based question answering system with the following key features:\\n    1. Web Interface: Provides routes for file management (upload/remove) and query processing\\n    2. Document Processing: Automatically extracts text from PDFs, splits into chunks, and generates embeddings\\n    3. Vector Storage: Uses Pinecone for efficient storage and retrieval of document embeddings\\n    4. Dual Mode Responses: Answers questions either from general knowledge (LLM only) or from uploaded documents (LLM + semantic search)\\n    5. Resource Management: Includes cleanup mechanisms for temporary files\\nThe application combines several AI components (Ollama LLM, HuggingFace embeddings) with web technologies (Flask) and vector database (Pinecone) to create an end-to-end system for document-based knowledge retrieval and question answering."
}
"""]

few_shots["java"] = [
"""
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Main class to demonstrate the inventory management system
 */
public class InventoryManagementSystem {
    public static void main(String[] args) {
        // Initialize inventory
        Inventory inventory = new Inventory();
        
        // Add sample products
        inventory.addProduct(new Product("P1001", "Laptop", 999.99, 10));
        inventory.addProduct(new Product("P1002", "Smartphone", 699.99, 15));
        inventory.addProduct(new Product("P1003", "Headphones", 149.99, 30));
        
        // Create order processor
        OrderProcessor orderProcessor = new OrderProcessor(inventory);
        
        // Process sample orders
        Order order1 = new Order("ORD001");
        order1.addItem("P1001", 2);
        order1.addItem("P1003", 1);
        
        Order order2 = new Order("ORD002");
        order2.addItem("P1002", 3);
        order2.addItem("P1003", 2);
        
        // Process orders
        orderProcessor.processOrder(order1);
        orderProcessor.processOrder(order2);
        
        // Generate reports
        ReportGenerator.generateInventoryReport(inventory);
        ReportGenerator.generateSalesReport(orderProcessor);
    }
}

/**
 * Represents a product in the inventory
 */
class Product {
    private String productId;
    private String name;
    private double price;
    private int quantity;
    
    public Product(String productId, String name, double price, int quantity) {
        this.productId = productId;
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }
    
    // Getters and setters
    public String getProductId() {
        return productId;
    }
    
    public String getName() {
        return name;
    }
    
    public double getPrice() {
        return price;
    }
    
    public int getQuantity() {
        return quantity;
    }
    
    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
    
    public void increaseQuantity(int amount) {
        this.quantity += amount;
    }
    
    public void decreaseQuantity(int amount) {
        this.quantity -= amount;
    }
    
    @Override
    public String toString() {
        return String.format("%s - %s ($%.2f) Qty: %d", 
            productId, name, price, quantity);
    }
}

/**
 * Manages the inventory of products
 */
class Inventory {
    private Map<String, Product> products;
    
    public Inventory() {
        this.products = new HashMap<>();
    }
    
    public void addProduct(Product product) {
        if (products.containsKey(product.getProductId())) {
            System.out.println("Product already exists. Updating quantity instead.");
            Product existing = products.get(product.getProductId());
            existing.increaseQuantity(product.getQuantity());
        } else {
            products.put(product.getProductId(), product);
        }
    }
    
    public boolean removeProduct(String productId) {
        if (products.containsKey(productId)) {
            products.remove(productId);
            return true;
        }
        return false;
    }
    
    public Product getProduct(String productId) {
        return products.get(productId);
    }
    
    public List<Product> getAllProducts() {
        return new ArrayList<>(products.values());
    }
    
    public boolean hasSufficientStock(String productId, int quantity) {
        Product product = products.get(productId);
        return product != null && product.getQuantity() >= quantity;
    }
    
    public void updateStock(String productId, int quantity) {
        Product product = products.get(productId);
        if (product != null) {
            product.decreaseQuantity(quantity);
        }
    }
    
    public void restockProduct(String productId, int quantity) {
        Product product = products.get(productId);
        if (product != null) {
            product.increaseQuantity(quantity);
        }
    }
}

/**
 * Represents an order from a customer
 */
class Order {
    private String orderId;
    private Map<String, Integer> items; // productId -> quantity
    private double totalAmount;
    private boolean isProcessed;
    
    public Order(String orderId) {
        this.orderId = orderId;
        this.items = new HashMap<>();
        this.totalAmount = 0.0;
        this.isProcessed = false;
    }
    
    public void addItem(String productId, int quantity) {
        items.put(productId, items.getOrDefault(productId, 0) + quantity);
    }
    
    public void removeItem(String productId) {
        items.remove(productId);
    }
    
    public Map<String, Integer> getItems() {
        return new HashMap<>(items);
    }
    
    public String getOrderId() {
        return orderId;
    }
    
    public double getTotalAmount() {
        return totalAmount;
    }
    
    public void setTotalAmount(double totalAmount) {
        this.totalAmount = totalAmount;
    }
    
    public boolean isProcessed() {
        return isProcessed;
    }
    
    public void setProcessed(boolean processed) {
        isProcessed = processed;
    }
    
    @Override
    public String toString() {
        return String.format("Order %s - Total: $%.2f (%s)", 
            orderId, totalAmount, isProcessed ? "Processed" : "Pending");
    }
}

/**
 * Processes customer orders
 */
class OrderProcessor {
    private Inventory inventory;
    private List<Order> processedOrders;
    
    public OrderProcessor(Inventory inventory) {
        this.inventory = inventory;
        this.processedOrders = new ArrayList<>();
    }
    
    public boolean processOrder(Order order) {
        // Check if all items are available
        for (Map.Entry<String, Integer> entry : order.getItems().entrySet()) {
            String productId = entry.getKey();
            int quantity = entry.getValue();
            
            if (!inventory.hasSufficientStock(productId, quantity)) {
                System.out.println("Insufficient stock for product: " + productId);
                return false;
            }
        }
        
        // Calculate total and update inventory
        double total = 0.0;
        for (Map.Entry<String, Integer> entry : order.getItems().entrySet()) {
            String productId = entry.getKey();
            int quantity = entry.getValue();
            
            Product product = inventory.getProduct(productId);
            total += product.getPrice() * quantity;
            inventory.updateStock(productId, quantity);
        }
        
        order.setTotalAmount(total);
        order.setProcessed(true);
        processedOrders.add(order);
        
        System.out.println("Order processed successfully: " + order.getOrderId());
        return true;
    }
    
    public List<Order> getProcessedOrders() {
        return new ArrayList<>(processedOrders);
    }
    
    public double getTotalSales() {
        return processedOrders.stream()
            .mapToDouble(Order::getTotalAmount)
            .sum();
    }
}

/**
 * Generates various reports
 */
class ReportGenerator {
    public static void generateInventoryReport(Inventory inventory) {
        System.out.println("\n=== INVENTORY REPORT ===");
        System.out.println("Total Products: " + inventory.getAllProducts().size());
        System.out.println("Product Details:");
        
        for (Product product : inventory.getAllProducts()) {
            System.out.println(product);
        }
        
        System.out.println("========================");
    }
    
    public static void generateSalesReport(OrderProcessor orderProcessor) {
        System.out.println("\n=== SALES REPORT ===");
        System.out.println("Total Orders Processed: " + orderProcessor.getProcessedOrders().size());
        System.out.println("Total Sales Amount: $" + orderProcessor.getTotalSales());
        
        System.out.println("\nOrder Details:");
        for (Order order : orderProcessor.getProcessedOrders()) {
            System.out.println(order);
            for (Map.Entry<String, Integer> entry : order.getItems().entrySet()) {
                System.out.println(" - Product: " + entry.getKey() + ", Qty: " + entry.getValue());
            }
        }
        
        System.out.println("====================");
    }
    
    public static void generateLowStockReport(Inventory inventory, int threshold) {
        System.out.println("\n=== LOW STOCK REPORT ===");
        System.out.println("Products with quantity below " + threshold + ":");
        
        for (Product product : inventory.getAllProducts()) {
            if (product.getQuantity() < threshold) {
                System.out.println(product);
            }
        }
        
        System.out.println("=======================");
    }
}
""",
"""
{
    "programming_language": "JAVA",
    "components": [
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "java.util.ArrayList",
            "component_code": "import java.util.ArrayList;",
            "component_description": "Imports the ArrayList class from java.util package"
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "java.util.HashMap",
            "component_code": "import java.util.HashMap;",
            "component_description": "Imports the HashMap class from java.util package"
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "java.util.List",
            "component_code": "import java.util.List;",
            "component_description": "Imports the List interface from java.util package"
        },
        {
            "component_type": "IMPORT_STATEMENT",
            "component_name": "java.util.Map",
            "component_code": "import java.util.Map;",
            "component_description": "Imports the Map interface from java.util package"
        },
        {
            "component_type": "CLASS_DEFINITION",
            "component_name": "InventoryManagementSystem",
            "component_code": "public class InventoryManagementSystem {\\n    public static void main(String[] args) {\\n        // Initialize inventory\\n        Inventory inventory = new Inventory();\\n        \\n        // Add sample products\\n        inventory.addProduct(new Product(\\"P1001\\", \\"Laptop\\", 999.99, 10));\\n        inventory.addProduct(new Product(\\"P1002\\", \\"Smartphone\\", 699.99, 15));\\n        inventory.addProduct(new Product(\\"P1003\\", \\"Headphones\\", 149.99, 30));\\n        \\n        // Create order processor\\n        OrderProcessor orderProcessor = new OrderProcessor(inventory);\\n        \\n        // Process sample orders\\n        Order order1 = new Order(\\"ORD001\\");\\n        order1.addItem(\\"P1001\\", 2);\\n        order1.addItem(\\"P1003\\", 1);\\n        \\n        Order order2 = new Order(\\"ORD002\\");\\n        order2.addItem(\\"P1002\\", 3);\\n        order2.addItem(\\"P1003\\", 2);\\n        \\n        // Process orders\\n        orderProcessor.processOrder(order1);\\n        orderProcessor.processOrder(order2);\\n        \\n        // Generate reports\\n        ReportGenerator.generateInventoryReport(inventory);\\n        ReportGenerator.generateSalesReport(orderProcessor);\\n    }\\n}",
            "component_description": "Main class demonstrating an inventory management system with sample product additions, order processing, and report generation"
        },
        {
            "component_type": "CLASS_DEFINITION",
            "component_name": "Product",
            "component_code": "class Product {\\n    private String productId;\\n    private String name;\\n    private double price;\\n    private int quantity;\\n    \\n    public Product(String productId, String name, double price, int quantity) {\\n        this.productId = productId;\\n        this.name = name;\\n        this.price = price;\\n        this.quantity = quantity;\\n    }\\n    \\n    // Getters and setters\\n    public String getProductId() {\\n        return productId;\\n    }\\n    \\n    public String getName() {\\n        return name;\\n    }\\n    \\n    public double getPrice() {\\n        return price;\\n    }\\n    \\n    public int getQuantity() {\\n        return quantity;\\n    }\\n    \\n    public void setQuantity(int quantity) {\\n        this.quantity = quantity;\\n    }\\n    \\n    public void increaseQuantity(int amount) {\\n        this.quantity += amount;\\n    }\\n    \\n    public void decreaseQuantity(int amount) {\\n        this.quantity -= amount;\\n    }\\n    \\n    @Override\\n    public String toString() {\\n        return String.format(\\"%s - %s ($%.2f) Qty: %d\\", \\n            productId, name, price, quantity);\\n    }\\n}",
            "component_description": "Represents a product with ID, name, price, and quantity, including quantity management methods"
        },
        {
            "component_type": "CLASS_DEFINITION",
            "component_name": "Inventory",
            "component_code": "class Inventory {\\n    private Map<String, Product> products;\\n    \\n    public Inventory() {\\n        this.products = new HashMap<>();\\n    }\\n    \\n    public void addProduct(Product product) {\\n        if (products.containsKey(product.getProductId())) {\\n            System.out.println(\\"Product already exists. Updating quantity instead.\\");\\n            Product existing = products.get(product.getProductId());\\n            existing.increaseQuantity(product.getQuantity());\\n        } else {\\n            products.put(product.getProductId(), product);\\n        }\\n    }\\n    \\n    public boolean removeProduct(String productId) {\\n        if (products.containsKey(productId)) {\\n            products.remove(productId);\\n            return true;\\n        }\\n        return false;\\n    }\\n    \\n    public Product getProduct(String productId) {\\n        return products.get(productId);\\n    }\\n    \\n    public List<Product> getAllProducts() {\\n        return new ArrayList<>(products.values());\\n    }\\n    \\n    public boolean hasSufficientStock(String productId, int quantity) {\\n        Product product = products.get(productId);\\n        return product != null && product.getQuantity() >= quantity;\\n    }\\n    \\n    public void updateStock(String productId, int quantity) {\\n        Product product = products.get(productId);\\n        if (product != null) {\\n            product.decreaseQuantity(quantity);\\n        }\\n    }\\n    \\n    public void restockProduct(String productId, int quantity) {\\n        Product product = products.get(productId);\\n        if (product != null) {\\n            product.increaseQuantity(quantity);\\n        }\\n    }\\n}",
            "component_description": "Manages product inventory with operations for adding, removing, and updating product quantities"
        },
        {
            "component_type": "CLASS_DEFINITION",
            "component_name": "Order",
            "component_code": "class Order {\\n    private String orderId;\\n    private Map<String, Integer> items; // productId -> quantity\\n    private double totalAmount;\\n    private boolean isProcessed;\\n    \\n    public Order(String orderId) {\\n        this.orderId = orderId;\\n        this.items = new HashMap<>();\\n        this.totalAmount = 0.0;\\n        this.isProcessed = false;\\n    }\\n    \\n    public void addItem(String productId, int quantity) {\\n        items.put(productId, items.getOrDefault(productId, 0) + quantity);\\n    }\\n    \\n    public void removeItem(String productId) {\\n        items.remove(productId);\\n    }\\n    \\n    public Map<String, Integer> getItems() {\\n        return new HashMap<>(items);\\n    }\\n    \\n    public String getOrderId() {\\n        return orderId;\\n    }\\n    \\n    public double getTotalAmount() {\\n        return totalAmount;\\n    }\\n    \\n    public void setTotalAmount(double totalAmount) {\\n        this.totalAmount = totalAmount;\\n    }\\n    \\n    public boolean isProcessed() {\\n        return isProcessed;\\n    }\\n    \\n    public void setProcessed(boolean processed) {\\n        isProcessed = processed;\\n    }\\n    \\n    @Override\\n    public String toString() {\\n        return String.format(\\"Order %s - Total: $%.2f (%s)\\", \\n            orderId, totalAmount, isProcessed ? \\"Processed\\" : \\"Pending\\");\\n    }\\n}",
            "component_description": "Represents a customer order with items, total amount, and processing status"
        },
        {
            "component_type": "CLASS_DEFINITION",
            "component_name": "OrderProcessor",
            "component_code": "class OrderProcessor {\\n    private Inventory inventory;\\n    private List<Order> processedOrders;\\n    \\n    public OrderProcessor(Inventory inventory) {\\n        this.inventory = inventory;\\n        this.processedOrders = new ArrayList<>();\\n    }\\n    \\n    public boolean processOrder(Order order) {\\n        // Check if all items are available\\n        for (Map.Entry<String, Integer> entry : order.getItems().entrySet()) {\\n            String productId = entry.getKey();\\n            int quantity = entry.getValue();\\n            \\n            if (!inventory.hasSufficientStock(productId, quantity)) {\\n                System.out.println(\\"Insufficient stock for product: \\" + productId);\\n                return false;\\n            }\\n        }\\n        \\n        // Calculate total and update inventory\\n        double total = 0.0;\\n        for (Map.Entry<String, Integer> entry : order.getItems().entrySet()) {\\n            String productId = entry.getKey();\\n            int quantity = entry.getValue();\\n            \\n            Product product = inventory.getProduct(productId);\\n            total += product.getPrice() * quantity;\\n            inventory.updateStock(productId, quantity);\\n        }\\n        \\n        order.setTotalAmount(total);\\n        order.setProcessed(true);\\n        processedOrders.add(order);\\n        \\n        System.out.println(\\"Order processed successfully: \\" + order.getOrderId());\\n        return true;\\n    }\\n    \\n    public List<Order> getProcessedOrders() {\\n        return new ArrayList<>(processedOrders);\\n    }\\n    \\n    public double getTotalSales() {\\n        return processedOrders.stream()\\n            .mapToDouble(Order::getTotalAmount)\\n            .sum();\\n    }\\n}",
            "component_description": "Processes customer orders by checking stock availability, calculating totals, and updating inventory"
        },
        {
            "component_type": "CLASS_DEFINITION",
            "component_name": "ReportGenerator",
            "component_code": "class ReportGenerator {\\n    public static void generateInventoryReport(Inventory inventory) {\\n        System.out.println(\\"\\n=== INVENTORY REPORT ===\\");\\n        System.out.println(\\"Total Products: \\" + inventory.getAllProducts().size());\\n        System.out.println(\\"Product Details:\\");\\n        \\n        for (Product product : inventory.getAllProducts()) {\\n            System.out.println(product);\\n        }\\n        \\n        System.out.println(\\"========================\\");\\n    }\\n    \\n    public static void generateSalesReport(OrderProcessor orderProcessor) {\\n        System.out.println(\\"\\n=== SALES REPORT ===\\");\\n        System.out.println(\\"Total Orders Processed: \\" + orderProcessor.getProcessedOrders().size());\\n        System.out.println(\\"Total Sales Amount: $\\" + orderProcessor.getTotalSales());\\n        \\n        System.out.println(\\"\\nOrder Details:\\");\\n        for (Order order : orderProcessor.getProcessedOrders()) {\\n            System.out.println(order);\\n            for (Map.Entry<String, Integer> entry : order.getItems().entrySet()) {\\n                System.out.println(\\" - Product: \\" + entry.getKey() + \\", Qty: \\" + entry.getValue());\\n            }\\n        }\\n        \\n        System.out.println(\\"====================\\");\\n    }\\n    \\n    public static void generateLowStockReport(Inventory inventory, int threshold) {\\n        System.out.println(\\"\\n=== LOW STOCK REPORT ===\\");\\n        System.out.println(\\"Products with quantity below \\" + threshold + \\":\\");\\n        \\n        for (Product product : inventory.getAllProducts()) {\\n            if (product.getQuantity() < threshold) {\\n                System.out.println(product);\\n            }\\n        }\\n        \\n        System.out.println(\\"=======================\\");\\n    }\\n}",
            "component_description": "Generates various reports including inventory status, sales information, and low stock alerts"
        }
    ],
    "overall_description": "A complete Java implementation of an inventory management system with product tracking, order processing, and reporting capabilities. The system includes classes for products, inventory management, order processing, and report generation, demonstrating object-oriented design principles."
}
"""]

few_shots["c"] = [
"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_LEN 50
#define MAX_STUDENTS 100

typedef struct {
    int id;
    char name[MAX_NAME_LEN];
    float gpa;
} Student;

enum Grade { A, B, C, D, F };

Student students[MAX_STUDENTS];
int student_count = 0;

const char* get_grade(float gpa) {
    if (gpa >= 3.5) return "A";
    else if (gpa >= 3.0) return "B";
    else if (gpa >= 2.5) return "C";
    else if (gpa >= 2.0) return "D";
    else return "F";
}

void add_student(int id, const char* name, float gpa) {
    if (student_count >= MAX_STUDENTS) {
        printf("Student limit reached.\n");
        return;
    }
    students[student_count].id = id;
    strncpy(students[student_count].name, name, MAX_NAME_LEN);
    students[student_count].gpa = gpa;
    student_count++;
}

void display_all_students(int with_grades) {
    for (int i = 0; i < student_count; i++) {
        Student* s = &students[i];
        if (with_grades)
            printf("ID: %d, Name: %s, GPA: %.2f, Grade: %s\n", s->id, s->name, s->gpa, get_grade(s->gpa));
        else
            printf("ID: %d, Name: %s, GPA: %.2f\n", s->id, s->name, s->gpa);
    }
}

Student* find_student(int id) {
    for (int i = 0; i < student_count; i++) {
        if (students[i].id == id)
            return &students[i];
    }
    return NULL;
}

int main() {
    add_student(1, "Alice", 3.8);
    add_student(2, "Bob", 2.9);
    add_student(3, "Charlie", 2.1);

    printf("Students (Basic Info):\n");
    display_all_students(0);

    printf("\nStudents (With Grades):\n");
    display_all_students(1);

    int search_id = 2;
    Student* found = find_student(search_id);
    if (found)
        printf("\nFound ID %d -> Name: %s, GPA: %.2f, Grade: %s\n", found->id, found->name, found->gpa, get_grade(found->gpa));
    else
        printf("\nStudent with ID %d not found.\n", search_id);

    return 0;
}
""",
"""
{
  "programming_language": "C",
  "components": [
    {
      "component_type": "INCLUDE_STATEMENT",
      "component_name": "stdio.h, stdlib.h, string.h",
      "component_code": "#include <stdio.h>\\n#include <stdlib.h>\\n#include <string.h>",
      "component_description": "Includes standard libraries for I/O, memory allocation, and string operations."
    },
    {
      "component_type": "STRUCT_DEFINITION",
      "component_name": "Student",
      "component_code": "typedef struct {\\n    int id;\\n    char name[MAX_NAME_LEN];\\n    float gpa;\\n} Student;",
      "component_description": "Defines the Student structure with fields for ID, name, and GPA."
    },
    {
      "component_type": "ENUM_DEFINITION",
      "component_name": "Grade",
      "component_code": "enum Grade { A, B, C, D, F };",
      "component_description": "Defines letter grades as enumeration values."
    },
    {
      "component_type": "FUNCTION_DEFINITION",
      "component_name": "get_grade",
      "component_code": "const char* get_grade(float gpa) {\\n    if (gpa >= 3.5) return \\\"A\\\";\\n    else if (gpa >= 3.0) return \\\"B\\\";\\n    else if (gpa >= 2.5) return \\\"C\\\";\\n    else if (gpa >= 2.0) return \\\"D\\\";\\n    else return \\\"F\\\";\\n}",
      "component_description": "Returns a letter grade string corresponding to the input GPA."
    },
    {
      "component_type": "FUNCTION_DEFINITION",
      "component_name": "add_student",
      "component_code": "void add_student(int id, const char* name, float gpa) {\\n    if (student_count >= MAX_STUDENTS) {\\n        printf(\\\"Student limit reached.\\n\\\");\\n        return;\\n    }\\n    students[student_count].id = id;\\n    strncpy(students[student_count].name, name, MAX_NAME_LEN);\\n    students[student_count].gpa = gpa;\\n    student_count++;\\n}",
      "component_description": "Adds a student to the array if the maximum limit hasn't been reached."
    },
    {
      "component_type": "FUNCTION_DEFINITION",
      "component_name": "display_all_students",
      "component_code": "void display_all_students(int with_grades) {\\n    for (int i = 0; i < student_count; i++) {\\n        Student* s = &students[i];\\n        if (with_grades)\\n            printf(\\\"ID: %d, Name: %s, GPA: %.2f, Grade: %s\\n\\\", s->id, s->name, s->gpa, get_grade(s->gpa));\\n        else\\n            printf(\\\"ID: %d, Name: %s, GPA: %.2f\\n\\\", s->id, s->name, s->gpa);\\n    }\\n}",
      "component_description": "Displays all student records, optionally including grades."
    },
    {
      "component_type": "FUNCTION_DEFINITION",
      "component_name": "find_student",
      "component_code": "Student* find_student(int id) {\\n    for (int i = 0; i < student_count; i++) {\\n        if (students[i].id == id)\\n            return &students[i];\\n    }\\n    return NULL;\\n}",
      "component_description": "Searches and returns a pointer to a student by ID or NULL if not found."
    },
    {
      "component_type": "FUNCTION_DEFINITION",
      "component_name": "main",
      "component_code": "int main() {\\n    add_student(1, \\\"Alice\\\", 3.8);\\n    add_student(2, \\\"Bob\\\", 2.9);\\n    add_student(3, \\\"Charlie\\\", 2.1);\\n\\n    printf(\\\"Students (Basic Info):\\n\\\");\\n    display_all_students(0);\\n\\n    printf(\\\"\\nStudents (With Grades):\\n\\\");\\n    display_all_students(1);\\n\\n    int search_id = 2;\\n    Student* found = find_student(search_id);\\n    if (found)\\n        printf(\\\"\\nFound ID %d -> Name: %s, GPA: %.2f, Grade: %s\\n\\\", found->id, found->name, found->gpa, get_grade(found->gpa));\\n    else\\n        printf(\\\"\\nStudent with ID %d not found.\\n\\\", search_id);\\n\\n    return 0;\\n}",
      "component_description": "Demonstrates adding students, displaying them, and searching by ID."
    }
  ],
  "overall_description": "This C program manages a student database using a static array. It allows adding students with ID, name, and GPA, displaying all records with optional letter grades, and searching for students by ID. A grade is computed from GPA using a defined scale. The program showcases basic use of structs, enums, conditionals, and function calls."
}
"""]

few_shots["csharp"] = [
"""
using System;
using System.Collections.Generic;
using System.Linq;

namespace BankingSystem
{
    public enum TransactionType { Deposit, Withdrawal, Transfer }

    public record Transaction(
        Guid Id,
        string AccountNumber,
        decimal Amount,
        TransactionType Type,
        DateTime Timestamp,
        string Description = ""
    );

    public class InsufficientFundsException : Exception
    {
        public InsufficientFundsException(decimal balance, decimal amount) 
            : base($"Insufficient funds. Balance: {balance}, Attempted: {amount}") {}
    }

    public class AccountNotFoundException : Exception
    {
        public AccountNotFoundException(string accountNumber) 
            : base($"Account not found: {accountNumber}") {}
    }

    public interface IAccountService
    {
        decimal GetBalance(string accountNumber);
        Transaction Deposit(string accountNumber, decimal amount, string description = "");
        Transaction Withdraw(string accountNumber, decimal amount, string description = "");
        Transaction Transfer(string sourceAccount, string targetAccount, decimal amount, string description = "");
        IEnumerable<Transaction> GetTransactionHistory(string accountNumber);
    }

    public class AccountService : IAccountService
    {
        private readonly Dictionary<string, decimal> _balances;
        private readonly Dictionary<string, List<Transaction>> _transactions;

        public AccountService()
        {
            _balances = new Dictionary<string, decimal>();
            _transactions = new Dictionary<string, List<Transaction>>();
        }

        public void CreateAccount(string accountNumber, decimal initialBalance = 0)
        {
            _balances[accountNumber] = initialBalance;
            _transactions[accountNumber] = new List<Transaction>();
        }

        public decimal GetBalance(string accountNumber)
        {
            if (!_balances.ContainsKey(accountNumber))
                throw new AccountNotFoundException(accountNumber);

            return _balances[accountNumber];
        }

        public Transaction Deposit(string accountNumber, decimal amount, string description = "")
        {
            ValidateAccount(accountNumber);
            
            var transaction = new Transaction(
                Guid.NewGuid(),
                accountNumber,
                amount,
                TransactionType.Deposit,
                DateTime.UtcNow,
                description
            );

            _balances[accountNumber] += amount;
            _transactions[accountNumber].Add(transaction);
            
            return transaction;
        }

        public Transaction Withdraw(string accountNumber, decimal amount, string description = "")
        {
            ValidateAccount(accountNumber);
            
            decimal balance = GetBalance(accountNumber);
            if (balance < amount)
                throw new InsufficientFundsException(balance, amount);

            var transaction = new Transaction(
                Guid.NewGuid(),
                accountNumber,
                amount,
                TransactionType.Withdrawal,
                DateTime.UtcNow,
                description
            );

            _balances[accountNumber] -= amount;
            _transactions[accountNumber].Add(transaction);
            
            return transaction;
        }

        public Transaction Transfer(string sourceAccount, string targetAccount, decimal amount, string description = "")
        {
            ValidateAccount(sourceAccount);
            ValidateAccount(targetAccount);

            Withdraw(sourceAccount, amount, $"Transfer to {targetAccount}: {description}");
            var depositTransaction = Deposit(targetAccount, amount, $"Transfer from {sourceAccount}: {description}");

            return new Transaction(
                Guid.NewGuid(),
                sourceAccount,
                amount,
                TransactionType.Transfer,
                DateTime.UtcNow,
                description
            );
        }

        public IEnumerable<Transaction> GetTransactionHistory(string accountNumber)
        {
            ValidateAccount(accountNumber);
            return _transactions[accountNumber].AsReadOnly();
        }

        private void ValidateAccount(string accountNumber)
        {
            if (!_balances.ContainsKey(accountNumber))
                throw new AccountNotFoundException(accountNumber);
        }
    }

    public class Program
    {
        public static void Main()
        {
            var accountService = new AccountService();
            accountService.CreateAccount("ACC123", 1000);
            accountService.CreateAccount("ACC456", 500);

            try
            {
                accountService.Deposit("ACC123", 200, "Salary");
                accountService.Withdraw("ACC123", 50, "ATM Withdrawal");
                accountService.Transfer("ACC123", "ACC456", 300, "Rent Payment");

                Console.WriteLine("ACC123 Balance: " + accountService.GetBalance("ACC123"));
                Console.WriteLine("ACC456 Balance: " + accountService.GetBalance("ACC456"));

                Console.WriteLine("\nACC123 Transaction History:");
                foreach (var tx in accountService.GetTransactionHistory("ACC123"))
                {
                    Console.WriteLine($"{tx.Timestamp} - {tx.Type}: {tx.Amount:C} - {tx.Description}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}
""",
"""
{
  "programming_language": "C#",
  "components": [
    {
      "component_type": "NAMESPACE_DEFINITION",
      "component_name": "BankingSystem",
      "component_code": "namespace BankingSystem",
      "component_description": "Root namespace for banking system components, providing logical organization."
    },
    {
      "component_type": "ENUM_DEFINITION",
      "component_name": "TransactionType",
      "component_code": "public enum TransactionType { Deposit, Withdrawal, Transfer }",
      "component_description": "Enumeration defining possible transaction types for type-safe operation handling."
    },
    {
      "component_type": "RECORD_DEFINITION",
      "component_name": "Transaction",
      "component_code": "public record Transaction(\\n    Guid Id,\\n    string AccountNumber,\\n    decimal Amount,\\n    TransactionType Type,\\n    DateTime Timestamp,\\n    string Description = \\\"\\\"\\n);",
      "component_description": "Immutable record representing a financial transaction with all relevant metadata, leveraging C# 9+'s record types for value equality and immutability."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "InsufficientFundsException",
      "component_code": "public class InsufficientFundsException : Exception\\n{\\n    public InsufficientFundsException(decimal balance, decimal amount) \\n        : base($\\\"Insufficient funds. Balance: {balance}, Attempted: {amount}\\\") {}\\n}",
      "component_description": "Custom exception for insufficient funds scenarios, providing detailed error message with current balance and attempted amount."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "AccountNotFoundException",
      "component_code": "public class AccountNotFoundException : Exception\\n{\\n    public AccountNotFoundException(string accountNumber) \\n        : base($\\\"Account not found: {accountNumber}\\\") {}\\n}",
      "component_description": "Custom exception for invalid account references, including the problematic account number in error message."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "IAccountService",
      "component_code": "public interface IAccountService\\n{\\n    decimal GetBalance(string accountNumber);\\n    Transaction Deposit(string accountNumber, decimal amount, string description = \\\"\\\");\\n    Transaction Withdraw(string accountNumber, decimal amount, string description = \\\"\\\");\\n    Transaction Transfer(string sourceAccount, string targetAccount, decimal amount, string description = \\\"\\\");\\n    IEnumerable<Transaction> GetTransactionHistory(string accountNumber);\\n}",
      "component_description": "Service contract defining core banking operations, following interface segregation principle."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "AccountService",
      "component_code": "public class AccountService : IAccountService\\n{\\n    private readonly Dictionary<string, decimal> _balances;\\n    private readonly Dictionary<string, List<Transaction>> _transactions;\\n\\n    public AccountService()\\n    {\\n        _balances = new Dictionary<string, decimal>();\\n        _transactions = new Dictionary<string, List<Transaction>>();\\n    }",
      "component_description": "Concrete implementation of banking service with in-memory storage using dictionaries for accounts and transactions."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.CreateAccount",
      "component_code": "public void CreateAccount(string accountNumber, decimal initialBalance = 0)\\n{\\n    _balances[accountNumber] = initialBalance;\\n    _transactions[accountNumber] = new List<Transaction>();\\n}",
      "component_description": "Account initialization method setting up storage for balances and transaction history with optional initial deposit."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.GetBalance",
      "component_code": "public decimal GetBalance(string accountNumber)\\n{\\n    if (!_balances.ContainsKey(accountNumber))\\n        throw new AccountNotFoundException(accountNumber);\\n\\n    return _balances[accountNumber];\\n}",
      "component_description": "Balance retrieval with account existence validation, throwing appropriate exception for invalid accounts."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.Deposit",
      "component_code": "public Transaction Deposit(string accountNumber, decimal amount, string description = \\\"\\\")\\n{\\n    ValidateAccount(accountNumber);\\n    \\n    var transaction = new Transaction(\\n        Guid.NewGuid(),\\n        accountNumber,\\n        amount,\\n        TransactionType.Deposit,\\n        DateTime.UtcNow,\\n        description\\n    );\\n\\n    _balances[accountNumber] += amount;\\n    _transactions[accountNumber].Add(transaction);\\n    \\n    return transaction;\\n}",
      "component_description": "Deposit operation creating transaction record, updating balance, and maintaining audit trail."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.Withdraw",
      "component_code": "public Transaction Withdraw(string accountNumber, decimal amount, string description = \\\"\\\")\\n{\\n    ValidateAccount(accountNumber);\\n    \\n    decimal balance = GetBalance(accountNumber);\\n    if (balance < amount)\\n        throw new InsufficientFundsException(balance, amount);\\n\\n    var transaction = new Transaction(\\n        Guid.NewGuid(),\\n        accountNumber,\\n        amount,\\n        TransactionType.Withdrawal,\\n        DateTime.UtcNow,\\n        description\\n    );\\n\\n    _balances[accountNumber] -= amount;\\n    _transactions[accountNumber].Add(transaction);\\n    \\n    return transaction;\\n}",
      "component_description": "Withdrawal operation with funds availability check, throwing exception if balance is insufficient."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.Transfer",
      "component_code": "public Transaction Transfer(string sourceAccount, string targetAccount, decimal amount, string description = \\\"\\\")\\n{\\n    ValidateAccount(sourceAccount);\\n    ValidateAccount(targetAccount);\\n\\n    Withdraw(sourceAccount, amount, $\\\"Transfer to {targetAccount}: {description}\\\");\\n    var depositTransaction = Deposit(targetAccount, amount, $\\\"Transfer from {sourceAccount}: {description}\\\");\\n\\n    return new Transaction(\\n        Guid.NewGuid(),\\n        sourceAccount,\\n        amount,\\n        TransactionType.Transfer,\\n        DateTime.UtcNow,\\n        description\\n    );\\n}",
      "component_description": "Atomic transfer operation composed of withdrawal and deposit, returning a new transfer transaction record."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.GetTransactionHistory",
      "component_code": "public IEnumerable<Transaction> GetTransactionHistory(string accountNumber)\\n{\\n    ValidateAccount(accountNumber);\\n    return _transactions[accountNumber].AsReadOnly();\\n}",
      "component_description": "Transaction history retrieval providing read-only access to audit trail for an account."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "AccountService.ValidateAccount",
      "component_code": "private void ValidateAccount(string accountNumber)\\n{\\n    if (!_balances.ContainsKey(accountNumber))\\n        throw new AccountNotFoundException(accountNumber);\\n}",
      "component_description": "Private validation method ensuring account exists before operations, reducing code duplication."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "Program",
      "component_code": "public class Program\\n{\\n    public static void Main()\\n    {\\n        var accountService = new AccountService();\\n        accountService.CreateAccount(\\\"ACC123\\\", 1000);\\n        accountService.CreateAccount(\\\"ACC456\\\", 500);",
      "component_description": "Main program class demonstrating service usage with sample account setup."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "Program.Main",
      "component_code": "try\\n{\\n    accountService.Deposit(\\\"ACC123\\\", 200, \\\"Salary\\\");\\n    accountService.Withdraw(\\\"ACC123\\\", 50, \\\"ATM Withdrawal\\\");\\n    accountService.Transfer(\\\"ACC123\\\", \\\"ACC456\\\", 300, \\\"Rent Payment\\\");\\n\\n    Console.WriteLine(\\\"ACC123 Balance: \\\" + accountService.GetBalance(\\\"ACC123\\\"));\\n    Console.WriteLine(\\\"ACC456 Balance: \\\" + accountService.GetBalance(\\\"ACC456\\\"));\\n\\n    Console.WriteLine(\\\"\\nACC123 Transaction History:\\\");\\n    foreach (var tx in accountService.GetTransactionHistory(\\\"ACC123\\\"))\\n    {\\n        Console.WriteLine($\\\"{tx.Timestamp} - {tx.Type}: {tx.Amount:C} - {tx.Description}\\\");\\n    }\\n}\\ncatch (Exception ex)\\n{\\n    Console.WriteLine($\\\"Error: {ex.Message}\\\");\\n}",
      "component_description": "Demonstration of banking operations with proper error handling and transaction history display."
    }
  ],
  "overall_description": "A complete C# banking system demonstrating: immutable records for transactions, custom exceptions, interface-based service design, in-memory data storage, and atomic financial operations. The architecture emphasizes type safety through enums, proper error handling, and transaction auditing while maintaining clean separation between business logic and demonstration code."
}
"""]

few_shots["typescript"] = [
"""
import { v4 as uuidv4 } from 'uuid';
import axios, { AxiosInstance } from 'axios';

type Currency = 'USD' | 'EUR' | 'GBP';

interface Money {
  amount: number;
  currency: Currency;
}

enum OrderStatus {
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
  SHIPPED = 'SHIPPED',
  DELIVERED = 'DELIVERED',
  CANCELLED = 'CANCELLED'
}

interface OrderItem {
  productId: string;
  quantity: number;
  unitPrice: Money;
}

interface Order {
  id: string;
  customerId: string;
  items: OrderItem[];
  status: OrderStatus;
  createdAt: Date;
  updatedAt: Date;
  total: Money;
}

interface PaymentResult {
  success: boolean;
  transactionId?: string;
  error?: string;
}

abstract class PaymentGateway {
  abstract processPayment(amount: Money): Promise<PaymentResult>;
}

class StripeGateway extends PaymentGateway {
  private client: AxiosInstance;

  constructor(apiKey: string) {
    super();
    this.client = axios.create({
      baseURL: 'https://api.stripe.com/v1',
      headers: { Authorization: `Bearer ${apiKey}` }
    });
  }

  async processPayment(amount: Money): Promise<PaymentResult> {
    try {
      const response = await this.client.post('/charges', {
        amount: Math.round(amount.amount * 100),
        currency: amount.currency.toLowerCase()
      });
      return {
        success: true,
        transactionId: response.data.id
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || 'Payment failed'
      };
    }
  }
}

class OrderService {
  constructor(
    private paymentGateway: PaymentGateway,
    private inventoryService: InventoryService
  ) {}

  async createOrder(
    customerId: string,
    items: Omit<OrderItem, 'unitPrice'>[]
  ): Promise<Order> {
    const enrichedItems = await Promise.all(
      items.map(async item => ({
        ...item,
        unitPrice: await this.inventoryService.getProductPrice(item.productId)
      }))
    );

    const order: Order = {
      id: uuidv4(),
      customerId,
      items: enrichedItems,
      status: OrderStatus.PENDING,
      createdAt: new Date(),
      updatedAt: new Date(),
      total: this.calculateTotal(enrichedItems)
    };

    return order;
  }

  async processPayment(order: Order): Promise<PaymentResult> {
    return this.paymentGateway.processPayment(order.total);
  }

  private calculateTotal(items: OrderItem[]): Money {
    if (items.length === 0) {
      throw new Error('Order must have at least one item');
    }

    const totalAmount = items.reduce(
      (sum, item) => sum + (item.unitPrice.amount * item.quantity),
      0
    );

    return {
      amount: totalAmount,
      currency: items[0].unitPrice.currency
    };
  }
}

class InventoryService {
  private productPrices: Map<string, Money> = new Map();

  constructor() {
    this.productPrices.set('prod_1', { amount: 29.99, currency: 'USD' });
    this.productPrices.set('prod_2', { amount: 49.99, currency: 'USD' });
  }

  async getProductPrice(productId: string): Promise<Money> {
    const price = this.productPrices.get(productId);
    if (!price) {
      throw new Error(`Product ${productId} not found`);
    }
    return price;
  }

  async reserveInventory(productId: string, quantity: number): Promise<boolean> {
    // In a real implementation, this would check inventory levels
    return true;
  }
}

interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(orderId: string): Promise<Order | null>;
  updateStatus(orderId: string, status: OrderStatus): Promise<void>;
}

class MemoryOrderRepository implements OrderRepository {
  private orders: Map<string, Order> = new Map();

  async save(order: Order): Promise<void> {
    this.orders.set(order.id, order);
  }

  async findById(orderId: string): Promise<Order | null> {
    return this.orders.get(orderId) || null;
  }

  async updateStatus(orderId: string, status: OrderStatus): Promise<void> {
    const order = await this.findById(orderId);
    if (order) {
      order.status = status;
      order.updatedAt = new Date();
      await this.save(order);
    }
  }
}
""",
"""
{
  "programming_language": "TYPESCRIPT",
  "components": [
    {
      "component_type": "IMPORT_STATEMENT",
      "component_name": "uuid",
      "component_code": "import { v4 as uuidv4 } from 'uuid';",
      "component_description": "Imports UUID v4 generator function for creating unique order identifiers, following the standard approach for distributed ID generation in web applications."
    },
    {
      "component_type": "IMPORT_STATEMENT",
      "component_name": "axios",
      "component_code": "import axios, { AxiosInstance } from 'axios';",
      "component_description": "Imports Axios HTTP client and its type definition for making API requests to payment processors, providing promise-based async HTTP requests with interceptors and transformers."
    },
    {
      "component_type": "TYPE_DEFINITION",
      "component_name": "Currency",
      "component_code": "type Currency = 'USD' | 'EUR' | 'GBP';",
      "component_description": "Union type defining supported currencies in the e-commerce system, enforcing compile-time validation of currency values and enabling auto-completion in IDEs."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "Money",
      "component_code": "interface Money {\\n  amount: number;\\n  currency: Currency;\\n}",
      "component_description": "Core value object interface representing monetary amounts with currency, ensuring type safety for all financial calculations throughout the application."
    },
    {
      "component_type": "ENUM_DEFINITION",
      "component_name": "OrderStatus",
      "component_code": "enum OrderStatus {\\n  PENDING = 'PENDING',\\n  PROCESSING = 'PROCESSING',\\n  SHIPPED = 'SHIPPED',\\n  DELIVERED = 'DELIVERED',\\n  CANCELLED = 'CANCELLED'\\n}",
      "component_description": "String enum defining all possible states of an order lifecycle, using string values for better serialization and debugging compared to numeric enums."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "OrderItem",
      "component_code": "interface OrderItem {\\n  productId: string;\\n  quantity: number;\\n  unitPrice: Money;\\n}",
      "component_description": "Interface representing a line item in an order, containing product reference, quantity, and priced information, forming the building block of order composition."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "Order",
      "component_code": "interface Order {\\n  id: string;\\n  customerId: string;\\n  items: OrderItem[];\\n  status: OrderStatus;\\n  createdAt: Date;\\n  updatedAt: Date;\\n  total: Money;\\n}",
      "component_description": "Core domain interface representing an e-commerce order with all metadata including customer reference, items list, status tracking, audit timestamps, and calculated total amount."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "PaymentResult",
      "component_code": "interface PaymentResult {\\n  success: boolean;\\n  transactionId?: string;\\n  error?: string;\\n}",
      "component_description": "Result type for payment operations, following the pattern of returning both success status and either transaction details or error information for failure cases."
    },
    {
      "component_type": "ABSTRACT_CLASS_DEFINITION",
      "component_name": "PaymentGateway",
      "component_code": "abstract class PaymentGateway {\\n  abstract processPayment(amount: Money): Promise<PaymentResult>;\\n}",
      "component_description": "Abstract base class defining the contract for payment processors, using the Strategy pattern to allow different payment provider implementations while maintaining a consistent interface."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "StripeGateway",
      "component_code": "class StripeGateway extends PaymentGateway {\\n  private client: AxiosInstance;\\n\\n  constructor(apiKey: string) {\\n    super();\\n    this.client = axios.create({\\n      baseURL: 'https://api.stripe.com/v1',\\n      headers: { Authorization: `Bearer ${apiKey}` }\\n    });\\n  }\\n\\n  async processPayment(amount: Money): Promise<PaymentResult> {\\n    try {\\n      const response = await this.client.post('/charges', {\\n        amount: Math.round(amount.amount * 100),\\n        currency: amount.currency.toLowerCase()\\n      });\\n      return {\\n        success: true,\\n        transactionId: response.data.id\\n      };\\n    } catch (error) {\\n      return {\\n        success: false,\\n        error: error.response?.data?.message || 'Payment failed'\\n      };\\n    }\\n  }\\n}",
      "component_description": "Concrete Stripe implementation of the payment gateway, handling currency conversion to cents, proper API authentication, and error handling for the Stripe payment processing API."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "OrderService",
      "component_code": "class OrderService {\\n  constructor(\\n    private paymentGateway: PaymentGateway,\\n    private inventoryService: InventoryService\\n  ) {}\\n\\n  async createOrder(\\n    customerId: string,\\n    items: Omit<OrderItem, 'unitPrice'>[]\\n  ): Promise<Order> {\\n    const enrichedItems = await Promise.all(\\n      items.map(async item => ({\\n        ...item,\\n        unitPrice: await this.inventoryService.getProductPrice(item.productId)\\n      }))\\n    );\\n\\n    const order: Order = {\\n      id: uuidv4(),\\n      customerId,\\n      items: enrichedItems,\\n      status: OrderStatus.PENDING,\\n      createdAt: new Date(),\\n      updatedAt: new Date(),\\n      total: this.calculateTotal(enrichedItems)\\n    };\\n\\n    return order;\\n  }\\n\\n  async processPayment(order: Order): Promise<PaymentResult> {\\n    return this.paymentGateway.processPayment(order.total);\\n  }\\n\\n  private calculateTotal(items: OrderItem[]): Money {\\n    if (items.length === 0) {\\n      throw new Error('Order must have at least one item');\\n    }\\n\\n    const totalAmount = items.reduce(\\n      (sum, item) => sum + (item.unitPrice.amount * item.quantity),\\n      0\\n    );\\n\\n    return {\\n      amount: totalAmount,\\n      currency: items[0].unitPrice.currency\\n    };\\n  }\\n}",
      "component_description": "Core domain service handling order creation and payment processing, demonstrating dependency injection, async operations, and business logic for order total calculation. Enforces business rules like non-empty orders."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "InventoryService",
      "component_code": "class InventoryService {\\n  private productPrices: Map<string, Money> = new Map();\\n\\n  constructor() {\\n    this.productPrices.set('prod_1', { amount: 29.99, currency: 'USD' });\\n    this.productPrices.set('prod_2', { amount: 49.99, currency: 'USD' });\\n  }\\n\\n  async getProductPrice(productId: string): Promise<Money> {\\n    const price = this.productPrices.get(productId);\\n    if (!price) {\\n      throw new Error(`Product ${productId} not found`);\\n    }\\n    return price;\\n  }\\n\\n  async reserveInventory(productId: string, quantity: number): Promise<boolean> {\\n    return true;\\n  }\\n}",
      "component_description": "Simplified inventory service with product price catalog and inventory reservation stubs, demonstrating the Facade pattern for product-related operations in an e-commerce context."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "OrderRepository",
      "component_code": "interface OrderRepository {\\n  save(order: Order): Promise<void>;\\n  findById(orderId: string): Promise<Order | null>;\\n  updateStatus(orderId: string, status: OrderStatus): Promise<void>;\\n}",
      "component_description": "Repository interface defining persistence operations for orders, following the Interface Segregation Principle with focused async methods for order storage and retrieval."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "MemoryOrderRepository",
      "component_code": "class MemoryOrderRepository implements OrderRepository {\\n  private orders: Map<string, Order> = new Map();\\n\\n  async save(order: Order): Promise<void> {\\n    this.orders.set(order.id, order);\\n  }\\n\\n  async findById(orderId: string): Promise<Order | null> {\\n    return this.orders.get(orderId) || null;\\n  }\\n\\n  async updateStatus(orderId: string, status: OrderStatus): Promise<void> {\\n    const order = await this.findById(orderId);\\n    if (order) {\\n      order.status = status;\\n      order.updatedAt = new Date();\\n      await this.save(order);\\n    }\\n  }\\n}",
      "component_description": "In-memory implementation of the order repository using Map for storage, suitable for testing and demonstration purposes while maintaining the same interface as production database implementations."
    }
  ],
  "overall_description": "A complete TypeScript e-commerce order processing module demonstrating: domain modeling with interfaces and enums, dependency injection for services, async operations with Promises, payment gateway abstraction, and repository pattern implementation. The architecture follows SOLID principles with clear separation of concerns between domain logic, payment processing, and data persistence."
}
"""]

few_shots["go"] = [
"""
package taskqueue

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"sync"
	"time"

	"github.com/google/uuid"
)

var (
	ErrTaskNotFound    = errors.New("task not found")
	ErrQueueEmpty      = errors.New("queue is empty")
	ErrTaskNotReady    = errors.New("task not ready for processing")
	ErrWorkerConflict  = errors.New("worker conflict")
)

type TaskState string

const (
	StatePending   TaskState = "PENDING"
	StateAssigned  TaskState = "ASSIGNED"
	StateCompleted TaskState = "COMPLETED"
	StateFailed    TaskState = "FAILED"
)

type Task struct {
	ID        string      `json:"id"`
	Payload   interface{} `json:"payload"`
	CreatedAt time.Time   `json:"created_at"`
	Timeout   time.Duration `json:"timeout"`
	State     TaskState   `json:"state"`
	WorkerID  string      `json:"worker_id,omitempty"`
}

type TaskResult struct {
	TaskID  string      `json:"task_id"`
	WorkerID string     `json:"worker_id"`
	Result  interface{} `json:"result,omitempty"`
	Error   string      `json:"error,omitempty"`
}

type TaskQueue struct {
	mu          sync.RWMutex
	tasks       map[string]*Task
	pending     []string
	completed   map[string]TaskResult
	workerTasks map[string]string // workerID -> taskID
}

func NewTaskQueue() *TaskQueue {
	return &TaskQueue{
		tasks:       make(map[string]*Task),
		completed:   make(map[string]TaskResult),
		workerTasks: make(map[string]string),
	}
}

func (q *TaskQueue) Enqueue(payload interface{}, timeout time.Duration) string {
	q.mu.Lock()
	defer q.mu.Unlock()

	taskID := uuid.New().String()
	task := &Task{
		ID:        taskID,
		Payload:   payload,
		CreatedAt: time.Now(),
		Timeout:   timeout,
		State:     StatePending,
	}

	q.tasks[taskID] = task
	q.pending = append(q.pending, taskID)
	return taskID
}

func (q *TaskQueue) AssignTask(workerID string) (*Task, error) {
	q.mu.Lock()
	defer q.mu.Unlock()

	if _, exists := q.workerTasks[workerID]; exists {
		return nil, ErrWorkerConflict
	}

	if len(q.pending) == 0 {
		return nil, ErrQueueEmpty
	}

	taskID := q.pending[0]
	q.pending = q.pending[1:]

	task, exists := q.tasks[taskID]
	if !exists {
		return nil, ErrTaskNotFound
	}

	task.State = StateAssigned
	task.WorkerID = workerID
	q.workerTasks[workerID] = taskID

	return task, nil
}

func (q *TaskQueue) CompleteTask(result TaskResult) error {
	q.mu.Lock()
	defer q.mu.Unlock()

	task, exists := q.tasks[result.TaskID]
	if !exists {
		return ErrTaskNotFound
	}

	if task.WorkerID != result.WorkerID {
		return ErrWorkerConflict
	}

	delete(q.workerTasks, result.WorkerID)
	task.State = StateCompleted
	q.completed[result.TaskID] = result
	return nil
}

func (q *TaskQueue) FailTask(taskID, workerID, errorMsg string) error {
	q.mu.Lock()
	defer q.mu.Unlock()

	task, exists := q.tasks[taskID]
	if !exists {
		return ErrTaskNotFound
	}

	if task.WorkerID != workerID {
		return ErrWorkerConflict
	}

	delete(q.workerTasks, workerID)
	task.State = StateFailed
	q.completed[taskID] = TaskResult{
		TaskID:  taskID,
		WorkerID: workerID,
		Error:   errorMsg,
	}
	return nil
}

func (q *TaskQueue) GetTaskStatus(taskID string) (TaskState, error) {
	q.mu.RLock()
	defer q.mu.RUnlock()

	task, exists := q.tasks[taskID]
	if !exists {
		return "", ErrTaskNotFound
	}

	return task.State, nil
}

func (q *TaskQueue) GetResult(taskID string) (TaskResult, error) {
	q.mu.RLock()
	defer q.mu.RUnlock()

	result, exists := q.completed[taskID]
	if !exists {
		return TaskResult{}, ErrTaskNotFound
	}

	return result, nil
}

func (q *TaskQueue) ReapExpiredTasks(ctx context.Context, interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			q.mu.Lock()
			now := time.Now()
			for workerID, taskID := range q.workerTasks {
				if task, exists := q.tasks[taskID]; exists {
					if now.Sub(task.CreatedAt) > task.Timeout {
						task.State = StateFailed
						q.completed[taskID] = TaskResult{
							TaskID:  taskID,
							WorkerID: workerID,
							Error:   "task timeout",
						}
						delete(q.workerTasks, workerID)
					}
				}
			}
			q.mu.Unlock()
		}
	}
}
""",
"""
{
  "programming_language": "GO",
  "components": [
    {
      "component_type": "PACKAGE_DEFINITION",
      "component_name": "taskqueue",
      "component_code": "package taskqueue",
      "component_description": "Root package declaration for the distributed task queue implementation, encapsulating all queue-related functionality."
    },
    {
      "component_type": "IMPORT_STATEMENT",
      "component_name": "standard_library",
      "component_code": "import (\\n\\t\\\"context\\\"\\n\\t\\\"encoding/json\\\"\\n\\t\\\"errors\\\"\\n\\t\\\"fmt\\\"\\n\\t\\\"sync\\\"\\n\\t\\\"time\\\"\\n\\n\\t\\\"github.com/google/uuid\\\"\\n)",
      "component_description": "Essential Go standard library imports for concurrency, JSON handling, error management, and UUID generation, along with external UUID package dependency."
    },
    {
      "component_type": "ERROR_DEFINITION",
      "component_name": "error_variables",
      "component_code": "var (\\n\\tErrTaskNotFound    = errors.New(\\\"task not found\\\")\\n\\tErrQueueEmpty      = errors.New(\\\"queue is empty\\\")\\n\\tErrTaskNotReady    = errors.New(\\\"task not ready for processing\\\")\\n\\tErrWorkerConflict  = errors.New(\\\"worker conflict\\\")\\n)",
      "component_description": "Sentinel error values defining all possible error conditions in the task queue system, following Go's error handling best practices."
    },
    {
      "component_type": "TYPE_DEFINITION",
      "component_name": "TaskState",
      "component_code": "type TaskState string",
      "component_description": "String-based type alias defining the state machine for task lifecycle, ensuring type safety for task state transitions."
    },
    {
      "component_type": "CONST_DEFINITION",
      "component_name": "state_constants",
      "component_code": "const (\\n\\tStatePending   TaskState = \\\"PENDING\\\"\\n\\tStateAssigned  TaskState = \\\"ASSIGNED\\\"\\n\\tStateCompleted TaskState = \\\"COMPLETED\\\"\\n\\tStateFailed    TaskState = \\\"FAILED\\\"\\n)",
      "component_description": "Complete set of possible task states as constants, representing the lifecycle of a task from creation to completion/failure."
    },
    {
      "component_type": "STRUCT_DEFINITION",
      "component_name": "Task",
      "component_code": "type Task struct {\\n\\tID        string      `json:\\\"id\\\"`\\n\\tPayload   interface{} `json:\\\"payload\\\"`\\n\\tCreatedAt time.Time   `json:\\\"created_at\\\"`\\n\\tTimeout   time.Duration `json:\\\"timeout\\\"`\\n\\tState     TaskState   `json:\\\"state\\\"`\\n\\tWorkerID  string      `json:\\\"worker_id,omitempty\\\"`\\n}",
      "component_description": "Core task structure containing all task metadata including unique ID, payload data, creation timestamp, processing timeout, current state, and optional worker assignment."
    },
    {
      "component_type": "STRUCT_DEFINITION",
      "component_name": "TaskResult",
      "component_code": "type TaskResult struct {\\n\\tTaskID  string      `json:\\\"task_id\\\"`\\n\\tWorkerID string     `json:\\\"worker_id\\\"`\\n\\tResult  interface{} `json:\\\"result,omitempty\\\"`\\n\\tError   string      `json:\\\"error,omitempty\\\"`\\n}",
      "component_description": "Result structure capturing task execution outcome, including success result or failure error message, with JSON serialization tags."
    },
    {
      "component_type": "STRUCT_DEFINITION",
      "component_name": "TaskQueue",
      "component_code": "type TaskQueue struct {\\n\\tmu          sync.RWMutex\\n\\ttasks       map[string]*Task\\n\\tpending     []string\\n\\tcompleted   map[string]TaskResult\\n\\tworkerTasks map[string]string // workerID -> taskID\\n}",
      "component_description": "Main queue structure containing all task management state with thread-safe access through RWMutex, including pending queue, in-progress tasks, and completion records."
    },
    {
      "component_type": "FUNCTION_DEFINITION",
      "component_name": "NewTaskQueue",
      "component_code": "func NewTaskQueue() *TaskQueue {\\n\\treturn &TaskQueue{\\n\\t\\ttasks:       make(map[string]*Task),\\n\\t\\tcompleted:   make(map[string]TaskResult),\\n\\t\\tworkerTasks: make(map[string]string),\\n\\t}\\n}",
      "component_description": "Constructor function initializing a new TaskQueue instance with empty collections for task storage, following Go's convention for object construction."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.Enqueue",
      "component_code": "func (q *TaskQueue) Enqueue(payload interface{}, timeout time.Duration) string {\\n\\tq.mu.Lock()\\n\\tdefer q.mu.Unlock()\\n\\n\\ttaskID := uuid.New().String()\\n\\ttask := &Task{\\n\\t\\tID:        taskID,\\n\\t\\tPayload:   payload,\\n\\t\\tCreatedAt: time.Now(),\\n\\t\\tTimeout:   timeout,\\n\\t\\tState:     StatePending,\\n\\t}\\n\\n\\tq.tasks[taskID] = task\\n\\tq.pending = append(q.pending, taskID)\\n\\treturn taskID\\n}",
      "component_description": "Thread-safe method for adding new tasks to the queue, generating UUIDs, initializing task state, and maintaining pending task list. Returns the new task ID."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.AssignTask",
      "component_code": "func (q *TaskQueue) AssignTask(workerID string) (*Task, error) {\\n\\tq.mu.Lock()\\n\\tdefer q.mu.Unlock()\\n\\n\\tif _, exists := q.workerTasks[workerID]; exists {\\n\\t\\treturn nil, ErrWorkerConflict\\n\\t}\\n\\n\\tif len(q.pending) == 0 {\\n\\t\\treturn nil, ErrQueueEmpty\\n\\t}\\n\\n\\ttaskID := q.pending[0]\\n\\tq.pending = q.pending[1:]\\n\\n\\ttask, exists := q.tasks[taskID]\\n\\tif !exists {\\n\\t\\treturn nil, ErrTaskNotFound\\n\\t}\\n\\n\\ttask.State = StateAssigned\\n\\ttask.WorkerID = workerID\\n\\tq.workerTasks[workerID] = taskID\\n\\n\\treturn task, nil\\n}",
      "component_description": "Critical section method for worker task assignment, handling worker conflicts, queue emptiness, and task state transitions with proper error returns."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.CompleteTask",
      "component_code": "func (q *TaskQueue) CompleteTask(result TaskResult) error {\\n\\tq.mu.Lock()\\n\\tdefer q.mu.Unlock()\\n\\n\\ttask, exists := q.tasks[result.TaskID]\\n\\tif !exists {\\n\\t\\treturn ErrTaskNotFound\\n\\t}\\n\\n\\tif task.WorkerID != result.WorkerID {\\n\\t\\treturn ErrWorkerConflict\\n\\t}\\n\\n\\tdelete(q.workerTasks, result.WorkerID)\\n\\ttask.State = StateCompleted\\n\\tq.completed[result.TaskID] = result\\n\\treturn nil\\n}",
      "component_description": "Task completion handler validating worker ownership, updating task state, and storing results while maintaining consistency through mutex protection."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.FailTask",
      "component_code": "func (q *TaskQueue) FailTask(taskID, workerID, errorMsg string) error {\\n\\tq.mu.Lock()\\n\\tdefer q.mu.Unlock()\\n\\n\\ttask, exists := q.tasks[taskID]\\n\\tif !exists {\\n\\t\\treturn ErrTaskNotFound\\n\\t}\\n\\n\\tif task.WorkerID != workerID {\\n\\t\\treturn ErrWorkerConflict\\n\\t}\\n\\n\\tdelete(q.workerTasks, workerID)\\n\\ttask.State = StateFailed\\n\\tq.completed[taskID] = TaskResult{\\n\\t\\tTaskID:  taskID,\\n\\t\\tWorkerID: workerID,\\n\\t\\tError:   errorMsg,\\n\\t}\\n\\treturn nil\\n}",
      "component_description": "Failure handling method similar to CompleteTask but marking tasks as failed with error messages, ensuring proper state cleanup."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.GetTaskStatus",
      "component_code": "func (q *TaskQueue) GetTaskStatus(taskID string) (TaskState, error) {\\n\\tq.mu.RLock()\\n\\tdefer q.mu.RUnlock()\\n\\n\\ttask, exists := q.tasks[taskID]\\n\\tif !exists {\\n\\t\\treturn \\\"\\\", ErrTaskNotFound\\n\\t}\\n\\n\\treturn task.State, nil\\n}",
      "component_description": "Read-only status check using RLock for better concurrent read performance, returning current task state or appropriate error."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.GetResult",
      "component_code": "func (q *TaskQueue) GetResult(taskID string) (TaskResult, error) {\\n\\tq.mu.RLock()\\n\\tdefer q.mu.RUnlock()\\n\\n\\tresult, exists := q.completed[taskID]\\n\\tif !exists {\\n\\t\\treturn TaskResult{}, ErrTaskNotFound\\n\\t}\\n\\n\\treturn result, nil\\n}",
      "component_description": "Result retrieval method providing access to completed task outcomes while maintaining thread safety with read locks."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "TaskQueue.ReapExpiredTasks",
      "component_code": "func (q *TaskQueue) ReapExpiredTasks(ctx context.Context, interval time.Duration) {\\n\\tticker := time.NewTicker(interval)\\n\\tdefer ticker.Stop()\\n\\n\\tfor {\\n\\t\\tselect {\\n\\t\\tcase <-ctx.Done():\\n\\t\\t\\treturn\\n\\t\\tcase <-ticker.C:\\n\\t\\t\\tq.mu.Lock()\\n\\t\\t\\tnow := time.Now()\\n\\t\\t\\tfor workerID, taskID := range q.workerTasks {\\n\\t\\t\\t\\tif task, exists := q.tasks[taskID]; exists {\\n\\t\\t\\t\\t\\tif now.Sub(task.CreatedAt) > task.Timeout {\\n\\t\\t\\t\\t\\t\\ttask.State = StateFailed\\n\\t\\t\\t\\t\\t\\tq.completed[taskID] = TaskResult{\\n\\t\\t\\t\\t\\t\\t\\tTaskID:  taskID,\\n\\t\\t\\t\\t\\t\\t\\tWorkerID: workerID,\\n\\t\\t\\t\\t\\t\\t\\tError:   \\\"task timeout\\\",\\n\\t\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t\\t\\tdelete(q.workerTasks, workerID)\\n\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t}\\n\\t\\t\\t}\\n\\t\\t\\tq.mu.Unlock()\\n\\t\\t}\\n\\t}\\n}",
      "component_description": "Background goroutine method for detecting and handling timed-out tasks, using context for graceful shutdown and periodic checking with mutex-protected state updates."
    }
  ],
  "overall_description": "A production-ready Go implementation of a distributed task queue featuring: thread-safe operations with mutex protection, task lifecycle management, worker coordination, timeout handling, and comprehensive error management. The design emphasizes concurrency safety, efficient locking strategies, and clear state transitions while maintaining simplicity through Go's native concurrency primitives."
}
"""]

few_shots["php"] = [
"""
<?php

declare(strict_types=1);

namespace App\Blog;

use PDO;
use DateTimeImmutable;
use Psr\Http\Message\ResponseInterface as Response;
use Psr\Http\Message\ServerRequestInterface as Request;
use Slim\Factory\AppFactory;
use Slim\Exception\HttpNotFoundException;

class BlogPost
{
    public function __construct(
        public readonly int $id,
        public readonly string $title,
        public readonly string $content,
        public readonly string $author,
        public readonly DateTimeImmutable $createdAt,
        public readonly ?DateTimeImmutable $updatedAt = null
    ) {}
}

interface BlogRepositoryInterface
{
    public function findAll(): array;
    public function findById(int $id): ?BlogPost;
    public function save(BlogPost $post): BlogPost;
    public function update(BlogPost $post): BlogPost;
    public function delete(int $id): void;
}

class PdoBlogRepository implements BlogRepositoryInterface
{
    public function __construct(private PDO $pdo) {}

    public function findAll(): array
    {
        $stmt = $this->pdo->query("SELECT * FROM posts ORDER BY created_at DESC");
        return array_map([$this, 'hydratePost'], $stmt->fetchAll());
    }

    public function findById(int $id): ?BlogPost
    {
        $stmt = $this->pdo->prepare("SELECT * FROM posts WHERE id = ?");
        $stmt->execute([$id]);
        $data = $stmt->fetch();
        
        return $data ? $this->hydratePost($data) : null;
    }

    public function save(BlogPost $post): BlogPost
    {
        $stmt = $this->pdo->prepare(
            "INSERT INTO posts (title, content, author, created_at) 
             VALUES (?, ?, ?, ?)"
        );
        
        $stmt->execute([
            $post->title,
            $post->content,
            $post->author,
            $post->createdAt->format('Y-m-d H:i:s')
        ]);
        
        return new BlogPost(
            (int)$this->pdo->lastInsertId(),
            $post->title,
            $post->content,
            $post->author,
            $post->createdAt
        );
    }

    public function update(BlogPost $post): BlogPost
    {
        $stmt = $this->pdo->prepare(
            "UPDATE posts SET 
                title = ?, 
                content = ?, 
                author = ?, 
                updated_at = ?
             WHERE id = ?"
        );
        
        $now = new DateTimeImmutable();
        $stmt->execute([
            $post->title,
            $post->content,
            $post->author,
            $now->format('Y-m-d H:i:s'),
            $post->id
        ]);
        
        return new BlogPost(
            $post->id,
            $post->title,
            $post->content,
            $post->author,
            $post->createdAt,
            $now
        );
    }

    public function delete(int $id): void
    {
        $stmt = $this->pdo->prepare("DELETE FROM posts WHERE id = ?");
        $stmt->execute([$id]);
    }

    private function hydratePost(array $data): BlogPost
    {
        return new BlogPost(
            (int)$data['id'],
            $data['title'],
            $data['content'],
            $data['author'],
            new DateTimeImmutable($data['created_at']),
            $data['updated_at'] ? new DateTimeImmutable($data['updated_at']) : null
        );
    }
}

class BlogController
{
    public function __construct(private BlogRepositoryInterface $repository) {}

    public function listPosts(Request $request, Response $response): Response
    {
        $posts = $this->repository->findAll();
        $response->getBody()->write(json_encode($posts));
        return $response->withHeader('Content-Type', 'application/json');
    }

    public function getPost(Request $request, Response $response, array $args): Response
    {
        $post = $this->repository->findById((int)$args['id']);
        
        if (!$post) {
            throw new HttpNotFoundException($request);
        }
        
        $response->getBody()->write(json_encode($post));
        return $response->withHeader('Content-Type', 'application/json');
    }

    public function createPost(Request $request, Response $response): Response
    {
        $data = json_decode((string)$request->getBody(), true);
        $post = new BlogPost(
            0,
            $data['title'],
            $data['content'],
            $data['author'],
            new DateTimeImmutable()
        );
        
        $savedPost = $this->repository->save($post);
        $response->getBody()->write(json_encode($savedPost));
        return $response
            ->withHeader('Content-Type', 'application/json')
            ->withStatus(201);
    }

    public function updatePost(Request $request, Response $response, array $args): Response
    {
        $post = $this->repository->findById((int)$args['id']);
        
        if (!$post) {
            throw new HttpNotFoundException($request);
        }
        
        $data = json_decode((string)$request->getBody(), true);
        $updatedPost = new BlogPost(
            $post->id,
            $data['title'] ?? $post->title,
            $data['content'] ?? $post->content,
            $data['author'] ?? $post->author,
            $post->createdAt
        );
        
        $result = $this->repository->update($updatedPost);
        $response->getBody()->write(json_encode($result));
        return $response->withHeader('Content-Type', 'application/json');
    }

    public function deletePost(Request $request, Response $response, array $args): Response
    {
        $this->repository->delete((int)$args['id']);
        return $response->withStatus(204);
    }
}

// Bootstrap code
$pdo = new PDO('mysql:host=localhost;dbname=blog', 'user', 'password');
$repository = new PdoBlogRepository($pdo);
$controller = new BlogController($repository);

$app = AppFactory::create();
$app->get('/posts', [$controller, 'listPosts']);
$app->get('/posts/{id}', [$controller, 'getPost']);
$app->post('/posts', [$controller, 'createPost']);
$app->put('/posts/{id}', [$controller, 'updatePost']);
$app->delete('/posts/{id}', [$controller, 'deletePost']);

$app->run();
""",
"""
{
  "programming_language": "PHP",
  "components": [
    {
      "component_type": "NAMESPACE_DEFINITION",
      "component_name": "App\\\\Blog",
      "component_code": "namespace App\\\\Blog;",
      "component_description": "PSR-4 namespace declaration for blog-related classes, following modern PHP package organization standards."
    },
    {
      "component_type": "IMPORT_STATEMENT",
      "component_name": "standard_imports",
      "component_code": "use PDO;\\nuse DateTimeImmutable;\\nuse Psr\\\\Http\\\\Message\\\\ResponseInterface as Response;\\nuse Psr\\\\Http\\\\Message\\\\ServerRequestInterface as Request;\\nuse Slim\\\\Factory\\\\AppFactory;\\nuse Slim\\\\Exception\\\\HttpNotFoundException;",
      "component_description": "Essential imports including PDO for database access, DateTime for immutable dates, PSR-7 interfaces for HTTP messages, and Slim framework components."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "BlogPost",
      "component_code": "class BlogPost\\n{\\n    public function __construct(\\n        public readonly int $id,\\n        public readonly string $title,\\n        public readonly string $content,\\n        public readonly string $author,\\n        public readonly DateTimeImmutable $createdAt,\\n        public readonly ?DateTimeImmutable $updatedAt = null\\n    ) {}\\n}",
      "component_description": "Immutable data class representing a blog post with readonly properties, leveraging PHP 8.0+'s constructor property promotion."
    },
    {
      "component_type": "INTERFACE_DEFINITION",
      "component_name": "BlogRepositoryInterface",
      "component_code": "interface BlogRepositoryInterface\\n{\\n    public function findAll(): array;\\n    public function findById(int $id): ?BlogPost;\\n    public function save(BlogPost $post): BlogPost;\\n    public function update(BlogPost $post): BlogPost;\\n    public function delete(int $id): void;\\n}",
      "component_description": "Repository interface defining CRUD operations for blog posts, following the dependency inversion principle."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "PdoBlogRepository",
      "component_code": "class PdoBlogRepository implements BlogRepositoryInterface\\n{\\n    public function __construct(private PDO $pdo) {}",
      "component_description": "Concrete PDO-based repository implementation, using constructor property promotion for dependency injection."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "PdoBlogRepository::findAll",
      "component_code": "public function findAll(): array\\n{\\n    $stmt = $this->pdo->query(\\\"SELECT * FROM posts ORDER BY created_at DESC\\\");\\n    return array_map([$this, 'hydratePost'], $stmt->fetchAll());\\n}",
      "component_description": "Fetches all blog posts from database, ordered by creation date, and hydrates them into BlogPost objects."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "PdoBlogRepository::findById",
      "component_code": "public function findById(int $id): ?BlogPost\\n{\\n    $stmt = $this->pdo->prepare(\\\"SELECT * FROM posts WHERE id = ?\\\");\\n    $stmt->execute([$id]);\\n    $data = $stmt->fetch();\\n    \\n    return $data ? $this->hydratePost($data) : null;\\n}",
      "component_description": "Finds a single blog post by ID using prepared statement, returning null if not found."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "PdoBlogRepository::save",
      "component_code": "public function save(BlogPost $post): BlogPost\\n{\\n    $stmt = $this->pdo->prepare(\\n        \\\"INSERT INTO posts (title, content, author, created_at) \\n         VALUES (?, ?, ?, ?)\\\"\\n    );\\n    \\n    $stmt->execute([\\n        $post->title,\\n        $post->content,\\n        $post->author,\\n        $post->createdAt->format('Y-m-d H:i:s')\\n    ]);\\n    \\n    return new BlogPost(\\n        (int)$this->pdo->lastInsertId(),\\n        $post->title,\\n        $post->content,\\n        $post->author,\\n        $post->createdAt\\n    );\\n}",
      "component_description": "Persists a new blog post to database and returns the saved version with generated ID."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "PdoBlogRepository::update",
      "component_code": "public function update(BlogPost $post): BlogPost\\n{\\n    $stmt = $this->pdo->prepare(\\n        \\\"UPDATE posts SET \\n            title = ?, \\n            content = ?, \\n            author = ?, \\n            updated_at = ?\\n         WHERE id = ?\\\"\\n    );\\n    \\n    $now = new DateTimeImmutable();\\n    $stmt->execute([\\n        $post->title,\\n        $post->content,\\n        $post->author,\\n        $now->format('Y-m-d H:i:s'),\\n        $post->id\\n    ]);\\n    \\n    return new BlogPost(\\n        $post->id,\\n        $post->title,\\n        $post->content,\\n        $post->author,\\n        $post->createdAt,\\n        $now\\n    );\\n}",
      "component_description": "Updates an existing blog post and sets the updated_at timestamp, returning the modified version."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "PdoBlogRepository::delete",
      "component_code": "public function delete(int $id): void\\n{\\n    $stmt = $this->pdo->prepare(\\\"DELETE FROM posts WHERE id = ?\\\");\\n    $stmt->execute([$id]);\\n}",
      "component_description": "Deletes a blog post by ID using prepared statement for safety."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "PdoBlogRepository::hydratePost",
      "component_code": "private function hydratePost(array $data): BlogPost\\n{\\n    return new BlogPost(\\n        (int)$data['id'],\\n        $data['title'],\\n        $data['content'],\\n        $data['author'],\\n        new DateTimeImmutable($data['created_at']),\\n        $data['updated_at'] ? new DateTimeImmutable($data['updated_at']) : null\\n    );\\n}",
      "component_description": "Private helper method converting database row to BlogPost object, handling optional updated_at field."
    },
    {
      "component_type": "CLASS_DEFINITION",
      "component_name": "BlogController",
      "component_code": "class BlogController\\n{\\n    public function __construct(private BlogRepositoryInterface $repository) {}",
      "component_description": "Controller class handling HTTP requests and delegating to repository, following dependency injection principles."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "BlogController::listPosts",
      "component_code": "public function listPosts(Request $request, Response $response): Response\\n{\\n    $posts = $this->repository->findAll();\\n    $response->getBody()->write(json_encode($posts));\\n    return $response->withHeader('Content-Type', 'application/json');\\n}",
      "component_description": "Action method for GET /posts route, returning all blog posts as JSON."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "BlogController::getPost",
      "component_code": "public function getPost(Request $request, Response $response, array $args): Response\\n{\\n    $post = $this->repository->findById((int)$args['id']);\\n    \\n    if (!$post) {\\n        throw new HttpNotFoundException($request);\\n    }\\n    \\n    $response->getBody()->write(json_encode($post));\\n    return $response->withHeader('Content-Type', 'application/json');\\n}",
      "component_description": "Action method for GET /posts/{id} route, returning single post or 404 if not found."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "BlogController::createPost",
      "component_code": "public function createPost(Request $request, Response $response): Response\\n{\\n    $data = json_decode((string)$request->getBody(), true);\\n    $post = new BlogPost(\\n        0,\\n        $data['title'],\\n        $data['content'],\\n        $data['author'],\\n        new DateTimeImmutable()\\n    );\\n    \\n    $savedPost = $this->repository->save($post);\\n    $response->getBody()->write(json_encode($savedPost));\\n    return $response\\n        ->withHeader('Content-Type', 'application/json')\\n        ->withStatus(201);\\n}",
      "component_description": "Action method for POST /posts route, creating new blog post and returning 201 status."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "BlogController::updatePost",
      "component_code": "public function updatePost(Request $request, Response $response, array $args): Response\\n{\\n    $post = $this->repository->findById((int)$args['id']);\\n    \\n    if (!$post) {\\n        throw new HttpNotFoundException($request);\\n    }\\n    \\n    $data = json_decode((string)$request->getBody(), true);\\n    $updatedPost = new BlogPost(\\n        $post->id,\\n        $data['title'] ?? $post->title,\\n        $data['content'] ?? $post->content,\\n        $data['author'] ?? $post->author,\\n        $post->createdAt\\n    );\\n    \\n    $result = $this->repository->update($updatedPost);\\n    $response->getBody()->write(json_encode($result));\\n    return $response->withHeader('Content-Type', 'application/json');\\n}",
      "component_description": "Action method for PUT /posts/{id} route, performing partial updates with null coalescing for optional fields."
    },
    {
      "component_type": "METHOD_DEFINITION",
      "component_name": "BlogController::deletePost",
      "component_code": "public function deletePost(Request $request, Response $response, array $args): Response\\n{\\n    $this->repository->delete((int)$args['id']);\\n    return $response->withStatus(204);\\n}",
      "component_description": "Action method for DELETE /posts/{id} route, returning empty 204 response on success."
    },
    {
      "component_type": "BOOTSTRAP_CODE",
      "component_name": "application_bootstrap",
      "component_code": "$pdo = new PDO('mysql:host=localhost;dbname=blog', 'user', 'password');\\n$repository = new PdoBlogRepository($pdo);\\n$controller = new BlogController($repository);\\n\\n$app = AppFactory::create();\\n$app->get('/posts', [$controller, 'listPosts']);\\n$app->get('/posts/{id}', [$controller, 'getPost']);\\n$app->post('/posts', [$controller, 'createPost']);\\n$app->put('/posts/{id}', [$controller, 'updatePost']);\\n$app->delete('/posts/{id}', [$controller, 'deletePost']);\\n\\n$app->run();",
      "component_description": "Application bootstrap code initializing dependencies, configuring routes, and starting the Slim application."
    }
  ],
  "overall_description": "A complete PHP backend for a blog API featuring: PSR-7/PSR-4 compliance, repository pattern with PDO, immutable data objects, RESTful routing with Slim, and proper HTTP status codes. The architecture demonstrates separation of concerns with clear layers for data access, business logic, and presentation while maintaining security through prepared statements and type safety with strict_types."
}
"""]