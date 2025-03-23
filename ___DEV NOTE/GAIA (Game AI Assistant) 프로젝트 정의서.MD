# GAIA (Game AI Assistant) 프로젝트 정의서

<!--
## 목차

### Part I: 시스템 기획
1. 시스템 개요 및 로드맵
   - 시스템 목적
   - 핵심 기능
   - 프로세스
   - 업데이트 계획

### Part II: 기술 명세
1. 개발 환경 및 기술 스택
2. 디렉토리 구조
3. 사용 데이터 정의
4. 시스템 상수
5. 시스템 프롬프트
   - Default System Prompt
   - CS Prompt
   - AI Linguist
6. 템플릿 활용 정책

### Part III: 히스토리
0. 문서 버전 관리
1. 완료 항목
2. 진행 상태
3. 보류 항목

### Part X: 기타
1. ★★★일정★★★
2. ☆기타 정보

<div style="page-break-after: always;"></div>
-->

## Part I: 시스템 기획
### 1. 시스템 개요 및 로드맵

#### 1.1 시스템 목적
- 게임 운영의 CS 업무 자동화/반자동화
- 글로벌 서비스(일본어 중심) CS 지원
- AI 기반 답변 생성 및 품질 관리
- 다국어 CS 처리 효율화

#### 1.2 핵심 기능
- CSV 기반 템플릿 관리
- Claude API 연동
- 기본 설정 관리
- 로깅 시스템
- 보안 시스템

### 1.3 프로세스

#### One-Step Process (일본어 가능자)
1. 입력/처리
   - [사용자] 일본어 문의 제목/내용 입력
   - [사용자] 희망 답변 입력
   - [사용자] 템플릿 직접 지정
   - [AI] 지정된 템플릿 기반으로 답변 자동 생성 (GAIA_SYSTEM_MAIN 및 GAIA_ONESTEP_PROMPT 활용)
   - [사용자] 품질 확인 및 발송

#### Two-Step Process (일본어 불가자)
1. 초기 분석
   - [사용자] 일본어 문의 접수
   - [AI] 문의 번역(한국어) (GAIA_SYSTEM_MAIN 및 GAIA_TWOSTEP_TRANSLATE 활용)
   - [AI] 문의 내용 분석 및 요약
   - [AI] 템플릿 추천 (키워드 기반 자동 추천)

2. 검토/수정
   - [사용자] 번역본 확인
   - [사용자] 희망 답변 추가 입력(선택)
   - [사용자] 템플릿 변경(선택)
   - [사용자] 최종 승인

3. 최종 처리
   - [AI] 답변 생성 (GAIA_SYSTEM_MAIN 및 GAIA_TWOSTEP_RESPONSE 활용)
   - [사용자] 답변 번역본 확인
   - [사용자] 답변 발송

#### 2단계 개발 시 프로세스 확장 예정 
* 템플릿 관리 기능 추가에 따른 프로세스 보강
* CRUD 기능 추가로 인한 워크플로우 확장
* 사용 통계 기반의 템플릿 추천 기능 강화
* [세부 내용 2단계 개발 시 업데이트 예정]

#### 1.4 업데이트 계획
##### 1차 릴리즈 (현재)
- 기본 CS 자동화
  * CSV 기반 템플릿 활용
  * 일본어 특화 CS 지원
  * 원스텝/투스텝 프로세스
  * 기본 UI/UX

  ※ 1단계에서는 CSV 기반으로 개발하며, 서버 연계 여부는 2단계 완료 이후 결정 예정<br>
  ※ AI 답변의 품질 관리는 1단계에서는 수동 검토 방식, 2단계 완료 이후 피드백 시스템 추가 논의

##### 2차 업데이트: 템플릿 관리 & 다국어 확장
- 템플릿 관리 시스템
  * 템플릿 CRUD 기능
  * 카테고리 관리
  * 버전 관리
  * 사용 통계

  ※상기 시스템 추가로 인한 프로세스 확장 추가(상세 내용 1.3 항목 참조)


- 다국어 지원 확장
  * 영어 지원
  * 중국어 간체
  * 중국어 번체
  * 언어별 품질 관리
  * 다국어 템플릿 최적화

