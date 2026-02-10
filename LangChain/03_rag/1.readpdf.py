# pip install "unstructured[all-docs]"
from langchain_community.document_loaders import UnstructuredPDFLoader
from pathlib import Path

path = Path.cwd()  / "LangChain" / "03_rag" / "data"
print(f'작업폴더> {path}')

# print(f'name> {Path.}')
loader = UnstructuredPDFLoader(path / "Samsung_Card_Manual_Korean_1.3.pdf")
pages = loader.load()
print("총 페이지 수: ",  len(pages))
print("미리보기: ",  pages[0].page_content[:500])