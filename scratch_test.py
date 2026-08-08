from loaders.pdf_loader import load_all_pdfs, load_pdf_text
from preprocessing.cleaner import clean_text
from services.ingestion import process_all_papers


documents = load_all_pdfs("research_papers")
print(f"Loaded {len(documents)} papers")

def clean_documents():
    cleaned_documents = []

    for doc in documents:
        if(doc["file_name"] == "2607.28287v1.pdf"):
            original_text = doc["text"]
            cleaned = clean_text(original_text)

            original_len = len(original_text)
            cleaned_len = len(cleaned)

            reduction = original_len - cleaned_len
            reduction_pct = (reduction / original_len * 100) if original_len > 0 else 0

            cleaned_documents.append({
                "file_name": doc["file_name"],
                "text": cleaned
            })

            print(f"{doc['file_name']}: {original_len} -> {cleaned_len} chars ({reduction_pct: .1f}% removed)")
            with open("paper_comparison.txt", "w", encoding="utf-8") as file:
                # Write a clear metadata header
                file.write("=" * 60 + "\n")
                file.write(f"FILE NAME: {doc['file_name']}\n")
                file.write(f"STATS: {original_len} -> {cleaned_len} chars ({reduction_pct:.1f}% removed)\n")
                file.write("=" * 60 + "\n\n")
                
                # Write the original raw text
                file.write("--- ORIGINAL TEXT ---\n")
                file.write(original_text + "\n\n")
                
                # Write the cleaned text
                file.write("--- CLEANED TEXT ---\n")
                file.write(cleaned + "\n")

chunks = process_all_papers("research_papers")
print(f"Total chunks: {len(chunks)}")
print(f"Sample chunk 6: \n{chunks[6]['text']}")
print(f"Sample chunk 7: \n{chunks[7]['text']}")
print(f"Sample chunk 8: \n{chunks[8]['text']}")
print(f"Sample chunk 9: {chunks[9]['text']}")
print(f"Sample chunk 10: {chunks[10]['text']}")
print(f"Sample chunk 11: {chunks[11]['text']}")
print(f"Processed {len(documents)} papers into {len(chunks)} chunks")

