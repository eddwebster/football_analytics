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


/*
 iOS specific functionality
*/
/*jslint browser: true, vars: true, white: false, forin: true, nomen: true */
/*global define,require,window,Modernizr */
define(
[
	'jquery/core',
	'jquery-plugin/cookiecomply/jquery.cookiecomply'
],
function($){
    'use strict';

    var $footer = $('#footer'),
		$alert,
		ALERT_FIXED_CLASS = 'headerDropTfixed',
		$window = $(window),
		positionToTop,
		alertFixed = true,
		positionAlert = function(){
			positionToTop = $footer.position().top - $window.height(true);
		},
		attachAlert = function(){
			$alert.removeClass(ALERT_FIXED_CLASS);
		},
		detachAlert = function(){
			$alert.addClass(ALERT_FIXED_CLASS);
		},
		attachScrollHandler = function(){
			detachAlert();
			$window.scroll(function(e){
				if(positionToTop < $window.scrollTop() && alertFixed){
					attachAlert();
					alertFixed = false;
				}
				if(positionToTop >= $window.scrollTop() && !alertFixed){
					detachAlert();
					alertFixed = true;
				}
			});	
		};
	
	return {
		init: function($elem){
			$alert = $elem;
			if(!Modernizr.touch){
				attachScrollHandler();
			}
			positionAlert();
			$elem.cookieComply();
		}
	};
});



}
/*
     FILE ARCHIVED ON 18:10:47 Apr 23, 2013 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:30:12 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  PetaboxLoader3.resolve: 53.374
  esindex: 0.012
  captures_list: 71.733
  RedisCDXSource: 8.963
  LoadShardBlock: 29.237 (3)
  PetaboxLoader3.datanode: 117.977 (4)
  exclusion.robots.policy: 0.138
  load_resource: 152.132
  CDXLines.iter: 29.617 (3)
  exclusion.robots: 0.152
*/