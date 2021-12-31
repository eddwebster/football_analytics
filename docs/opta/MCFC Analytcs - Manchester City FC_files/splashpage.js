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


/*global MCFC */
/*jslint browser: true, nomen: false, white:false*/
/*
	
	Custom javascript for the splash page
	
	
*/
MCFC.splashpage = (function ($) {
    'use strict';
	
	var $splashContent,
		$close,
		$return,
		$swfElement,
		cookieId,
		pageId;
		
		
	var pub = {
		hidePage: function(){
			//remove flash element and then it's container to bybass browser glitches with hiding container element
			$splashContent.find('object').remove();
			$splashContent.remove();
		}
	},
	setCookie = function(){
		$.cookie(cookieId, true, {expires: 365});
	},
	cookieMatch = function(){
		return $.cookie(cookieId) ? true : false;
	},
	showPage = function(){
		$splashContent.css({'visibility':'visible'});
		$splashContent.show();
	},
	attachHandlers = function(){
		$close = $splashContent.find('.mod-splash-content-close');
		$return = $splashContent.find('.mod-splash-content-returnAnchor');
		$swfElement = $splashContent.find('.mod-splash-content-return');
		
		$close.click(function(e){
			//user has requested to not see page again so set cookie
			setCookie();
			pub.hidePage();
			e.preventDefault();
		});
		$return.click(function(e){
			pub.hidePage();
			e.preventDefault();
		});
	},
	pageInit = function(){
		if (!cookieMatch()){
			showPage();
			attachHandlers();
		}else{
			pub.hidePage();
		}
	},
	init = function () {
		$splashContent = $('.mod-splash');
		pageId = $splashContent.find('input.mod-splash-content-id').val();
		cookieId = pageId;
		if($splashContent.length){
			pageInit();
		}
	};
	
	
	MCFC.init.add_on_dom_ready(init);
	
	return pub;
	
}(window.jQuery));

}
/*
     FILE ARCHIVED ON 18:27:37 Aug 23, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:29:29 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  LoadShardBlock: 57.467 (3)
  captures_list: 109.876
  load_resource: 45.485
  exclusion.robots: 0.293
  exclusion.robots.policy: 0.278
  PetaboxLoader3.datanode: 60.282 (4)
  esindex: 0.034
  RedisCDXSource: 2.875
  CDXLines.iter: 39.846 (3)
  PetaboxLoader3.resolve: 20.988
*/