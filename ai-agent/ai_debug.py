import os
import subprocess
from openai import OpenAI

# 🔐 Set your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 🔹 Step 1: Get logs from Kubernetes
def get_logs():
    try:
        cmd = "kubectl logs deployment/flask-app --tail=50"
        #cmd = "kubectl logs deployment/flask-app | findstr /i error"   (to find only error logs)
        logs = subprocess.getoutput(cmd)
        return logs
    except Exception as e:
        return f"Error fetching logs: {str(e)}"


# 🔹 Step 2: Analyze logs using AI
def analyze_logs(logs):
    prompt = f"""
    You are a DevOps expert.

    Analyze the following Kubernetes logs and:
    1. Identify the root cause of the issue
    2. Suggest a clear fix

    Logs:
    {logs}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# 🔹 Step 3: Main execution
if __name__ == "__main__":
    print("Fetching logs from Kubernetes...\n")

    logs = get_logs()
    print("==== RAW LOGS ====\n")
    print(logs)

    print("\n==== AI ANALYSIS ====\n")
    result = analyze_logs(logs)
    print(result)