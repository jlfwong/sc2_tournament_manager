(function($) {
    $('#id_name').live('keyup',function() {
        console.log($(this).val());
    });
})(django.jQuery);
