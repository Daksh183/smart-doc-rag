import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

#Load the embedding model once at startup
model=SentenceTransformer('all-MiniLM-L6-v2')

def convert_to_embeddings(texts,batch_size=32):
    #Converts a list of text chunks into normalized embedding vectors.
    #Normalization allows inner product search to behave like cosine similarity.
    
    embeddings=model.encode(texts,batch_size=batch_size,show_progress_bar=True)
    embeddings=np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)
    return embeddings

def create_faiss_index(embeddings):
    #Creates a FAISS index using inner product similarity.

    dimension=embeddings.shape[1]
    index=faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index

def search_faiss_index(index,query,text_chunks,top_k=5,threshold=0.1):
    #Searches FAISS index and returns chunks only if similarity exceeds threshold.

    query_embedding=model.encode([query])
    query_embedding=np.array(query_embedding).astype("float32")
    faiss.normalize_L2(query_embedding)
    scores,indices=index.search(query_embedding,top_k)

    results=[]
    #scores[0] = similarity scores for top_k results
    #indices[0] = corresponding indices
    for score,i in zip(scores[0],indices[0]):

        if score>=threshold and i<len(text_chunks):
            results.append(text_chunks[i])

    return results

#Used only for local testing and debugging
if __name__=="__main__":
    chunks = [
        "The capital of France is Paris.",
        "The Earth revolves around the Sun.",
        "The RTX 4050 is a mid-range GPU."
    ]
    embeddings=convert_to_embeddings(chunks)
    index=create_faiss_index(embeddings)
    query="what is capital of france?"
    query_embedding=convert_to_embeddings([query])
    query_embedding=np.array(query_embedding).astype("float32")
    faiss.normalize_L2(query_embedding)
    scores,indices=index.search(query_embedding,2)
    print("Similarity Scores:")
    for score,i in zip(scores[0],indices[0]):
        print(f"Score: {score:.4f}, Chunk: {chunks[i]}")