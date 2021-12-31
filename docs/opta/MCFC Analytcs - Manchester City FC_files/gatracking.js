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
-------------------------------------------------------------
// Author: Stephen Zsolnai / David Taylor

Documentation:
-	Default setup of Google Analytics. 

-	Include this file in the solution, run window.tracking.init
	and make sure that the GA ket is supplied on every page in an element with ID: 'googleAnalyticsKey'

-	This code also tracks downloads by regexing all links on a page for a supplies set of file extensions
	runs the event tracker.

-	This download event tracker will also run and use the link title of any link containing the class 'trackLink'.
	This is to ensure tracking of files that get served through handlers where the filenames are not available.
-------------------------------------------------------------
*/
/*jslint browser: true, nomen: false, white:true*/
/*global window, jQuery, _gaq:true */


(function($) {
    "use strict";
	
   

    var tracking = {
    	trackEvent: function(category, action, label, value) {
	        if (typeof _gaq !== 'undefined') {
	            _gaq = _gaq || [];
	            _gaq.push(['_trackEvent', '\'' + category + '\'', '\'' + action + '\'', '\'' + label + '\'', 0]);
	        }
	    },
    	playListTracking: function($wrapper){
    		var self = this;
    		if($wrapper.length){
				$wrapper.delegate('a', "click", function(e){
					var link = this,
						$link = $(link),
						eventAction = 'Playlist video play',
						videoName = $(link).attr('title') + '(Playlist: ' + $wrapper.closest('.mod-carousel').find('h4').html() + ')';
					
					self.trackEvent('Videos', eventAction, videoName, '');

					/*Is playlist part of a player or is it meant to contain hard links?*/
					if($('#playlist-player').length <= 0){
						setTimeout(function () {window.location.href = link.href;}, 100);
					}
					return false;
				});
    		}
			
    	},
		init: function() {
			var $body = $('body'),
				self = this;
			$body.delegate("a", "click", function(e){
				var t = this,
					$t = $(t),
					ext,
					fileName,
					filetypes = /(zip|ZIP|pdf|PDF|csv|CSV|doc*|DOC*|xls*|XLS*)+$/;
					
					fileName = /(\w|[\-.])+$/.exec(t.href)[0];
					ext = /[^\.]+$/.exec(fileName)[0];
					if (filetypes.test(ext)){
						var eventAction = 'Downloaded - ' + ext + ' Document';
						self.trackEvent('Download', eventAction, fileName, '');
						setTimeout(function () {
							window.location.href = t.href;
						}, 100);
						return false;
					}	
			});
		}
	};
	
	window.tracking = tracking;

} (jQuery));



}
/*
     FILE ARCHIVED ON 18:29:20 Aug 23, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:29:32 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  exclusion.robots: 0.198
  load_resource: 116.689
  captures_list: 104.913
  CDXLines.iter: 23.835 (3)
  RedisCDXSource: 20.684
  exclusion.robots.policy: 0.184
  PetaboxLoader3.datanode: 48.451 (4)
  LoadShardBlock: 53.059 (3)
  esindex: 0.015
  PetaboxLoader3.resolve: 90.977
*/