##### 3차 업데이트: 현지화 시스템 (장기 계획)
- 웹사이트 분리
  * CS 자동화 섹션
  * 현지화 섹션

- 현지화 기능
  * 게임 컨텐츠 번역
  * 마케팅 자료 번역
  * 현지화 품질 관리
  * 용어집 관리

<div style="page-break-after: always;"></div>

## Part II: 기술 명세

### 1. 개발 환경 및 기술 스택

#### 1.1 기본 개발 환경
- **Python 버전**: 3.13+ (테스트 및 확인 완료)
- **운영체제**: macOS 및 Windows 10 이상
- **권장 IDE**
  - Visual Studio Code (VS Code 실행 구성 설정 필요)

#### 1.2 백엔드 스택
- **주요 라이브러리** 업데이트된 버전
  - anthropic: 0.49.0 (Claude 3.7 지원 확인)
  - pandas: 2.2.3
  - flask: 3.1.0
  - python-dotenv: 1.0.1
  - requests: 2.32.3
  - flask-login: 0.6.3
  - flask-wtf: 1.2.2

  ※ SQLAlchemy는 2단계 이후 DB 확장 가능성을 고려하여 포함.<br>
  현재 1단계에서는 CSV 기반 데이터 처리에 집중하며, DB 도입 여부는 후속 논의 예정

#### 1.3 프론트엔드 스택
- **HTML**: HTML5
- **CSS**
  - Bootstrap 5 프레임워크
  - SASS 전처리기
- **JavaScript**
  - ES6+ 기준
  - 주요 라이브러리
    - jQuery: DOM 조작 및 AJAX
    - axios: HTTP 클라이언트
    - chart.js: 데이터 시각화

#### 1.4 데이터 처리
- **기본 저장소**: CSV 파일 시스템
- **데이터 처리 도구**
  - pandas: CSV 처리 및 데이터 분석
  - numpy: 수치 계산 및 배열 처리
- **파일 형식**
  - 템플릿: CSV
  - 설정: JSON
  - 로그: TXT

#### 1.5 외부 서비스
- **AI 서비스**
  - Claude API v3.7 (claude-3-7-sonnet-20250219)
  - API 응답 로깅 기능 구현 완료
  - 주요 기능
    - 텍스트 생성
    - 번역
    - 컨텍스트 분석

  ※ AI API는 현재 Claude 기반으로 진행하며, 추가 모델 도입 여부는 1단계 이후 테스트 및 평가 예정

### 2. 디렉토리 구조
개발 진행 중 변경 가능성 있으며, 변경 시 추가 업데이트 예정.

```
gaia/
├── __init__.py        # 패키지 초기화
├── __main__.py        # 메인 진입점 (애플리케이션 시작)
├── core/              # 핵심 기능
│   ├── __init__.py
│   ├── config/                    # 일반 설정 관리
│   │   ├── settings.py           # 기본 설정
│   │   └── constants.py          # 상수 정의
│   └── logger/                    # 기본 로깅
│       └── logger.py             # 로그 처리
│
├── security/                      # 보안 관련
│   ├── __init__.py
│   ├── credentials/              # 인증 정보
│   │   ├── api_keys.py          # API 키 관리
│   │   └── auth.py              # 인증 관리
│   ├── encryption/               # 암호화 관련
│   │   ├── cipher.py            # 암호화 처리
│   │   └── keys.py              # 키 관리
│   └── policies/                 # 보안 정책
│       └── constants.py          # 보안 상수
│
├── services/                      # 서비스 모듈
│   ├── __init__.py
│   ├── ai/                       # AI 서비스
│   │   ├── claude.py            # Claude API
│   │   └── processor.py         # 응답 처리
│   └── translator/               # 번역 서비스
│       └── translator.py        # 번역 처리
│
├── templates/                     # 템플릿 관리
│   ├── __init__.py
│   ├── loader.py                 # CSV 로더
│   └── manager.py                # 템플릿 관리
│
├── cs/                           # CS 시스템
│   ├── __init__.py
│   ├── workflow/                 # 워크플로우
│   │   ├── onestep.py          # 원스텝 프로세스
│   │   └── twostep.py          # 투스텝 프로세스
│   └── responses/               # 응답 관리
│       └── generator.py         # 응답 생성
│
├── utils/                        # 유틸리티
│   ├── __init__.py
│   ├── validators/              # 통합 검증
│   │   ├── template.py         # 템플릿 검증
│   │   ├── response.py         # 응답 검증
│   │   └── common.py           # 공통 검증
│   └── formatters/             # 포맷 처리
│       ├── text.py             # 텍스트 포맷
│       └── response.py         # 응답 포맷
│
├── ui/                           # 사용자 인터페이스
│   ├── static/                  # 정적 파일
│   │   ├── css/                # 스타일시트
│   │   │   ├── main.css       # 메인 스타일
│   │   │   └── components/    # 컴포넌트 스타일
│   │   ├── js/                 # 자바스크립트
│   │   │   ├── main.js        # 메인 스크립트
│   │   │   └── modules/       # 기능별 모듈
│   │   └── images/            # 이미지
│   └── templates/              # HTML 템플릿
│       ├── base.html          # 기본 템플릿
│       ├── components/        # 재사용 컴포넌트
│       └── pages/             # 페이지 템플릿
│
└── data/                         # 데이터 저장
    └── templates/               # 템플릿 CSV 저장
        ├── DB_CS_JA_Template_Common2.csv  # 문의 답변 템플릿
        ├── DB_PROJECT_DATA.csv            # 프로젝트 정보
        └── DB_SYSTEM_PROMPT.csv           # AI 프롬프트 템플릿 (시스템 및 사용자 프롬프트)
```

