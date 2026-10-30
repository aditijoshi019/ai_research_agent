from app.llm import get_llm

llm = get_llm()

response = llm.invoke("Explain RAG in two sentences.")

print("Model response:")
print(response.content)