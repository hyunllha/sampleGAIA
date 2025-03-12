"""
Claude API 연동 테스트 스크립트
"""
import os
import sys
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 현재 디렉토리를 시스템 경로에 추가 (상대 경로 임포트 지원)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 필요한 모듈 임포트
from security.credentials.api_keys import APIKeyManager
from services.ai.claude import ClaudeService

def main():
    # API 키 검증
    if not APIKeyManager.validate_api_keys():
        print("필수 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        return
    
    # Claude 서비스 초기화
    claude_service = ClaudeService()
    
    # 간단한 테스트 프롬프트
    system_prompt = "당신은 게임 고객 지원을 위한 AI 비서입니다."
    user_input = "안녕하세요, 게임에서 아이템을 잃어버렸어요. 어떻게 해야 하나요?"
    
    print("Claude API에 요청을 보내는 중...")
    
    # 응답 생성
    response = claude_service.generate_response(system_prompt, user_input)
    
    # 결과 출력
    if response:
        print("\n=== Claude API 응답 ===")
        print(response)
        print("======================")
        print("\nAPI 테스트가 성공적으로 완료되었습니다!")
    else:
        print("API 호출 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()