<div style="page-break-after: always;"></div>

### 3. 사용 데이터 정의

#### 3.1 CSV 파일 구조
```python
# CSV 파일명 정의
CSV_FILES = {
    "RESPONSE_TEMPLATE": "DB_CS_JA_Template_Common2.csv",  # CS 답변 템플릿
    "PROJECT_INFO": "DB_PROJECT_DATA.csv",                 # 프로젝트 기본 정보
    "PROMPT_TEMPLATE": "DB_SYSTEM_PROMPT.csv"             # AI 시스템 프롬프트
}

# CS 답변 템플릿 컬럼
RESPONSE_TEMPLATE_COLUMNS = {
    "NO": "NO",                       # 템플릿 고유 번호
    "TEMP_KEY": "Temp_Key",           # 템플릿 키
    "TEMP_CATEGORY": "Temp_Category", # 템플릿 카테고리
    "TEMP_SECTION": "Temp_Section",   # 템플릿 섹션
    "TEMP_CONTENT_KR": "Temp_Content_KR",  # 한국어 템플릿 내용
    "TEMP_CONTENT_JP": "Temp_Content_JP",  # 일본어 템플릿 내용
    "TEMP_DATE": "Temp_Date"          # 템플릿 최종 수정일
}

# 프로젝트 정보 컬럼
PROJECT_INFO_COLUMNS = {
    "NO": "NO",                       # 프로젝트 고유 번호
    "TITLE_KEY": "Title_Key",         # 프로젝트 키
    "TITLE_NAME": "Title_Name",       # 프로젝트명 (한국어)
    "TITLE_NAME_JP": "Title_Name_JP", # 프로젝트명 (일본어)
    "GREETING": "Greeting",           # 인사말 템플릿
    "CLOSING": "Closing",             # 맺음말 템플릿
    "USER_TITLE": "User_Title",       # 유저 호칭
    "USE_YN": "Use_YN",               # 사용 여부
    "UPDATE_DATE": "Update_Date"      # 정보 최종 수정일
}

# AI 프롬프트 템플릿 컬럼
PROMPT_TEMPLATE_COLUMNS = {
    "NO": "NO",                           # 프롬프트 고유 번호
    "PROMPT_KEY": "Prompt_Key",           # 프롬프트 키
    "PROMPT_CATEGORY": "Prompt_Category", # 프롬프트 카테고리
    "PROMPT_SECTION": "Prompt_Section",   # 프롬프트 섹션
    "PROMPT_CONTENT": "Prompt_Content",   # 프롬프트 내용
    "PROMPT_DESCRIPTION": "Prompt_Description",  # 프롬프트 설명
    "UPDATE_DATE": "Update_Date"          # 프롬프트 최종 수정일
}
```
### 3.2 CSV 파일 구조 업데이트
```
DB_SYSTEM_PROMPT.csv 파일에 다음 행 추가:
2,GAIA_ONESTEP_PROMPT,Workflow,OneStep,"# 문의 정보\n문의 제목: {inquiry_title}\n문의 내용: {inquiry_content}\n\n# 프로젝트 정보\n프로젝트명: {project_name}\n프로젝트명(일본어): {project_name_jp}\n유저 호칭: {user_title}\n인사말: {greeting}\n맺음말: {closing}\n\n{template_section}\n{custom_response_section}\n# 지시사항\n위 정보를 바탕으로 문의에 대한 응답을 작성해주세요.\n응답은 반드시 지정된 JSON 형식으로 출력해주세요.\nsummary는 한국어로 문의 내용을 요약해주세요.\nsuggestion은 한국어로 어떤 답변을 할지 제안해주세요.\nresponse_mail은 일본어로 작성하되, 인사말과 맺음말을 포함해주세요.","원스텝 프로세스용 프롬프트 템플릿",2025-02-26
3,GAIA_TWOSTEP_TRANSLATE,Workflow,TwoStep,"# 문의 정보\n문의 제목: {inquiry_title}\n문의 내용: {inquiry_content}\n\n# 지시사항\n위 일본어 문의 내용을 한국어로 번역 및 분석해주세요.\n응답은 반드시 지정된 JSON 형식으로 출력해주세요.\nsummary는 한국어로 문의 내용을 요약 및 번역해주세요.\nsuggestion은 한국어로 어떤 답변을 할지 제안해주세요.\nresponse_mail은 일단 번역 단계이므로 간단한 일본어 메시지로 작성해주세요.","투스텝 프로세스 번역용 프롬프트 템플릿",2025-02-26
4,GAIA_TWOSTEP_RESPONSE,Workflow,TwoStep,"# 문의 정보\n문의 제목: {inquiry_title}\n문의 내용: {inquiry_content}\n번역된 요약: {translated_summary}\n\n# 프로젝트 정보\n프로젝트명: {project_name}\n프로젝트명(일본어): {project_name_jp}\n유저 호칭: {user_title}\n인사말: {greeting}\n맺음말: {closing}\n\n{template_section}\n{custom_response_section}\n# 지시사항\n위 정보를 바탕으로 문의에 대한 응답을 작성해주세요.\n응답은 반드시 지정된 JSON 형식으로 출력해주세요.\nsummary는 한국어로 문의 내용을 요약해주세요.\nsuggestion은 한국어로 어떤 답변을 할지 제안해주세요.\nresponse_mail은 일본어로 작성하되, 인사말과 맺음말을 포함해주세요.","투스텝 프로세스 응답용 프롬프트 템플릿",2025-02-26
5,GAIA_TEMPLATE_SECTION,Component,Section,"# 선택한 템플릿\n카테고리: {temp_category}\n섹션: {temp_section}\n템플릿 내용(한국어): \n{temp_content_kr}\n템플릿 내용(일본어): \n{temp_content_jp}\n","템플릿 섹션 프롬프트 컴포넌트",2025-02-26
6,GAIA_CUSTOM_RESPONSE,Component,Section,"# 희망 답변\n{custom_response}\n","커스텀 응답 섹션 프롬프트 컴포넌트",2025-02-26
```


