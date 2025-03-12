"""
API 키 관리를 위한 모듈
환경 변수나 암호화된 파일에서 API 키를 안전하게 로드합니다.
"""
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class APIKeyManager:
    """API 키 관리 클래스"""
    
    @staticmethod
    def get_claude_api_key():
        """
        Claude API 키를 안전하게 가져옵니다.
        
        Returns:
            str: API 키 또는 키가 없는 경우 None
        """
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.")
        return api_key
    
    @staticmethod
    def validate_api_keys():
        """
        모든 필수 API 키가 설정되어 있는지 확인합니다.
        
        Returns:
            bool: 모든 키가 설정되어 있으면 True, 그렇지 않으면 False
        """
        required_keys = ['ANTHROPIC_API_KEY', 'CLAUDE_API_VERSION']
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            print(f"경고: 다음 API 키/설정이 환경 변수에 없습니다: {', '.join(missing_keys)}")
            return False
        return True