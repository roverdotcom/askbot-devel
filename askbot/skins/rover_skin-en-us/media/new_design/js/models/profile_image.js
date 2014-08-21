var ProfileImage = Backbone.Model.extend({
    defaults: {
            id: null,
            thumb: null,
            image: null,
            title: null
    }
});


var ProfileImageCollection = Backbone.Collection.extend({
    model: ProfileImage
});
