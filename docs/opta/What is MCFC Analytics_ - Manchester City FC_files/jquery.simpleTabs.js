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
    jQuery.simpleTabs v0.1
    Stephen Zsolnai http://www.zolla.co.uk

    @license The MIT License (MIT)
    @preserve Copyright (c) <2012> <Stephen Zsolnai http://www.zolla.co.uk>


*/
/*jslint browser: true, vars: true, white: false, forin: true */
/*global define,require */
(function($){
    'use strict';

    $.simpleTabs = {
        defaults: {
            onClass: 'simpleTabs-on',
            speed: 500,
            window: '.simpleTabs-contentWrap'
        }
    };

    $.fn.simpleTabs = function(options) {
        return this.each(function(){
            var settings = $.extend({}, $.simpleTabs.defaults, options),
                self = this,
                $simpleTabs = $(this),
                $tabWrap = $simpleTabs.find('> ul'),
                $tabs = $tabWrap.find('li'),
                $containers = $simpleTabs.find('>div'),

                showItem = function($item){
                    $item.siblings('div').fadeOut();
                    $item.show().fadeIn();
                },
                initTabs = function(){
                    var $firstLink = $simpleTabs.find('li:first-child a'),
                        $firstContainer = $($firstLink.attr('href'));
                        $firstLink.closest('li').addClass(settings.onClass);
                        showItem($firstContainer);
                };

            
            $tabs.find('a').click(function(e){

                var $this = $(this),
                    $page = $($this.attr('href'))
                    //left = $page.position().left,
                    //$window = $page.closest(settings.window)
                ;
                $this.closest('li').siblings().removeClass(settings.onClass);
                $this.closest('li').addClass(settings.onClass);
                //$window.animate({ scrollLeft: left }, 300);
                $page.siblings('div').fadeOut();
                $page.fadeIn();

                e.preventDefault();
            });

            initTabs();
        });
    };

}(window.jQuery));


}
/*
     FILE ARCHIVED ON 18:10:49 Apr 23, 2013 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:30:19 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  esindex: 0.015
  CDXLines.iter: 24.199 (3)
  LoadShardBlock: 189.242 (3)
  RedisCDXSource: 15.502
  load_resource: 73.606
  captures_list: 233.306
  exclusion.robots.policy: 0.188
  PetaboxLoader3.resolve: 142.621 (2)
  PetaboxLoader3.datanode: 115.533 (4)
  exclusion.robots: 0.202
*/