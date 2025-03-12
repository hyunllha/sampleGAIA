// gaia/ui/static/js/main.js

$(document).ready(function() {
    // 프로젝트 선택
    $('.project-select').on('click', function(e) {
        e.preventDefault();
        const projectKey = $(this).data('key');
        const projectName = $(this).text().trim();
        
        // 선택된 프로젝트 저장 (세션 스토리지)
        sessionStorage.setItem('selectedProject', projectKey);
        sessionStorage.setItem('selectedProjectName', projectName);
        
        // 드롭다운 버튼 텍스트 업데이트
        $('#projectDropdown').html('<i class="fas fa-gamepad me-1"></i> ' + projectName);
        
        // 프로젝트 필드 업데이트 (있는 경우)
        if($('#project_key').length) {
            $('#project_key').val(projectKey);
        }
    });
    
    // 페이지 로드 시 세션에서 선택된 프로젝트 복원
    if(sessionStorage.getItem('selectedProject')) {
        const projectKey = sessionStorage.getItem('selectedProject');
        const projectName = sessionStorage.getItem('selectedProjectName');
        
        $('#projectDropdown').html('<i class="fas fa-gamepad me-1"></i> ' + projectName);
        
        if($('#project_key').length) {
            $('#project_key').val(projectKey);
        }
    }
    
    // 템플릿 항목 선택
    $(document).on('click', '.template-item', function() {
        $('.template-item').removeClass('selected');
        $(this).addClass('selected');
        
        // 템플릿 키 필드 업데이트
        const templateKey = $(this).data('key');
        $('#template_key').val(templateKey);
    });
    
    // 폼 제출 시 로딩 스피너 표시
    $('form').on('submit', function() {
        $('#loading-spinner').show();
    });
});