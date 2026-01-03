def chunk_text(text,chunk_size=500,chunk_overlap=100):
    #Splits text into overlapping chunks.
    chunks=[]
    stride=chunk_size-chunk_overlap
    current_position=0
    #Slide over the text and create overlapping chunks
    while current_position<len(text):
        chunk=text[current_position:current_position+chunk_size]
        if not chunk:
            break
        chunks.append(chunk)
        current_position+=stride
    return chunks

#Used only for local debugging
if __name__=="__main__":
    sample_text="This is a sample text to demonstrate the chunking functionality."*50
    chunks=chunk_text(sample_text,chunk_size=100,chunk_overlap=20)
    for i,chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")