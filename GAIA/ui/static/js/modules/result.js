// gaia/ui/static/js/modules/result.js

$(document).ready(function() {
    // 서버에서 전달된 데이터와 세션 스토리지의 데이터 처리
    const initializeResultData = function() {
        // 세션 스토리지에서 결과 데이터 로드
        const resultData = sessionStorage.getItem('result');
        
        // 이미 페이지에 데이터가 있는지 확인 (서버 렌더링 데이터)
        const summaryEl = $('#result-summary');
        const suggestionEl = $('#result-suggestion');
        const responseContentEl = $('#response-content');
        const responseEditorEl = $('#response-editor');
        
        // 세션 스토리지에 데이터가 있고, 서버 데이터가 없거나 미비한 경우에만 사용
        if (resultData) {
            const result = JSON.parse(resultData);
            
            // 결과 내용이 비어있는 경우에만 세션 스토리지의 데이터로 대체
            if (!summaryEl.text().trim() || summaryEl.text().includes('문의 내용 요약이 없습니다')) {
                summaryEl.html(result.summary ? result.summary.replace(/\n/g, '<br>') : '문의 내용 요약이 없습니다.');
            }
            
            if (!suggestionEl.text().trim() || suggestionEl.text().includes('답변 방향 제안이 없습니다')) {
                suggestionEl.html(result.suggestion ? result.suggestion.replace(/\n/g, '<br>') : '답변 방향 제안이 없습니다.');
            }
            
            if (!responseContentEl.text().trim() || responseContentEl.text().includes('응답 메일이 없습니다')) {
                // 줄바꿈 처리 개선
                responseContentEl.html(
                    result.response_mail ? formatTextForDisplay(result.response_mail) : '응답 메일이 없습니다.'
                );
            }
            
            // 에디터에도 같은 내용 설정
            if (!responseEditorEl.val().trim()) {
                responseEditorEl.val(result.response_mail || '');
            }
        }
    };
    
    // 텍스트 형식 변환 함수들
    
    // 화면 표시용 텍스트 형식 변환 (모든 줄바꿈 -> <br>)
    const formatTextForDisplay = function(text) {
        if (!text) return '';
        return text
            .replace(/\\n/g, '\n')  // 이스케이프된 \n을 실제 줄바꿈으로
            .replace(/\n/g, '<br>'); // 모든 줄바꿈을 <br>로
    };
    
    // 에디터용 텍스트 형식 변환 (HTML -> 일반 텍스트)
    const formatTextForEditor = function(html) {
        if (!html) return '';
        // 임시 div를 사용하여 HTML 디코딩
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        
        // HTML에서 텍스트 추출
        let text = tempDiv.textContent || tempDiv.innerText || '';
        
        // <br> 태그를 줄바꿈으로 변환 (텍스트 추출 전에 이미 처리되었을 수 있지만 안전을 위해)
        text = html.replace(/<br\s*\/?>/gi, '\n')
                  .replace(/&lt;/g, '<')
                  .replace(/&gt;/g, '>')
                  .replace(/&amp;/g, '&')
                  .replace(/&quot;/g, '"')
                  .replace(/&#39;/g, "'");
                  
        // DOM 파싱된 텍스트 요소의 내용만 추출 (HTML 태그 제거)
        tempDiv.innerHTML = text;
        text = tempDiv.textContent || tempDiv.innerText || '';
        
        return text;
    };
    
    // 복사용 텍스트 형식 변환
    const formatTextForCopy = function(html) {
        if (!html) return '';
        // HTML 태그 제거 및 줄바꿈 보존
        return html.replace(/<br\s*\/?>/gi, '\n')  // <br> 태그를 줄바꿈으로
                  .replace(/&lt;/g, '<')
                  .replace(/&gt;/g, '>')
                  .replace(/&amp;/g, '&')
                  .replace(/&quot;/g, '"')
                  .replace(/&#39;/g, "'")
                  .replace(/<[^>]*>/g, '');  // 나머지 HTML 태그 제거
    };
    
    // 페이지 로드시 데이터 초기화
    initializeResultData();
    
    // 표시된 내용의 줄바꿈 처리
    const processDisplayContent = function() {
        const responseContent = $('#response-content');
        const currentContent = responseContent.html();
        
        if (currentContent && !currentContent.includes('응답 메일이 없습니다')) {
            // 줄바꿈 처리 (이스케이프된 \n 및 실제 줄바꿈 모두 처리)
            responseContent.html(formatTextForDisplay(currentContent));
        }
    };
    
    // 페이지 로드 후 추가적인 줄바꿈 처리
    processDisplayContent();
    
    // 답변 복사 버튼
    $('#copy-response').on('click', function() {
        let responseText;
        
        if ($('#response-editor').is(':visible')) {
            // 에디터가 표시되어 있는 경우 에디터의 텍스트 사용
            responseText = $('#response-editor').val();
        } else {
            // 표시 영역의 내용을 가져와 복사용으로 포맷
            responseText = formatTextForCopy($('#response-content').html());
        }
        
        // 복사 기능 실행
        navigator.clipboard.writeText(responseText).then(function() {
            alert('답변이 클립보드에 복사되었습니다.');
        }, function(err) {
            console.error('복사 실패:', err);
            
            // 대체 복사 방법 시도
            try {
                // 임시 텍스트 영역 생성
                const textarea = document.createElement('textarea');
                textarea.value = responseText;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                alert('답변이 클립보드에 복사되었습니다.');
            } catch (e) {
                console.error('대체 복사 방법 실패:', e);
                alert('복사 중 오류가 발생했습니다. 수동으로 복사해주세요.');
            }
        });
    });
    
    // 답변 수정 버튼
    $('#edit-response').on('click', function() {
        // 현재 표시 내용을 가져와 에디터용으로 변환
        const displayContent = $('#response-content').html();
        const editorContent = formatTextForEditor(displayContent);
        
        // 에디터에 내용 설정
        $('#response-editor').val(editorContent);
        
        // UI 상태 변경
        $('#response-content').hide();
        $('#response-editor').show();
        $('#save-edit').show();
        $('#cancel-edit').show();
        $(this).hide();
    });
    
    // 수정 저장 버튼
    $('#save-edit').on('click', function() {
        // 에디터 내용 가져오기
        const editedText = $('#response-editor').val();
        
        // 표시 영역에 HTML 형식으로 변환하여 설정
        $('#response-content').html(formatTextForDisplay(editedText));
        
        // 세션 스토리지의 결과 데이터 업데이트
        const resultData = sessionStorage.getItem('result');
        if (resultData) {
            const parsedResult = JSON.parse(resultData);
            parsedResult.response_mail = editedText;
            sessionStorage.setItem('result', JSON.stringify(parsedResult));
        } else {
            // 세션 스토리지에 데이터가 없는 경우 새로 생성
            const newResult = {
                summary: $('#result-summary').text(),
                suggestion: $('#result-suggestion').text(),
                response_mail: editedText
            };
            sessionStorage.setItem('result', JSON.stringify(newResult));
        }
        
        // UI 상태 변경
        $('#response-content').show();
        $('#response-editor').hide();
        $('#save-edit').hide();
        $('#cancel-edit').hide();
        $('#edit-response').show();
    });
    
    // 수정 취소 버튼
    $('#cancel-edit').on('click', function() {
        // UI 상태 변경
        $('#response-content').show();
        $('#response-editor').hide();
        $('#save-edit').hide();
        $('#cancel-edit').hide();
        $('#edit-response').show();
    });
    
    // 새 문의 처리 버튼
    $('#new-inquiry').on('click', function() {
        const lastProcess = sessionStorage.getItem('lastProcess') || 'onestep';
        if (lastProcess === 'onestep') {
            window.location.href = "/onestep";
        } else {
            window.location.href = "/twostep/translate";
        }
    });
});