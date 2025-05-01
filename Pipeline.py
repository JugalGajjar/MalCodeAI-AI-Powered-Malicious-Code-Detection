import json
import sys
import torch
from mlx_lm.utils import load
from mlx_lm.generate import generate
from Phase_1_Scripts_and_Notebooks.Phase_1_few_shots import few_shots
from Phase_2_Scripts_and_Notebooks.Phase_2_few_shots import few_shots as few_shots_2

def parse_and_print_json(response):
    try:
        json_response = json.loads(response)
        return json_response
    except json.JSONDecodeError as e:
        return None
    
model, tokenizer = load(path_or_hf_repo="jugalgajjar/CSCI6366-Spring2025-MalCodeAI-Phase-1")

system_prompt = """
You are an expert code analyzer that outputs ONLY valid and parsable JSON. Strictly follow these rules:
1. Analyze the provided code completely, but ONLY for top-level components
2. Output MUST be ONLY the JSON object with no extra text, formatting, or characters
3. Use this exact structure (including only components that exist in the code):
{
    "programming_language": "<C|JAVA|PYTHON|SQL|C#|JAVASCRIPT|RUBY|TYPESCRIPT|C++|KOTLIN|RUST|GO|PHP|SCALA>",
    "components": [
      {
        "component_type": "<IMPORT_STATEMENT|INCLUDE_STATEMENT|USING_STATEMENT|FUNCTION_DEFINITION|CLASS_DEFINITION|METHOD_DEFINITION|INTERFACE_DEFINITION|STRUCT_DEFINITION|ENUM_DEFINITION|GLOBAL_CODE|MODULE_DEFINITION|PACKAGE_DEFINITION|SCHEMA_DEFINITION|PROCEDURE_DEFINITION|TRIGGER_DEFINITION|MACRO_DEFINITION>",
        "component_name": "<name>",
        "component_code": "<complete_top_level_code_segment>",
        "component_description": "<technical_description>"
      }
    ],
    "overall_description": "<complete_code_summary>"
}

Requirements:
- ONLY analyze top-level components (do NOT break down internal implementation details)
- For functions/classes/methods: include the ENTIRE definition (including all nested code)
- Never split components into internal blocks (loops, conditionals, variable declarations)
- Only include the component types listed above
- Skip all other component types completely
- Never include null or empty fields
- Escape all special characters in JSON values properly
- Include complete top-level code segments exactly as they appear
- Provide detailed technical descriptions for each extracted component
- Describe overall functionality and architecture concisely
- Ensure the output is valid JSON that can be parsed directly
- Never add comments, notes, or text outside the JSON structure
- Never use markdown formatting or code blocks
- Maintain consistent JSON structure with proper escaping
- Only output the raw JSON object with no additional text
"""

pathname = input("Enter path to the code file: ") or "Test_Code_Files/SimpleNotesApp.py"

with open(pathname, "r") as f:
    code = f.read()

few_shots_prompt = []

count = 0

for k, v in few_shots.items():
    few_shots_prompt.append({"role": "user", "content": v[0].strip()})
    few_shots_prompt.append({"role": "assistant", "content": v[1].strip()})
    count += len(v[0].strip()) + len(v[1].strip())

messages = []
messages.append({"role": "assistant", "content": system_prompt.strip()})
messages += few_shots_prompt
messages.append({"role": "user", "content": code.strip()})

prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

response = generate(
    model,
    tokenizer,
    prompt=prompt,
    max_tokens=3072
)

json_response = parse_and_print_json(response)

if json_response is None:
    print("System crashed!")
    sys.exit()

model, tokenizer = load(path_or_hf_repo="jugalgajjar/CSCI6366-Spring2025-MalCodeAI-Phase-2")

