var _____WB$wombat$assign$function_____ = function(name) {return (self._wb_wombat && self._wb_wombat.local_init && self._wb_wombat.local_init(name)) || self[name]; };
if (!self.__WB_pmw) { self.__WB_pmw = function(obj) { this.__WB_source = obj; return this; } }
{
  let window = _____WB$wombat$assign$function_____("window");
  let self = _____WB$wombat$assign$function_____("self");
  let document = _____WB$wombat$assign$function_____("document");
  let location = _____WB$wombat$assign$function_____("location");
  let top = _____WB$wombat$assign$function_____("top");
  let parent = _____WB$wombat$assign$function_____("parent");
  let frames = _____WB$wombat$assign$function_____("frames");
  let opener = _____WB$wombat$assign$function_____("opener");

// Define main namespace
var MCFC = {};

	window.log = window.log || function(message){
		if (window.console && window.console.log){
			window.console.log(message);
		}
	};
// Define init object that 
// handles on load events
MCFC.init = function ($) {

    // First make sure we can debug using console
    if (!window.console) {
        window.console = {};
        methods = ['trace', 'log', 'info', 'debug', 'warn', 'error'];
        for (var key in methods) {
            window.console[methods[key]] = function (msg) { };
        };
    };

    // private variables
    var _dom_ready_callbacks = [];
    var _dom_ready = false;

    // on dom ready fires when jQuery document.ready fires.
    var on_dom_ready = function () {
        _dom_ready = true;
        obj.dispatch_ready(_dom_ready_callbacks);

        if (MCFC.membership != undefined) {
            MCFC.membership.init();
        }

        // set homepage link in the header requests to set 
        // as the homepage in IE or redirects to a page 
        // explaining how to.
        $('#header-makehome a').click(function(){
				try {
					this.style.behavior='url(#default#homepage)';

                    this.setHomePage(location.href);
					return false;
				} catch(ex){
					MCFC.window.log(ex);
				}
        });
        $('body').addClass('js');

    };

    // This is the object what will represent MCFC.init	
    var obj = {

        add_on_dom_ready: function (fn) {
            if (_dom_ready) return fn();
            _dom_ready_callbacks.push(fn);
        },

        // utility method that fires the callbacks.
        dispatch_ready: function (callbacks) {
            callbacks.reverse();
            while (callbacks.length) {
                callbacks.pop()();
            }
        }
    };

    $(document).ready(on_dom_ready);

    return obj;

} (jQuery);



/*
	Manages URL hashes
*/
MCFC.hash = function($) {
	
	var current_hash = "";
	var change_callbacks = [];
	var hash_change = function () {
		if(current_hash.toString() != pub.get().toString()) {
			for (var i=0; i < change_callbacks.length; i++) {
				change_callbacks[i](pub.get());
			};
			current_hash = pub.get();
		}
	};
	
	setInterval(hash_change, 150);
	
	var pub = {
		get : function(index){
			var url = document.location.hash;
			if(url.length === 0){
				return false;
			}
			var values = url.split("#/")[1];
			if(!values){
				return url;
			}
			var value = index !== undefined ? values.split("/")[index] : values && values.split("/") || false; 
			return value || false;
		},
		
		// string or array
		set : function(hash){
			if(hash !== undefined){
				hash = (typeof hash == 'object' && hash.length !== undefined) ? hash.join('/') : hash;
				hash = "#/" + hash;
			}else{
				hash = "#";
			}
			document.location.hash = hash;
			current_hash = this.get();
		},
		
		replace : function (index, value) {
			var all = this.get() || [];
			all[index]=value;
			this.set(all);
		},
		
		on_change : function (fn) {
			change_callbacks.push(fn);
		}
	};
	current_hash = pub.get();
		
	return pub;	
}(jQuery);


MCFC.swf = function($) {
	
	var default_flashvars = {
		debug : 0
	};
	var default_attributes = {};
	var default_params = {
		allowScriptAccess : 'sameDomain',
		allowFullScreen:"true",
		menu : false,
		quality : 'best',
		salign : 'tl',
		wmode : 'window'
	};
	
	return {
		embed : function (url, element_id, width, height, flashvars, params, attributes) {
			var flashvars = 	$.extend({}, default_flashvars, flashvars);
			var attributes = 	$.extend({}, default_attributes, attributes);
			var params = 		$.extend({}, default_params, params);
			if(!attributes.id) { attributes.id = element_id; }
			swfobject.embedSWF(url, element_id, width, height, "9.0.28", "/flash/expressInstall.swf", flashvars, params, attributes);
			setTimeout(function(){MCFC.swf.focus(element_id);}, 500);
			return document.getElementById(attributes.id);
		},

		remove : function (element_id) {
			swfobject.removeSWF(element_id);
		},
		
		focus : function (element_id) {
			$('#'+element_id).focus();
		}
	};
	
}(jQuery);


/* Behaviour for global search form */
MCFC.search = function ($) {
    var init = function () {
        if (MCFC.resources && MCFC.resources.search) {
            var search_fields = [
			    {
			        element: '#searchterm',
			        idle: MCFC.resources.search.SearchText
			    }
		    ];

            for (var i = 0; i < search_fields.length; i++) {
                bindEventsForSearchElement($(search_fields[i].element), search_fields[i].idle);
                $(search_fields[i].element).blur();
            };
        }
    };

    var bindEventsForSearchElement = function (el, idle) {
        el.blur(function () {
            if (!el.val()) {
                el.val(idle);
                el.addClass('blur');
            }
        });
        el.focus(function () {
            if (el.val() == idle) {
                el.val('');
                el.removeClass('blur');
            }
        });
    };

    MCFC.init.add_on_dom_ready(init);

} (jQuery);





/* setup all jquery UI tabs */
MCFC.jquery_ui_tabs = function ($) {
	MCFC.init.add_on_dom_ready(function(){
		$(".jquery-ui-tabs").tabs();
	});
}(jQuery);



/* simple one click share services */
MCFC.share = function ($) {
    var hover_timer;
    var init = function () {
        $('body').prepend('<div id="share_container" style="width:1px;height:1px;display:none;"></div>');    
        $('#mini-tab-add-this').mouseover(function (){
            clearTimeout(hover_timer);
            $('ul.sharing-list').show();
        });
        $('ul.sharing-list').mouseout(function () {
            hover_timer = setTimeout(function() {
                $('ul.sharing-list').hide();
            }, 500);
        });
    };
    
    MCFC.init.add_on_dom_ready(init);
    
	var popup = function (url) {
		window.open(url, 'share','scrollbars=yes,toolbar=0,status=0,width=750,height=500');
		return false;
	};	
	var services = {
		facebook : function (url, title) {
			return popup('https://web.archive.org/web/20120817225823/http://www.facebook.com/sharer.php?u='+url+'&t='+title);
		},
		digg : function (url, title) {
			return popup('https://web.archive.org/web/20120817225823/http://digg.com/submit?url='+url+'&amp;title='+title+'&amp;media=news&amp;topic=soccer');
		},		
		delicious : function (url, title) {
			return popup('https://web.archive.org/web/20120817225823/http://delicious.com/save?v=5&amp;noui&amp;jump=close&amp;url='+url+'&amp;title='+title);
		},
		twitter : function (url, title) {
		    var msg = title + '%20@%20' + url;
		    return popup('https://web.archive.org/web/20120817225823/http://twitter.com/home?status='+msg);
		},
		more : function (url, title) {
		    return addthis_open($('#share_container').get(0),'more', url, title);
		}
	};	
	return function(service, url, title) {
		var url = encodeURIComponent(url || location.href);
		var title = encodeURIComponent(title || document.title);
		return services[service](url, title);
	};
}(jQuery);


var addthis_pub="pokemcfc"; // addThis.com user. Ovverride this in the DOM if we need to change settings for different templates.
var addthis_options = 'email, facebook, twitter, delicious, digg, more';


/* takes a json object and returns a query string*/
MCFC.serialize = function (obj, url) {
	var s = url && url+'?'||'';
	for(k in obj) {
		s += '&'+k+'='+obj[k];
	}
	return s;
};


MCFC.decorators = {
	scope : function (fn, obj) {
		var wrapper = function() {
			return fn.apply(obj);
		};
		return wrapper;
	}
};

MCFC.decorators = {
    scope: function (fn, obj) {
        var wrapper = function () {
            return fn.apply(obj);
        };
        return wrapper;
    }
};

MCFC.showLikeButton = function (element) {

    FBIFrame = '<div id=fblike-container style="position:absolute; top:410px; left:20px; border:none; overflow:hidden; width:450px; height:21px;"><iframe src="https://web.archive.org/web/20120817225823/http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fmcfc.co.uk&amp;layout=button_count&amp;show_faces=true&amp;width=200&amp;action=like&amp;font=arial&amp;colorscheme=dark&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:200px; height:21px;" allowTransparency="true"></iframe></div>';
    $(element).html(FBIFrame + $(element).html());
}

//Add like button to a Flash element
$(document).ready(function () {
    if ($('#content-main input[type = "hidden"]').val() == '1') {
        MCFC.showLikeButton('#content-main-feature');
    }
});

MCFC.loadDialog = function (header, content, show) {

    var html = '<div class="jqmWindow jqmID1 dialogBox"><div class="jqmHeader"><h2 class="">' + header + '</h2><a href="#" class="close jqmClose"><span>Close</span></a></div><div class="jqmBody jqmBodyTgeneric"><p>' + content + '</p></div></div>';
    $("#container").after(html);

    /*Initialise and show the dialog*/
    $('.dialogBox').jqm();
    if (show) {
        $('.dialogBox').jqmShow();
    }
}

MCFC.language_selection = function ($) {
    var init = function () {
        if (MCFC.language_selection.show && $.jqm) {
            $('#language_selection').jqm({modal:false});
            $('#language_selection').jqmShow(); 
        };
    };
    MCFC.init.add_on_dom_ready(init);
    return {};
}(jQuery);

(function ($) {

    MCFC.direction = function () {
        return $(document.body).css('direction');
    };

})(jQuery);

MCFC.site_selection = function ($) {
    var init = function () {
        if (MCFC.site_selection.show && $.jqm) {
            $('#site_selection').jqm({ modal: false });
            $('#site_selection').jqmShow();
        };
    };
    MCFC.init.add_on_dom_ready(init);
    return {};
}(jQuery);

/*Load Google Tracking code*/
MCFC.gaTracking = function ($) {
    MCFC.init.add_on_dom_ready(function () {
        if (window.tracking) {
            window.tracking.init();
        }
    });
} (jQuery);
/*
{"error":false,"message":"You've signed up","success":true,"title":"Success","validationError":false}
*/
MCFC.signupValidation = function ($) {
    var actionUrl = '/Services/EmailSignUpService.svc/signupservice/${emailAddress}/list/${exactTargetListId}/id/${itemId}';
    var fadeMessage = function($msgWrapper){
		$msgWrapper.fadeOut('slow');
	},
	hideMessage = function($msgWrapper){
		$msgWrapper.hide();
	},
	showMessage = function($msgWrapper, msg){
		$msgWrapper.html(msg);
		$msgWrapper.show();
	},
	hideForm = function($form, $msgBox){
		$msgBox.css({'bottom':'0'});
	},
	processFormAjaxResponse = function (data, status, $form, $msgBox) {
        if (status === 'success') {
			showMessage($msgBox, data.message);
			if (!data.validationError){
				hideForm($form, $msgBox);
				//setTimeout(function(){fadeMessage($msgBox)}, 3000);
			}
        } else {
            showMessage($msgBox, 'There was an error. Please try again');
        }
    },
	setFormAction = function ($form, emailAddress, exactTargetListIdValue, emailCaptureIdValue) {
		var emailAd = emailAddress.replace('/','').replace(/\+/g, '%2B');
		action = actionUrl.replace('${emailAddress}', encodeURI(emailAd));
		action = action.replace('${exactTargetListId}', encodeURI(exactTargetListIdValue));
		action = action.replace('${itemId}', encodeURI(emailCaptureIdValue));
		$form.get(0).setAttribute('action', action);
	},
	addHandlers = function ($form, $emailfield, $exactTargetListIdfield, $emailCaptureIdfield, $msgBox) {
		$form.submit(function(e){
			hideMessage($msgBox);
			showMessage($msgBox, '<span class="cp-loading">Sending...</span>');
			var emailValue = $emailfield.val();
			var exactTargetListIdValue = $exactTargetListIdfield.val();
			var emailCaptureIdValue = $emailCaptureIdfield.val();
			if (emailValue !== ''){
			    setFormAction($form, emailValue, exactTargetListIdValue, emailCaptureIdValue);
			}else{
				showMessage($msgBox, 'Please enter your email address.');
			}
			submitWithAjax($form, function(data, status){
				processFormAjaxResponse(data, status, $form, $msgBox);
			});
			e.preventDefault();
			
		});
	},
    submitWithAjax = function ($form, callback) {
        $.post($form.attr('action'), $form.serialize(), callback, 'json')
            .error(function(xhr, status){
                callback.call(this, {}, status);
            });;
        return true;
    },
	init = function () {
		$('.signupValidation').each(function(){
			
			var $form = $(this),
				$formWrapper = $form.closest('div');
				$emailfield = $form.find('input:text'),
                $exactTargetListIdfield = $form.find('input[name=ExactTargetListId]'),
                $emailCaptureIdfield = $form.find('input[name=ItemId]'),
				$msgBox = $('<p class="promo-footer-error"></p>').appendTo($formWrapper);
			addHandlers($form, $emailfield, $exactTargetListIdfield, $emailCaptureIdfield, $msgBox);
		});
    };
    MCFC.init.add_on_dom_ready(init);
    return {};
}(jQuery);



}
/*
     FILE ARCHIVED ON 22:58:23 Aug 17, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:29:55 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  esindex: 0.013
  CDXLines.iter: 22.97 (3)
  exclusion.robots: 0.193
  exclusion.robots.policy: 0.178
  PetaboxLoader3.resolve: 71.396
  load_resource: 99.497
  captures_list: 75.917
  LoadShardBlock: 45.956 (3)
  RedisCDXSource: 1.104
  PetaboxLoader3.datanode: 62.375 (4)
*/