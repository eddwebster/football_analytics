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
    jQuery.cookieComply v1.0
    Stephen Zsolnai http://www.zolla.co.uk

    To be used together with a simple alert box dropdown at the top of a site
    
    Relies on:
    Simple Tabs: https://github.com/zolitch/jQuery.simpleTabs
    jQuery-cookie: https://github.com/carhartl/jquery-cookie
    

    @license The MIT License (MIT)
    @preserve Copyright (c) <2012> <Stephen Zsolnai http://www.zolla.co.uk>


*/
/*jslint browser: true, vars: true, white: true, forin: true */
/*global define,require */
define(
[
    'jquery/core',
    'jquery-plugin/jquery.cookie',
    'jquery-plugin/jquery.simpleTabs'
],
function($){
    'use strict';

    $.cookieComply = {
        defaults: {
            globalComplianceCookie: 'CookieLawCompliance',
            cssActiveClass:'activated',
            timeLength: 9999,
            animationSpeed:300
        }
    };

    $.fn.cookieComply = function(options) {
        var $wrapper,
            $dropdown,
            $intro,
            $start,
            $success,
            contentHeight;
        return this.each(function(){
            var settings = $.extend({}, $.cookieComply.defaults, options),
                self = this,
                $wrapper = $(this),
                deleteCookie = function(cookie){
                    $.cookie(cookie, null);
                },
                setCookie = function(cookie, value, time){
                    $.cookie(cookie, value, { expires: time, path: '/' });
                },
                cookiePresent = function(cookie){
                    return $.cookie(cookie) ? true : false;
                },
                showSuccess = function(){
                    $start.html('<p>' + 'Thank you' + '</p>');
                    $start.fadeIn(settings.animationSpeed);
                    setTimeout(function(){
                        $wrapper
                            .css({'z-index:':0, 'overflow':'hidden'})
                           .animate({height:0}, settings.animationSpeed);
                    },2000);
                },
                fadeIntro = function(){
                    $start.fadeOut(settings.animationSpeed, showSuccess);
                },
                showContent = function(){
                    $wrapper.show();
                },
                hideContent = function(){
                    $wrapper.hide();
                },
                showDropdown = function(){
                    $dropdown.animate({"height":contentHeight},300);
                },
                hideDropdown = function(){
                    $dropdown.animate({"height":0},300);
                },
                initContent = function(){
                    $wrapper.find('.js-headerTabs').simpleTabs();
                    $dropdown = $wrapper.find('.headerDrop-dropDown');
                    $intro = $('.headerDrop-intro');
                    $start = $('.headerDrop-intro-start');
                    $dropdown.css({'top':$intro.outerHeight(true)});
                    $success = $('.headerDrop-intro-success');
                    contentHeight = $dropdown.find('.headerDrop-dropDown-inner').outerHeight(true);
                },
                attachHandlers = function(){
                    $('.js-cookieSet').click(function(e){
                        e.preventDefault();
                        var cookie = settings.globalComplianceCookie;
                        setCookie(cookie, 'allow', settings.timeLength);
                        hideDropdown();
                        fadeIntro();
                    });
                    $('.js-dropDownTrigger').click(function(e){
                        e.preventDefault();
                        var $this = $(this);
                        if($this.hasClass(settings.cssActiveClass)){
                            hideDropdown();
                            $this.removeClass(settings.cssActiveClass);
                        }else{
                            showDropdown();
                            $this.addClass(settings.cssActiveClass);
                        }

                    });
                },
                init = function(){
                    if(!cookiePresent(settings.globalComplianceCookie)){
                        initContent();
                        attachHandlers();
                    }
                    
                };
            init();
        });
    };

});


}
/*
     FILE ARCHIVED ON 18:10:48 Apr 23, 2013 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:30:15 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  LoadShardBlock: 1924.333 (3)
  captures_list: 1953.528
  load_resource: 78.631
  exclusion.robots: 0.213
  exclusion.robots.policy: 0.197
  PetaboxLoader3.datanode: 1752.472 (4)
  esindex: 0.024
  RedisCDXSource: 2.169
  CDXLines.iter: 22.502 (3)
  PetaboxLoader3.resolve: 43.86
*/