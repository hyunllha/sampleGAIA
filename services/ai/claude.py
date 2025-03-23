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
        # 환경 변수에서 모델명 가져오기
        self.model = os.getenv("CLAUDE_API_VERSION", "claude-3-7-sonnet-20250219")

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
            # 디버깅을 위한 로그 추가
            print("\n===== Claude API 호출 정보 =====")
            print(f"사용 모델: {self.model}")
            print(f"API 키: {self.api_key[:10]}...{self.api_key[-5:] if len(self.api_key) > 15 else '***'}")
            print(f"시스템 프롬프트 길이: {len(system_prompt) if system_prompt else 0}")
            print("===============================\n")


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

            # API 호출 (최신 버전에 맞는 방식)
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_input}]
            )
            # 여기에 응답 로그 코드 추가
            if response:
                print("\n===== Claude API 응답 정보 =====")
                # 최신 API에서는 response.model로 사용된 모델 확인 가능
                if hasattr(response, 'model'):
                    print(f"응답한 모델: {response.model}")
                else:
                    print("응답 객체에 모델 정보가 없습니다")
                print("===============================\n")

            # 응답 검증
            if response and hasattr(response, 'content'):
                # 최신 API에서는 content 속성에 배열로 응답이 있음
                return response.content[0].text  # 결과 반환
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