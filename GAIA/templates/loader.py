"""
CSV 템플릿 파일을 로드하고 관리하는 모듈
"""
import pandas as pd
import os
from pathlib import Path
from core.config.constants import CSV_PATHS, CSV_SETTINGS

class TemplateLoader:
    """
    CSV 파일에서 템플릿을 로드하고 관리하는 클래스
    """
    
    @staticmethod
    def load_template_csv(template_type):
        """
        CSV 템플릿 파일을 로드하는 함수
        
        Args:
            template_type (str): 템플릿 타입 (RESPONSE_TEMPLATE, PROJECT_INFO, PROMPT_TEMPLATE)
            
        Returns:
            DataFrame: 로드된 템플릿 데이터
        """
        try:
            file_path = CSV_PATHS.get(template_type)
            if not file_path:
                raise ValueError(f"템플릿 타입 '{template_type}'에 대한 경로가 정의되지 않았습니다.")
                
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"템플릿 파일이 존재하지 않습니다: {file_path}")
                
            df = pd.read_csv(
                file_path,
                delimiter=CSV_SETTINGS["DELIMITER"],
                encoding=CSV_SETTINGS["ENCODING"]
            )
            print(f"템플릿 '{template_type}' 로드 완료: {len(df)} 행")
            return df
        except Exception as e:
            print(f"템플릿 로드 중 오류 발생: {str(e)}")
            return pd.DataFrame()
    
    @staticmethod
    def get_template_by_key(template_type, key_column, key_value):
        """
        특정 키에 해당하는 템플릿 행을 가져옵니다.
        
        Args:
            template_type (str): 템플릿 타입 (RESPONSE_TEMPLATE, PROJECT_INFO, PROMPT_TEMPLATE)
            key_column (str): 키 컬럼 이름
            key_value (str): 찾을 키 값
            
        Returns:
            Series: 해당 키를 가진 템플릿 행 (없으면 None)
        """
        try:
            df = TemplateLoader.load_template_csv(template_type)
            if df.empty:
                return None
                
            # 해당 키를 가진 행 찾기
            matching_rows = df[df[key_column] == key_value]
            
            if matching_rows.empty:
                print(f"키 '{key_value}'에 해당하는 템플릿을 찾을 수 없습니다.")
                return None
                
            # 첫 번째 일치하는 행 반환
            return matching_rows.iloc[0]
        except Exception as e:
            print(f"템플릿 검색 중 오류 발생: {str(e)}")
            return None