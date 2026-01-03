from processing import extract_text_from_pdf
from chunking import chunk_text
from vector_store import convert_to_embeddings, create_faiss_index, search_faiss_index
from qa_engine import ask_question

def main():
    #Path to the PDF document
    pdf_path="rag_test_document.pdf"

    #Extract text from the PDF
    text=extract_text_from_pdf(pdf_path)

    #Break text into smaller chunks
    text_chunks=chunk_text(text)

    #Create embeddings and build FAISS index
    embeddings=convert_to_embeddings(text_chunks)
    index=create_faiss_index(embeddings)

    #Keep taking questions from the user
    while True:
        question=input("\nAsk your question (or type 'exit' to quit): ")
        if question.lower()=="exit":
            break

        #Retrieve relevant chunks for the question
        relevant_chunks=search_faiss_index(index,question,text_chunks,top_k=3)

        #Do not answer if nothing relevant is found
        if not relevant_chunks:
            print("No relevant information found in the document.")
            continue

        #Generate answer using retrieved context
        answer=ask_question(question,relevant_chunks)
        print(f"\nAnswer: {answer}")

#Run the pipeline   
if __name__=="__main__":
    main()