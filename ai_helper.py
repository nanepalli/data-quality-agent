from openai import OpenAI

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY"
)

def explain_issue(issue, rows):

    prompt = f"""
You are a data quality expert.

Issue:
{issue}

Bad rows:
{rows}

Explain:
1. Why this is a problem.
2. Suggest a fix.
3. Give Pandas code.
4. Give SQL code.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content