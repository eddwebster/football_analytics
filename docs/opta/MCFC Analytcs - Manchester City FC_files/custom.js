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

(function ($) {
    MCFC.custom = function (scope) {

        if (scope == undefined) {
            scope = document;
        }

        // Additional unsemantic elements can be written in for styled links
        $('a.btn:not(._btn)', scope).each(function () {
            var b = $(this);
            b.addClass('_btn');
            var tt = b.html() || b.val();
            b.html('').css({ cursor: 'pointer' }).prepend('<i></i>').append($('<span>').
		html(tt).append('<i></i><em></em><span></span>'));
        });

        /* ------------- Proxy links -------------- */
        // When the link is pressed it "clicks" the button.
        // The initial HTML looks like this:
        // 
        //    <input class="proxy" type="submit" value="Save">
        // 
        // After jQuery has done it's thing it look like this:
        //
        //    <a class="proxy" href="#"><i/><span>Save<i/><em/><span/><a href="#" class="proxy">Save</a>
        // The a, i, em and span elements have css applied to give the whole rounded corners.
        // Also if the original has a dos (disable on submit) class then the a element is disabled
        // and it and its children are greyed out when the image button is pressed.
        $('input.btn', scope).each(function () {
            var input = $(this);
            var dos = input.hasClass('dos');
            try {
                var isIE6 = navigator.userAgent.toLowerCase().indexOf('msie 6') != -1;
                var className = this.className;
                if (isIE6) {
                    className = "btnarw";
                }

                $('<a class="' + className + '" href="#"><i></i><span>' + this.value + '<i></i><em></em><span></span></span></a>')



			.insertBefore(this)
			.click(function () {
			    if (input.attr('type') == 'submit'
				 	&& MCFC.validation
					&& !MCFC.validation.validate(this)) {
			        return false;
			    }
			    if (dos) {
			        $(this).attr('disabled', 'disabled').css('background-color', '#888888');
			        $(this).find('*').css('background-color', '#888888');
			    }
			    input.click();
			    return false;
			});
                input.hide();
            } catch (err) { alert('here'); }
        });

        /* ------------- For dropdowns used as navigation, hide input buttons, unless JS is disabled  -------------- */
        $('.ifjs-hide', scope).hide();

        /* ------------- Navigation rounded corners  ---*/
        $('ul#nav-secondary li:first').addClass('first-top-left-corner');
        $('ul#nav-secondary li:last').addClass('bottom-left-corner');

        // Fine for nav items where there is a sub list
        //If no sub nab, this class should not be added
        if ($('ul#nav-secondary li.active ul')) {
            $('ul#nav-secondary li.active ul').parent().next().addClass('top-left-corner');
        }

        /* ------------- Reveal hidden tickets content  -------------- */
        $(".tickets-drawer-open").hide();
        $('.tickets-drawer a.handle').toggle(
			function () {
			    $(this).removeClass('open');
			    $(this).parent().find('div').slideDown();
			    $(this).html('Close');
			    $(this).addClass('close');
			},
			function () {
			    // $(this).prev().slideUp('slow');
			    $(this).removeClass('close');
			    $(this).parent().find('div').slideUp();
			    $(this).html('Prices &amp; release dates');
			    $(this).addClass('open');
			}
		);

        /* ------------- Players pages -----------------*/
        $("#players #content-main-feature .cmf-inner").addClass("js-enabled");

        /* ------------- jqModal boxes -----------------*/

        /* all jqmodals should have this method as onShow method */
        if ($.jqm) {
            var jqModalShow = function (hash) { hash.w.show(); MCFC.fontsizes(hash.w); MCFC.custom(hash.w); };
            $('#shop #allocatetickets', scope).jqm({
                trigger: 'a.trigger-allocatetickets',
                onShow: jqModalShow
            });

            // Size charts
            $('#shop #sizechart', scope).jqm({
                trigger: 'a.trigger-sizechart',
                onShow: jqModalShow
            });
        }

        /* ------------- open new windows using 'rel' attribute -----------------*/
        $("a[rel*='external']").each(function () {
            $(this).attr({
                title: "This link will open in a new window"
            });
            // add target attribute to link
            $(this).attr('target', '_blank');
        });

        /* ------------- set hidden h2swf text to show -----------------*/
        // $(".h2swf span").css("display","none");
        // $(".h2swf span").css("line-height","auto");


    };

    MCFC.init.add_on_dom_ready(MCFC.custom);

    function CheckBoxRequired_ClientValidate(sender, e) {
        e.IsValid = jQuery(".AcceptedAgreement input:checkbox").is(':checked');
    }

})(jQuery);

}
/*
     FILE ARCHIVED ON 18:27:45 Aug 23, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:29:29 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 244.859
  exclusion.robots: 0.144
  exclusion.robots.policy: 0.1
  RedisCDXSource: 4.258
  esindex: 0.006
  LoadShardBlock: 84.782 (3)
  PetaboxLoader3.datanode: 103.911 (4)
  CDXLines.iter: 18.661 (3)
  load_resource: 97.174
  PetaboxLoader3.resolve: 35.508
*/