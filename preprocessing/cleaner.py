import re
from utils.logger import get_logger
import ftfy

logger = get_logger(__name__)

def fix_encoding(text: str) -> str:
    """
    Fixes text encoding issues using ftfy library.
    """
    fixed_text = ftfy.fix_text(text)
    if fixed_text != text:
        logger.info("Fixed encoding issues in text.")
    return fixed_text

def remove_references_section(text: str) -> str:
    """
    Cuts off everything from a 'References' or 'Bibliography'.
    """
    pattern = r"\n\s*(references|bibliography)\s*\n"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        logger.info(f"Removed references section {len(text) - match.start()} chars cut.")
        return text[:match.start()]

    return text

def normalize_whitespaces(text: str) -> str:
    """Collapses 3+ consecutive newlines down to 2, strips trailing spaces."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[\t]+\n", "\n", text)

    return text.strip()

def fix_missing_spaces(text: str) -> str:
    """
    Inserts a space where a lowercase letter is immediately followed by
    an uppercase letter with no space - a common PDF extraction artifact
    where two separate text blocks got concatenated.
    """
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

def remove_numbered_reference_lines(text: str) -> str:
    """ 
    Remove inline citations
    e.g. 46. Sutton, R. S. & Barto...
    """
    lines = text.split("\n")
    cleaned_lines = [line for line in lines if not re.match(r"^\d{1,3}\.\s+[A-Z]", line.strip())]
    return "\n".join(cleaned_lines)

def remove_inline_citations(text: str) -> str:
    """
    Removes inline citation markers - single [1], lists [4, 17, 25],
    and ranges [4-6] or [4–6] (en-dash).
    """
    pattern = r"\s*\[\d+(?:\s*[-–,]\s*\d+)*\]"
    return re.sub(pattern, "", text)


def clean_text(text: str) -> str:
    text = fix_encoding(text)
    text = remove_references_section(text)
    text = remove_numbered_reference_lines(text)
    text = remove_inline_citations(text)
    text = fix_missing_spaces(text)
    text = normalize_whitespaces(text)
    return text