<div style="page-break-after: always;"></div>

### 4. 시스템 상수
개발 진행 중 변경 가능성 있으며, 변경 시 추가 업데이트 예정.

#### 4.1 파일 처리 설정
```python
# 파일 인코딩 설정
FILE_ENCODING = "utf-8"

# CSV 처리 설정
CSV_SETTINGS = {
    "DELIMITER": ",",       # CSV 구분자
    "QUOTECHAR": '"',       # 인용 부호
    "ENCODING": "utf-8"     # 파일 인코딩
}
```

#### 4.2 언어 설정
```python
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
```

#### 4.3 시스템 설정
```python
# 처리 상태 코드
STATUS_CODES = {
    "PENDING": "pending",        # 대기 중
    "PROCESSING": "processing",  # 처리 중
    "COMPLETED": "completed",    # 완료
    "ERROR": "error"             # 오류
}

# 사용 여부 상태
USE_STATUS = {
    "ACTIVE": "Y",    # 사용 중
    "INACTIVE": "N"   # 미사용
}

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
    "PROMPT": 8000           # 프롬프트 최대 길이
}

# 기본 설정
DEFAULT_SETTINGS = {
    "LOG_LEVEL": LOG_LEVELS["INFO"],
    "MAX_RETRY": 3,             # 최대 재시도 횟수
    "TIMEOUT": 30,              # 타임아웃 (초)
    "CACHE_EXPIRE": 3600,       # 캐시 만료 시간 (초)
}
```

