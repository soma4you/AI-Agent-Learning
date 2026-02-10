# ---------------------------------
# 파일 경로 설정
# ---------------------------------
from pathlib import Path

# 현재 작업 디렉터리 (파이썬 실행 위치)
path = Path.cwd()
print(f'작업 폴더> {path}')

# 데이터 폴더 경로
path = path / "LangChain" / "03_rag" 
print(f'Data 폴더> {path}')

# PDF 파일 경로
path = path / "data" / "Samsung_Card_Manual_Korean_1.3.pdf"
print(f'(최종) PDF 파일> {path}')



# ---------------------------------
# PDF 읽어오기
# ---------------------------------
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(path)
pages = loader.load()
print("총 페이지 수: ",  len(pages))
print("미리보기: ",  pages[0].page_content[:200])

# 출력 결과에 빈 공간이 생기는 이유는 'PyPDFLoader'가 이미지 부분을 처리하지 못하기 때문!
'''
미리보기:  사용설명서           SAMSUNG PROPRIETARY 
Revision1.3
1













.

법적 고지 사항
삼성 전자는 통지 없이 제품, 정보 및 사양을 변경할 권리를 보유합니다.    
여기에 언급된 제품 및 사양은 참조용으로만 사용되며, 여기에 언급된 모든  정보는 공지 없이 변경될 수 있고
어떠
'''