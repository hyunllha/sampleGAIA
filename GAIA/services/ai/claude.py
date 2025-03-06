"""
Claude API와 통신하기 위한 서비스 모듈
"""
import anthropic
import os
from security.credentials.api_keys import APIKeyManager

class ClaudeService:
    def __init__(self):
        """Claude API 서비스 초기화"""
        self.api_key = APIKeyManager.get_claude_api_key()
        self.client = anthropic.Anthropic(api_key=self.api_key)
        # 환경 변수에서 모델 버전 가져오기
        self.model = os.getenv('CLAUDE_API_VERSION', "claude-3-7-sonnet-20250219")
    
    def generate_response(self, system_prompt, user_input):
        """
        Claude API를 사용하여 응답 생성
        
        Args:
            system_prompt (str): 시스템 프롬프트
            user_input (str): 사용자 입력
            
        Returns:
            str: 생성된 응답
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_input}
                ],
                max_tokens=2000
            )
            return response.content[0].text
        except Exception as e:
            print(f"Claude API 호출 중 오류 발생: {str(e)}")
            return None