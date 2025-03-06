"""
CS 응답 생성 모듈
원스텝/투스텝 프로세스를 통합하여 응답을 생성합니다.
"""
from cs.workflow.onestep import OneStepProcess
from cs.workflow.twostep import TwoStepProcess

class ResponseGenerator:
    """
    CS 응답 생성 클래스
    """
    
    def __init__(self):
        """응답 생성기 초기화"""
        self.onestep = OneStepProcess()
        self.twostep = TwoStepProcess()
    
    def process_onestep(self, inquiry_title, inquiry_content, project_key, template_key=None, custom_response=None):
        """
        원스텝 프로세스로 문의 처리 (일본어 가능자용)
        
        Args:
            inquiry_title (str): 문의 제목
            inquiry_content (str): 문의 내용
            project_key (str): 프로젝트 키 (예: GBTW)
            template_key (str, optional): 사용할 템플릿 키 (없으면 None)
            custom_response (str, optional): 커스텀 응답 메시지 (없으면 None)
            
        Returns:
            dict: 처리 결과 (summary, suggestion, response_mail)
        """
        # 응답 생성
        result = self.onestep.process_inquiry(
            inquiry_title, inquiry_content, project_key, template_key, custom_response
        )
        
        # 결과 유효성 검사 - 필수 필드가 없거나 비어있는 경우 기본값 제공
        if not result.get("summary"):
            result["summary"] = "문의 내용 요약이 생성되지 않았습니다."
        if not result.get("suggestion"):
            result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
        if not result.get("response_mail"):
            result["response_mail"] = "응답 메일이 생성되지 않았습니다."
            
        return result
    
    def process_twostep_translation(self, inquiry_title, inquiry_content):
        """
        투스텝 프로세스의 첫 번째 단계: 번역 및 분석 (일본어 불가자용)
        
        Args:
            inquiry_title (str): 문의 제목 (일본어)
            inquiry_content (str): 문의 내용 (일본어)
            
        Returns:
            dict: 번역 및 분석 결과
        """
        return self.twostep.translate_inquiry(inquiry_title, inquiry_content)
    
    def process_twostep_response(self, inquiry_title, inquiry_content, translated_summary, 
                               project_key, template_key=None, custom_response=None):
        """
        투스텝 프로세스의 두 번째 단계: 응답 생성 (일본어 불가자용)
        
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
        # 응답 생성
        result = self.twostep.generate_response(
            inquiry_title, inquiry_content, translated_summary,
            project_key, template_key, custom_response
        )
        
        # 결과 유효성 검사 - 필수 필드가 없거나 비어있는 경우 기본값 제공
        if not result.get("summary"):
            result["summary"] = "문의 내용 요약이 생성되지 않았습니다."
        if not result.get("suggestion"):
            result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
        if not result.get("response_mail"):
            result["response_mail"] = "응답 메일이 생성되지 않았습니다."
            
        return result