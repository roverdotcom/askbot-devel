$(function() {
    if (!$('body').hasClass('js-full-service-request')) {
        return;
    }

    var handleSuccessfulSubmit = function(data) {
        if (data['status'] === 'error') {
            alert("Error encountered. Please try again later or contact support");
        }

        $('.js-send-request').fadeOut(function() {
            $('.js-confirmation').hide().removeClass('hide').fadeIn();
        });
    };

    var handleSubmit = function() {
        if ($('body').hasClass('js-premier')) {
            dataLayer.push({event: 'premier-form-submit'});
        }
        if ($('body').hasClass('js-walking-landing-page')) {
            dataLayer.push({event: "walking-form-submit"});
        }
        $('.js-full-service-request-form').ajaxSubmit({
            success: handleSuccessfulSubmit
        });
     };

    var initializeValidation = function() {
        $('.js-full-service-request-form').validate({
            submitHandler: handleSubmit
        });
    };

    var initializeDateRangePicker = function() {
        $('.js-daterangepicker').daterangepicker({
            startElementSelector: '.js-start-date',
            endElementSelector: '.js-end-date'
        });
    };

    var init = function() {
        dataLayer.push({event: 'premier-page-view'});
        initializeValidation();
        initializeDateRangePicker();
    };

    init();
});
