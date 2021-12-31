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

$(document).ready(function () {
    MCFC.matchdaycentre.make_link();
});

MCFC.matchdaycentre = function () {
    var optadata = $('span.optadata').html();
    var params = {
        base: '/flash/mdc/en/'
    };

    var attrs = {};

    var settings = {};

    return {

        element_id: "content-main-feature",

        play: function (element_id, default_flashvars) {
            settings.html = $('#' + element_id).clone().get(0);
            MCFC.swf.embed('/flash/mdc/en/loader.swf', this.element_id, 800, 450, default_flashvars, params, attrs);
        },

        on_close: function () {
            this.revert_to_html(this.element_id);
        },

        revert_to_html: function () {
            $('#' + this.element_id).replaceWith(settings.html);
            MCFC.fontsizes($('#' + this.element_id).parent());
        },

        make_link: function () {
            $('a.matchday-centre').live("click", function () {
                var default_flashvars = {
                    isArchived: "true", // isArchived - must have the value "true"
                    close_js_function: "MCFC.matchdaycentre.on_close",
                    base_url: "/mdc_matchreport/" + $('span.optadata').html() + "/"
                };

                MCFC.matchdaycentre.play('content-main-feature', default_flashvars);
                return false;
            })
        }

    };

} ();


}
/*
     FILE ARCHIVED ON 22:56:38 Aug 17, 2012 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 00:30:00 Dec 07, 2020.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
/*
playback timings (ms):
  CDXLines.iter: 24.202 (3)
  exclusion.robots: 0.199
  RedisCDXSource: 8.304
  PetaboxLoader3.datanode: 1156.505 (4)
  captures_list: 1159.476
  esindex: 0.01
  load_resource: 101.764
  exclusion.robots.policy: 0.186
  PetaboxLoader3.resolve: 42.413
  LoadShardBlock: 1119.88 (3)
*/