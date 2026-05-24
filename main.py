from dotenv import load_dotenv
from langchain_google_genai import
chatGoogleGenrativeAI

load_dotenv()

llm=chatGoogleGenrativeAI(
    model="genai-1.5-flash"
)
response=llm.invoke("what is the capital of france...?")

print(response)