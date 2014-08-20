(function($) {
    $.fn.serializeObject = function() {
        var obj = {};
        var data = this.serializeArray();
        $.each(data, function() {
            if (obj.hasOwnProperty(this.name)) {
                if (!obj[this.name].push) {
                    obj[this.name] = [obj[this.name]];
                }
                obj[this.name].push(this.value || '');
            } else {
                obj[this.name] = this.value || '';
            }
        });
        return obj;
    }
})(jQuery);
