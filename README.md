# Code-Reviewer

This application takes short Python code snippets as input and uses an LLM API (OpenAI) to generate code review comments. The script logs the responses and assigns a basic quality flag to each snippet (e.g., “Good,” “Needs Improvement,” or “Buggy”).

## Approach
For this project, I began with a dataset of 1,000 buggy code snippets paired with their corrected versions. I collected the dataset from Kaggle, [Python Code Bug & Fix Pairs](https://www.kaggle.com/datasets/shamimhasan8/python-code-bug-and-fix-pairs). I combined the buggy and fixed code columns into a single collection and shuffled the entries to mix both clean and buggy code. The resulting data was saved in a file named code_snippets.csv.

The main application loads this CSV into a Pandas DataFrame and processes the first five rows. Each snippet is reviewed in sequence, with the results stored in a list. Once the iteration is complete, the review list is converted into a Pandas DataFrame and exported to a file named output_file.csv.

This project was initially created in **Python 3.11**. To run the project, the following dependencies are required:
- `pandas`
- `python-dotenv`
- `openai`
- `notebook`

All dependencies are listed in `requirements.txt`.

## Project Structure 

```
  .
├── app                     # Main Application
│   └── app.py
├── data                    # Dataset with 1000 code snippets
│   └── code_bug_fix_pairs.csv
├── notebooks               # Exploratory notebook
│   └── starter_file_analysis.ipynb
├── requirements.txt        # Python dependencies
├── reflection.txt          # Commets on ways to improve the application
├── code_snippets.csv       # Code snippets to be reviewed
├── output_file.csv         # Output CSV file with code reviews
└── README.md               # You're here!

```


## Installation Guide
### 1. Clone the repository

```bash
git clone https://github.com/mait002/Code-Reviewer.git
cd Code-Reviewer
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash 
pip install -r requirements.txt
```

### 4. Set up the .env file
Create a .env file in the root of the repo with the following content:
```env
OPENAI_API_KEY=your-openai-api-key
```

### 5. Run the App
```bash
cd app
python app.py
```

Hope you can get your buggy codes reviewed! 😊