<div style="page-break-after: always;"></div>

### 5. 시스템 프롬프트

#### 5.1 프롬프트 구조 및 관리
- 모든 프롬프트는 CSV 파일(`DB_SYSTEM_PROMPT.csv`)에서 관리
- 주요 프롬프트 유형:
  * GAIA_SYSTEM_MAIN: 기본 시스템 프롬프트 (Claude API system 파라미터)
  * GAIA_ONESTEP_PROMPT: 원스텝 프로세스용 프롬프트 템플릿
  * GAIA_TWOSTEP_TRANSLATE: 투스텝 프로세스 번역용 프롬프트 템플릿
  * GAIA_TWOSTEP_RESPONSE: 투스텝 프로세스 응답용 프롬프트 템플릿
  * GAIA_TEMPLATE_SECTION: 템플릿 섹션 프롬프트 컴포넌트
  * GAIA_CUSTOM_RESPONSE: 커스텀 응답 섹션 프롬프트 컴포넌트

#### 5.2 프롬프트 확장 방식
- 코드 수정 없이 CSV 파일 수정만으로 프롬프트 업데이트 가능
- 각 프로세스에서 자동으로 해당 프롬프트 템플릿 로드
- 템플릿 없을 경우 폴백으로 하드코딩된 기본 템플릿 사용

#### 5.3 AI Linguist
일본어 검증 및 수정 프롬프트
```
스펙 확인 필요
```
※ AI Linguist는 내부 프롬프트 활용 예정이며,
세부 역할 및 적용 방식은 제작자와의 미팅 후 확정 예정

### 6. 템플릿 활용 정책

#### 1단계 방침

* 개발 준비 단계에서 기구축된 템플릿 파일 사용
* 템플릿 파일 접근 규칙
  - 기존 템플릿 파일은 오직 읽기(Read)만 가능
  - 어떠한 경우에도 파일 수정/추가/삭제 금지
  - 파일 내용과 구조를 변경하지 않고 그대로 사용
* CSV 파일 로드 및 처리 방식
  - [개발 진행 중 업데이트 예정]
* 템플릿 선택 및 매칭 프로세스
  - [개발 진행 중 업데이트 예정]
* 응답 생성 활용 방안
  - [개발 진행 중 업데이트 예정]
* 제한사항
  - 템플릿 수정 불가
  - 신규 템플릿 추가 불가
  - 템플릿 삭제 불가

※ 1단계에서는 CSV 템플릿을 수정 없이 읽기 전용으로 운영하며, 2단계에서 CRUD 기능 도입 및 버전 관리 방식 검토 예정

#### 2단계 방침
- [구체적인 구현 상세 업데이트 예정]
* 템플릿 CRUD 기능 구현
* 카테고리 관리 시스템 추가
* 버전 관리 기능 도입
* 사용 통계 시스템 구축


### 7. AI 개발 가이드라인

#### 7.1 코드 품질 기준
- **기본 원칙**
  - PEP 8 기반 파이썬 코드 스타일 준수
  - 함수/클래스의 단일 책임 원칙 준수
  - 코드 재사용성 고려

- **구조 분리**
  ```python
  # 나쁜 예: 라우트에서 모든 처리
  @app.route('/process', methods=['POST'])
  def process():
      # CSV 읽기, 데이터 처리, API 호출 등 모두 여기서 처리
      data = pd.read_csv('file.csv')
      result = process_data(data)
      response = call_api(result)
      return jsonify(response)

  # 좋은 예: 책임 분리
  @app.route('/process', methods=['POST'])
  def process():
      # 라우트는 요청 처리와 응답만 담당
      try:
          result = template_service.process_request(request.json)
          return jsonify(result)
      except Exception as e:
          return handle_error(e)
  ```

