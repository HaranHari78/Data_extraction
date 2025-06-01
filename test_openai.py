import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Initialize client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

model = os.getenv("AZURE_OPENAI_MODEL")

# Try a test chat request
try:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Are you working?"}]
    )
    print("[✅ SUCCESS] Response:", response.choices[0].message.content)
except Exception as e:
    print("[❌ ERROR]", str(e))
