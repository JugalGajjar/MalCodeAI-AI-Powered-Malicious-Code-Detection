# MalCodeAI: AI-Powered Malicious Code Detection

This project aimed to develop an AI-driven malicious code detection system with explainability, and language-agnostic capabilities (detect malicious code across multiple programming languages without depending on the syntax or structure of just one language), making it scalable and adaptable for different coding environments.

This project uses a two-part pipeline to identify vulnerable code within software components. The first model breaks down code files (trained on a small subset of the GitHub dataset), while the second model analyzes each component for vulnerabilities using synthetic data combined with CVE and Exploit DB information, providing exploit details and fixes. The tool outputs component-specific analysis to the console and a text file.

---

## Features:
 
- **Code Decomposition** – Splits the program into independent code components for analysis.  
- **Security Scoring** – Assigns a CVE score (0-10) to each component based on its security and fail-safety.  
- **Deep Security Inspection** – Analyzes vulnerable components for threats, backdoors, and exploits.  
- **Explainability & Mitigation** – Explains the possible ways in which your code can be exploited from a red-hat perspective and sugests code fixes to eradicate threats.  

---

## How It Works?

1. **User Input:** Provide path of the code file you want to analyze.
2. **Code Understanding:** Fine-tuned `Qwen2.5-Coder-3B-Instruct` model extracts independent code components and generates a description of the code.
4. **Security Analysis:** Each component is assigned a tentative CVSS score based on static and AI-powered security analysis.  
5. **Detailed Security Scrutiny:** Components with vulnerabilities undergo further checks by another fine-tuned `Qwen2.5-Coder-3B-Instruct` model to detect potential malicious behavior and recommend fixes.  

---

## Installation:

### Clone the Repository
```bash
git clone https://github.com/JugalGajjar/MalCodeAI-AI-Powered-Malicious-Code-Detection.git
cd MalCodeAI-AI-Powered-Malicious-Code-Detection
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage:

1. Execute the main pipeline.
```bash

python Pipeline.py

```

2. Enter the path of the code file you want to analyze. <br>
NOTE: Some safe and unsafe code files are available in the 'Test_Code_Files' directory for testing purposes.

3. The analysis output will be displayed on the console as well as stored in the 'Output_Files' directory.

---

## Experimentations:

### Phase 1
Base Model: Qwen2.5-Coder-3B-Instruct | Fine Tuning Technique: LoRA | Framework Used: MLX <br>
Base Hyperparameters: Iterations = 100, Trainable Layers = 6, Learning Rate = 2 e-5, and Max. Tokens = 3072

#### Iterations: (Keeping others’ base value)
Init. Valid Loss: 0.865
- 100 iter. (0.470)
- 150 iter. (0.417)
- 200 iter. (0.399)

#### Trainable Layers: (Keeping others’ base value)
Init. Valid Loss: 0.865
- 6 layers (0.470)
- 5 layers (0.504)
- 4 layers (0.555)

#### Learning Rate: (Keeping others’ base value)
Init. Valid Loss: 0.865
- 2 e-5 (0.470)
- 3 e-5 (0.415)
- 4 e-5 (0.397)

Final chosen parameters: Iterations = 200, Trainable Layers = 6, Learning Rate = 2 e-5, and Max. Tokens = 3072 <br>
Final Model link: [Hugging Face](https://huggingface.co/jugalgajjar/CSCI6366-Spring2025-MalCodeAI-Phase-1)

### Phase 2
Base Model: Qwen2.5-Coder-3B-Instruct | Fine Tuning Technique: LoRA | Framework Used: MLX <br>
Base Hyperparameters: Iterations = 100, Trainable Layers = 6, Learning Rate = 2 e-5, and Max. Tokens = 3072

#### Iterations: (Keeping others’ base value)
Init Valid Loss: 1.639
- 100 iter. (0.325)
- 150 iter. (0.222)
- 200 iter. (0.203)

#### Trainable Layers: (Keeping others’ base value)
Init Valid Loss: 1.639
- 6 layers (0.325)
- 5 layers (0.442)
- 4 layers (0.585)

#### Learning Rate: (Keeping others’ base value)
Init Valid Loss: 1.639
- 2 e-5 (0.325)
- 3 e-5 (0.221)
- 4 e-5 (0.199)

Final chosen parameters: Iterations = 100, Trainable Layers = 6, Learning Rate = 4 e-5, and Max. Tokens = 3072 <br>
Final Model link: [Hugging Face](https://huggingface.co/jugalgajjar/CSCI6366-Spring2025-MalCodeAI-Phase-2)

---

## Results:

**Quantitative**: Cross-Entropy Loss <br>
**Qualitative**: Developer feedback on the usefulness, readability, and interpretability of the analysis.

### Usefulness Score
All Feedback Scores: 8, 7, 9, 6, 9, 8, 9, 9, 10, 10, 5, 9, 6, 9, 7
- Mean		-	8.06
- Median	-	9.0
- Mode		-	9
- Std. Dev.	-	1.48
- Minimum	-	5
- Maximum	-	10

### Readability Score
All Feedback Scores: 10, 10, 10, 10, 9, 8, 10, 6, 7, 10, 5, 5, 2, 1, 2
- Mean		-	7.00
- Median    -	8.0
- Mode		-	10
- Std. Dev.	-	3.20
- Minimum	-	1
- Maximum	-	10

### Interpretability Score
All Feedback Scores: 8, 8, 7, 8, 8, 6, 6, 8, 7, 8, 9, 7, 7, 10, 4
- Mean		-	7.40
- Median	-	8.0
- Mode		-	8
- Std. Dev.	-	1.36
- Minimum	-	4
- Maximum	-	10

---

## License:

This project is licensed under the MIT License.
