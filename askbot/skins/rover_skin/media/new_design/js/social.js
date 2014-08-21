var Rover = Rover || {};

$(function() {
    Rover.facebook = Rover.facebook || {};
    Rover.googlePlus = Rover.googlePlus || {};
    Rover.share_local_callback = Rover.share_local_callback || function() {};

    // A function that will be called by every social action callback
    // function with its social network and action. Example
    //
    // 'facebook', 'share'
    //
    // Specific pages can implement this function to perform
    // page-specific actions
    Rover.track_social = function(social_network, action, content_type, object_id) {
        if (object_id && content_type) {
            $.ajax({
                type: 'POST',
                url: Rover.urls.analyticsTrackShare,
                data: JSON.stringify({
                    content_type: content_type,
                    object_id: object_id,
                    social_network: social_network,
                    action: action
                }),
                contentType: 'application/json; charset=utf-8',
                dataType: 'json',
                success: function(data) { },
                failure: function(err) { }
            });
        }
    };

    // Callback for plus one events. Has to be global.
    Rover.googlePlus.plusOneClick = function(response) {
        url = response.href;
        if (response.state === 'on') {
            dataLayer.push({
                event: 'google-plus-share',
                shared_url: url
            });
            Rover.share_local_callback('g_plus', 'share');
        }
    };

    /**
     * Log in via Facebook's FB API, returning Facebook auth credentials
     */
    Rover.facebook.login = function(successCallback, errorCallback) {
        errorCallback = errorCallback || defaultFBLoginError;
        // First call is to login to get auth information
        dataLayer.push({'event': 'facebook-login-started'});
        FB.login(
            function(response) {
                if (response.status === 'connected') {
                    dataLayer.push({'event': 'facebook-login-success'});

                    // Reset any DOM state related to connecting
                    $('.js-need-connect-to-share').addClass('hide');

                    Rover.facebook.connected = true;

                    if ($.isFunction(successCallback)) {
                        successCallback({
                            access_token: response.authResponse.accessToken,
                            signed_request: response.authResponse.signedRequest,
                            user_id: response.authResponse.userID
                        });
                    }
                } else {
                    if (response.status === 'not_authorized') {
                        dataLayer.push({'event': 'facebook-login-did-not-authorize'});
                    } else {
                        dataLayer.push({'event': 'facebook-login-error'});
                    }

                    errorCallback(response);
                }
            },
            // Specify which permissions we're requesting: email address,
            // ability to post on their timeline
            { scope: 'email,publish_stream' }
        );
    };

    Rover.facebook.signup = function(successCallback, errorCallback) {
        errorCallback = $.isFunction(errorCallback) ? errorCallback : defaultFBSignupError;
        var wrappedSuccessCallback = function(authData) {
            if ($.isFunction(successCallback)) {
                successCallback(authData);
            }

            var $form = $('.js-facebook-register');
            $('[name=access_token]', $form).val(authData.access_token);
            $('[name=signed_request]', $form).val(authData.signed_request);
            $('[name=facebook_id]', $form).val(authData.user_id);
            $form.submit();
        };
        Rover.facebook.login(wrappedSuccessCallback, errorCallback);
    };

    var handleConnectButtonClick = function(e) {
        Rover.facebook.currentConnectButton = $(e.currentTarget);
        Rover.facebook.currentConnectButton.btn('loading');
        Rover.facebook.connectLocation = Rover.facebook.currentConnectButton.attr('data-connect-location');

        var resetButton = function(success) {
            Rover.facebook.currentConnectButton.btn('reset');

            if (success) {
                if (Rover.facebook.currentConnectButton.attr('data-hide-on-success')) {
                    Rover.facebook.currentConnectButton.hide();
                    if (Rover.facebook.currentConnectButton.parents('.js-connect-facebook-wrapper')) {
                        Rover.facebook.currentConnectButton.parents('.js-connect-facebook-wrapper').hide();
                    }
                }
                if (Rover.facebook.currentConnectButton.attr('data-show-success-message')) {
                    Rover.alerts.showAlert('success', 'Your account is now connected with Facebook!');
                }
                $(window).trigger('connectsuccess.facebook.rover');
            }
        };

        Rover.facebook.login(
            function() {
                resetButton(true);
            },
            function() {
                resetButton(false);
            }
        );
    };

    var handleSignupButtonClick = function(e) {
        Rover.facebook.currentConnectButton = $(e.currentTarget);
        Rover.facebook.currentConnectButton.btn('loading');
        Rover.facebook.signup(false, function() {
            Rover.facebook.currentConnectButton.btn('reset');
            var errorContainer = Rover.facebook.currentConnectButton.attr('data-error-container');
            if (errorContainer) {
                Rover.alerts.showAlert('danger', 'We were unable to sign you up', errorContainer);
            } else {
                defaultFBSignupError();
            }
        });
    };

    var defaultFBSignupError = function() {
        alert("We're sorry, we were unable to connect your Facebook account " +
              "due to an error. If you would like immediate help email " +
              "support@rover.com, or call us at 888-453-7889");
    };

    var defaultFBLoginError = function() {
        alert("We're sorry, we were unable to authenticate with Facebook. " +
              "If you would like immediate help email " +
              "support@rover.com, or call us at 888-453-7889");
    };

    var resetSharingDialog = function($form, clearCopy) {
        clearCopy = clearCopy === true;

        $('.js-sharing-copy').prop('disabled', false);
        $form.find('.js-facebook-share-photo-button').btn('reset');

        if (clearCopy) {
            $('.js-sharing-copy').val('');
        }
    };

    var connectAndResubmit = function(connect) {
        if (connect) {
            Rover.facebook.login(function() {
                $('.js-need-connect-to-share').addClass('hide');
                Rover.facebook.submittedForm.trigger('submit');
            }, function() {
                defaultFBSignupError();
                resetSharingDialog($form);
            });
        }
    };

    var validatePermissionsAndShareOnFacebook = function(e) {
        var $form = $(e.currentTarget);
        $form.find('.js-facebook-share-photo-button').btn('loading');
        $('.js-sharing-copy').prop('disabled', true);

        Rover.facebook.submittedForm = $form;

        if (Rover.person.id === 0) {
            $('.js-need-to-log-in').removeClass('hide');
            return false;
        }

        if (!Rover.facebook.connected) {
            connectAndResubmit(true);
            return false;
        }

        FB.api('/me/permissions', function(response) {
            if (response.data && response.data[0].publish_stream === 1) {
                sharePhotoOnFacebook();
            } else {
                $('.js-need-connect-to-share').removeClass('hide');
                connectAndResubmit(false);
            }
        });

        return false;
    };

    var sharePhotoOnFacebook = function() {
        var $form = Rover.facebook.submittedForm;

        var caption = $.trim($('.js-sharing-copy').val()),
            imageToShare = $form.find('[name=imageToShare]').val(),
            urlToShare = $form.find('[name=urlToShare]').val(),
            contentType = $form.find('[name=contentType]').val(),
            objectId = $form.find('[name=objectId]').val();

        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: {
                message_image_id: objectId,
                photo_url: imageToShare,
                caption: caption,
                link: urlToShare
            },
            success: function(data) {
                if (data.status === 'success') {
                    dataLayer.push({
                        event: 'facebook-share',
                        share_location: $form.find('[name=shareLocation]').val(),
                        has_caption: $.trim(caption) !== ''
                    });

                    $form.find('.js-facebook-share-photo-button').btn('complete');

                    setTimeout(function() {
                        $('.js-facebook-share-modal').on('hidden.bs.modal', function() {
                            resetSharingDialog($form, true);
                        }).modal('hide');
                    }, 1500);

                    Rover.track_social('facebook', 'image-share', contentType, objectId);
                } else {
                    if (data.type === 'needs_connect') {
                        connectAndResubmit(false);
                    } else {
                        defaultFBLoginError();
                    }
                }
            }
        });
    };

    // Facebook's API automatically calls this function once it has finished loading
    window.fbAsyncInit = function() {
        FB.init({
            appId: Rover.facebook.appId, // App ID
            status: true, // check login status
            cookie: true, // enable cookies to allow the server to access the session
            xfbml: true,  // parse XFBML
            channelUrl: Rover.facebook.channelUrl
        });

        FB.Event.subscribe('edge.create', handleFacebookLike);

        FB.Event.subscribe('message.send', handleFacebookSend);

        FB.Event.subscribe('auth.authResponseChange', handleFacebookAuthChange);

        FB.Event.subscribe('comment.create', handleFacebookCommentCreate);

        // Show all FBui elements
        $('.FBui').show();
    };

    var handleFacebookLike = function(url, html_element) {
        var data = {
            event: 'facebook-like',
            shared_url: url
        };

        var trackingEvent = $(html_element).attr('data-tracking-event');
        if (trackingEvent) {
            data.event = trackingEvent;
        }

        dataLayer.push(data);

        Rover.share_local_callback('facebook', 'like');
    };

    var handleFacebookSend = function(targetUrl) {
        dataLayer.push({
            event: 'facebook-message-sent',
            shared_url: targetUrl
        });
    };

    var handleFacebookCommentCreate = function(response) {
        $.post('{% url "marketing-comment-notify" %}', {
            link: response.href
        });
    };

    /**
     * Callback for FB Authentication status
     */
    var handleFacebookAuthChange = function(response) {
        Rover.facebook.connected = response.status === 'connected';

        if (!Rover.facebook.connected || Rover.facebook.hasToken === false) {
            $.removeCookie('longtermtoken');
        }

        if (!Rover.facebook.connected) {
            return;
        }

        // Uncomment this once we're set on updating everyone
        // if ($.cookie('longtermtoken')) {
        //     return;
        // }

        // Only ask for a longterm token once a day
        $.cookie('longtermtoken', true, { expires: 1, path: '/'});

        var data = {
            token: response.authResponse.accessToken,
            facebook_id: response.authResponse.userID
        };

        if (Rover.facebook.connectLocation) {
            data.connect_location = Rover.facebook.connectLocation;
        }

        // Ping our server to renew/get a long term access token
        $.ajax({
            url: Rover.facebook.authCallbackUrl,
            type: 'POST',
            data: data
        });
    };

    var handleFBuiClick = function($elt, method) {
        $elt = $(this);
        var linkUrl = $elt.attr('data-link');
        // NOTE: Do not specify the data-* attributes if you want to use the
        // OpenGraph tags on the page (which you should do)
        var data = {
            method: $elt.attr('data-method') || 'feed',
            link: $elt.attr('data-link'),
            name: $elt.attr('data-name'),
            picture: $elt.attr('data-picture'),
            source: $elt.attr('data-source'),
            caption: $elt.attr('data-caption'),
            description: $elt.attr('data-description')
        };

        FB.ui(data, function(response) {
            if (response) {
                var tracking_event = $elt.attr('data-tracking-event') || 'share_review';
                if (tracking_event === 'share_review') {
                    dataLayer.push({
                        event: 'review-shared',
                        shared_url: linkUrl
                    });
                } else if (tracking_event === 'share_scrapsbook') {
                    dataLayer.push({
                        event: 'scrapsbook-shared',
                        shared_url: linkUrl
                    });
                } else if (tracking_event === 'testimonial-request-sent') {
                    $.post(
                        Rover.urls.trackTestimonialRequest,
                        {
                            method: 'facebook'
                        }
                    );
                }

                var shareAction = 'share';
                if ($elt.hasClass('js-enter-contest')) {
                    shareAction = 'contest-share';
                }

                Rover.track_social('facebook', shareAction, $elt.attr('data-content-type'), $elt.attr('data-object-id'));
                Rover.share_local_callback('facebook', 'share');
            }
        });
    };

    var handlePinItClick = function() {
        dataLayer.push({
            event: 'pinterest-share',
            shared_url: $(this).attr('data-link')
        });

        var newwindow = window.open($(this).attr('href'),'name','height=300,width=600');

        if (window.focus) {
            newwindow.focus();
        }

        Rover.share_local_callback('pinterest', 'share');
        return false;
    };

    var handleTwitterLoad = function() {
        if (window.hasOwnProperty('twttr')) {
            twttr.ready(function(twttr) {
                twttr.events.bind('follow', function() {
                    dataLayer.push({event: 'twitter-followed'});
                    Rover.share_local_callback('twitter', 'like');
                });
                twttr.events.bind('tweet', function() {
                    dataLayer.push({event: 'twitter-tweeted'});
                    Rover.share_local_callback('twitter', 'share');
                });
            });
        }
    };

    var loadSocialScripts = function() {
        $.getScript('//connect.facebook.net/en_US/all.js');

        // Google plus API configuration
        window.___gcfg = {
            lang: 'en-US'
        };
        $.getScript('https://apis.google.com/js/plusone.js');

        $.getScript('//platform.twitter.com/widgets.js', handleTwitterLoad);
    };

    var handleSocialSharePhoto = function(e) {
        var $currentTarget = $(e.currentTarget),
            network = $currentTarget.attr('data-network'),
            $wrapper = $currentTarget.parents('.js-sharing-wrapper');

        var urlToShare = $wrapper.attr('data-url-to-share'),
            imageToShare = $wrapper.attr('data-image-to-share'),
            imageThumb = $wrapper.attr('data-image-thumbnail'),
            contentType = $wrapper.attr('data-content-type'),
            objectId = $wrapper.attr('data-object-id'),
            campaign = $wrapper.attr('data-campaign'),
            trackingContent = $wrapper.attr('data-tracking-content'),
            shareLocation = $wrapper.attr('data-share-location');

        var utmParams = {
            utm_medium: 'onsite',
            utm_source: network,
            utm_campaign: campaign,
            utm_content: trackingContent
        };

        urlToShare = urlToShare + '?' + $.param(utmParams);

        if (network === 'facebook') {

            var facebookShareFormRendered = Mustache.template('new_design/social/facebook_share_form').render({
                imageToShare: imageToShare,
                urlToShare: urlToShare,
                imageThumb: imageThumb,
                contentType: contentType,
                objectId: objectId,
                shareLocation: shareLocation,
                signinUrl: Rover.urls.signin
            });

            $('.js-share-photo-to-facebook-form-content').html(facebookShareFormRendered);
            $('.js-facebook-share-modal').modal('show');

            dataLayer.push({
                event: 'facebook-share-shown',
                share_location: shareLocation
            });

        } else if (network === 'pinterest') {

            var popupWidth = 750,
                popupHeight = 331,
                left = (screen.width / 2) - (popupWidth / 2),
                top = (screen.height / 2) - (popupHeight / 2),
                popupOptions = 'top='+top+',left='+left+',height='+popupHeight+',width='+popupWidth+',toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=no,resizable=no';

            var pinterestUrl = Mustache.template('new_design/social/pinterest_share_link').render({
                url: encodeURIComponent(urlToShare),
                imageUrl: encodeURIComponent(imageToShare)
            });

            window.open(pinterestUrl, 'Share on Pinterest!', popupOptions);

            dataLayer.push({
                event: 'pinterest-share-shown',
                share_location: shareLocation
            });
        }
    };

    var addBindings = function() {
        // Feed is for displaying a story on your own news feed
        $(document).on('click', '.FBui', handleFBuiClick);
        // Pinterest - open a popup window
        $(document).on('click', '.pin-it-button', handlePinItClick);
        $(document).on('click', '.js-connect-facebook', handleConnectButtonClick);
        $(document).on('click', '.js-signup-with-facebook', handleSignupButtonClick);

        // New sharing
        $(document).on('click', '.js-social-share-photo-button', handleSocialSharePhoto);
        $(document).on('submit', '.js-share-photo-to-facebook-form', validatePermissionsAndShareOnFacebook);
    };

    var init = function() {
        // Hide all FBui elements until FB is loaded
        $('.FBui').hide();
        addBindings();
        loadSocialScripts();
    };

    init();
});
