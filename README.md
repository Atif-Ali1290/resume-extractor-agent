#  Resume Extractor using Gemini API and Google Sheets Integration

This project automates the extraction of structured information from resumes in PDF format. It uses Google’s **Gemini 2.0 model** (OpenAI-compatible API) to parse CVs and then exports the relevant candidate data into an **Excel spreadsheet** (and optionally Google Sheets).

---

##  Features

-  Automatically scans a folder for `.pdf` resumes  
-  Uses Gemini AI to extract structured fields like:
  - Name, Email, Phone
  - Education, Degree, Institute
  - Skills & Experience  
-  Saves data into an Excel file  
-  Modular and easily extendable to connect with Google Sheets API or a database

---

##  Tech Stack

- Python 3.x  
- [`pdfplumber`](https://pypi.org/project/pdfplumber/) – for reading PDF content  
- [`openpyxl`](https://pypi.org/project/openpyxl/) – for writing Excel files  
- OpenAI-compatible [Gemini API](https://ai.google.dev/)  
- Custom LLM Agent Architecture

---

##  Folder Structure

```
resume-extractor/
│
├── agents/
│   └── run.py              # Agent runner logic
├── resume_extractor.py     # Main script
├── candidates.xlsx         # Output Excel file
├── README.md               # Project documentation
```

---

##  How to Run

### 1. Install Dependencies

```bash
pip install pdfplumber openpyxl
```

### 2. Run the Script

```bash
python resume_extractor.py /path/to/pdf/folder
```

> Replace `/path/to/pdf/folder` with the actual folder path where your CV PDFs are stored.

---

##  Sample Output

```json
{
  "Candidate Name": "Ali Raza",
  "Phone No": "+92300XXXXXXX",
  "Email": "ali@example.com",
  "Education": "BS in Computer Science",
  "Program": "Bachelor",
  "Institution": "ABC University",
  "Location": "Lahore, Pakistan",
  "Programming Skills": "Python, Java, SQL",
  "Experience": "2 years at XYZ Corp"
}
```

---

##  Notes

- You must have a valid **Gemini API key** to run this project.
- To use **Google Sheets** instead of Excel, integrate with libraries like:
  - [`gspread`](https://pypi.org/project/gspread/)
  - [`google-auth`](https://pypi.org/project/google-auth/)

---

##  License

- This project is licensed under the **MIT License**. Feel free to use and adapt it.
