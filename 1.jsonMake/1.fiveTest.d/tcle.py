""" 텍스트 정제 모듈
    영어, 특수기호 모두 제거
"""
 
import re
 
# 입,출력 파일명
#INPUT_FILE_NAME = 'hyundai_html_test.txt'
INPUT_FILE_NAME = 'ilotte_cleaned_test.txt'
OUTPUT_FILE_NAME = 'output_cleand.txt'

# 클리닝 함수
def clean_text(text):
    #cleaned_text = re.sub('[a-zA-Z]', '', text)
    #cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
    #                      '', cleaned_text)
    # 공백을 삭제하는 코드.
    #cleaned_text = " ".join(cleaned_text.split())
    cleaned_text = re.sub('t', '', text)
    return cleaned_text
     
# 메인 함수
def main():
    read_file = open(INPUT_FILE_NAME, 'r')
    write_file = open(OUTPUT_FILE_NAME, 'w')
    text = read_file.read()
    text = clean_text(text)
    write_file.write(text)
    read_file.close()
    write_file.close()

if __name__ == "__main__":
    main()

