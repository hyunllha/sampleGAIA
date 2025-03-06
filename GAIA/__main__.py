from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from dotenv import load_dotenv
import json

# 필요한 모듈 임포트
from cs.responses.generator import ResponseGenerator
from templates.loader import TemplateLoader
from core.config.constants import RESPONSE_TEMPLATE_COLUMNS, PROJECT_INFO_COLUMNS

# 환경 변수 로드
load_dotenv()

# Flask 앱 초기화
def create_app():
    app = Flask(__name__, 
                static_folder='ui/static', 
                template_folder='ui/templates')
    
    # 세션을 위한 시크릿 키
    app.secret_key = os.getenv('SECRET_KEY', 'dev-key-for-testing')
    
    # nl2br 필터 추가 - 다양한 줄바꿈 형식 처리 기능 개선
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        if not text:
            return ""
        # 이스케이프된 줄바꿈과 일반 줄바꿈 모두 처리
        return text.replace('\\n', '<br>').replace('\n', '<br>')
    
    # 프로젝트 정보 로드
    projects_df = TemplateLoader.load_template_csv("PROJECT_INFO")
    projects = []
    if not projects_df.empty:
        for _, row in projects_df.iterrows():
            projects.append({
                'key': row[PROJECT_INFO_COLUMNS["TITLE_KEY"]],
                'name': row[PROJECT_INFO_COLUMNS["TITLE_NAME"]],
                'name_jp': row[PROJECT_INFO_COLUMNS["TITLE_NAME_JP"]]
            })
    
    # 응답 생성기 초기화
    response_generator = ResponseGenerator()
    
    # 컨텍스트 프로세서 - 모든 템플릿에서 사용 가능한 전역 변수
    @app.context_processor
    def inject_projects():
        return dict(projects=projects)
    
    # 라우트 정의
    @app.route('/')
    def index():
        return render_template('dashboard/index.html')
    
    # 원스텝 프로세스 라우트
    @app.route('/onestep', methods=['GET', 'POST'])
    def onestep():
        templates_df = TemplateLoader.load_template_csv("RESPONSE_TEMPLATE")
        templates = []
        
        if not templates_df.empty:
            for _, row in templates_df.iterrows():
                templates.append({
                    'key': row[RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"]],
                    'category': row[RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]],
                    'section': row[RESPONSE_TEMPLATE_COLUMNS["TEMP_SECTION"]]
                })
        
        if request.method == 'POST':
            # 폼 데이터 처리
            inquiry_title = request.form.get('inquiry_title', '')
            inquiry_content = request.form.get('inquiry_content', '')
            project_key = request.form.get('project_key', '')
            template_key = request.form.get('template_key', '')
            custom_response = request.form.get('custom_response', '')
            
            # 응답 생성
            result = response_generator.process_onestep(
                inquiry_title, inquiry_content, project_key, template_key, custom_response
            )
            
            # 결과 유효성 검사 추가
            if not result.get("summary"):
                result["summary"] = "문의 내용 요약이 생성되지 않았습니다."
            if not result.get("suggestion"):
                result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
            if not result.get("response_mail"):
                result["response_mail"] = "응답 메일이 생성되지 않았습니다."
            
            # AJAX 요청인 경우 JSON 응답
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(result)
            
            # 세션에 결과 저장
            session['result'] = result
            session['lastProcess'] = 'onestep'
            
            # 일반 요청인 경우 결과 페이지로 리다이렉트
            return redirect(url_for('result'))
        
        return render_template('cs/onestep.html', templates=templates)

    
    # 투스텝 프로세스 - 번역 라우트
    @app.route('/twostep/translate', methods=['GET', 'POST'])
    def twostep_translate():
        if request.method == 'POST':
            # 폼 데이터 처리
            inquiry_title = request.form.get('inquiry_title', '')
            inquiry_content = request.form.get('inquiry_content', '')
            
            # 번역 및 분석
            result = response_generator.process_twostep_translation(
                inquiry_title, inquiry_content
            )
            
            # 결과 유효성 확인 및 기본값 설정
            if not result.get("summary"):
                result["summary"] = "번역된 요약이 생성되지 않았습니다."
            if not result.get("suggestion"):
                result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
            if not result.get("title_jp"):
                result["title_jp"] = inquiry_title
            if not result.get("content_jp"):
                result["content_jp"] = inquiry_content
            
            # 세션에 번역 결과 저장
            session['translation'] = result
            session['inquiry_title'] = inquiry_title
            session['inquiry_content'] = inquiry_content
            
            # AJAX 요청인 경우 JSON 응답
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(result)
            
            # 일반 요청인 경우 다음 단계로 리다이렉트
            return redirect(url_for('twostep_response'))
        
        return render_template('cs/twostep_translate.html')
    
    # 투스텝 프로세스 - 응답 생성 라우트
    # __main__.py 파일의 twostep_response 라우트 수정

    @app.route('/twostep/response', methods=['GET', 'POST'])
    def twostep_response():
        templates_df = TemplateLoader.load_template_csv("RESPONSE_TEMPLATE")
        templates = []
        
        if not templates_df.empty:
            for _, row in templates_df.iterrows():
                templates.append({
                    'key': row[RESPONSE_TEMPLATE_COLUMNS["TEMP_KEY"]],
                    'category': row[RESPONSE_TEMPLATE_COLUMNS["TEMP_CATEGORY"]],
                    'section': row[RESPONSE_TEMPLATE_COLUMNS["TEMP_SECTION"]]
                })
        
        if request.method == 'POST':
            # 폼 데이터 처리
            inquiry_title = request.form.get('inquiry_title', '')
            inquiry_content = request.form.get('inquiry_content', '')
            translated_summary = request.form.get('translated_summary', '')
            project_key = request.form.get('project_key', '')
            template_key = request.form.get('template_key', '')
            custom_response = request.form.get('custom_response', '')
            
            # 응답 생성
            result = response_generator.process_twostep_response(
                inquiry_title, inquiry_content, translated_summary,
                project_key, template_key, custom_response
            )
            
            # 결과 유효성 검사 추가
            if not result.get("summary"):
                result["summary"] = "문의 내용 요약이 생성되지 않았습니다."
            if not result.get("suggestion"):
                result["suggestion"] = "답변 방향 제안이 생성되지 않았습니다."
            if not result.get("response_mail"):
                result["response_mail"] = "응답 메일이 생성되지 않았습니다."
            
            # 세션에 결과 저장
            session['result'] = result
            session['lastProcess'] = 'twostep'
            
            # AJAX 요청인 경우 JSON 응답
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(result)
            
            # 일반 요청인 경우 결과 페이지로 리다이렉트
            return redirect(url_for('result'))
        
        # GET 요청 처리
        # 세션에서 번역 결과 및 문의 정보 가져오기
        translation = session.get('translation', {})
        inquiry_title = session.get('inquiry_title', request.args.get('inquiry_title', ''))
        inquiry_content = session.get('inquiry_content', request.args.get('inquiry_content', ''))
        
        # 번역 결과가 없는 경우 기본값 설정
        if not translation:
            translation = {
                'summary': '번역된 요약 정보가 없습니다.',
                'suggestion': '답변 방향 제안 정보가 없습니다.',
                'recommended_templates': []
            }
        
        return render_template('cs/twostep_response.html', 
                            templates=templates,
                            inquiry_title=inquiry_title,
                            inquiry_content=inquiry_content,
                            translation=translation)
    
    @app.route('/result')
    def result():
        """
        응답 결과를 표시하는 페이지입니다.
        """
        # 세션에서 결과 가져오기
        result = session.get('result')
        
        # 결과가 없으면 기본값 사용
        if not result:
            result = {
                'summary': '문의 내용 요약이 여기에 표시됩니다.',
                'suggestion': '답변 방향 제안이 여기에 표시됩니다.',
                'response_mail': '생성된 응답 메일이 여기에 표시됩니다.'
            }
        
        return render_template('cs/result.html', result=result)

    return app  # 여기에 app 객체 반환 추가

    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)