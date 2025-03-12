// gaia/ui/static/js/modules/templates.js

$(document).ready(function() {
    // 템플릿 검색
    $('#template-search').on('input', function() {
        const searchTerm = $(this).val().toLowerCase();
        
        $('.template-item').each(function() {
            const templateText = $(this).text().toLowerCase();
            if(templateText.includes(searchTerm)) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
    
    // 템플릿 카테고리 필터
    $('#template-category').on('change', function() {
        const selectedCategory = $(this).val();
        
        if(selectedCategory === 'all') {
            $('.template-item').show();
        } else {
            $('.template-item').each(function() {
                if($(this).data('category') === selectedCategory) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        }
    });
});