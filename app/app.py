from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import json, re

load_dotenv()

client = OpenAI()

#Load input file with code snippets
df = pd.read_csv("code_snippets.csv", header=0)
print("Successfully loaded the input file!")

#Prepare the code reviewer
res_df_cols = ["id", "code snippet", "summary", "line-specific comments", "quality flag"]
FLAGS = {"Good", "Needs Improvement", "Buggy"}
code_reviewed_rows = []
for _, row in df.head(5).iterrows():
    code_id = row["id"]
    code_snippet = row["code snippet"]

    prompt = (
        "You are a code reviewer. Analyze the following Python code snippet and return JSON with keys:\n"
        '- "summary": a brief quality summary (1-3 sentences)\n'
        '- "line-specific comments": Line-specific comments for any issues.\n'
        '- "quality flag": one of "Good", "Needs Improvement", "Buggy"\n\n'
        f"CODE:\n{code_snippet}"
    )

    try:
        response = client.responses.create(model='gpt-5-nano', input=prompt)
        print(response)
        txt = response.output_text.strip()

        try:
            data = json.loads(txt)
            print("Successfully parsed JSON!")
        except json.JSONDecodeError:
            m = re.search(r"\{.*?\}", txt, flags=re.S)

            if m:
                try:
                    data = json.loads(m.group(0))
                except json.JSONDecodeError:
                    data = {"summary": txt, "line-specific comments": [], "quality flag": ""}
            else:
                data = {"summary": txt, "line-specific comments": [], "quality flag": ""}

        summary = str(data.get("summary", "")).strip()
        comments = data.get("line-specific comments") or data.get("line comments") or []
        comments_out = json.dumps(comments, ensure_ascii=False) if isinstance(comments, (list, dict)) else str(comments)
        flag = str(data.get("quality flag", "")).strip()

        if flag not in FLAGS:
            m = re.search(r"\b(Good|Needs Improvement|Buggy)\b", txt, flags=re.I)
            flag = m.group(1).title() if m else "Needs Improvement"

    except Exception as e:
        summary = f"Error: {e}"
        comments_out = "[]"
        flag = "Needs Improvement"

    code_reviewed_rows.append({
        "id": code_id,
        "code snippet": code_snippet,
        "summary": summary,
        "line-specific comments": comments_out,
        "quality flag": flag,
    }
    )
    print("Successfully appended!")

#Create output file with code reviews
res_df = pd.DataFrame(code_reviewed_rows, columns=res_df_cols)
res_df.to_csv("output_file.csv", index=False)
print("Successfully saved the output file!")


