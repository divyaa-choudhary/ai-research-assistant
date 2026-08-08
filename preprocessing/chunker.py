from utils.logger import get_logger
import re

logger = get_logger(__name__)

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap = 100) -> list[str]:
    """
    Splits text into overlapping chunks, preferring paragraph breaks,
    then sentence breaks, then word breaks - in that priority order.
    """
    if len(text) <= chunk_size and not text.strip():
        return [text]

    seperators = ["\n\n", ". ", " "] #seperate by (hierarchial order) paragraph, then sentence, then word
    chunks = _recursive_split(text, chunk_size, seperators)
    #chunks = _add_overlap(chunks, chunk_overlap)
    chunks = _add_overlap_by_sentence(chunks, chunk_overlap)
    logger.info(f"Split text ({len(text)} chars)  into {len(chunks)} chunks")
    return chunks


def _recursive_split(text: str, chunk_size: int, seperators: list[str]) -> list[str]:
    """
    Recursively splits text into chunks of size chunk_size, using the provided separators.
    """
    seperator = seperators[0] 
    remaining_seperators = seperators[1:] if len(seperators) > 1 else [" "] #if no more seperators, just split by space

    pieces = text.split(seperator)
    chunks = []
    current_chunk = ""

    for piece in pieces:
        candidate_chunk = current_chunk + seperator + piece if current_chunk else piece

        if len(candidate_chunk) <= chunk_size:
            current_chunk = candidate_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            if len(piece) > chunk_size and remaining_seperators:
                # If the piece itself is too large, split it further using the next separator
                chunks.extend(_recursive_split(piece, chunk_size, remaining_seperators))
                current_chunk = ""
            else:
                current_chunk = piece

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def _add_overlap_by_sentence(chunks: list[str], overlap: int) -> list[str]:
    """
    Overlaps chunks by carrying whole sentences from the end of the
    previous chunk, instead of raw characters or words.
    """
    if len(chunks) <= 1:
        return chunks

    overlapped = [chunks[0]]

    for i in range(1, len(chunks)):
        prev_chunk = chunks[i - 1]

        # Split into sentences - simple rule: split after ". ", "! ", "? "
        sentences = re.split(r"(?<=[.!?])\s+", prev_chunk)

        # Walk backward through sentences, accumulating until ~overlap chars
        prev_tail = ""
        for sentence in reversed(sentences):
            if not prev_tail:
                prev_tail = sentence
                continue
            candidate = sentence + " " + prev_tail if prev_tail else sentence
            if len(candidate) > overlap:
                break
            prev_tail = candidate

        overlapped.append(prev_tail + " " + chunks[i] if prev_tail else chunks[i])

    return overlapped

# def _add_overlap_by_character(chunks: list[str], overlap: int) -> list[str]:
#     """
#     Adds overlap between chunks to ensure context is preserved.
#     """
#     if len(chunks) <= 1:
#         return chunks

#     overlapped = [chunks[0]]
#     for i in range(1, len(chunks)):
#         prev_trail = chunks[i-1][-overlap:]
#         overlapped.append(prev_trail + chunks[i])
#     return overlapped