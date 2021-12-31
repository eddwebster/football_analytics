// @license  magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3.0
/* eslint-disable no-var, semi, prefer-arrow-callback, prefer-template */

/**
 * Collection of methods for sending analytics events to Archive.org's analytics server.
 *
 * These events are used for internal stats and sent (in anonymized form) to Google Analytics.
 *
 * @see analytics.md
 *
 * @type {Object}
 */
window.archive_analytics = (function defineArchiveAnalytics() {
  // keep orignal Date object so as not to be affected by wayback's
  // hijacking global Date object
  var Date = window.Date;
  var ARCHIVE_ANALYTICS_VERSION = 2;
  var DEFAULT_SERVICE = 'ao_2';
  var NO_SAMPLING_SERVICE = 'ao_no_sampling'; // sends every event instead of a percentage

  var startTime = new Date();

  /**
   * @return {Boolean}
   */
  function isPerformanceTimingApiSupported() {
    return 'performance' in window && 'timing' in window.performance;
  }

  /**
   * Determines how many milliseconds elapsed between the browser starting to parse the DOM and
   * the current time.
   *
   * Uses the Performance API or a fallback value if it's not available.
   *
   * @see https://developer.mozilla.org/en-US/docs/Web/API/Performance_API
   *
   * @return {Number}
   */
  function getLoadTime() {
    var start;

    if (isPerformanceTimingApiSupported())
      start = window.performance.timing.domLoading;
    else
      start = startTime.getTime();

    return new Date().getTime() - start;
  }

  /**
   * Determines how many milliseconds elapsed between the user navigating to the page and
   * the current time.
   *
   * @see https://developer.mozilla.org/en-US/docs/Web/API/Performance_API
   *
   * @return {Number|null} null if the browser doesn't support the Performance API
   */
  function getNavToDoneTime() {
    if (!isPerformanceTimingApiSupported())
      return null;

    return new Date().getTime() - window.performance.timing.navigationStart;
  }

  /**
   * Performs an arithmetic calculation on a string with a number and unit, while maintaining
   * the unit.
   *
   * @param {String} original value to modify, with a unit
   * @param {Function} doOperation accepts one Number parameter, returns a Number
   * @returns {String}
   */
  function computeWithUnit(original, doOperation) {
    var number = parseFloat(original, 10);
    var unit = original.replace(/(\d*\.\d+)|\d+/, '');

    return doOperation(number) + unit;
  }

  /**
   * Computes the default font size of the browser.
   *
   * @returns {String|null} computed font-size with units (typically pixels), null if it cannot be computed
   */
  function getDefaultFontSize() {
    var fontSizeStr;

    if (!('getComputedStyle' in window))
      return null;

    var style = window.getComputedStyle(document.documentElement);
    if (!style)
      return null;

    fontSizeStr = style.fontSize;

    // Don't modify the value if tracking book reader.
    if (document.documentElement.classList.contains('BookReaderRoot'))
      return fontSizeStr;

    return computeWithUnit(fontSizeStr, function reverseBootstrapFontSize(number) {
      // Undo the 62.5% size applied in the Bootstrap CSS.
      return number * 1.6;
    });
  }

  /**
   * Get the URL parameters for a given Location
   * @param  {Location}
   * @return {Object} The URL parameters
   */
  function getParams(location) {
    if (!location) location = window.location;
    var vars;
    var i;
    var pair;
    var params = {};
    var query = location.search;
    if (!query) return params;
    vars = query.substring(1).split('&');
    for (i = 0; i < vars.length; i++) {
      pair = vars[i].split('=');
      params[pair[0]] = decodeURIComponent(pair[1]);
    }
    return params;
  }

  function getMetaProp(name) {
    var metaTag = document.querySelector('meta[property=' + name + ']');
    return metaTag ? metaTag.getAttribute('content') || null : null;
  }

  var ArchiveAnalytics = {
    /**
     * @type {String|null}
     */
    service: getMetaProp('service'),
    mediaType: getMetaProp('mediatype'),
    primaryCollection: getMetaProp('primary_collection'),

    /**
     * Key-value pairs to send in pageviews (you can read this after a pageview to see what was
     * sent).
     *
     * @type {Object}
     */
    values: {},

    /**
     * Sends an analytics ping, preferably using navigator.sendBeacon()
     * @param {Object}   values
     * @param {Function} [onload_callback]      (deprecated) callback to invoke once ping to analytics server is done
     * @param {Boolean}  [augment_for_ao_site]  (deprecated) if true, add some archive.org site-specific values
     */
    send_ping: function send_ping(values, onload_callback, augment_for_ao_site) {
      if (typeof window.navigator !== 'undefined' && typeof window.navigator.sendBeacon !== 'undefined')
        this.send_ping_via_beacon(values);
      else
        this.send_ping_via_image(values);
    },

    /**
     * Sends a ping via Beacon API
     * NOTE: Assumes window.navigator.sendBeacon exists
     * @param {Object} values Tracking parameters to pass
     */
    send_ping_via_beacon: function send_ping_via_beacon(values) {
      var url = this.generate_tracking_url(values || {});
      window.navigator.sendBeacon(url);
    },

    /**
     * Sends a ping via Image object
     * @param {Object} values Tracking parameters to pass
     */
    send_ping_via_image: function send_ping_via_image(values) {
      var url = this.generate_tracking_url(values || {});
      var loadtime_img = new Image(1, 1);
      loadtime_img.src = url;
      loadtime_img.alt = '';
    },

    /**
     * Construct complete tracking URL containing payload
     * @param {Object} params Tracking parameters to pass
     * @return {String} URL to use for tracking call
     */
    generate_tracking_url: function generate_tracking_url(params) {
      var baseUrl = '//analytics.archive.org/0.gif';
      var keys;
      var outputParams = params;
      var outputParamsArray = [];

      outputParams.service = outputParams.service || this.service || DEFAULT_SERVICE;

      // Build array of querystring parameters
      keys = Object.keys(outputParams);
      keys.forEach(function keyIteration(key) {
        outputParamsArray.push(encodeURIComponent(key) + '=' + encodeURIComponent(outputParams[key]));
      });
      outputParamsArray.push('version=' + ARCHIVE_ANALYTICS_VERSION);
      outputParamsArray.push('count=' + (keys.length + 2)); // Include `version` and `count` in count

      return baseUrl + '?' + outputParamsArray.join('&');
    },

    /**
     * @param {int} page Page number
     */
    send_scroll_fetch_event: function send_scroll_fetch_event(page) {
      var additionalValues = { ev: page };
      var loadTime = getLoadTime();
      var navToDoneTime = getNavToDoneTime();
      if (loadTime) additionalValues.loadtime = loadTime;
      if (navToDoneTime) additionalValues.nav_to_done_ms = navToDoneTime;
      this.send_event('page_action', 'scroll_fetch', location.pathname, additionalValues);
    },

    send_scroll_fetch_base_event: function send_scroll_fetch_base_event() {
      var additionalValues = {};
      var loadTime = getLoadTime();
      var navToDoneTime = getNavToDoneTime();
      if (loadTime) additionalValues.loadtime = loadTime;
      if (navToDoneTime) additionalValues.nav_to_done_ms = navToDoneTime;
      this.send_event('page_action', 'scroll_fetch_base', location.pathname, additionalValues);
    },

    /**
     * @param {Object} [options]
     * @param {String} [options.mediaType]
     * @param {String} [options.mediaLanguage]
     * @param {String} [options.page] The path portion of the page URL
     */
    send_pageview: function send_pageview(options) {
      var settings = options || {};

      var defaultFontSize;
      var loadTime = getLoadTime();
      var mediaType = settings.mediaType;
      var primaryCollection = settings.primaryCollection;
      var page = settings.page;
      var navToDoneTime = getNavToDoneTime();

      /**
       * @return {String}
       */
      function get_locale() {
        if (navigator) {
          if (navigator.language)
            return navigator.language;

          else if (navigator.browserLanguage)
            return navigator.browserLanguage;

          else if (navigator.systemLanguage)
            return navigator.systemLanguage;

          else if (navigator.userLanguage)
            return navigator.userLanguage;
        }
        return '';
      }

      defaultFontSize = getDefaultFontSize();

      // Set field values
      this.values.kind     = 'pageview';
      this.values.timediff = (new Date().getTimezoneOffset()/60)*(-1); // *timezone* diff from UTC
      this.values.locale   = get_locale();
      this.values.referrer = (document.referrer == '' ? '-' : document.referrer);

      if (loadTime)
        this.values.loadtime = loadTime;

      if (navToDoneTime)
        this.values.nav_to_done_ms = navToDoneTime;

      /* START CUSTOM DIMENSIONS */
      if (defaultFontSize)
        this.values.ga_cd1 = defaultFontSize;

      if ('devicePixelRatio' in window)
        this.values.ga_cd2 = window.devicePixelRatio;

      if (mediaType)
        this.values.ga_cd3 = mediaType;

      if (settings.mediaLanguage) {
        this.values.ga_cd4 = settings.mediaLanguage;
      }

      if (primaryCollection) {
        this.values.ga_cd5 = primaryCollection;
      }
      /* END CUSTOM DIMENSIONS */

      if (page)
        this.values.page = page;

      this.send_ping(this.values);
    },

    /**
     * Sends a tracking "Event".
     * @param {string} category
     * @param {string} action
     * @param {string} label
     * @param {Object} additionalEventParams
     */
    send_event: function send_event(
        category,
        action,
        label,
        additionalEventParams
    ) {
      if (!label) label = window.location.pathname;
      if (!additionalEventParams) additionalEventParams = {};
      if (additionalEventParams.mediaLanguage) {
        additionalEventParams.ga_cd4 = additionalEventParams.mediaLanguage;
        delete additionalEventParams.mediaLanguage;
      }
      var eventParams = Object.assign(
        {
          kind: 'event',
          ec: category,
          ea: action,
          el: label,
          cache_bust: Math.random(),
        },
        additionalEventParams
      );
      this.send_ping(eventParams);
    },

    /**
     * Sends every event instead of a small percentage.
     *
     * Use this sparingly as it can generate a lot of events.
     *
     * @param {string} category
     * @param {string} action
     * @param {string} label
     * @param {Object} additionalEventParams
     */
    send_event_no_sampling: function send_event_no_sampling(
      category,
      action,
      label,
      additionalEventParams
    ) {
      var extraParams = additionalEventParams || {};
      extraParams.service = NO_SAMPLING_SERVICE;
      this.send_event(category, action, label, extraParams);
    },

    /**
     * @param {Object} options see this.send_pageview options
     */
    send_pageview_on_load: function send_pageview_on_load(options) {
      var self = this;
      window.addEventListener('load', function send_pageview_with_options() {
        self.send_pageview(options);
      });
    },

    /**
     * Handles tracking events passed in URL.
     * Assumes category and action values are separated by a "|" character.
     * NOTE: Uses the unsampled analytics property. Watch out for future high click links!
     * @param {Location}
     */
    process_url_events: function process_url_events(location) {
      var eventValues;
      var actionValue;
      var eventValue = getParams(location).iax;
      if (!eventValue) return;
      eventValues = eventValue.split('|');
      actionValue = eventValues.length >= 1 ? eventValues[1] : '';
      this.send_event_no_sampling(
        eventValues[0],
        actionValue,
        window.location.pathname
      );
    },

    /**
     * Attaches handlers for event tracking.
     *
     * To enable click tracking for a link, add a `data-event-click-tracking`
     * attribute containing the Google Analytics Event Category and Action, separated
     * by a vertical pipe (|).
     * e.g. `<a href="foobar" data-event-click-tracking="TopNav|FooBar">`
     *
     * To enable form submit tracking, add a `data-event-form-tracking` attribute
     * to the `form` tag.
     * e.g. `<form data-event-form-tracking="TopNav|SearchForm" method="GET">`
     *
     * Additional tracking options can be added via a `data-event-tracking-options`
     * parameter. This parameter, if included, should be a JSON string of the parameters.
     * Valid parameters are:
     * - service {string}: Corresponds to the Google Analytics property data values flow into
     */
    set_up_event_tracking: function set_up_event_tracking() {
      var self = this;
      var clickTrackingAttributeName = 'event-click-tracking';
      var formTrackingAttributeName = 'event-form-tracking';
      var trackingOptionsAttributeName = 'event-tracking-options';

      function handleAction(event, attributeName) {
        var selector = '[data-' + attributeName + ']';
        var eventTarget = event.target;
        if (!eventTarget) return;
        var target = eventTarget.closest(selector);
        if (!target) return;
        var categoryAction;
        var categoryActionParts;
        var options;
        categoryAction = target.dataset[attributeName];
        if (!categoryAction) return;
        categoryActionParts = categoryAction.split('|');
        options = target.dataset[trackingOptionsAttributeName] || {}; // Converts to JSON
        self.send_event(
          categoryActionParts[0],
          categoryActionParts[1],
          window.location.pathname,
          options.service ? { service: options.service } : {}
        );
      }

      document.addEventListener('click', function(e) {
        handleAction(e, clickTrackingAttributeName);
      });

      document.addEventListener('submit', function(e) {
        handleAction(e, formTrackingAttributeName);
      });
    },

    /**
     * @returns {Object[]}
     */
    get_data_packets: function get_data_packets() {
      return [this.values];
    },
  };

  return ArchiveAnalytics;
}());
// @license-end
