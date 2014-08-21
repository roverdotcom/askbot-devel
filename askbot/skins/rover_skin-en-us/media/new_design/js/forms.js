Rover.forms = Rover.forms || {};

$(function() {
    // Reset the selects to have their selected value
    // This is for back button support for selects
    var initializeSelects = function() {
        $('select').each(function() {
            var $this = $(this);
            $this.val($this.find('option:selected').val());
        });
    };

    // Reset any previously disabled submit buttons
    // NOTE: If we ever disable a submit button on load, we need to
    //       make this more specific
    var resetDisabledForms = function() {
        $('.js-auto-disable-form [type=submit]:disabled').prop('disabled', false);
        // If this is called with a form object as this, reset that form.
        if ($(this).is('form')) {
            var $submitBtn = $(this).find('[type=submit]:disabled');
            if ($submitBtn.attr('data-loading-text')) {
                $submitBtn.btn('reset');
            } else {
                $submitBtn.prop('disabled', false);
            }
        }
    };

    // Disable the submit button on submit of the form for all
    // forms that do not have the data-validate attribute
    var handleAutoDisableSubmit = function() {
        var $form = $(this),
            $submitBtn = $form.find('[type=submit]');

        if ($submitBtn.attr('data-loading-text')) {
            $submitBtn.btn('loading');
        } else {
            $submitBtn.prop('disabled', true);
        }
        $form.attr('data-is-valid', 'true');
    };

    // Fix chrome bug where hitting enter will submit a form where
    // the submit button is disabled
    // http://code.google.com/p/chromium/issues/detail?id=37402
    var handleDocumentSubmitEvent = function() {
        var $form = $(this);
        if ($form.attr('data-submitted') !== 'true' && $form.attr('data-is-valid') === 'true') {
          $form.attr('data-submitted', 'true');
          return true;
        } else if ($form.attr('data-submitted') === 'true') {
          return false;
        }
        return true;
    };

    $.fn.autoDisableAjaxForm = function(options) {
        options = options || {};
        var mainBeforeSubmit = options.beforeSubmit || null;
        options.beforeSubmit = function(arr, $form, options) {
            if ($form.is(':not([data-validate=true])')) {
                handleAutoDisableSubmit.call($form);
            } else {
                if (!handleDocumentSubmitEvent.call($form)) {
                    return false;
                }
            }
            if (mainBeforeSubmit && !mainBeforeSubmit(arr, $form, options)) {
                resetDisabledForms.call($form);
                return false;
            }
        };
        var mainError = options.error;
        options.error = function(response, status, xhr, $form) {
            resetDisabledForms.call($form);
            if (mainError) {
                mainError(response, status, xhr, $form);
            }
        };
        var mainSuccess = options.success;
        options.success = function(response, status, xhr, $form) {
            if (mainSuccess) {
                mainSuccess(response, status, xhr, $form);
            }
            resetDisabledForms.call($form);
        };

        return this.each(function() {
            $(this).ajaxForm(options);
        });
    };

    $.fn.autoDisableAndValidateAjaxForm = function(options) {
        options = options || {};

        return this.each(function() {
            $(this).validate();

            options.beforeSubmit = function(arr, $form, options) {
                if (!$form.valid()) {
                    return false;
                }
                return true;
            };

            $(this).autoDisableAjaxForm(options);
        });
    };

    /**
     * Wrapper to disable the submit button before validation
     */
    $.fn.roverValidate = function(options) {
        return this.each(function() {
            var $form = $(this);

            var handleSubmit = function() {
                $form.find('[type=submit]').prop('disabled', true);
            };

            $form.on('submit', handleSubmit);
            $form.validate(options);
        });
    };


    var showSuccess = function(response, status, xhr, $form) {
        var successAlertText = $form.attr('data-success-alert-text');
        if (successAlertText) {
            Rover.alerts.showAlert('success', successAlertText, $form.find('.js-success-alert'));
        }
    };

    var addBindings = function() {
        $('.js-auto-disable-form:not([data-validate=true])').on('submit', handleAutoDisableSubmit);
        $(document).on('submit', '.js-auto-disable-form', handleDocumentSubmitEvent);
        $('.js-auto-ajax-form').autoDisableAjaxForm({
            success: showSuccess
        });
    };

    var init = function() {
        addBindings();
        initializeSelects();
        resetDisabledForms();
    };

    init();
});
