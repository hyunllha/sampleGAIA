// gaia/ui/static/js/modules/twostep-response.js

$(document).ready(function() {
    // 초기 데이터 로드 및 표시
    const initializeData = function() {
        // 저장된 번역 결과 및 문의 정보 복원
        let translation;
        try {
            translation = JSON.parse(sessionStorage.getItem('translation') || '{}');
        } catch (e) {
            console.error('세션 스토리지 데이터 파싱 오류:', e);
            translation = {};
        }
        
        const inquiryTitle = sessionStorage.getItem('inquiry_title') || '';
        const inquiryContent = sessionStorage.getItem('inquiry_content') || '';
        
        // 페이지에 번역 결과가 없는 경우 세션 스토리지 데이터 사용
        const summaryElement = $('.translation-summary');
        const suggestionElement = $('.translation-suggestion');
        
        if (summaryElement.length && (!summaryElement.text().trim() || summaryElement.text().includes('번역된 요약 정보가 없습니다'))) {
            if (translation.summary) {
                summaryElement.html(translation.summary.replace(/\n/g, '<br>'));
            }
        }
        
        if (suggestionElement.length && (!suggestionElement.text().trim() || suggestionElement.text().includes('답변 방향 제안 정보가 없습니다'))) {
            if (translation.suggestion) {
                suggestionElement.html(translation.suggestion.replace(/\n/g, '<br>'));
            }
        }
        
        // 폼 필드에 값 설정
        if (!$('#inquiry_title_display').text()) {
            $('#inquiry_title_display').text(inquiryTitle);
        }
        
        if (!$('#inquiry_content_display').html()) {
            $('#inquiry_content_display').html(inquiryContent.replace(/\n/g, '<br>'));
        }
        
        // 히든 필드에 값 설정
        $('input[name="inquiry_title"]').val(inquiryTitle);
        $('input[name="inquiry_content"]').val(inquiryContent);
        $('input[name="translated_summary"]').val(translation.summary || '');
        
        // 템플릿 항목 클릭 이벤트
        $('.template-item').on('click', function() {
            $('.template-item').removeClass('active');
            $(this).addClass('active');
            
            // 템플릿 키 저장
            const templateKey = $(this).data('key');
            $('#template_key').val(templateKey);
        });
        
        // 카테고리 필터 이벤트
        $('#template-category').on('change', function() {
            const category = $(this).val();
            
            if (category === 'all') {
                $('.template-item').show();
            } else {
                $('.template-item').hide();
                $(`.template-item[data-category="${category}"]`).show();
            }
        });
        
        // 템플릿 검색 이벤트
        $('#template-search').on('input', function() {
            const searchTerm = $(this).val().toLowerCase();
            
            if (searchTerm === '') {
                $('.template-item').show();
            } else {
                $('.template-item').each(function() {
                    const templateText = $(this).text().toLowerCase();
                    if (templateText.includes(searchTerm)) {
                        $(this).show();
                    } else {
                        $(this).hide();
                    }
                });
            }
        });
    };
    
    // 페이지 로드 시 데이터 초기화
    initializeData();
    
    // 폼 제출 처리
    $('#twostep-response-form').on('submit', function(e) {
        e.preventDefault();
        
        // 필수 필드 검증
        if(!$('#project_key').val()) {
            alert('프로젝트를 선택해주세요.');
            return false;
        }
        
        // 로딩 스피너 표시
        $('#loading-spinner').show();
        
        // 폼 데이터 구성
        const formData = $(this).serialize();
        
        // AJAX 요청
        $.ajax({
            url: "/twostep/response",
            type: "POST",
            data: formData,
            dataType: "json",
            success: function(response) {
                // 로드 완료 후 스피너 숨기기
                $('#loading-spinner').hide();
                
                // 응답 데이터를 세션 스토리지에 저장
                sessionStorage.setItem('result', JSON.stringify(response));
                sessionStorage.setItem('lastProcess', 'twostep');
                
                // 결과 페이지로 이동
                window.location.href = "/result";
            },
            error: function(xhr, status, error) {
                $('#loading-spinner').hide();
                console.error('API 응답 에러:', xhr.responseText);
                alert('응답 생성 중 오류가 발생했습니다: ' + error);
            }
        });
    });
});