- **프론트엔드 구조**
  - HTML: `templates/base.html` 기본 템플릿과 `templates/components/`, `templates/pages/`로 분리
  - CSS: `static/css/main.css`와 `static/css/components/`로 분리
  - JavaScript: `static/js/main.js`와 `static/js/modules/`로 분리

- **명명 규칙**
  - 변수/함수: snake_case 사용
    ```python
    # 좋은 예
    template_data = load_template("template_id")
    user_message = get_user_input()
    
    # 나쁜 예
    templateData = load("t1")
    msg = get()
    ```
  
  - 클래스: PascalCase 사용
    ```python
    # 좋은 예
    class TemplateManager:
    class UserDataProcessor:
    
    # 나쁜 예
    class template_handler:
    class userProcessor:
    ```

#### 7.2 문서화 요구사항
- **함수 문서화**
  ```python
  def process_template(template_id: str) -> dict:
      """
      템플릿을 처리하는 함수입니다.

      Args:
          template_id: 템플릿 식별자

      Returns:
          처리된 템플릿 데이터 (딕셔너리)

      Raises:
          FileNotFoundError: 파일을 찾을 수 없는 경우
          ValueError: 템플릿 ID가 잘못된 경우
      """
  ```

- **주석 작성**
  ```python
  # 데이터 로드
  template_data = load_data("sample_template")
  
  # 응답 생성
  response = generate_response(template_data)
  ```

#### 7.3 에러 처리
- **예외 처리**
  ```python
  try:
      # 데이터 처리 시도
      data = process_data(input_data)
  except FileNotFoundError:
      logger.error("파일을 찾을 수 없습니다")
      raise
  except ValueError as e:
      logger.error(f"데이터 처리 오류: {e}")
      raise
  ```

- **로깅**
  ```python
  # 성공 로그
  logger.info(f"처리 완료: {process_id}")
  
  # 에러 로그
  logger.error(f"처리 실패: {error_message}")
  ```

#### 7.4 테스트 요구사항
- **기본 테스트**
  ```python
  def test_data_processing():
      """데이터 처리 테스트"""
      result = process_data("sample_data")
      assert result is not None
      assert "status" in result
  ```

- **엣지 케이스 테스트**
  ```python
  def test_invalid_input():
      """잘못된 입력 테스트"""
      with pytest.raises(ValueError):
          process_data("")
  ```

#### 7.5 보안 가이드라인
- **API 키 관리**
  ```python
  # 환경 변수에서 키 로드
  api_key = os.getenv("API_KEY")
  if not api_key:
      raise ValueError("API 키가 설정되지 않았습니다")
  ```

- **입력 검증**
  ```python
  def validate_input(user_input: str) -> bool:
      """입력값 검증"""
      if not user_input:
          return False
      if len(user_input) > 1000:  # 예시 길이 제한
          return False
      return True
  ```


<div style="page-break-after: always;"></div>

## Part III: 히스토리

### 0. 문서
| 버전  | 날짜 | 작성자 | 주요 변경사항 |
|-------|------|--------|---------------|
| v0.9  | 2025.02.21 | 김상현 | 초기 문서 작성 |
| v0.9  | 2025.02.22 | 김상현 | - Part II에 템플릿 활용 정책 추가<br>- 1/2단계 템플릿 활용 방침 명확화<br>- 히스토리 섹션 추가 |
| v0.9  | 2025.02.22 | 김상현 | - Part I 프로세스 섹션 상세화 (작업 주체 명시)<br>- 1.3/1.4 섹션 연계성 강화<br>- '운영'을 '활용'으로 용어 통일<br>- 템플릿 활용 정책 보완 |
| v0.9  | 2025.02.26 | 김상현 | - CSV 기반 프롬프트 관리 시스템 구현<br>- 원스텝/투스텝 프로세스 세부 구현<br>- DB_SYSTEM_PROMPT.csv 구조 확장<br>- 프롬프트 구조 및 관리 섹션 추가<br>- 개발 현황 업데이트 |
| v0.9  | 2025.03.22 | 김상현 | - Claude 3.7 API 연동 확인<br>- 환경 구성 가이드 추가<br>- 최신 라이브러리 버전 테스트<br>- API 로깅 기능 구현 |


