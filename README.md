# 🚀 MalCodeAI - AI-Powered Malicious Code Detection

MalCodeAI is an AI-powered system that analyzes code files by breaking them into independent components and detecting potential malicious behavior. It compares the code's intent with a user-provided description, assigns a robustness score (1-10) to each component, and performs extensive security checks for low-scoring components.

---

## 🛠 Features

- **Code Intent Verification** – Uses Qwen2.5-Coder-3B-instruct to generate a description of the code and compare it with the user-provided description.  
- **Program Decomposition** – Splits the program into independent code components for analysis.  
- **Security Scoring** – Assigns a robustness score (1-10) to each component based on its security and fail-safety.  
- **Deep Security Inspection** – Analyzes vulnerable components (score < 5) for threats, backdoors, and exploits.  
- **Explainability & Mitigation** – Explains the possible ways in which your code can be exploited from a red-hat perspective and sugests code fixes to eradicate threats.  

---

## 📌 How It Works

1. **User Input:** Provide a code file and a short description of its intended functionality.  
2. **Code Understanding:** `deepseek-coder-1.3b-instruct` generates a description of the code, which is then compared with the user’s description using `gtr-t5-large` for semantic similarity.  
3. **Code Splitting:** The system extracts independent code components using program slicing and AST-based analysis.  
4. **Security Analysis:** Each component is assigned a robustness score based on static and AI-powered security analysis.  
5. **Detailed Security Scrutiny:** Components scoring below 5 undergo further checks to detect potential malicious behavior and recommend fixes.  

---

## 📦 Installation

### Clone the Repository
```bash
git clone https://github.com/JugalGajjar/MalCodeAI.git
cd MalCodeAI
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Usage

```python
from malcodeai import MalCodeAI

# Initialize the AI system
malcode = MalCodeAI()

# Provide code and description
code_snippet = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
"""

user_description = "This function calculates the factorial of a number."

# Run the analysis
result = malcode.analyze_code(code_snippet, user_description)

# Print results
print(result)
```

---

## 🧠 Technologies Used

- **[DeepSeek Coder](https://arxiv.org/abs/2401.14196)** – Code understanding and description generation.
- **[GTR-T5-Large](https://arxiv.org/abs/2112.07899)** – Advanced similarity model for description comparison.
- **AST Parsing & Graph Analysis** – Extracts independent code components.
- **Static & AI Security Analysis** – Detects vulnerabilities and malicious behavior.

---

## 📄 Roadmap

- Implement dynamic execution analysis for deeper security insights.
- Expand support for multiple programming languages.
- Train a custom security model on a large dataset of vulnerable code.
- Build a web-based UI for easier interaction.

---


## 🐜 License

This project is licensed under the MIT License.

---

## 📩 Contact

- Created by **Jugal Gajjar**
- LinkedIn: [Link](https://www.linkedin.com/in/jugal-gajjar/)
