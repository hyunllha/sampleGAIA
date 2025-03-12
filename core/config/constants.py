"""
GAIA (Game AI Assistant) 시스템 상수 정의
모든 고정 값과 설정값을 이 파일에서 관리합니다.
"""

### 1. CSV 파일 관련 설정 ###

# CSV 파일명 정의
CSV_FILES = {
   "RESPONSE_TEMPLATE": "DB_CS_JA_Template_Common2.csv",  # CS 답변 템플릿
   "PROJECT_INFO": "DB_PROJECT_DATA.csv",                 # 프로젝트 기본 정보
   "PROMPT_TEMPLATE": "DB_SYSTEM_PROMPT.csv"             # AI 시스템 프롬프트
}

# CSV 파일 경로 설정
CSV_PATHS = {
   "RESPONSE_TEMPLATE": "data/templates/DB_CS_JA_Template_Common2.csv",
   "PROJECT_INFO": "data/templates/DB_PROJECT_DATA.csv",
   "PROMPT_TEMPLATE": "data/templates/DB_SYSTEM_PROMPT.csv"
}

# CS 답변 템플릿 컬럼 (DB_CS_JA_Template_Common2.csv)
RESPONSE_TEMPLATE_COLUMNS = {
   "NO": "NO",                       # 템플릿 고유 번호
   "TEMP_KEY": "Temp_Key",           # 템플릿 키 (시스템 내부 참조용)
   "TEMP_CATEGORY": "Temp_Category", # 템플릿 카테고리 (결제/계정/게임 등)
   "TEMP_SECTION": "Temp_Section",   # 템플릿 섹션 (상세 분류)
   "TEMP_CONTENT_KR": "Temp_Content_KR",  # 한국어 템플릿 내용
   "TEMP_CONTENT_JP": "Temp_Content_JP",  # 일본어 템플릿 내용
   "TEMP_DATE": "Temp_Date"          # 템플릿 최종 수정일
}

# 프로젝트 정보 컬럼 (DB_PROJECT_DATA.csv)
PROJECT_INFO_COLUMNS = {
   "NO": "NO",                       # 프로젝트 고유 번호
   "TITLE_KEY": "Title_Key",         # 프로젝트 키 (시스템 내부 참조용)
   "TITLE_NAME": "Title_Name",       # 프로젝트명 (한국어)
   "TITLE_NAME_JP": "Title_Name_JP", # 프로젝트명 (일본어)
   "GREETING": "Greeting",           # 인사말 템플릿
   "CLOSING": "Closing",             # 맺음말 템플릿
   "USER_TITLE": "User_Title",       # 유저 호칭 (예: 제독님, 기사님 등)
   "USE_YN": "Use_YN",               # 사용 여부 (Y/N)
   "UPDATE_DATE": "Update_Date"      # 정보 최종 수정일
}

# AI 프롬프트 템플릿 컬럼 (DB_SYSTEM_PROMPT.csv)
PROMPT_TEMPLATE_COLUMNS = {
   "NO": "NO",                           # 프롬프트 고유 번호
   "PROMPT_KEY": "Prompt_Key",           # 프롬프트 키 (시스템 내부 참조용)
   "PROMPT_CATEGORY": "Prompt_Category", # 프롬프트 카테고리
   "PROMPT_SECTION": "Prompt_Section",   # 프롬프트 섹션
   "PROMPT_CONTENT": "Prompt_Content",   # 프롬프트 내용
   "PROMPT_DESCRIPTION": "Prompt_Description",  # 프롬프트 설명
   "UPDATE_DATE": "Update_Date"          # 프롬프트 최종 수정일
}

### 2. 파일 처리 관련 설정 ###

# 파일 인코딩 설정
FILE_ENCODING = "utf-8"

# CSV 처리 설정
CSV_SETTINGS = {
   "DELIMITER": ",",        # CSV 구분자
   "QUOTECHAR": '"',       # 인용 부호
   "ENCODING": "utf-8"     # 파일 인코딩
}

### 3. 언어 관련 설정 ###

# 지원 언어 코드
LANGUAGES = {
   "KO": "ko",  # 한국어
   "JA": "ja",  # 일본어
   "EN": "en",  # 영어 (향후 확장용)
   "ZH_CN": "zh-CN",  # 중국어 간체 (향후 확장용)
   "ZH_TW": "zh-TW"   # 중국어 번체 (향후 확장용)
}

# 기본 언어 설정
DEFAULT_SOURCE_LANG = LANGUAGES["JA"]  # 기본 입력 언어
DEFAULT_TARGET_LANG = LANGUAGES["KO"]  # 기본 번역 언어

### 4. 처리 상태 관련 설정 ###

# 처리 상태 코드
STATUS_CODES = {
   "PENDING": "pending",        # 대기 중
   "PROCESSING": "processing",  # 처리 중
   "COMPLETED": "completed",    # 완료
   "ERROR": "error"            # 오류
}

# 사용 여부 상태
USE_STATUS = {
   "ACTIVE": "Y",    # 사용 중
   "INACTIVE": "N"   # 미사용
}

### 5. 시스템 설정 ###

# 로깅 레벨
LOG_LEVELS = {
   "DEBUG": "DEBUG",
   "INFO": "INFO",
   "WARNING": "WARNING",
   "ERROR": "ERROR",
   "CRITICAL": "CRITICAL"
}

# 컨텐츠 길이 제한
CONTENT_LENGTH_LIMITS = {
   "TEMPLATE_KR": 3000,     # 한국어 템플릿 최대 길이
   "TEMPLATE_JP": 4000,     # 일본어 템플릿 최대 길이
   "RESPONSE": 5000,        # 최종 응답 최대 길이
   "PROMPT": 8000          # 프롬프트 최대 길이
}

# 기본 설정
DEFAULT_SETTINGS = {
   "LOG_LEVEL": LOG_LEVELS["INFO"],
   "MAX_RETRY": 3,             # 최대 재시도 횟수
   "TIMEOUT": 30,              # 타임아웃 (초)
   "CACHE_EXPIRE": 3600,       # 캐시 만료 시간 (초)
}