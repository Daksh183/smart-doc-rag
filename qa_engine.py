import requests
import json

#Ollama runs as a local HTTP server on this endpoint
OLLAMA_URL="http://localhost:11434/api/generate"
MODEL_NAME="llama3.1:8b"

def ask_question(question,context_chunks):
    #Generates an answer to the given question using only the retrieved context.
    context="\n".join(context_chunks)
    prompt=f"""Use the context to answer the question. You may rephrase and explain the information in your own words to make the answer clear and natural.
    Do NOT add any new information that is not present in the context. If the answer is not present, say: "Not found in the document." This is very important.
    Answer only from pdf and no other source or any prior knowledge.
    Context:
    {context}
    
    Question: 
    {question}

    Answer:""".strip()
    
    #Request payload for Ollama
    payload={"model":MODEL_NAME,"prompt":prompt,"stream":False,}
    response=requests.post(OLLAMA_URL,headers={"Content-Type":"application/json"},data=json.dumps(payload))
    
    #Raise error if request fails
    if response.status_code!=200:
        raise RuntimeError(response.text)
    
    #Return the generated answer
    return response.json().get("response","").strip()