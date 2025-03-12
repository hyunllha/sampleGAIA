"""
투스텝 프로세스 모듈
일본어 문의 내용을 번역하고 검토한 후 답변을 생성하는 프로세스를 처리합니다.
"""
import os
import json
from templates.loader import TemplateLoader
from services.ai.claude import ClaudeService
from core.config.constants import RESPONSE_TEMPLATE_COLUMNS, PROJECT_INFO_COLUMNS, PROMPT_TEMPLATE_COLUMNS


class TwoStepProcess:
    """
    일본어 불가자를 위한 투스텝 프로세스 클래스
    """

    def __init__(self):
        """투스텝 프로세스 초기화"""
        self.claude_service = ClaudeService()

    def translate_inquiry(self, inquiry_title, inquiry_content):
        """
        문의 내용을 번역하고 분석하는 첫 번째 단계

        Args:
            inquiry_title (str): 문의 제목 (일본어)
            inquiry_content (str): 문의 내용 (일본어)

        Returns:
            dict: 번역 및 분석 결과
        """
        try:
            # 1. 시스템 프롬프트 로드
            system_prompt_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"],
                "GAIA_SYSTEM_MAIN")

            if system_prompt_row is None:
                raise ValueError("시스템 프롬프트를 찾을 수 없습니다.")

            system_prompt = system_prompt_row[
                PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]]

            # 2. 사용자 입력 구성
            user_input = self._create_translation_input(
                inquiry_title, inquiry_content)

            # 3. Claude API 호출
            response = self.claude_service.generate_response(
                system_prompt, user_input)

            # 3-1. 응답이 None인지 확인
            if response is None:
                print("Claude API가 None을 반환했습니다.")
                return {
                    "summary": "API가 응답을 생성하지 못했습니다.",
                    "suggestion": "API 키와 연결을 확인해주세요.",
                    "title_jp": inquiry_title,
                    "content_jp": inquiry_content,
                    "response_mail": "システムエラーが発生しました。",
                    "recommended_templates": []
                }

            # 4. 응답 파싱 (JSON 형식으로 반환됨) - 개선된 코드
            try:
                result = json.loads(response)

                # 필수 필드 확인 및 기본값 설정
                if "summary" not in result or not result["summary"]:
                    result["summary"] = "번역된 요약이 생성되지 않았습니다."
                if "suggestion" not in result or not result["suggestion"]:
                    result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
                if "title_jp" not in result:
                    result["title_jp"] = inquiry_title
                if "content_jp" not in result:
                    result["content_jp"] = inquiry_content

                # 템플릿 추천 정보 추가
                result["recommended_templates"] = self._recommend_templates(
                    result["summary"])
                return result
            except json.JSONDecodeError:
                print("API 응답을 JSON으로 파싱할 수 없습니다.")
                print(f"받은 응답: {response[:200]}...")  # 처음 200자만 로깅
                # 비 JSON 응답의 경우 기본 형식으로 변환
                fallback_result = {
                    "summary": "일본어 문의를 번역하는 중 오류가 발생했습니다.",
                    "suggestion": "원본 일본어 내용을 확인해주세요.",
                    "title_jp": inquiry_title,
                    "content_jp": inquiry_content,
                    "response_mail": "翻訳中にエラーが発生しました。",
                    "recommended_templates": []
                }
                return fallback_result

        except Exception as e:
            print(f"문의 번역 중 오류 발생: {str(e)}")
            return {
                "summary": f"오류 발생: {str(e)}",
                "suggestion": "시스템 오류가 발생했습니다. 로그를 확인해주세요.",
                "title_jp": inquiry_title,
                "content_jp": inquiry_content,
                "response_mail": "システムエラーが発生しました。",
                "recommended_templates": []
            }

    def generate_response(self,
                          inquiry_title,
                          inquiry_content,
                          translated_summary,
                          project_key,
                          template_key=None,
                          custom_response=None):
        """
        번역된 문의에 대한 답변을 생성하는 두 번째 단계

        Args:
            inquiry_title (str): 문의 제목 (일본어)
            inquiry_content (str): 문의 내용 (일본어)
            translated_summary (str): 번역된 요약 (한국어)
            project_key (str): 프로젝트 키 (예: GBTW)
            template_key (str, optional): 사용할 템플릿 키 (없으면 None)
            custom_response (str, optional): 커스텀 응답 메시지 (없으면 None)

        Returns:
            dict: 처리 결과 (summary, suggestion, response_mail)
        """
        try:
            # 1. 프로젝트 정보 로드
            project_info = TemplateLoader.get_template_by_key(
                "PROJECT_INFO", PROJECT_INFO_COLUMNS["TITLE_KEY"], project_key)

            if project_info is None:
                raise ValueError(
                    f"프로젝트 키 '{project_key}'에 해당하는 정보를 찾을 수 없습니다.")

            # 2. 템플릿 로드 (지정된 경우)
            template = None
            if template_key:
                template = TemplateLoader.get_template_by_key(
                    "RESPONSE_TEMPLATE", RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"],
                    template_key)

            # 3. 시스템 프롬프트 로드
            system_prompt_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"],
                "GAIA_SYSTEM_MAIN")

            if system_prompt_row is None:
                raise ValueError("시스템 프롬프트를 찾을 수 없습니다.")

            system_prompt = system_prompt_row[
                PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]]

            # 4. 사용자 입력 구성
            user_input = self._create_response_input(inquiry_title,
                                                     inquiry_content,
                                                     translated_summary,
                                                     project_info, template,
                                                     custom_response)

            # 5. Claude API 호출
            response = self.claude_service.generate_response(
                system_prompt, user_input)

            # 5-1. 응답이 None인지 확인
            if response is None:
                print("Claude API가 None을 반환했습니다.")
                return {
                    "summary": "API가 응답을 생성하지 못했습니다.",
                    "suggestion": "API 키와 연결을 확인해주세요.",
                    "response_mail": "システムエラーが発生しました。"
                }

            # 6. 응답 파싱 (JSON 형식으로 반환됨)
            try:
                result = json.loads(response)
                # 필수 필드 확인 및 기본값 설정
                if "summary" not in result or not result["summary"]:
                    result["summary"] = "문의 내용 요약이 생성되지 않았습니다."
                if "suggestion" not in result or not result["suggestion"]:
                    result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
                if "response_mail" not in result or not result["response_mail"]:
                    result["response_mail"] = "응답 메일이 생성되지 않았습니다."
                return result
            except json.JSONDecodeError:
                print("API 응답을 JSON으로 파싱할 수 없습니다.")
                print(f"받은 응답: {response[:200]}...")  # 처음 200자만 로깅
                return {
                    "summary": "응답 파싱 실패",
                    "suggestion": "API 응답 형식을 확인해주세요.",
                    "response_mail": "システムエラーが発生しました。"
                }

        except Exception as e:
            print(f"응답 생성 중 오류 발생: {str(e)}")
            return {
                "summary": f"오류 발생: {str(e)}",
                "suggestion": "시스템 오류가 발생했습니다. 로그를 확인해주세요.",
                "response_mail": "システムエラーが発生しました。"
            }

    def _create_translation_input(self, inquiry_title, inquiry_content):
        """
        Claude API에 전달할 번역 요청 입력을 구성합니다.

        Args:
            inquiry_title (str): 문의 제목 (일본어)
            inquiry_content (str): 문의 내용 (일본어)

        Returns:
            str: 구성된 사용자 입력
        """
        # 투스텝 번역 프롬프트 템플릿 로드
        prompt_template_row = TemplateLoader.get_template_by_key(
            "PROMPT_TEMPLATE", PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"],
            "GAIA_TWOSTEP_TRANSLATE")

        if prompt_template_row is None:
            # 폴백: 하드코딩된 템플릿 사용
            base_prompt = "# 문의 정보\n문의 제목: {inquiry_title}\n문의 내용: {inquiry_content}\n\n# 지시사항\n위 일본어 문의 내용을 한국어로 번역 및 분석해주세요.\n응답은 반드시 지정된 JSON 형식으로 출력해주세요.\nsummary는 한국어로 문의 내용을 요약 및 번역해주세요.\nsuggestion은 한국어로 어떤 답변을 할지 제안해주세요.\nresponse_mail은 일단 번역 단계이므로 간단한 일본어 메시지로 작성해주세요."
        else:
            base_prompt = prompt_template_row[
                PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]]

        # 프롬프트 구성
        prompt = base_prompt.format(inquiry_title=inquiry_title,
                                    inquiry_content=inquiry_content)

        return prompt

    def _create_response_input(self,
                               inquiry_title,
                               inquiry_content,
                               translated_summary,
                               project_info,
                               template=None,
                               custom_response=None):
        """
        Claude API에 전달할 응답 생성 입력을 구성합니다.

        Args:
            inquiry_title (str): 문의 제목 (일본어)
            inquiry_content (str): 문의 내용 (일본어)
            translated_summary (str): 번역된 요약 (한국어)
            project_info (Series): 프로젝트 정보
            template (Series, optional): 응답 템플릿
            custom_response (str, optional): 커스텀 응답 내용

        Returns:
            str: 구성된 사용자 입력
        """
        # 프로젝트 정보 추출
        project_name = project_info[PROJECT_INFO_COLUMNS["TITLE_NAME"]]
        project_name_jp = project_info[PROJECT_INFO_COLUMNS["TITLE_NAME_JP"]]
        greeting = project_info[PROJECT_INFO_COLUMNS["GREETING"]]
        closing = project_info[PROJECT_INFO_COLUMNS["CLOSING"]]
        user_title = project_info[PROJECT_INFO_COLUMNS["USER_TITLE"]]

        # 투스텝 응답 프롬프트 템플릿 로드
        prompt_template_row = TemplateLoader.get_template_by_key(
            "PROMPT_TEMPLATE", PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"],
            "GAIA_TWOSTEP_RESPONSE")

        if prompt_template_row is None:
            # 폴백: 하드코딩된 템플릿 사용
            base_prompt = "# 문의 정보\n문의 제목: {inquiry_title}\n문의 내용: {inquiry_content}\n번역된 요약: {translated_summary}\n\n# 프로젝트 정보\n프로젝트명: {project_name}\n프로젝트명(일본어): {project_name_jp}\n유저 호칭: {user_title}\n인사말: {greeting}\n맺음말: {closing}\n\n{template_section}\n{custom_response_section}\n# 지시사항\n위 정보를 바탕으로 문의에 대한 응답을 작성해주세요.\n응답은 반드시 지정된 JSON 형식으로 출력해주세요.\nsummary는 한국어로 문의 내용을 요약해주세요.\nsuggestion은 한국어로 어떤 답변을 할지 제안해주세요.\nresponse_mail은 일본어로 작성하되, 인사말과 맺음말을 포함해주세요."
        else:
            base_prompt = prompt_template_row[
                PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]]

        # 템플릿 섹션 구성
        template_section = ""
        if template is not None:
            # 템플릿 섹션 프롬프트 컴포넌트 로드
            template_section_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"],
                "GAIA_TEMPLATE_SECTION")

            if template_section_row is not None:
                template_section = template_section_row[
                    PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]].format(
                        temp_category=template[
                            RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]],
                        temp_section=template[
                            RESPONSE_TEMPLATE_COLUMNS["TEMP_SECTION"]],
                        temp_content_kr=template[
                            RESPONSE_TEMPLATE_COLUMNS["TEMP_CONTENT_KR"]],
                        temp_content_jp=template[
                            RESPONSE_TEMPLATE_COLUMNS["TEMP_CONTENT_JP"]])

        # 커스텀 응답 섹션 구성
        custom_response_section = ""
        if custom_response:
            # 커스텀 응답 섹션 프롬프트 컴포넌트 로드
            custom_response_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"],
                "GAIA_CUSTOM_RESPONSE")

            if custom_response_row is not None:
                custom_response_section = custom_response_row[
                    PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]].format(
                        custom_response=custom_response)

        # 최종 프롬프트 구성
        prompt = base_prompt.format(
            inquiry_title=inquiry_title,
            inquiry_content=inquiry_content,
            translated_summary=translated_summary,
            project_name=project_name,
            project_name_jp=project_name_jp,
            user_title=user_title,
            greeting=greeting,
            closing=closing,
            template_section=template_section,
            custom_response_section=custom_response_section)

        return prompt

    def _recommend_templates(self, summary):
        """
        문의 내용 요약을 기반으로, 적합한 템플릿을 추천합니다.

        Args:
            summary (str): 문의 내용 요약 (한국어)

        Returns:
            list: 추천 템플릿 목록 [{"key": "템플릿키", "category": "카테고리", "section": "섹션"}, ...]
        """
        # 모든 응답 템플릿 로드
        templates_df = TemplateLoader.load_template_csv("RESPONSE_TEMPLATE")
        if templates_df.empty:
            return []

        # 키워드 기반 간단한 추천 알고리즘
        # 실제 구현에서는 더 복잡한 알고리즘이나 임베딩 기반 검색 등을 사용할 수 있습니다.
        keywords = {
            "결제": ["결제", "구매", "환불", "취소", "충전", "구입", "환급"],
            "계정": ["계정", "로그인", "비밀번호", "연동", "탈퇴", "삭제", "복구"],
            "오류": ["오류", "버그", "에러", "문제", "안됨", "불가", "작동"],
            "건의사항": ["제안", "건의", "개선", "추가", "업데이트", "바람"],
            "아이템": ["아이템", "상품", "보상", "보석", "코인", "골드", "재화"]
        }

        recommended = []

        # 요약에서 키워드 찾기
        for category, word_list in keywords.items():
            for word in word_list:
                if word in summary:
                    # 해당 카테고리의 템플릿 찾기
                    category_templates = templates_df[templates_df[
                        RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]] ==
                                                      category]

                    # 결과에 추가
                    for idx, row in category_templates.iterrows():
                        template_info = {
                            "key":
                            row[RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"]],
                            "category":
                            row[RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]],
                            "section":
                            row[RESPONSE_TEMPLATE_COLUMNS["TEMP_SECTION"]]
                        }
                        if template_info not in recommended:
                            recommended.append(template_info)

                    # 중복 방지를 위해 해당 카테고리 키워드 검색 중단
                    break

        # 기본 템플릿 항상 추가
        basic_templates = templates_df[templates_df[
            RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]] == "기본"]

        for idx, row in basic_templates.iterrows():
            template_info = {
                "key": row[RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"]],
                "category": row[RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]],
                "section": row[RESPONSE_TEMPLATE_COLUMNS["TEMP_SECTION"]]
            }
            if template_info not in recommended:
                recommended.append(template_info)

        # 최대 5개만 반환
        return recommended[:5]
