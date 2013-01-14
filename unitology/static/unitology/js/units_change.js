// units_change.js

(function($) {
    $(document).ready(function() {
        $('#id_units').change(function() {
            $(document).trigger("unitsChanged", [this.value]);
        });
    })
})(jQuery || django.jQuery);
