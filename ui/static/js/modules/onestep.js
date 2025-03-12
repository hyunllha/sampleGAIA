// gaia/ui/static/js/modules/onestep.js
$(document).ready(function() {
    // 템플릿 필터링
    $('#template-category').on('change', function() {
        const category = $(this).val();
        
        if (category === 'all') {
            $('.template-item').show();
        } else {
            $('.template-item').hide();
            $(`.template-item[data-category="${category}"]`).show();
        }
    });
    
    // 템플릿 검색
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
    
    // 템플릿 아이템 클릭 이벤트
    $('.template-item').on('click', function() {
        $('.template-item').removeClass('active');
        $(this).addClass('active');
        
        // 히든 필드에 템플릿 키 저장
        const templateKey = $(this).data('key');
        $('#template_key').val(templateKey);
    });
    
    // 폼 제출 이벤트 - AJAX로 변경
    $('#onestep-form').on('submit', function(e) {
        e.preventDefault();
        
        const formData = $(this).serialize();
        const formAction = $(this).attr('action');
        
        // 로딩 표시
        $('#loading-spinner').show();
        
        // AJAX 요청
        $.ajax({
            url: formAction,
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function(response) {
                // 응답 데이터를 세션 스토리지에 저장
                sessionStorage.setItem('result', JSON.stringify(response));
                sessionStorage.setItem('lastProcess', 'onestep');
                
                // 로딩 숨기기
                $('#loading-spinner').hide();
                
                // 결과 페이지로 이동
                window.location.href = '/result';
            },
            error: function(xhr, status, error) {
                // 로딩 숨기기
                $('#loading-spinner').hide();
                
                // 오류 메시지 표시
                alert('응답 생성 중 오류가 발생했습니다: ' + error);
                console.error('Error details:', xhr.responseText);
            }
        });
    });
});