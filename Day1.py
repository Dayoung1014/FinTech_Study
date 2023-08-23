import OpenDartReader
from dotenv import load_dotenv
import os

### 0. 객체 생성 ###
# 객체 생성 (API KEY 지정)
load_dotenv()
api_key = os.getenv("API_KEY")

#종목 번호
company_code = '005930'
start_date = '2023-01-01'
end_date = '2023-08-22'

dart = OpenDartReader(api_key)
dart_list = dart.list(company_code, start= start_date, end= end_date, kind='A', final=False) #기업 번호, 조회 기간 설정

# 조회 기간 중 가장 최신 사업보고서의 idx
report_idx = dart_list['rcept_no'][0]

# 해당 idx에 해당하는 사업보고서 Raw Text 추출
xml_text = dart.document(report_idx)
#print(xml_text)

import re
# 전처리 함수
def extract_refine_text(html_string):
    # Remove CSS styles
    no_css = re.sub('<style.*?</style>', '', html_string, flags=re.DOTALL)

    # Remove Inline CSS
    no_inline_css = re.sub('\..*?{.*?}', '', no_css, flags=re.DOTALL)

    # Remove specific undesired strings
    no_undesired = re.sub('\d{4}[A-Za-z0-9_]*" ADELETETABLE="N">', '', no_inline_css)

    # Remove HTML tags
    no_tags = re.sub('<[^>]+>', ' ', no_undesired)

    # Remove special characters and whitespaces
    cleaned = re.sub('\s+', ' ', no_tags).strip()

    # Remove the □ character
    no_square = re.sub('□', '', cleaned)

    # Replace \' with '
    final_text = re.sub(r"\\'", "'", no_square)

    return final_text


refined_text = extract_refine_text(xml_text)
#print(refined_text) # 텍스트 전처리 여부 확인


# 텍스트 파일 저장
with open(f"삼성전자_{report_idx}.txt", 'w', encoding='utf-8') as f:
    f.write(refined_text)


import FinanceDataReader as fdr
import mplfinance as mpf

# 삼성전자(005930), 최근 6개월 데이터
df = fdr.DataReader(company_code, start_date, end_date)

# 캔들차트 그리기
mpf.plot(df, type='candle', volume=True, title='Samsung Electronics (005930)', mav=(5,20))