### 1. 완료 항목
- 시스템 기획 초안 작성
- 기술 명세 초안 작성
- 템플릿 활용 정책 정의
- 히스토리 섹션 구조화
- 기본 API 연동 구현
- CSV 템플릿 로더 구현
- 원스텝/투스텝 프로세스 기본 구현
- CSV 기반 프롬프트 관리 시스템 구현
- Python 3.13 환경에서 프로젝트 구동 검증
- Claude 3.7 API 연동 및 응답 확인
- API 호출 및 응답 모니터링 로깅 구현
- 다중 환경 설정 방법 표준화
- 포트 충돌 문제 해결 (8080 포트 사용)

### 2. 진행 상태
- 1단계 개발 진행 중
- 기본 CS 자동화 시스템 구축 완료
- 원스텝/투스텝 프로세스 기본 기능 구현 완료
- 템플릿 시스템 읽기 전용 운영 중
- 프롬프트 시스템 구현 완료
- Claude API 연동 완료 (0.3.0 버전, claude-2 모델)
- 웹 인터페이스 기본 기능 구현 완료
- 1단계 개발 진행 중 (약 75% 완료)
- API 응답 모니터링 시스템 구현
- 다중 환경 구성 표준화 완료

### 3. 보류 항목
- 2단계 템플릿 관리 시스템 상세 설계
- 다국어 확장 계획 구체화
- 현지화 시스템 세부 스펙 정의
- 오류 처리 및 로깅 시스템 강화
- 사용자 편의성 개선 및 UI/UX 고도화

<div style="page-break-after: always;"></div>

## Part X: 기타

### ★★★일정★★★

- **1차 개발 (2025.02.24 ~ 2025.03.31) \\당면 목표**
  - 기본 CS 자동화 시스템 구축 [완료]
  - CSV 기반 템플릿 시스템 개발 [완료]
  - 일본어 특화 CS 지원 구현 [완료]
  - 기본 UI/UX 개발 [완료]
  - 오류 처리 및 예외 상황 대응 강화 [예정]
  - 최종 테스트 및 사용자 피드백 반영 [예정]

- **2차 개발 (미정) \\일정 및 상세 논의 필요**
  - 템플릿 관리 시스템 고도화
  - 다국어 지원 확장 (영어, 중국어)
  - 템플릿 버전 관리 시스템 구축
  - 사용 통계 기능 추가

- **(임시)3차 개발 (미정) \\전체 논의 필요**
  - 현지화 시스템 개발
  - 게임 컨텐츠 번역 기능 구현
  - 현지화 품질 관리 시스템 구축
  - 용어집 관리 기능 개발

### ☆기타 정보
  - 작성일: 2025.02.21
  - 작성자: 글로벌서비스 2팀 일본어 2파트 김상현
  - 추후 개발 과정에서 점진적 업데이트 예정
  
<div style="page-break-after: always;"></div>

## 부록: 표준 구동 프로세스 가이드

### GAIA 프로젝트 구동 방법

#### 환경 설정 및 실행 명령어

1. 프로젝트 디렉토리로 이동
```bash
cd /Users/hyun/Documents/HyuN/Python/GAIA
```

2. 가상 환경 활성화
```bash
source .venv/bin/activate
```

3. 프로젝트 실행
```bash
.venv/bin/python __main__.py
```

#### 새 환경에서 GAIA 프로젝트 설정하기

1. 프로젝트 디렉토리로 이동
```bash
cd /path/to/GAIA
```

2. 가상 환경 생성
```bash
python3 -m venv .venv
```

3. 가상 환경 활성화
```bash
source .venv/bin/activate
```

4. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

5. 환경 변수 설정 (.env 파일이 없는 경우)
```bash
cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_API_VERSION=claude-3-7-sonnet-20250219
EOF
```

6. 프로젝트 실행
```bash
.venv/bin/python __main__.py
```
