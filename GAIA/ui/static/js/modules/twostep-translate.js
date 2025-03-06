// gaia/ui/static/js/modules/twostep-translate.js

$(document).ready(function() {
    // 현재 프로세스 저장
    sessionStorage.setItem('lastProcess', 'twostep');
    
    $('#twostep-translate-form').on('submit', function(e) {
        e.preventDefault();
        
        // 필수 필드 검증
        if(!$('#inquiry_title').val() || !$('#inquiry_content').val()) {
            alert('문의 제목과 내용을 입력해주세요.');
            return false;
        }
        
        // 폼 데이터 구성
        const formData = $(this).serialize();
        
        // 로딩 스피너 표시
        $('#loading-spinner').show();
        
        // AJAX 요청
        $.ajax({
            url: "/twostep/translate",
            type: "POST",
            data: formData,
            dataType: "json",
            success: function(response) {
                // 로드 완료 후 스피너 숨기기
                $('#loading-spinner').hide();
                
                // 응답이 비어있는지 확인
                if (!response || !response.summary) {
                    alert('번역 결과가 생성되지 않았습니다. 다시 시도해주세요.');
                    return;
                }
                
                // 번역 결과 및 문의 정보를 세션 스토리지에 저장
                sessionStorage.setItem('translation', JSON.stringify(response));
                sessionStorage.setItem('inquiry_title', $('#inquiry_title').val());
                sessionStorage.setItem('inquiry_content', $('#inquiry_content').val());
                
                // 응답 생성 페이지로 이동
                window.location.href = "/twostep/response";
            },
            error: function(xhr, status, error) {
                $('#loading-spinner').hide();
                console.error('API 응답 에러:', xhr.responseText);
                alert('번역 중 오류가 발생했습니다: ' + error);
            }
        });
    });
});