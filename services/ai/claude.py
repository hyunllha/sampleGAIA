"""
Claude API와 통신하기 위한 서비스 모듈
"""
import anthropic
import os
import json
from security.credentials.api_keys import APIKeyManager

class ClaudeService:
    def __init__(self):
        """Claude API 서비스 초기화"""
        self.api_key = APIKeyManager.get_claude_api_key()
        self.client = anthropic.Anthropic(api_key=self.api_key)
        # 0.3.0 버전에서 지원하는 모델로 변경
        self.model = "claude-2"  # 환경변수 무시하고 강제 설정

    def generate_response(self, system_prompt, user_input):
        """
        Claude API를 사용하여 응답 생성

        Args:
            system_prompt (str): 시스템 프롬프트
            user_input (str): 사용자 입력

        Returns:
            str: 생성된 응답 또는 오류 메시지가 포함된 JSON 문자열
        """
        try:
            # 입력 유효성 검사
            if not self.api_key:
                error_msg = "Claude API 키가 설정되지 않았습니다."
                print(error_msg)
                return json.dumps({
                    "error": error_msg,
                    "summary": "API 키 오류",
                    "suggestion": "API 키를 설정해주세요.",
                    "response_mail": "APIキーが設定されていません。"
                })

            if not user_input:
                error_msg = "사용자 입력이 비어 있습니다."
                print(error_msg)
                return json.dumps({
                    "error": error_msg,
                    "summary": "입력 오류",
                    "suggestion": "사용자 입력을 제공해주세요.",
                    "response_mail": "ユーザー入力が空です。"
                })

            # Anthropic 0.3.0 버전에 맞는 방식으로 시스템 프롬프트와 사용자 입력 결합
            combined_prompt = f"{anthropic.HUMAN_PROMPT} "

            if system_prompt:
                combined_prompt += f"<시스템>\n{system_prompt}\n</시스템>\n\n"

            combined_prompt += f"{user_input}{anthropic.AI_PROMPT}"

            # API 호출 (0.3.0 버전에 맞는 방식)
            response = self.client.completions.create(
                prompt=combined_prompt,
                model=self.model,
                max_tokens_to_sample=2000,
                stop_sequences=[anthropic.HUMAN_PROMPT]
            )

            # 응답 검증
            if response and hasattr(response, 'completion'):
                return response.completion.strip()  # 결과 반환
            else:
                error_msg = "API에서 유효한 응답을 받지 못했습니다."
                print(error_msg)
                return json.dumps({
                    "error": error_msg,
                    "summary": "API 응답 오류",
                    "suggestion": "API 응답이 비어있습니다.",
                    "response_mail": "APIからの応答が空です。"
                })

        except anthropic.APIError as api_err:
            error_msg = f"Claude API 오류: {str(api_err)}"
            print(error_msg)
            return json.dumps({
                "error": error_msg,
                "summary": "API 오류",
                "suggestion": "API 오류가 발생했습니다. 다시 시도해주세요.",
                "response_mail": "APIエラーが発生しました。"
            })

        except Exception as e:
            error_msg = f"Claude API 호출 중 오류 발생: {str(e)}"
            print(error_msg)
            return json.dumps({
                "error": error_msg,
                "summary": "시스템 오류",
                "suggestion": "오류가 발생했습니다. 기술 지원팀에 문의하세요.",
                "response_mail": "システムエラーが発生しました。"
            })