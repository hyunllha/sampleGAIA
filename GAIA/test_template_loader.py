"""
템플릿 로더 테스트 스크립트
"""
import os
import sys
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 현재 디렉토리를 시스템 경로에 추가 (상대 경로 임포트 지원)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 필요한 모듈 임포트
from templates.loader import TemplateLoader
from core.config.constants import RESPONSE_TEMPLATE_COLUMNS, PROJECT_INFO_COLUMNS, PROMPT_TEMPLATE_COLUMNS

def test_load_templates():
    """
    각 템플릿 파일을 로드하고 기본 정보를 출력하는 테스트
    """
    print("\n=== 템플릿 로드 테스트 ===")
    
    # 1. 응답 템플릿 로드
    print("\n--- 응답 템플릿 ---")
    response_templates = TemplateLoader.load_template_csv("RESPONSE_TEMPLATE")
    if not response_templates.empty:
        print(f"총 {len(response_templates)} 개의 응답 템플릿을 로드했습니다.")
        print("첫 5개 템플릿 키:")
        for idx, key in enumerate(response_templates[RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"]].head(5)):
            print(f"  {idx+1}. {key}")
    
    # 2. 프로젝트 정보 로드
    print("\n--- 프로젝트 정보 ---")
    project_info = TemplateLoader.load_template_csv("PROJECT_INFO")
    if not project_info.empty:
        print(f"총 {len(project_info)} 개의 프로젝트를 로드했습니다.")
        print("프로젝트 목록:")
        for idx, (key, name) in enumerate(zip(
            project_info[PROJECT_INFO_COLUMNS["TITLE_KEY"]],
            project_info[PROJECT_INFO_COLUMNS["TITLE_NAME"]]
        )):
            print(f"  {idx+1}. {key}: {name}")
    
    # 3. 프롬프트 템플릿 로드
    print("\n--- 프롬프트 템플릿 ---")
    prompt_templates = TemplateLoader.load_template_csv("PROMPT_TEMPLATE")
    if not prompt_templates.empty:
        print(f"총 {len(prompt_templates)} 개의 프롬프트 템플릿을 로드했습니다.")
        print("프롬프트 키:")
        for idx, key in enumerate(prompt_templates[PROMPT_TEMPLATE_COLUMNS["PROMPT_KEY"]]):
            print(f"  {idx+1}. {key}")

def test_template_search():
    """
    특정 키로 템플릿을 검색하는 테스트
    """
    print("\n=== 템플릿 검색 테스트 ===")
    
    # 1. 응답 템플릿 검색
    key_to_search = "Temp_common_basic"  # 기본 틀 템플릿
    print(f"\n--- 응답 템플릿 검색: '{key_to_search}' ---")
    template = TemplateLoader.get_template_by_key(
        "RESPONSE_TEMPLATE", 
        RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"], 
        key_to_search
    )
    
    if template is not None:
        print(f"템플릿 ID: {template[RESPONSE_TEMPLATE_COLUMNS['NO']]}")
        print(f"카테고리: {template[RESPONSE_TEMPLATE_COLUMNS['TEMP_CATEGORY']]}")
        print(f"섹션: {template[RESPONSE_TEMPLATE_COLUMNS['TEMP_SECTION']]}")
        print(f"한국어 내용: {template[RESPONSE_TEMPLATE_COLUMNS['TEMP_CONTENT_KR']][:100]}...")
        print(f"일본어 내용: {template[RESPONSE_TEMPLATE_COLUMNS['TEMP_CONTENT_JP']][:100]}...")
    
    # 2. 프로젝트 정보 검색
    key_to_search = "GBTW"  # 건쉽배틀
    print(f"\n--- 프로젝트 정보 검색: '{key_to_search}' ---")
    project = TemplateLoader.get_template_by_key(
        "PROJECT_INFO", 
        PROJECT_INFO_COLUMNS["TITLE_KEY"], 
        key_to_search
    )
    
    if project is not None:
        print(f"프로젝트 ID: {project[PROJECT_INFO_COLUMNS['NO']]}")
        print(f"프로젝트명: {project[PROJECT_INFO_COLUMNS['TITLE_NAME']]}")
        print(f"프로젝트명(일본어): {project[PROJECT_INFO_COLUMNS['TITLE_NAME_JP']]}")
        print(f"인사말: {project[PROJECT_INFO_COLUMNS['GREETING']]}")

if __name__ == "__main__":
    test_load_templates()
    test_template_search()