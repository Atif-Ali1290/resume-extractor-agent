
import os
import json
import pdfplumber
import openpyxl
import sys
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# ------------------------ Gemini OpenAI-Compatible Config ------------------------
gemini_api_key = "AIzaSyB-bEr3YaXdlbmgVqBv4Ms7CLkhrKwM-9A"

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(
    name="ResumeExtractor",
    instructions="""
You are a helpful assistant. Given a resume text, extract the following information:
- Candidate Name
- Phone No.
- Email
- Education
- Program
- Institution
- Location
- Programming Skills
- Experience

Respond only in JSON format like:
{
  "Candidate Name": "",
  "Phone No.": "",
  "Email": "",
  "Education": "",
  "Program": "",
  "Institution": "",
  "Location": "",
  "Programming Skills": "",
  "Experience": ""
}
"""
)

# ------------------------ PDF Reader ------------------------
def read_pdfs_from_folder(folder_path):
    data = {}
    if not os.path.isdir(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return data

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            try:
                with pdfplumber.open(os.path.join(folder_path, file)) as pdf:
                    text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    data[file] = text
            except Exception as e:
                print(f"⚠ Could not read {file}: {e}")
    return data

# ------------------------ Save to Excel ------------------------
def save_to_excel(data_list, filename="candidates.xlsx"):
    headers = [
        "Candidate Name", "Phone No.", "Email", "Education",
        "Program", "Institution", "Location", "Programming Skills", "Experience"
    ]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Candidates"
    ws.append(headers)

    for data in data_list:
        if data:
            row = [data.get(h, "") for h in headers]
            ws.append(row)

    wb.save(filename)
    print(f"✅ Saved to {filename}")

# ------------------------ Main Pipeline ------------------------
def main():
    # Support dynamic folder path via command line
    folder = sys.argv[1] if len(sys.argv) > 1 else "/home/muhammad-noman/PDFS-Write"
    print(f"📂 Scanning folder: {folder}")
    pdfs = read_pdfs_from_folder(folder)

    if not pdfs:
        print("❌ No valid PDFs found.")
        return

    results = []
    for file_name, resume_text in pdfs.items():
        print(f"🔍 Processing: {file_name}")
        print(f"[DEBUG] Resume text being sent to agent:\n{resume_text[:500]}\n---END---")
        try:
            result = Runner.run_sync(agent, resume_text, run_config=config)
            print(f"[DEBUG] Raw agent output:\n{result.final_output}")
            # Remove markdown code block markers if present
            raw_output = result.final_output.strip()
            if raw_output.startswith('json'):
                raw_output = raw_output[len('json'):].strip()
            if raw_output.endswith('```'):
                raw_output = raw_output[:-3].strip()
            extracted_json = json.loads(raw_output)
            results.append(extracted_json)
        except Exception as e:
            print(f"❌ Error with {file_name}: {e}")

    save_to_excel(results)

# ------------------------ Run It ------------------------
if _name_ == "_main_":
    main()