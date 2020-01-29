/**
 * Form class.
 * Helps build forms with validation
 */
var Form = function () {
    WrappedElement.call(this);
    /* all dicts have key of field name */
    this._errors = {};
    this._errorElements = {};
    this._validators = {};
    this._inputs = {};
};
inherits(Form, WrappedElement);

Form.prototype.fieldHasErrors = function (fieldName) {
    return this._errors[fieldName];
};

Form.prototype.formHasErrors = function () {
    var fields = this._fieldNames;
    for (var i=0; i<fields.length; i++) {
        var field = fields[i];
        if (this.fieldHasErrors(field)) {
            return true;
        }
    }
    return false;
};

Form.prototype.validateForm = function () {
    var fields = this._fieldNames;
    for (var i=0; i<fields.length; i++) {
        this.validateField(fields[i]);
    }
};

Form.prototype.getFormValidationHandler = function () {
    var me = this;
    var submit = this._submit;
    return function () {
        if (submit.length)
            submit.attr('disabled', 'disabled');
        me.validateForm();
        if (me.formHasErrors()) {
            if (submit.length)
                submit.removeAttr('disabled');
            return false;
        }
    };
};

Form.prototype.setFieldError = function (fieldName, errorMsg) {
    var error = this._errorElements[fieldName];
    error.html(errorMsg);
    this._errors[fieldName] = true;
};

Form.prototype.clearFieldError = function (fieldName) {
    var error = this._errorElements[fieldName];
    error.html('');
    this._errors[fieldName] = false;
};

Form.prototype.validateField = function (fieldName) {
    var input = this._inputs[fieldName];
    var validator = this._validators[fieldName];
    var val = input.val();
    try {
        validator(val);
        this.clearFieldError(fieldName);
    } catch (error) {
        this.setFieldError(fieldName, error);
    }
};

Form.prototype.decorateField = function (fieldName) {
    //get validator
    var element = $(this._element);
    var validator = element.data(fieldName + 'Validator');
    validator = getObjectByPath(validator);
    this._validators[fieldName] = validator;

    var error = element.find('.js-' + fieldName + '-error');
    this._errorElements[fieldName] = error;

    var input = element.find('input[name="' + fieldName + '"]');
    if (input.length == 0) {
        input = element.find('textarea[name="' + fieldName + '"]');
    }
    if (input.length == 0) {
        input = element.find('select[name="' + fieldName + '"]');
    }
    this._inputs[fieldName] = input;

    var me = this;
    input.change(function () {
        me.validateField(fieldName);
        return false;
    });
};

Form.prototype.decorate = function (element) {
    this._element = element;
    this._submit = element.find('[type=submit]');
    //look for validated fields
    var fieldNames = $(element).data('validatedFields');
    fieldNames = $.trim(fieldNames).split(',');

    for (var i=0; i<fieldNames.length; i++) {
        var fieldName = $.trim(fieldNames[i]);
        fieldNames[i] = fieldName;//save cleaned field name
        this.decorateField(fieldName);
    }
    this._fieldNames = fieldNames;

    element.submit(this.getFormValidationHandler());
};
