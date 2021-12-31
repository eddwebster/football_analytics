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
    MCFC.fontsizes = function (scope) {

        if (scope === undefined) {
            scope = document;
        }

        // 60px white text with transparent background
        $('h2.white-60', scope).h2swf({
            alpha: 0,
            blocking: [13, 5, 4, -3],
            leading: 3,
            tracking: -4,
            background_color: '1C2732',
            color: 'ffffff',
            font_size: 60,
            pad_desc: 5,
            sharpness: 0,
            thickness: 0,
            swf: "/flash/h2swf/header.swf",
            height: 'callback',
            width: 'callback'
        });

        // 60px white text with transparent background
        $('h2.white-50', scope).h2swf({
            alpha: 0,
            blocking: [13, 5, 4, -3],
            leading: 3,
            tracking: -4,
            background_color: '1C2732',
            color: 'ffffff',
            font_size: 50,
            pad_desc: 5,
            sharpness: 0,
            thickness: 0,
            swf: "/flash/h2swf/header.swf",
            height: 'callback',
            width: 'callback'
        });

        // 60px blue text with transparent background
        $('h2.blue-60', scope).h2swf({
            alpha: 0,
            blocking: [13, 5, 4, -3],
            leading: 3,
            tracking: -3,
            background_color: '1C2732',
            color: MCFC.resources.h2swf.fg1,
            font_size: 60,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            swf: "/flash/h2swf/header.swf",
            height: 'callback',
            width: 'callback'
        });

        // 60px blue text with transparent background
        $('h2.dblue-60', scope).h2swf({
            alpha: 0,
            blocking: [13, 5, 4, -3],
            leading: 3,
            tracking: -7,
            background_color: '1C2732',
            color: '101a24',
            font_size: 60,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            swf: "/flash/h2swf/header.swf",
            height: 'callback',
            width: 'callback'
        });

        // 60px white text on an opaque black background
        $('h2.white-60-opaque', scope).h2swf({
            // debug : 0,
            alpha: 0.74,
            blocking: [13, 20, 6, 9],
            leading: 2,
            tracking: -3,
            background_color: '000000',
            color: 'ffffff',
            font_size: 60,
            pad_desc: 10,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
		height: 'callback'
});

// 50px white text on an opaque black background
$('h2.white-50-opaque', scope).h2swf({
    // debug : 0,
    alpha: 0.74,
    blocking: [13, 20, 6, 9],
    leading: 2,
    tracking: -3,
    background_color: '000000',
    color: 'ffffff',
    font_size: 50,
    pad_desc: 10,
    sharpness: 0,
    thickness: 0,
    wordwrap: true,
    swf: "/flash/h2swf/header.swf",
    height: 'callback'
});

        // 41.1px Lottery numbers 
        $('h3.lotto-numbers', scope).h2swf({
            // debug : 0,
            alpha: 0,
            blocking: [0, 0, 0, 0],
            leading: 0,
            tracking: 45,
            background_color: '000000',
            color: 'ffffff',
            font_size: 41.1,
            pad_desc: 5,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // 40px white text on transparent background
        $('h2.white-40', scope).h2swf({
            // debug : 0,
            alpha: 0,
            blocking: [8, 10, 6, -3],
            leading: 2,
            tracking: -2,
            background_color: MCFC.resources.h2swf.bg1,
            color: 'ffffff',
            font_size: 40,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        $('h3.white-40', scope).h2swf({
            // debug : 0,
            alpha: 0,
            blocking: [1, 5, 5, 1],
            leading: 4,
            tracking: -2,
            background_color: MCFC.resources.h2swf.bg1,
            color: 'ffffff',
            font_size: 40,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // 40px bright blue text on transparent background
        $('h3.blue-40', scope).h2swf({
            alpha: 0,
            blocking: [8, 10, 6, -3],
            leading: 2,
            tracking: -2,
            background_color: '3a7895',
            color: '5cbfeb',
            font_size: 40,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // 40px blue on transparent background
        $('.sign-in h3.blue-40', scope).h2swf({
            alpha: 0,
            blocking: [0, 10, 6, -3],
            leading: 2,
            tracking: -2,
            background_color: 'FFFFFF',
            color: '48849f',
            font_size: 40,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // 40px blue on transparent background
        $('.card-selection h3.blue-40', scope).h2swf({
            alpha: 0,
            blocking: [0, 10, 6, -3],
            leading: 2,
            tracking: -2,
            background_color: 'FFFFFF',
            color: '48849f',
            font_size: 40,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // Tickets 24px dark blue text on transparent background
        $('h3.dblue-24', scope).h2swf({
            alpha: 0,
            blocking: [0, 0, 0, -2],
            leading: 0,
            tracking: -1,
            background_color: '000000',
            color: '101a24',
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        
        // Light blue sharing box with dark blue text
        $('h3.sharingblue-24', scope).h2swf({
            alpha: 0,
            blocking: [0, 0, 0, -2],
            leading: 0,
            tracking: -1,
            background_color: '000000',
            color: '223344',
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // Fans 24px bright blue text on transparent background
        $('h3.blue-24', scope).h2swf({
            alpha: 0,
            blocking: [0, 0, 0, -2],
            leading: 0,
            tracking: -1,
            background_color: '000000',
            color: MCFC.resources.h2swf.fg1,
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // Fans 24px white text on transparent background
        $('h3.white-24', scope).h2swf({
            alpha: 0,
            blocking: [0, 0, 0, -2],
            leading: 3,
            tracking: -1,
            background_color: '000000',
            color: 'ffffff',
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // QUOTE: 24px black text on white
        $('.article blockquote p.quote', scope).h2swf({
            alpha: 0,
            blocking: [5, 5, 5, 5],
            leading: 6,
            tracking: -1,
            background_color: 'ffffff',
            color: '5cbfeb',
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // PROMO: offer promo white text on transparent background
        $('.offer h3.white-36', scope).h2swf({
            alpha: 0,
            blocking: [5, 5, 0, 6],
            leading: 0,
            tracking: -1.75,
            background_color: '000000',
            color: 'ffffff',
            font_size: 36,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0.1,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // PROMO: offer promo blue text on transparent background
        $('.offer h3.blue-36', scope).h2swf({
            alpha: 0,
            blocking: [0, 5, 0, 6],
            leading: 0,
            tracking: -1.75,
            background_color: 'ffa800',
            color: MCFC.resources.h2swf.fg1,
            font_size: 36,
            pad_desc: 0,
            sharpness: 0,
            thickness: 5,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        // Homepage - Modules
        // Fans text - handwriting 
        $('.fans h4', scope).h2swf({
            alpha: 0,
            blocking: [0, 0, 10, 0],
            leading: -10,
            tracking: 0,
            background_color: '000000',
            color: 'ffffff',
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0.1,
            swf: "/flash/h2swf/felttip.swf",
            height: 'callback'
        });
        // Shop body text 24px white text on opaque black background
        $('h3.promo-title', scope).h2swf({
            alpha: 0.74,
            blocking: [5, 5, 5, 5],
            leading: 2,
            tracking: -1,
            background_color: '000000',
            color: 'ffffff',
            font_size: 24,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });

        ////////////// FONT SIZING WITHIN TICKETS - MEMBERSHIP
        // 40px Dark blue ticketing text
        $('.seats h3.dblue-40', scope).h2swf({
            alpha: 0,
            blocking: [1, 5, 0, 1],
            leading: 4,
            tracking: -2,
            background_color: '3a7895',
            color: '101a24',
            font_size: 40,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // White 18px text in Tickets
        $('h3.white-18', scope).h2swf({
            alpha: 0,
            blocking: [5, 5, 5, 0],
            leading: 4,
            tracking: -1,
            background_color: '000000',
            color: 'ffffff',
            font_size: 18,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // White 14px text transparent background
        $('h3.white-14', scope).h2swf({
            alpha: 0,
            blocking: [5, 5, 5, 0],
            leading: 4,
            tracking: -1,
            background_color: '000000',
            color: 'ffffff',
            font_size: 14,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // White 20px text in Tickets on transparent background
        $('h3.white-20', scope).h2swf({
            alpha: 0,
            blocking: [5, 5, 5, 0],
            leading: 4,
            tracking: -1,
            background_color: '000000',
            color: 'ffffff',
            font_size: 20,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });
        // Dark Blue 18px text in Tickets
        $('#tickets h3.dblue-18', scope).h2swf({
            alpha: 0,
            blocking: [5, 5, 5, 0],
            leading: 4,
            tracking: -1,
            background_color: '000000',
            color: '101A24',
            font_size: 18,
            pad_desc: 0,
            sharpness: 0,
            thickness: 0,
            wordwrap: true,
            swf: "/flash/h2swf/header.swf",
            height: 'callback'
        });


    };

    MCFC.init.add_on_dom_ready(MCFC.fontsizes);

})(jQuery);

}
/*
     FILE ARCHIVED ON 22:57:04 Aug 17, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:29:58 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  captures_list: 72.081
  exclusion.robots.policy: 0.18
  esindex: 0.015
  RedisCDXSource: 1.563
  PetaboxLoader3.datanode: 72.505 (4)
  PetaboxLoader3.resolve: 26.384
  CDXLines.iter: 25.193 (3)
  exclusion.robots: 0.194
  load_resource: 71.75
  LoadShardBlock: 39.091 (3)
*/