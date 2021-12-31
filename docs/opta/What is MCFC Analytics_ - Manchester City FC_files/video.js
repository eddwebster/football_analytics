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
	Video handler
	====
	Author:     Stephen Zsolnai (steve@zolla.co.uk)

	The video_spec object is output globally and contains 
	data for the video to be played. This module will only be 
	loaded if the video_spec is found.
	Only one player instance per page at this point.
-------------------------------------------------------*/

/*jslint browser: true, vars: true, white: false, forin: true */
/*global define,require,brightcove,window,console,video_spec,MCFC */
define([
    'jquery/core'
], function ($) {
	'use strict';

	var $body = $('body'),
		$videoWrapper,
		wrapperId = 'content-main-feature',
		playerSpec;

	window.onMediaPlay =  function(e) {
		console.log(window.tracking);
		var action = (video_spec.isPlayist) ? 'Playlist video played' : 'Video played';
		if(window.tracking){
			console.log('Track video: (category, action, label, value) action: ' + action + ' id: ' + e.media.id + 'title: ' + e.media.displayName );
			window.tracking.trackEvent('Videos', action, e.media.displayName + ' | #' + e.media.id + '#', '');
		}
	};
    window.onTemplateReady = function(evt) {
        var pollVideo;
        /*Wait for the Brighcove Player template to load*/
		if (typeof window.modVP !== 'undefined'){
		//loadNextVideo();
			if(video_spec.isPlayist){
				window.modVP.addEventListener(brightcove.api.events.MediaEvent.COMPLETE, window.onMediaComplete);
			}
			window.modVP.addEventListener(brightcove.api.events.MediaEvent.PLAY, window.onMediaPlay);
			clearTimeout(pollVideo);
		}else{
			pollVideo = setTimeout(window.onTemplateReady,200);
		}
    };
    window.playerTemplateLoaded = function(experienceID) {
        window.bcPlayer = brightcove.api.getExperience(experienceID);
        window.modVP = window.bcPlayer.getModule(brightcove.api.modules.APIModules.VIDEO_PLAYER);
        window.modExp = window.bcPlayer.getModule(brightcove.api.modules.APIModules.EXPERIENCE);
        window.modExp.addEventListener(brightcove.api.events.ExperienceEvent.TEMPLATE_READY, window.onTemplateReady);
		console.log('window.modExp: ' + window.modExp);
	};
	return {
		embedVideo: function(){
			if(brightcove !== undefined){
				var videoTemplate = $('#videoPlayerTmpl').html(),
				$video;
				$videoWrapper.html('');

				if(playerSpec.isPlayist){
					$video = $(videoTemplate).appendTo($videoWrapper);
				}else{
					videoTemplate = videoTemplate.replace('${videoId}', playerSpec.video_reference);
					$video = $(videoTemplate).appendTo($videoWrapper);
				}
			}
			brightcove.createExperiences();
		},
        play: function (element_id) {
			var elementId = (element_id) ? element_id : wrapperId;
			$videoWrapper = $('#' + elementId);
			playerSpec = video_spec;
			// stop the timer if we're on the homepage.
			if (window.MCFC.carousel) { window.MCFC.carousel.nav_manager.stop_timer(); }
			this.embedVideo();
			return false;
		},
		bindVideoPlay: function(){
			var self = this;
			$('.playVideo').click(function(e){
				self.play();
				e.preventDefault();
			});
		},
		attachHandlers: function(){
			var self =this;
			self.bindVideoPlay();
			$body.bind('slideChanged', function(ev){
				self.bindVideoPlay();
			});

		},
		init: function(){
			this.attachHandlers();
		}
	};

});


}
/*
     FILE ARCHIVED ON 12:01:00 Jan 12, 2013 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:30:06 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  RedisCDXSource: 2.173
  CDXLines.iter: 23.847 (3)
  exclusion.robots.policy: 1.398
  captures_list: 111.258
  load_resource: 80.37
  esindex: 0.015
  exclusion.robots: 1.422
  LoadShardBlock: 79.191 (3)
  PetaboxLoader3.resolve: 31.415
  PetaboxLoader3.datanode: 89.105 (4)
*/