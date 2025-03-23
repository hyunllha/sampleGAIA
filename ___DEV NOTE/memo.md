# GAIA 프로젝트 구동 방법

## 환경 설정 및 실행 명령어

```bash
# 1. 프로젝트 디렉토리로 이동
cd /Users/hyun/Documents/HyuN/Python/GAIA

# 2. 가상 환경 활성화
source .venv/bin/activate

# 3. 프로젝트 실행
.venv/bin/python __main__.py
```

## 새 환경에서 GAIA 프로젝트 설정하기

```bash
# 1. 프로젝트 디렉토리로 이동
cd /path/to/GAIA

# 2. 가상 환경 생성
python3 -m venv .venv

# 3. 가상 환경 활성화
source .venv/bin/activate

# 4. 필요한 패키지 설치
pip install -r requirements.txt

# 5. 환경 변수 설정 (.env 파일이 없는 경우)
cat > .env << EOF
ANTHROPIC_API_KEY=your_api_key_here
CLAUDE_API_VERSION=claude-3-7-sonnet-20250219
EOF

# 6. 프로젝트 실행
.venv/bin/python __main__.py
```

## 문제 해결

```bash
# 가상 환경 경로 확인
echo $VIRTUAL_ENV

# 실행 중인 Python 확인
which python

# 설치된 패키지 확인
pip list
```