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

/**
* Main
* ====
* This is the main js initialiser for the page
* it is triggered by the data-main attribute on the
* require script tag.
* <script data-main="/js/main" src="/lib/require.js"></script>
* for more information see <http://requirejs.org>
*/
/*jslint browser: true, vars: true, white: false, forin: true */
/*global define,require,VideoJS,video_spec */
(function(){
    'use strict';

		var options = {
			paths: {
			jquery: '../lib/jquery-core',
			lib: '../lib', 
			'jquery-plugin': '../lib/jquery-plugins',
			images: '../images'
			}
		};
		require(options, 
		[
			'jquery/core',
			'video/video'
		], function($, video) {

		    var $window = $(window),
		        $body = $('body')
		    ;
		   

		
			
		/*	video_spec is output to the page with details of the video
		to be played. Load video module if it exists
		*/
	    if(typeof video_spec !== 'undefined'){
			if(video_spec.isPlayist){
				require(['video/playlists'], function(playlists){
					playlists.init();
				});
			}else{
				video.init();
			}
		}else{
			video.init();
		}

		/*
			Is the main carousel on the page?
			
		*/
		var $carousel = $('#carousel');
		if($carousel.length){
			require(['core/carousel'], function(carousel){
				//this will not return a require object. Old file.
				
			});
		}

		/*If no video_spec exists, we may still need to load playlists*/
		var $bcPlaylist = $('.brightcovePlaylistID');
		if(typeof video_spec === 'undefined' && $bcPlaylist.length){
			require(['video/playlists'], function(playlists){
				playlists.init($bcPlaylist);
			});
		}

	/*
		=> Load custom tweet river and it's scroll functionality
	**********************************************/
		var $tweetRiverWrapper = $('.tweetRiver');
		if ($tweetRiverWrapper.length){

			$tweetRiverWrapper.each(function(){
				var $self = $(this);
				require(['core/tweetriver'], function(tweetriver){
					tweetriver.init($self);
				});
			});
		}
	
	/*
		=> Trigger mobile + tablet touch specific actions
	**********************************************/
		if (window.Modernizr.touch){
			require(['core/touchspecific'], function(touch){
				touch.init();
			});
			require(['core/ios'], function(ios){
				ios.init();
			});
		}

	/*
	=> Simple Tabbing
	**********************************************/
		var $simpleTabs = $('.simpleTabs');
		if ($simpleTabs.length){
			$simpleTabs.each(function(){
				var $self = $(this);
				require(['jquery-plugin/jquery.simpleTabs'], function(st){
					$self.simpleTabs();
				});
			});
		}
	/*
	=> Animated Paging
	**********************************************/
		var $stepPager = $('.stepPager');
		if ($stepPager.length){
			$stepPager.each(function(){
				var $self = $(this);
				require(['jquery-plugin/jquery.stepPager'], function(sp){
					$self.stepPager();
				});
			});
		}
	/*
	=> Cookie Compliance
	**********************************************/
		var $cookieComply = $('.js-cookieComply');
		if ($cookieComply.length){
			$cookieComply.each(function(){
				var $self = $(this);
				require(['core/footeralert'], function(footeralert){
					footeralert.init($self);
				});
			});
		}
	});
}());



}
/*
     FILE ARCHIVED ON 16:39:47 Aug 03, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:29:44 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  exclusion.robots.policy: 0.186
  esindex: 0.016
  exclusion.robots: 0.202
  LoadShardBlock: 73.802 (3)
  CDXLines.iter: 24.501 (3)
  RedisCDXSource: 52.405
  captures_list: 154.925
  PetaboxLoader3.datanode: 332.396 (4)
  load_resource: 345.261
  PetaboxLoader3.resolve: 55.85
*/