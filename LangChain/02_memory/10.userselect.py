from callfunction import *

# 사용자 선택에 따라서 사용할 프로프트 템플릿 정의
prompt_map = {
    '1': ('요약','다음 내용을 한 문장으로 **요약**\n내용:{text}'),
    '2': ('키워드','다음 내용에서 **핵심 키워드 5개** 추천\n내용:{text}'),
    '3': ('답변','다음 질문에 **3문장 이내**로 답변\n내용:{text}'),
    '4': ('종료','다음 질문에 **3문장 이내**로 답변\n내용:{text}'),
}

# 메뉴 선택
for k, v in prompt_map.items():
    print(f'{k}) {v[0]}')
    
while True:
    sel = input('메뉴 선택:  ').strip()
    if sel not in prompt_map:
        raise SystemExit('메뉴 선택 오류')
    
    if sel == '4':
        print('프로그램 종료')
        break
        
    name, template = prompt_map[sel]

    llm= ChatOpenAI(model='gpt-4o-mini')
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    question = input(f'{name} 입력: ')
    print(chain.invoke({'text':question}))