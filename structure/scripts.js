/* Plugins 
______________________________________________________________________________*/

// Defines combined opacity/slider toggle
$.fn.opacitySlideToggle = function (speed, easing, callback) {
  return this.animate(
    {opacity: 'toggle',
    height: 'toggle'},
    speed, easing, callback);
};

// Defines simplistic toggleAttr method
$.fn.toggleAttr = function (attr, attr1, attr2) {
  return this.each(function() {
    if ($(this).attr(attr) == attr1)
      $(this).attr(attr, attr2);
    else
      $(this).attr(attr, attr1);
  });
};

// Set default display and tags for <details> elements
$.fn.detailsDefaults = function () {
  $(this).attr("aria-expanded","false");
  $(this).find("summary").click(function( event ) { event.preventDefault(); });
  $(this).find("summary a").click(function( event ) {
    event.stopPropagation(); // stop <summary> click disable from propagating
  });
};

// Adds expander button to details object
$.fn.addToggleAnchor = function () {
  var anchor = $('<a class="toggle_anchor" role="button" href="#" aria-label="Expand or collapse details"></a>');
  anchor.click(function( event ) {
    event.preventDefault();
    $(this).parent().parent().toggleClass('open');
    $(this).parent().parent().toggleAttr("aria-expanded","true","false");
    $(this).parent().parent().toggleAttr("open","open",null);
    $(this).parent().nextAll(".elaboration").first().opacitySlideToggle('fast','linear');    
  });
  anchor.appendTo(this);
};

// Adds menu anchor
$.fn.addMenuAnchor = function () {
  var anchor = $('<a class="menu_anchor" role="button" href="#" aria-label="Toggle navigation menu"></a>');
  anchor.click(function( event ) {
    event.preventDefault();
    $(this).parent().toggleClass('open');
    // prevent stuck color
    $(this).on('touchend', function () {
      $(this).css('color', 'white');
    });
  });
  anchor.prependTo(this);
};

// Add caption control anchors
$.fn.addCaptionControlAnchors = function () {
  var anchorHideCaption = $('<a class="hide-caption-anchor" href="#" aria-label="Hide caption and show full image"></a>');
  anchorHideCaption.click(function( event ) {
    event.preventDefault();
    $(this).parent().addClass('hide-caption');
  });
  var anchorShowCaption = $('<a class="show-caption-anchor" href="#" aria-label="Show caption"></a>');
  anchorShowCaption.click(function( event ) {
    event.preventDefault();
    $(this).parent().removeClass('hide-caption');
  });
  anchorHideCaption.prependTo(this);
  anchorShowCaption.prependTo(this);
};

/* DOM Functions
______________________________________________________________________________*/

// Hack to avoid webkit bug with pseudo-elements and after selector
// (applies irrelevant CSS property to force style update)
function webkitBugFix () {
  var href = $(this).attr('href');
  if (href.indexOf('http://') >= 0 | href.indexOf('https://') >= 0 ) {
  }
  else {
    $(this).css("animation","none");
  }
}

/* Ready-state executions
______________________________________________________________________________*/

$(document).ready(function() {

  // MSIE detection
  if (!navigator.userAgent.match(/msie|trident/i)) { $("html").addClass('no-ie'); };

  // Add nav menu anchor
  $("nav").addMenuAnchor();

  // Insert dynamic controls for <summary> elements
  $("details").detailsDefaults();
  $("summary").addToggleAnchor();
  
  // Insert dynamic controls for <figure#introduction> elements
  $("figure#introduction").addCaptionControlAnchors();
  
  // Webkit BugFix
  $("body").find("a").each(webkitBugFix);
  
  // Hyphenator
  Hyphenator.run();
 
  // first pass at wcag functionality
  var wcaglink = $("footer").find('a[href^="https://wave.webaim.org/report#/"]').first();
  var wcaghref = wcaglink.attr('href');
  var cururl = $(location).attr('href');
  wcaglink.attr('href',wcaghref+cururl);
  
  // iframe resize
  $("iframe").on("load", function() {
    var contentHeight = $(this).contents().find("body").height();
    $(this).height( 1.05 * contentHeight );
  });
  
  // dynamically add noncompliant css
  //yepnope.injectCss( './structure/noncompliant.css' ); -- Deprecated and removed from Modernizr
  $('head').append('<link rel="stylesheet" type="text/css" href="./structure/noncompliant.css" />');

  // expand details if inline anchor in URL
  var page_url = window.location.href, idx = page_url.indexOf("#");
  var hash = idx != -1 ? page_url.substring(idx+1) : "";
  var hash_details = $("#"+hash);
  hash_details.toggleClass('open');
  hash_details.toggleAttr("aria-expanded","true","false");
  hash_details.toggleAttr("open","open",null);
  hash_details.find(".elaboration").first().toggle();

  // hack to override Chrome behavior re details summary a span
  $("details summary a span").on('click touchstart', function () {
    var resource = $(this).parent().attr('href');
    window.location.href = resource;
  });

});