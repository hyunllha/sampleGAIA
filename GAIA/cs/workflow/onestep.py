"""
원스텝 프로세스 모듈
일본어 문의에 대해 직접 답변을 작성하는 프로세스를 처리합니다.
"""
import os
import json
from templates.loader import TemplateLoader
from services.ai.claude import ClaudeService
from core.config.constants import RESPONSE_TEMPLATE_COLUMNS, PROJECT_INFO_COLUMNS, PROMPT_TEMPLATE_COLUMNS

class OneStepProcess:
    """
    일본어 가능자를 위한 원스텝 프로세스 클래스
    """
    
    def __init__(self):
        """원스텝 프로세스 초기화"""
        self.claude_service = ClaudeService()
        
    def process_inquiry(self, inquiry_title, inquiry_content, project_key, template_key=None, custom_response=None):
        """
        문의 처리 함수
        
        Args:
            inquiry_title (str): 문의 제목
            inquiry_content (str): 문의 내용
            project_key (str): 프로젝트 키 (예: GBTW)
            template_key (str, optional): 사용할 템플릿 키 (없으면 None)
            custom_response (str, optional): 커스텀 응답 메시지 (없으면 None)
            
        Returns:
            dict: 처리 결과 (summary, suggestion, response_mail)
        """
        try:
            # 1. 프로젝트 정보 로드
            project_info = TemplateLoader.get_template_by_key(
                "PROJECT_INFO", 
                PROJECT_INFO_COLUMNS["TITLE_KEY"], 
                project_key
            )
            
            if project_info is None:
                raise ValueError(f"프로젝트 키 '{project_key}'에 해당하는 정보를 찾을 수 없습니다.")
            
            # 2. 템플릿 로드 (지정된 경우)
            template = None
            if template_key:
                template = TemplateLoader.get_template_by_key(
                    "RESPONSE_TEMPLATE", 
                    RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"], 
                    template_key
                )
            
            # 3. 시스템 프롬프트 로드
            system_prompt_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", 
                PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"], 
                "GAIA_SYSTEM_MAIN"
            )
            
            if system_prompt_row is None:
                raise ValueError("시스템 프롬프트를 찾을 수 없습니다.")
            
            system_prompt = system_prompt_row[PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]]
            
            # 4. 사용자 입력 (프롬프트) 구성
            user_input = self._create_user_input(
                inquiry_title, 
                inquiry_content,
                project_info,
                template,
                custom_response
            )
            
            # 5. Claude API 호출
            response = self.claude_service.generate_response(system_prompt, user_input)
            
            # 6. 응답 파싱 (JSON 형식으로 반환됨) - 개선된 코드
            try:
                result = json.loads(response)
                # 필수 필드가 있는지 확인하고 없으면 기본값 제공
                if "summary" not in result or not result["summary"]:
                    result["summary"] = "문의 내용 요약이 생성되지 않았습니다."
                if "suggestion" not in result or not result["suggestion"]:
                    result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
                if "response_mail" not in result or not result["response_mail"]:
                    result["response_mail"] = "응답 메일이 생성되지 않았습니다."
                return result
            except json.JSONDecodeError:
                print("API 응답을 JSON으로 파싱할 수 없습니다.")
                return {
                    "summary": "응답 파싱 실패",
                    "suggestion": "API 응답 형식을 확인해주세요.",
                    "response_mail": response
                }
            
        except Exception as e:
            print(f"원스텝 프로세스 처리 중 오류 발생: {str(e)}")
            return {
                "summary": f"오류 발생: {str(e)}",
                "suggestion": "시스템 오류가 발생했습니다. 로그를 확인해주세요.",
                "response_mail": "システムエラーが発生しました。"
            }
    
    def _create_user_input(self, inquiry_title, inquiry_content, project_info, template=None, custom_response=None):
        """
        Claude API에 전달할 사용자 입력을 구성합니다.
        
        Args:
            inquiry_title (str): 문의 제목
            inquiry_content (str): 문의 내용
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
        
        # 원스텝 프롬프트 템플릿 로드
        prompt_template_row = TemplateLoader.get_template_by_key(
            "PROMPT_TEMPLATE", 
            PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"], 
            "GAIA_ONESTEP_PROMPT"
        )
        
        if prompt_template_row is None:
            # 폴백: 하드코딩된 템플릿 사용
            base_prompt = "# 문의 정보\n문의 제목: {inquiry_title}\n문의 내용: {inquiry_content}\n\n# 프로젝트 정보\n프로젝트명: {project_name}\n프로젝트명(일본어): {project_name_jp}\n유저 호칭: {user_title}\n인사말: {greeting}\n맺음말: {closing}\n\n{template_section}\n{custom_response_section}\n# 지시사항\n위 정보를 바탕으로 문의에 대한 응답을 작성해주세요.\n응답은 반드시 지정된 JSON 형식으로 출력해주세요.\nsummary는 한국어로 문의 내용을 요약해주세요.\nsuggestion은 한국어로 어떤 답변을 할지 제안해주세요.\nresponse_mail은 일본어로 작성하되, 인사말과 맺음말을 포함해주세요."
        else:
            base_prompt = prompt_template_row[PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]]
        
        # 템플릿 섹션 구성
        template_section = ""
        if template is not None:
            # 템플릿 섹션 프롬프트 컴포넌트 로드
            template_section_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", 
                PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"], 
                "GAIA_TEMPLATE_SECTION"
            )
            
            if template_section_row is not None:
                template_section = template_section_row[PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]].format(
                    temp_category=template[RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]],
                    temp_section=template[RESPONSE_TEMPLATE_COLUMNS["TEMP_SECTION"]],
                    temp_content_kr=template[RESPONSE_TEMPLATE_COLUMNS["TEMP_CONTENT_KR"]],
                    temp_content_jp=template[RESPONSE_TEMPLATE_COLUMNS["TEMP_CONTENT_JP"]]
                )
        
        # 커스텀 응답 섹션 구성
        custom_response_section = ""
        if custom_response:
            # 커스텀 응답 섹션 프롬프트 컴포넌트 로드
            custom_response_row = TemplateLoader.get_template_by_key(
                "PROMPT_TEMPLATE", 
                PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"], 
                "GAIA_CUSTOM_RESPONSE"
            )
            
            if custom_response_row is not None:
                custom_response_section = custom_response_row[PROMPT_TEMPLATE_COLUMNS["PROMPT_CONTENT"]].format(
                    custom_response=custom_response
                )
        
        # 최종 프롬프트 구성
        prompt = base_prompt.format(
            inquiry_title=inquiry_title,
            inquiry_content=inquiry_content,
            project_name=project_name,
            project_name_jp=project_name_jp,
            user_title=user_title,
            greeting=greeting,
            closing=closing,
            template_section=template_section,
            custom_response_section=custom_response_section
        )
        
        return prompt