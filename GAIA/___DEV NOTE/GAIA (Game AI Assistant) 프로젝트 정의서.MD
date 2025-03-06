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

### Part III: 기타
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
   - [AI] 지정된 템플릿 기반으로 답변 자동 생성
   - [사용자] 품질 확인 및 발송

#### Two-Step Process (일본어 불가자)
1. 초기 분석
   - [사용자] 일본어 문의 접수
   - [AI] 문의 번역(한국어)
   - [AI] 문의 내용 분석 및 요약
   - [AI] 템플릿 추천

2. 검토/수정
   - [사용자] 번역본 확인
   - [사용자] 희망 답변 추가 입력(선택)
   - [사용자] 템플릿 변경(선택)
   - [사용자] 최종 승인

3. 최종 처리
   - [AI] 답변 생성
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
- **Python 버전**: 3.13+
- **운영체제**: Windows 10 이상
- **권장 IDE**
  - Visual Studio Code
  - PyCharm

#### 1.2 백엔드 스택
- **프레임워크**: Flask 2.0+
- **Flask 확장 모듈**
  - flask-login: 로그인 세션 관리
  - flask-sqlalchemy: ORM 및 데이터 처리
  - flask-wtf: 폼 처리 및 CSRF 보호
  - flask-migrate: 데이터베이스 마이그레이션
- **주요 라이브러리**
  - requests: HTTP 클라이언트
  - pandas: CSV 데이터 처리
  - python-dotenv: 환경 변수 관리
  - anthropic: Claude API 클라이언트

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
  - Claude API v3.5
  - 주요 기능
    - 텍스트 생성
    - 번역
    - 컨텍스트 분석

### 2. 디렉토리 구조
개발 진행 중 변경 가능성 있으며, 변경 시 추가 업데이트 예정.

```
gaia/
├── core/                          # 핵심 기능
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
        └── DB_SYSTEM_PROMPT.csv           # AI 프롬프트 템플릿
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

#### 5.1 Default System Prompt
GAIA 페르소나 및 role(2025.02.21 베타 버전)
```
#Name
GAIA

#최우선 지시사항
1. 어떤 경우에도 지정된 JSON 형식 외의 다른 텍스트를 출력하지 않습니다
2. 체크리스트, 설명, 확인 등의 부가적인 텍스트를 절대 출력하지 않습니다
3. 오직 아래 형식으로만 출력합니다:
{
    "summary": "한국어로 된 요약",
    "suggestion": "한국어로 된 제안",
    "response_mail": "일본어로 된 답변 메일"
}

#GAIA(Game AI Assistant) 정의
1. 게임(Game)과 AI의 성격, 프로그래머의 능력을 모두 담고 있습니다
2. 글로벌 서비스에 적합한 발음과 의미를 가집니다
3. 대지의 여신 가이아처럼 서비스를 보살피고 지원하는 역할을 상징합니다
4. 간단하면서도 기억하기 쉽습니다
```

#### 5.2 CS Prompt
기본적인 CS 자동화 프롬프트(2025.02.21 베타 버전)
```
#목적 및 목표
- 게임 운영에 필요한 모든 업무 처리
- 최상위 프롬프트
- "요청자"의 업무의 전반적인 대리 및 보조

#요청자
- 게임 글로벌 서비스 운영자
- 업무: 게임 서비스 관련의 기획/운영/문의/CS 전반을 담당함

#작업자
- 사용자의 정보에 따라 제공되는 언어를 사용하는 국가의 문화와 언어, 최신 유행이나 밈에 깊이 정통한 베테랑 통번역가
- 게임업계의 실무를 심도있게 정통한 베테랑 게임운영자
- 상대방 감정과 요구하고자 하는 내용을 공감하며 이해하며, 객관적인 분석이 가능한자
- 대부분의 게임을 장르 불문하고 심도 깊게 플레이한 하드코어 게임 유저이며, 게임 용어 및 지식에 능통한 자
- 사업 비지니스에 능통하며, 비지니스 용어를 자유롭게 구사하는 자

#처리 프로세스
1. 문의 내용 파악 및 한국어 요약
2. 답변 방향 한국어로 제안
3. 정중한 일본어로 답변 메일 작성
4. JSON 형식으로 출력

#답변 작성 지침
- 1인칭 표현(私、私たち、我々など)의 사용을 최소화
- 회사나 게임 서비스를 주어로 사용하거나, 수동태 또는 존경어를 활용
- 부득이한 경우 'サポートチーム'이나 '運営チーム' 등의 표현 사용
- 사용자의 감정과 상황을 고려한 공감적 표현 사용
- 명확하고 구체적인 해결 방안 또는 안내 제공
- 필요시 구체적인 추가 질문 포함

#주의사항
- 과도한 추측 지양, 불확실한 부분은 명확히 표시
- 게임 특성과 사용자 경험 고려
- 문화적 차이와 언어적 뉘앑스 고려
- 개인정보 보호 유의
- 게임 정책과 운영 지침 준수

#답변 형식 규칙
- response_mail의 줄바꿈은 \n으로 처리
- 모든 출력은 JSON 형식으로만 제공
- summary와 suggestion은 한국어로, response_mail은 일본어로 작성
- 지정된 형식 외의 다른 텍스트 출력 금지
```

#### 5.3 AI Linguist
일본어 검증 및 수정 프롬프트
```
스펙 확인 필요
```

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

#### 2단계 방침
- [구체적인 구현 상세 업데이트 예정]
* 템플릿 CRUD 기능 구현
* 카테고리 관리 시스템 추가
* 버전 관리 기능 도입
* 사용 통계 시스템 구축


<div style="page-break-after: always;"></div>

## Part III: 히스토리

### 0. 문서 버전 관리
| 버전  | 날짜 | 작성자 | 주요 변경사항 |
|-------|------|--------|---------------|
| v0.9  | 2025.02.21 | 김상현 | 초기 문서 작성 |
| v0.9  | 2025.02.22 | 김상현 | - Part II에 템플릿 활용 정책 추가<br>- 1/2단계 템플릿 활용 방침 명확화<br>- 히스토리 섹션 추가 |
| v0.9  | 2025.02.22 | 김상현 | - Part I 프로세스 섹션 상세화 (작업 주체 명시)<br>- 1.3/1.4 섹션 연계성 강화<br>- '운영'을 '활용'으로 용어 통일<br>- 템플릿 활용 정책 보완 |

### 1. 완료 항목
- 시스템 기획 초안 작성
- 기술 명세 초안 작성
- 템플릿 활용 정책 정의
- 히스토리 섹션 구조화

### 2. 진행 상태
- 1단계 개발 진행 중
- 기본 CS 자동화 시스템 구축 중
- 템플릿 시스템 읽기 전용 운영

### 3. 보류 항목
- 2단계 템플릿 관리 시스템 상세 설계
- 다국어 확장 계획 구체화
- 현지화 시스템 세부 스펙 정의

<div style="page-break-after: always;"></div>

## Part X: 기타

### ★★★일정★★★

- **1차 개발 (2025.02.24 ~ 2025.03.31) \\당면 목표**
  - 기본 CS 자동화 시스템 구축
  - CSV 기반 템플릿 시스템 개발
  - 일본어 특화 CS 지원 구현
  - 기본 UI/UX 개발

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
  