system_prompt = """
You are a highly skilled AI Security Code Auditor designed to deeply analyze source code components.

You must:
1. Identify any security vulnerabilities in each code component.
2. For each vulnerability found, provide:
    - The exact vulnerability type (e.g., "Insecure Deserialization", "Broken Authentication").
    - A CVE-like severity score on a scale of 0.0 to 10.0.
    - 3-4 realistic, step-by-step exploitation methods, showing how an attacker can practically exploit this vulnerability.
      (Each method must be described clearly, including prerequisites and the sequence of actions.)
    - Specific, actionable developer fixes to eliminate or mitigate the vulnerability.
      (Avoid vague advice like "use better security"; be exact.)

Additional Requirements:
- If no vulnerabilities are found, return an empty list for vulnerabilities.
- Maintain a consistent output format in strict JSON:
  
  {
      "component_type": "<COMPONENT_TYPE>",
      "component_name": "<COMPONENT_NAME>",
      "component_code": "<COMPONENT_CODE>",
      "component_description": "<COMPONENT_DESCRIPTION>",
      "vulnerabilities": [
          {
              "vul_type": "<VULNERABILITY_TYPE>",
              "cve_score": <FLOAT_SCORE>,
              "exploitation_methods": [
                  "<Step-by-step exploitation method 1>",
                  "<Step-by-step exploitation method 2>",
                  "<Step-by-step exploitation method 3>",
                  "<Optional: Step-by-step exploitation method 4>"
              ],
              "developer_fixes": [
                  "<Specific fix 1>",
                  "<Specific fix 2>",
                  "<Optional: fix 3>"
              ]
          },
          ...
      ]
  }

Rules:
- Include all relevant fields in the JSON output.
- Do not add any additional fields or comments.
- Do not include any non-code text or explanations.
- Be highly realistic. Only suggest exploitation methods that are practical in real-world attack scenarios.
- Be very strict in vulnerability identification — do not miss major vulnerabilities.
- Be concise but complete. No unnecessary repetition.
- Do not hallucinate vulnerabilities if the code is safe.
- Output only the structured JSON. No explanations outside JSON.

Important:
- You must think like a real security researcher.
- If a component includes multiple vulnerabilities, list each separately under the "vulnerabilities" field.

Output must be deterministic, clean, and immediately parsable by downstream systems.
"""

few_shots_prompt = []

for k, v in few_shots_2.items():
    few_shots_prompt.append({"role": "user", "content": v[0].strip()})
    few_shots_prompt.append({"role": "assistant", "content": v[1].strip()})

results = []
if json_response["components"]:
    for component in json_response["components"]:
        messages = []
        messages.append({"role": "assistant", "content": system_prompt.strip()})
        messages += few_shots_prompt
        messages.append({"role": "user", "content": str(component)})

        prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

        response = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=3072
        )

        results.append(response)

json_result = []
if results:
    for result in results:
        try:
            json_response = json.loads(result)
            json_result.append(json_response)
        except json.JSONDecodeError as e:
            continue

output_path = f"Pineline_Outputs/{pathname.split('/')[-1].split('.')[-1].upper()}_{pathname.split('/')[-1].split('.')[0]}_ANALYSIS.txt"
with open(output_path, "w") as outfile:
    for ind, i in enumerate(json_result):
        if "component_type" in i:
            if "error" in i["component_type"].lower():
                continue
            print("Component Type:", i["component_type"])
            outfile.write(f"Component Type: {i['component_type']}\n")
        if "component_name" in i:
            print("Component Name:", i["component_name"])
            outfile.write(f"Component Name: {i['component_name']}\n")
        if "component_code" in i:
            print(f"Component Code: \n{i['component_code']}")
            outfile.write(f"Component Code: \n{i['component_code']}\n")
        if "component_description" in i:
            print("Component Description:", i["component_description"])
            outfile.write(f"Component Description: {i['component_description']}\n")
        if "vulnerabilities" in i:
            print("Vulnerabilities:")
            outfile.write("Vulnerabilities:\n")
            if not i["vulnerabilities"]:
                print(" - No vulnerabilities found.")
                outfile.write(" - No vulnerabilities found.\n")
            else:
                print(" - Vulnerabilities found!")
                outfile.write(" - Vulnerabilities found!\n")
                print(" - Number of vulnerabilities:", len(i["vulnerabilities"]))
                outfile.write(f" - Number of vulnerabilities: {len(i['vulnerabilities'])}\n")
                print(" - Vulnerability Details:")
                outfile.write(" - Vulnerability Details:\n")
                for vulnerability in i["vulnerabilities"]:
                    print(f"   - Type: {vulnerability['vul_type']}")
                    outfile.write(f"   - Type: {vulnerability['vul_type']}\n")
                    print(f"   - CVE Score: {vulnerability['cve_score']}")
                    outfile.write(f"   - CVE Score: {vulnerability['cve_score']}\n")
                    print("   - Exploitation Methods:")
                    outfile.write("   - Exploitation Methods:\n")
                    for method in vulnerability["exploitation_methods"]:
                        print(f"     - {method}")
                        outfile.write(f"     - {method}\n")
                    print("   - Developer Fixes:")
                    outfile.write("   - Developer Fixes:\n")
                    for fix in vulnerability["developer_fixes"]:
                        print(f"     - {fix}")
                        outfile.write(f"     - {fix}\n")
        print("-" * 50)
        outfile.write("-" * 50 + "\n")

print(f"Data written to {output_path}")