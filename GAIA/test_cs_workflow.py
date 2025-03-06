"""
CS 워크플로우 테스트 스크립트
"""
import os
import sys
import json
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 현재 디렉토리를 시스템 경로에 추가 (상대 경로 임포트 지원)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 필요한 모듈 임포트
from cs.responses.generator import ResponseGenerator
from security.credentials.api_keys import APIKeyManager

def test_onestep_process():
    """원스텝 프로세스 테스트"""
    print("\n=== 원스텝 프로세스 테스트 ===")
    
    # API 키 검증
    if not APIKeyManager.validate_api_keys():
        print("필수 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        return
    
    # 응답 생성기 초기화
    generator = ResponseGenerator()
    
    # 테스트 데이터
    inquiry_title = "ゲーム内アイテムが届きません"
    inquiry_content = """
    先日、「ダイヤ×100」の課金をしました。決済は完了しましたが、アイテムが届いていません。
    注文番号: GPA.3384-5923-9827-62486
    購入日: 2023/11/20
    プレイヤーID: 83751254
    
    早急にご対応お願いいたします。
    """
    project_key = "GBTW"
    template_key = "Temp_common_payment_missing_no_receipt"
    
    # 결제 미반영 (영수증 미지참) 템플릿 사용
    result = generator.process_onestep(
        inquiry_title, 
        inquiry_content, 
        project_key, 
        template_key
    )
    
    # 결과 출력
    print("\n원스텝 프로세스 결과:")
    print(f"요약: {result['summary']}")
    print(f"제안: {result['suggestion']}")
    print("\n응답 메일:")
    print(result['response_mail'])


def test_twostep_process():
    """투스텝 프로세스 테스트"""
    print("\n=== 투스텝 프로세스 테스트 ===")
    
    # API 키 검증
    if not APIKeyManager.validate_api_keys():
        print("필수 API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
        return
    
    # 응답 생성기 초기화
    generator = ResponseGenerator()
    
    # 테스트 데이터
    inquiry_title = "アップデート後にログインできません"
    inquiry_content = """
    最近のアップデート後、ゲームにログインできなくなりました。
    起動するとすぐにクラッシュします。
    端末: iPhone 13 Pro
    OSバージョン: iOS 16.5
    アプリバージョン: 2.5.0
    
    どうすれば良いでしょうか？
    """
    
    # 1단계: 번역 및 분석
    print("\n[1단계] 번역 및 분석 중...")
    translation_result = generator.process_twostep_translation(
        inquiry_title,
        inquiry_content
    )
    
    # 번역 결과 출력
    print("\n1단계 결과:")
    print(f"요약: {translation_result['summary']}")
    print(f"제안: {translation_result['suggestion']}")
    print("\n추천 템플릿:")
    for idx, template in enumerate(translation_result['recommended_templates']):
        print(f"  {idx+1}. {template['key']} ({template['category']} - {template['section']})")
    
    # 2단계: 응답 생성
    project_key = "GBTW"
    template_key = "Temp_common_troubleshooting"  # 트러블슈팅 템플릿 사용
    
    print("\n[2단계] 응답 생성 중...")
    response_result = generator.process_twostep_response(
        inquiry_title,
        inquiry_content,
        translation_result['summary'],
        project_key,
        template_key
    )
    
    # 응답 결과 출력
    print("\n2단계 결과:")
    print(f"요약: {response_result['summary']}")
    print(f"제안: {response_result['suggestion']}")
    print("\n응답 메일:")
    print(response_result['response_mail'])


if __name__ == "__main__":
    # 원스텝 프로세스 테스트
    test_onestep_process()
    
    # 투스텝 프로세스 테스트
    test_twostep_process()