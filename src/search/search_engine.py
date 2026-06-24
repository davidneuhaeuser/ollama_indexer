from pathlib import Path
from ollama import chat
import hashlib
from config import *


def split_txt_file(file_path: Path, max_chars: int = MAX_CHARS_PER_CHUNKED_FILE) -> list[str]:
    """
    Splits a text file into chunks of at most max_chars characters.
    Returns a list of file paths (original or generated chunk files).
    """
    content = file_path.read_text(encoding="utf-8")

    # No split needed
    if len(content) <= max_chars:
        return [str(file_path)]

    chunk_files: list[str] = []

    for i in range(0, len(content), max_chars):
        chunk = content[i:i + max_chars]

        chunk_path = file_path.with_name(
            f"{file_path.stem}_part{len(chunk_files) + 1}{file_path.suffix}"
        )

        chunk_path.write_text(chunk, encoding="utf-8")
        chunk_files.append(str(chunk_path))

    return chunk_files


def propmt_for_keywords(txt_file_name: str) -> str:
    with open(txt_file_name, "r", encoding="utf-8") as f:
            txt_file_content = f.read()

            prompt: str = f"""
            {SYSTEM_PROMPT}

            Context:
            {txt_file_content}
            """

            response = chat(
                model=MODEL,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
            )

    return response['message']['content']


def prepare_keywords(keywords: str) -> str:
    return keywords.strip().replace(" ", "").lower()


def add_to_index(entry: str, file_name: str, index_file_path: str) -> None:
    with open(Path(index_file_path), "a", encoding="utf-8") as f:
        f.write(f"{entry}:{file_name}\n")


def split_txt_files_of_dir(dir: str) -> None:
    directory = Path(dir)

    for txt_file in directory.glob("*.txt"):
        split_txt_file(txt_file)


def get_txt_file_names_of_dir(dir: str) -> list[str]:
    directory = Path(dir)

    txt_file_names: list[str] = []

    for txt_file_name in directory.glob("*.txt"):
        txt_file_names.append(str(txt_file_name))

    return txt_file_names

def read_index(index_file_name: str = INDEX_FILE_PATH) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    with open(index_file_name, "r", encoding="utf-8") as f:
        for line in f.readlines():
            
            keywords_file_split = line.split(":")
            keywords = keywords_file_split[0].split(",")
            file = keywords_file_split[1]

            # index.append({file, keywords})
            index[file] = keywords
            
            pass
    return index

"""
TODO:   replace " with '
TODO:   how will the llm make use of index?
        > user enters question
        > py extracts indexed keywords from question
        > py adds respective files to context
        > py prompts llm with question and new context

TODO    maye set ???

TODO    Take Path everywhere and convert string to path only once in `main`

TODO    add header with checksum to file or keep checksum per indexed file 
        in order to re-index changed files

TODO    decide on how to index and chunk files in the first place...
        there should not be a large file split into multiple files, which
        would mean that if one char changes in the large file, full file
        has to be cunked and re-indexed....

TODO    read file into ram instead of file
"""


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os

def main():
    
    # txt_file_names = get_txt_file_names_of_dir(WIKI_DIR)
    txt_file_names = ["whatsapp_chat_part1.txt", "whatsapp_chat_part2.txt"]
    # txt_file_names = split_txt_files_of_dir(WIKI_DIR)

    txt_file_names = ["decrypted.txt"]

    for txt_file_name in txt_file_names:

        keywords: str = propmt_for_keywords(WIKI_DIR + txt_file_name)

        keywords = prepare_keywords(keywords)

        add_to_index(keywords, txt_file_name, INDEX_FILE_PATH)

        print(f"indexed {txt_file_name} with: {keywords}")

if __name__ == "__main__":
    main()

def directory_checksum(directory: str, algorithm="sha256"):
    h = hashlib.new(algorithm)
    root = Path(directory)

    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel_path = path.relative_to(root)

            # Include filename/path in the checksum
            h.update(str(rel_path).encode("utf-8"))
            h.update(b"\0")

            # Include file contents
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)

    return h.hexdigest()

# Example usage
checksum = directory_checksum("/path/to/directory")
print(checksum)
