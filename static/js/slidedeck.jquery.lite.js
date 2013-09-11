/**
 * SlideDeck 1.1.7 Lite - 2010-07-18
 * Copyright (c) 2010 digital-telepathy (http://www.dtelepathy.com)
 *
 * Support the developers by purchasing the Pro version at http://www.slidedeck.com/download
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 * More information on this project:
 * http://www.slidedeck.com/
 *
 * Requires: jQuery v1.3+
 *
 * Full Usage Documentation: http://www.slidedeck.com/usage-documentation
 * Usage:
 *     $(el).slidedeck(opts);
 *
 * @param {HTMLObject} el    The <DL> element to extend as a SlideDeck
 * @param {Object} opts        An object to pass custom override options to
 */

var SlideDeck;

(function($){
    SlideDeck = function(el,opts){
        var self = this,
            el = $(el);

        var VERSION = "1.1.7";

        this.options = {
            speed: 500,
            transition: 'swing',
            start: 1,
            activeCorner: true,
            index: true,
            scroll: true,
            keys: true,
            autoPlay: false,
            autoPlayInterval: 5000,
            hideSpines: false,
            cycle: false
        };

        this.classes = {
            slide: 'slide',
            spine: 'spine',
            label: 'label',
            index: 'index',
            active: 'active',
            indicator: 'indicator',
            activeCorner: 'activeCorner',
            disabled: 'disabled',
            vertical: 'slidesVertical',
            previous: 'previous',
            next: 'next'
        };

        this.current = 1;
        this.deck = el;
        this.spines = el.find('dt');
        this.slides = el.find('dd');
        this.controlTo = 1;
        this.session = [];
        this.disabledSlides = [];
        this.pauseAutoPlay = false;
        this.isLoaded = false;

        var UA = navigator.userAgent.toLowerCase();
        this.browser = {
            chrome: UA.match(/chrome/) ? true : false,
            firefox: UA.match(/firefox/) ? true : false,
            firefox2: UA.match(/firefox\/2/) ? true : false,
            firefox30: UA.match(/firefox\/3\.0/) ? true : false,
            msie: UA.match(/msie/) ? true : false,
            msie6: (UA.match(/msie 6/) && !UA.match(/msie 7|8/)) ? true : false,
            msie7: UA.match(/msie 7/) ? true : false,
            msie8: UA.match(/msie 8/) ? true : false,
            chromeFrame: (UA.match(/msie/) && UA.match(/chrome/)) ? true : false,
            opera: UA.match(/opera/) ? true : false,
            safari: (UA.match(/safari/) && !UA.match(/chrome/)) ? true : false
        };
        for(var b in this.browser){
            if(this.browser[b] === true){
                this.browser._this = b;
            }
        }
        if(this.browser.chrome === true) {
            this.browser.version = UA.match(/chrome\/([0-9\.]+)/)[1];
        }
        if(this.browser.firefox === true) {
            this.browser.version = UA.match(/firefox\/([0-9\.]+)/)[1];
        }
        if(this.browser.msie === true) {
            this.browser.version = UA.match(/msie ([0-9\.]+)/)[1];
        }
        if(this.browser.opera === true) {
            this.browser.version = UA.match(/version\/([0-9\.]+)/)[1];
        }
        if(this.browser.safari === true) {
            this.browser.version = UA.match(/version\/([0-9\.]+)/)[1];
        }

        var width;
        var height;

        var spine_inner_width,
            spine_outer_width,
            slide_width,
            spine_half_width;

        var FixIEAA = function(spine){
            if(self.browser.msie && !self.browser.chromeFrame){
                var bgColor = spine.css('background-color');
                var sBgColor = bgColor;
                if(sBgColor == "transparent"){
                    bgColor = "#ffffff";
                } else {
                    if(sBgColor.match('#')){
                        // Hex, convert to RGB
                        if(sBgColor.length < 7){
                            var t = "#" + sBgColor.substr(1,1) + sBgColor.substr(1,1) + sBgColor.substr(2,1) + sBgColor.substr(2,1) + sBgColor.substr(3,1) + sBgColor.substr(3,1);
                            bgColor = t;
                        }
                    }
                }
                bgColor = bgColor.replace("#","");
                cParts = {
                    r: bgColor.substr(0,2),
                    g: bgColor.substr(2,2),
                    b: bgColor.substr(4,2)
                };
                var bgRGB = "#";
                var hexVal = "01234567890ABCDEF";
                for(var k in cParts){
                    cParts[k] = Math.max(0,(parseInt(cParts[k],16) - 1));
                    cParts[k] = hexVal.charAt((cParts[k] - cParts[k]%16)/16) + hexVal.charAt(cParts[k]%16);

                    bgRGB += cParts[k];
                }

                spine.find('.' + self.classes.index).css({
                    'filter': 'progid:DXImageTransform.Microsoft.BasicImage(rotation=1) chroma(color=' + bgRGB + ')',
                    backgroundColor: bgRGB
                });
            }
        };


        /**
         * Visual Attribution "Bug"
         *
         * This is a visual "bug" that is placed in the lower right of the SlideDeck to give
         * visual recognition to SlideDeck and for us to see where any implementations that might
         * be worth placing in our community examples page reside. To help keep this plugin free
         * we ask (although we cannot force) you to keep this visual "bug" on the page since it
         * helps support the author.
         *
         * If you would like to remove the visual "bug", we recommend you comment out the
         * updateBug(); function and remove any references to the updateBug(); command.
         */
        var BUG = {
            id: "SlideDeck_Bug"+(Math.round(Math.random()*100000000)),
            styles: "position:absolute !important;height:"+13+"px !important;width:"+130+"px !important;display:block !important;margin:0 !important;overflow:hidden !important;visibility:visible !important;opacity:1 !important;padding:0 !important;z-index:20000 !important",
            width: 130,
            height: 13
        };
        var updateBug = function(){
            if(!document.getElementById(BUG.id)){
                var bugLink = document.createElement('A');
                    bugLink.id = BUG.id;
                    bugLink.href = "http://www.slidedeck.com/?ref=" + document.location.hostname;
                    bugLink.target = "_blank";
                var bugImg = document.createElement('IMG');
                    bugImg.src = (document.location.protocol == "https:" ? "https:" : "http:") + "//www.slidedeck.com/6885858486f31043e5839c735d99457f045affd0/" + VERSION + "/lite";
                    bugImg.alt = "Powered by SlideDeck&trade;";
                    bugImg.width = BUG.width;
                    bugImg.height = BUG.height;
                    bugImg.border = "0";
                bugLink.appendChild(bugImg);

                BUG.top = (el.offset().top + el.height() + 5);
                BUG.left = el.offset().left + el.width() - BUG.width;

                var s = document.createElement('STYLE');
                    s.type = "text/css";
                var sText = '#' + BUG.id + '{top:' + BUG.top + 'px;left:' + BUG.left + 'px;' + BUG.styles + '}' + '#' + BUG.id + ' img{top:0 !important;left:0 !important;' + BUG.styles + '}';
                if(s.styleSheet){
                    s.styleSheet.cssText = sText;
                } else {
                    s.appendChild(document.createTextNode(sText));
                }
                $('head').append(s);

                if(Math.random() < 0.5){
                    $(document.body).prepend(bugLink);
                } else {
                    $(document.body).append(bugLink);
                }

                $(window).resize(function(){
                    updateBug();
                });
            }
            BUG.top = (el.offset().top + el.height() + 5);
            BUG.left = el.offset().left + el.width() - BUG.width;

            $('#' + BUG.id).css({
                top: BUG.top + "px",
                left: BUG.left + "px"
            });
        };


        var autoPlay = function(){
            gotoNext = function(){
                if(self.pauseAutoPlay === false){
                    if(self.options.cycle === false && self.current == self.slides.length){
                        self.pauseAutoPlay = true;
                    } else {
                        self.next();
                    }
                }
            };

            setInterval(gotoNext,self.options.autoPlayInterval);
        };


        var buildDeck = function(){
            if($.inArray(el.css('position'),['position','absolute','fixed'])){
                el.css('position', 'relative');
            }
            el.css('overflow', 'hidden');
            for(var i=0; i<self.slides.length; i++){
                var slide = $(self.slides[i]);
                if(self.spines.length > i){
                    var spine = $(self.spines[i]);
                }
                var sPad = {
                    top: parseInt(slide.css('padding-top'),10),
                    right: parseInt(slide.css('padding-right'),10),
                    bottom: parseInt(slide.css('padding-bottom'),10),
                    left: parseInt(slide.css('padding-left'),10)
                };
                var sBorder = {
                    top: parseInt(slide.css('border-top-width'),10),
                    right: parseInt(slide.css('border-right-width'),10),
                    bottom: parseInt(slide.css('border-bottom-width'),10),
                    left: parseInt(slide.css('border-left-width'),10)
                };
                for(var k in sBorder){
                    sBorder[k] = isNaN(sBorder[k]) ? 0 : sBorder[k];
                }
                if(i < self.current) {
                    if(i == self.current - 1){
                        if(self.options.hideSpines !== true){
                            spine.addClass(self.classes.active);
                        }
                        slide.addClass(self.classes.active);
                    }
                    offset = i * spine_outer_width;
                    if(self.options.hideSpines === true){
                        offset = 0 - (i * el.width());
                    }
                } else {
                    offset = i * spine_outer_width + slide_width;
                    if(self.options.hideSpines === true){
                        offset = i * el.width();
                    }
                }

                self.slide_width = (slide_width - sPad.left - sPad.right - sBorder.left - sBorder.right);

                slide.css({
                    position: 'absolute',
                    left: offset,
                    zIndex: 1,
                    height: (height - sPad.top - sPad.bottom - sBorder.top - sBorder.bottom) + "px",
                    width: self.slide_width + "px",
                    margin: 0,
                    paddingLeft: sPad.left + spine_outer_width + "px"
                }).addClass(self.classes.slide).addClass(self.classes.slide + "_" + (i + 1));

                if (self.options.hideSpines !== true) {
                    var spinePad = {
                        top: parseInt(spine.css('padding-top'),10),
                        right: parseInt(spine.css('padding-right'),10),
                        bottom: parseInt(spine.css('padding-bottom'),10),
                        left: parseInt(spine.css('padding-left'),10)
                    };
                    for(var k in spinePad) {
                        if(spinePad[k] < 10 && (k == "left" || k == "right")){
                            spinePad[k] = 10;
                        }
                    }
                    var spinePadString = spinePad.top + "px " + spinePad.right + "px " + spinePad.bottom + "px " + spinePad.left + "px";
                    spine.css({
                        position: 'absolute',
                        zIndex: 3,
                        display: 'block',
                        left: offset,
                        width: (height - spinePad.left - spinePad.right) + "px",
                        height: spine_inner_width + "px",
                        padding: spinePadString,
                        rotation: '270deg',
                        '-webkit-transform': 'rotate(270deg)',
                        '-webkit-transform-origin': spine_half_width + 'px 0px',
                        '-moz-transform': 'rotate(270deg)',
                        '-moz-transform-origin': spine_half_width + 'px 0px',
                        '-o-transform': 'rotate(270deg)',
                        '-o-transform-origin': spine_half_width + 'px 0px',
                        textAlign: 'right',
                        top: (self.browser.msie && !self.browser.chromeFrame) ? 0 : (height - spine_half_width) + "px",
                        marginLeft: ((self.browser.msie && !self.browser.chromeFrame) ? 0 : (0 - spine_half_width)) + "px",
                        filter: 'progid:DXImageTransform.Microsoft.BasicImage(rotation=3)'
                    }).addClass(self.classes.spine).addClass(self.classes.spine + "_" + (i + 1));
                } else {
                    if(typeof(spine) != "undefined"){
                        spine.hide();
                    }
                }
                if(i == self.slides.length-1){
                    slide.addClass('last');
                    if(self.options.hideSpines !== true){
                        spine.addClass('last');
                    }
                }

                // Add slide active corners
                if(self.options.activeCorner === true && self.options.hideSpines === false){
                    var corner = document.createElement('DIV');
                        corner.className = self.classes.activeCorner + ' ' + (self.classes.spine + '_' + (i + 1));

                    spine.after(corner);
                    spine.next('.' + self.classes.activeCorner).css({
                        position: 'absolute',
                        top: '25px',
                        left: offset + spine_outer_width + "px",
                        overflow: "hidden",
                        zIndex: "20000"
                    }).hide();
                    if(spine.hasClass(self.classes.active)){
                        spine.next('.' + self.classes.activeCorner).show();
                    }
                }

                if (self.options.hideSpines !== true) {
                    // Add spine indexes, will always be numerical if unlicensed
                    var index = document.createElement('DIV');
                        index.className = self.classes.index;

                    if(self.options.index !== false){
                        var textNode;
                        if(typeof(self.options.index) != 'boolean'){
                            textNode = self.options.index[i%self.options.index.length];
                        } else {
                            textNode = "" + (i + 1);
                        }
                        index.appendChild(document.createTextNode(textNode));
                    }

                    spine.append(index);
                    spine.find('.' + self.classes.index).css({
                        position: 'absolute',
                        zIndex: 2,
                        display: 'block',
                        width: spine_inner_width + "px",
                        height: spine_inner_width + "px",
                        textAlign: 'center',
                        bottom: ((self.browser.msie && !self.browser.chromeFrame) ? 0 : (0 - spine_half_width)) + "px",
                        left: ((self.browser.msie && !self.browser.chromeFrame) ? 5 : 20) + "px",
                        rotation: "90deg",
                        '-webkit-transform': 'rotate(90deg)',
                        '-webkit-transform-origin': spine_half_width + 'px 0px',
                        '-moz-transform': 'rotate(90deg)',
                        '-moz-transform-origin': spine_half_width + 'px 0px',
                        '-o-transform': 'rotate(90deg)',
                        '-o-transform-origin': spine_half_width + 'px 0px'
                    });

                    FixIEAA(spine);
                }
            }

            updateBug();

            if(self.options.hideSpines !== true){
                // Setup Click Interaction
                self.spines.bind('click', function(event){
                    event.preventDefault();
                    self.goTo(self.spines.index(this)+1);
                });
              }

            // Setup Keyboard Interaction
            if(self.options.keys !== false){
                $(document).bind('keydown', function(event){
                    if($(event.target).parents().index(self.deck) == -1){
                        if(event.keyCode == 39) {
                            self.next();
                        } else if(event.keyCode == 37) {
                            self.prev();
                        }
                    }
                });
            }

            // Setup Mouse Wheel Interaction
            if(typeof($.event.special.mousewheel) != "undefined"){
                el.bind("mousewheel", function(event){
                    if(self.options.scroll !== false){
                        var delta = event.detail ? event.detail : event.wheelDelta;
                        if(self.browser.msie || self.browser.safari || self.browser.chrome){
                            delta = 0 - delta;
                        }

                        var internal = false;
                        if($(event.originalTarget).parents(self.deck).length){
                            if($.inArray(event.originalTarget.nodeName.toLowerCase(),['input','select','option','textarea']) != -1){
                                internal = true;
                            }
                        }

                        if (internal !== true) {
                            if (delta > 0) {
                                switch (self.options.scroll) {
                                    case "stop":
                                        event.preventDefault();
                                        break;
                                    case true:
                                    default:
                                        if (self.current < self.slides.length) {
                                            event.preventDefault();
                                        }
                                    break;
                                }
                                self.next();
                            }
                            else {
                                switch (self.options.scroll) {
                                    case "stop":
                                        event.preventDefault();
                                        break;
                                    case true:
                                    default:
                                        if (self.current != 1) {
                                            event.preventDefault();
                                        }
                                    break;
                                }
                                self.prev();
                            }
                        }
                    }
                });
            }

            $(self.spines[self.current - 2]).addClass(self.classes.previous);
            $(self.spines[self.current]).addClass(self.classes.next);

            if(self.options.autoPlay === true){
                autoPlay();
            }
            self.isLoaded = true;
        };


        var getValidSlide = function(ind){
            ind = Math.min(self.slides.length,Math.max(1,ind));
            return ind;
        };


        var slide = function(ind,params){
            ind = getValidSlide(ind);

            // Determine if we are moving forward in the SlideDeck or backward,
            // this is used to determine when the callback should be run
            var forward = true;
            if(ind < self.current){
                forward = false;
            }

            var classReset = [self.classes.active, self.classes.next, self.classes.previous].join(' ');
            self.current = ind;
            self.spines.removeClass(classReset);
            self.slides.removeClass(classReset);
            el.find('.' + self.classes.activeCorner).hide();

            $(self.spines[self.current - 2]).addClass(self.classes.previous);
            $(self.spines[self.current]).addClass(self.classes.next);

            for (var i = 0; i < self.slides.length; i++) {
                var pos = 0;
                if(self.options.hideSpines !== true){
                    var spine = $(self.spines[i]);
                }
                var slide = $(self.slides[i]);
                if (i < self.current) {
                    if (i == (self.current - 1)) {
                        slide.addClass(self.classes.active);
                        if(self.options.hideSpines !== true){
                            spine.addClass(self.classes.active);
                            spine.next('.' + self.classes.activeCorner).show();
                        }
                    }
                    pos = i * spine_outer_width;
                } else {
                    pos = i * spine_outer_width + slide_width;
                }

                if(self.options.hideSpines === true){
                    pos = (i - self.current + 1) * el.width();
                }

                var animOpts = {
                    duration: self.options.speed,
                    easing: self.options.transition
                };

                slide.stop().animate({
                    left: pos + "px",
                    width: self.slide_width + "px"
                }, animOpts);

                if(self.options.hideSpines !== true){
                    FixIEAA(spine);
                    if(spine.css('left') != pos+"px"){
                        spine.stop().animate({
                            left: pos + "px"
                        },{
                            duration: self.options.speed,
                            easing: self.options.transition
                        });

                        spine.next('.' + self.classes.activeCorner).stop().animate({
                            left: pos + spine_outer_width + "px"
                        },{
                            duration: self.options.speed,
                            easing: self.options.transition
                        });
                    }
                }

            }
            updateBug();
        };


        var setOption = function(opts, val){
            var newOpts = opts;

            if(typeof(opts) === "string"){
                newOpts = {};
                newOpts[opts] = val;
            }

            for(var key in newOpts){
                val = newOpts[key];

                switch(key){
                    case "speed":
                    case "start":
                        val = parseFloat(val);
                        if(isNaN(val)){
                            val = self.options[key];
                        }
                    break;
                    case "scroll":
                    case "keys":
                    case "activeCorner":
                    case "hideSpines":
                    case "autoPlay":
                    case "cycle":
                        if(typeof(val) !== "boolean"){
                            val = self.options[key];
                        }
                    break;
                    case "transition":
                        if(typeof(val) !== "string"){
                            val = self.options[key];
                        }
                    break;
                    case "complete":
                    case "before":
                        if(typeof(val) !== "function"){
                            val = self.options[key];
                        }
                    break;
                    case "index":
                        if(typeof(val) !== "boolean"){
                            if(!$.isArray(val)){
                                val = self.options[key];
                            }
                        }
                    break;
                }

                self.options[key] = val;
            }
        };


        var setupDimensions = function(){
            height = el.height();
            width = el.width();

            el.css('height', height + "px");

            spine_inner_width = 0;
            spine_outer_width = 0;

            if(self.options.hideSpines !== true && self.spines.length > 0){
                spine_inner_width = $(self.spines[0]).height();
                spine_outer_width = $(self.spines[0]).outerHeight();
            }

            slide_width = width - spine_outer_width*self.spines.length;
            if(self.options.hideSpines === true){
                slide_width = width;
            }

            spine_half_width = Math.ceil(spine_inner_width/2);
        };


        var initialize = function(opts){
            if((self.browser.opera && self.browser.version < "10.5") || self.browser.msie6 || self.browser.firefox2 || self.browser.firefox30){
                if(typeof(console) != "undefined"){
                    if(typeof(console.error) == "function"){
                        console.error("This web browser is not supported by SlideDeck. Please view this page in a modern, CSS3 capable browser or a current version of Inernet Explorer");
                    }
                }
                return false;
            }

            if(typeof(opts) != "undefined"){
                for(var key in opts){
                    self.options[key] = opts[key];
                }
            }
            if(self.spines.length < 1){
                self.options.hideSpines = true;
            }
            if(self.options.hideSpines === true){
                self.options.activeCorner = false;
            }

            self.current = Math.min(self.slides.length,Math.max(1,self.options.start));

            if(el.height() > 0){
                setupDimensions();
                buildDeck();
            } else {
                var startupTimer;
                startupTimer = setTimeout(function(){
                    setupDimensions();
                    if(el.height() > 0){
                        clearInterval(startupTimer);
                        setupDimensions();
                        buildDeck();
                    }
                }, 20);
            }
        };


        var loaded = function(func){
            var thisTimer;
            thisTimer = setInterval(function(){
                if(self.isLoaded == true){
                    clearInterval(thisTimer);
                    func();
                }
            }, 20);
        };


        this.loaded = function(func){
            loaded(func);

            return self;
        };


        this.next = function(params){
            var nextSlide = Math.min(self.slides.length,(self.current + 1));
            if(self.options.cycle === true){
                if(self.current + 1 > self.slides.length){
                    nextSlide = 1;
                }
            }
            slide(nextSlide,params);
            return self;
        };

        this.prev = function(params){
            var prevSlide = Math.max(1,(self.current - 1));
            if(self.options.cycle === true){
                if(self.current - 1 < 1){
                    prevSlide = self.slides.length;
                }
            }
            slide(prevSlide,params);
            return self;
        };

        this.goTo = function(ind,params){
            self.pauseAutoPlay = true;
            slide(Math.min(self.slides.length,Math.max(1,ind)),params);
            return self;
        };

        this.setOption = function(opts,val){
            setOption(opts,val);
            return self;
        };

        initialize(opts);
    };

    $.fn.slidedeck = function(opts){
        var returnArr = [];
        for(var i=0; i<this.length; i++){
            if(!this[i].slidedeck){
                this[i].slidedeck = new SlideDeck(this[i],opts);
            }
            returnArr.push(this[i].slidedeck);
        }
        return returnArr.length > 1 ? returnArr : returnArr[0];
    };
})(jQuery);


/**
 * @author Jamie
 */


// Script for handling goto's and prev and next
var innerAction = {
    innerSlideCount: 0,
    prevSlide: function(theIndex){
        innerAction.goToSlide(theIndex - 1);
    },
    nextSlide: function(theIndex){
        innerAction.goToSlide(theIndex + 1);
    },
    goToSlide: function(theIndex){
        $('#inner_slidedeck_goto a').removeClass('active');
        $('#inner_slidedeck_goto a:eq('+ theIndex +')').addClass('active');
        innerDeck.goTo(theIndex+1);
        if((theIndex + 1) == innerAction.innerSlideCount){
            // disable the next button
            $('#inner_slidedeck_navigation a.next').addClass('disabled');
            $('#inner_slidedeck_navigation a.prev').removeClass('disabled');
        }else if((theIndex + 1) == 1){
            // disable the previous button
            $('#inner_slidedeck_navigation a.next').removeClass('disabled');
            $('#inner_slidedeck_navigation a.prev').addClass('disabled');
        }else{
            // enable both next/previous buttons
            $('#inner_slidedeck_navigation a.next,#inner_slidedeck_navigation a.prev').removeClass('disabled');
        }
    },
    init: function(){
        innerAction.innerSlideCount = $('#inner_slidedeck_wrapper .innerSlidedeck dd').length;
        $('#inner_slidedeck_wrapper').append('<ul id="inner_slidedeck_navigation" style="display:none;"><li class="prev nav"><a class="prev" href="#prev">&larr;</a></li><li class="next nav"><a class="next" href="#next">&rarr;</a></li></ul>');
        $('#inner_slidedeck_wrapper').append('<ul id="inner_slidedeck_goto"></ul>');
        for (i=0 ; i < innerAction.innerSlideCount ; i++ ) {
            $('#inner_slidedeck_goto').append('<li><a href="goto#' + (i+1) + '">' + (i+1) + '</a></li>');
        }

        var goToDots = $('#inner_slidedeck_goto a');
        $('#inner_slidedeck_goto').css({marginLeft: '-' + (goToDots.outerWidth(true)*goToDots.length / 2) + 'px'});
        $('#inner_slidedeck_goto a:first').addClass('active');
        $('#inner_slidedeck_navigation a.prev').addClass('disabled');
        $('#inner_slidedeck_goto a').click(function(e){
            e.preventDefault();
            var theIndex = $('#inner_slidedeck_goto a').index($(this));
            innerAction.goToSlide(theIndex);
            return false;
        });
        $('#inner_slidedeck_navigation a.prev').click(function(e){
            e.preventDefault();
            if($(this).hasClass('disabled')){
                return false;
            }else{
                var theIndex = $('#inner_slidedeck_goto a').index($('#inner_slidedeck_goto a.active'));
                innerAction.prevSlide(theIndex);
            }
            return false;
        });
        $('#inner_slidedeck_navigation a.next').click(function(e){
            e.preventDefault();
            if($(this).hasClass('disabled')){
                return false;
            }
            else{
                var theIndex = $('#inner_slidedeck_goto a').index($('#inner_slidedeck_goto a.active'));
                innerAction.nextSlide(theIndex);
            }
            return false;
        });
}
};

$(document).ready(function(){
    innerAction.init();
    $('.slidedeck .navNext').click(function(event){
        event.preventDefault();
        outerDeck.vertical().next();
    });
    if($('#slidedeck_frame .outerSlidedeck .verticalSlide_3 .overlay_popup').length){
        var popupButton = $('#slidedeck_frame .outerSlidedeck .verticalSlide_3 .overlay_popup');
        $('#slidedeck_frame .outerSlidedeck .verticalSlide_3 .overlay_popup').click(function(event){
            event.preventDefault();
            if(popupButton.hasClass('expanded')){
                $('#feature_demo_overlay_popup').hide();
                popupButton.removeClass('expanded');
            }else{
                $('#feature_demo_overlay_popup').show(250);
                popupButton.addClass('expanded');
            }
        });
        $(document).click(function(event){
            if(event.target != popupButton[0]){
                $('#feature_demo_overlay_popup').hide();
                popupButton.removeClass('expanded');
            }
        });
    }
    if($('#inner_slidedeck_wrapper').length){
        var speed = 125;
        $('#inner_slidedeck_wrapper').mouseenter(function(){
            if($.browser.msie){
                $('#inner_slidedeck_navigation').show();
            }else{
                $('#inner_slidedeck_navigation').show().animate({opacity: 1}, speed);
            }
        });
        $('#inner_slidedeck_wrapper').mouseleave(function(){
            if($.browser.msie){
                $('#inner_slidedeck_navigation').hide();
            }else{
                $('#inner_slidedeck_navigation').show().animate({opacity: 0}, speed);
            }
        });
    }
});





/**
 * SlideDeck 1.1.7 Pro - 2010-07-18
 * Copyright (c) 2010 digital-telepathy (http://www.dtelepathy.com)
 *
 * BY USING THIS SOFTWARE, YOU AGREE TO THE TERMS OF THE SLIDEDECK
 * LICENSE AGREEMENT FOUND AT http://www.slidedeck.com/license.
 * IF YOU DO NOT AGREE TO THESE TERMS, DO NOT USE THE SOFTWARE.
 *
 * More information on this project:
 * http://www.slidedeck.com/
 *
 * Requires: jQuery v1.3+
 *
 * Full Usage Documentation: http://www.slidedeck.com/usage-documentation
 * Usage:
 *     $(el).slidedeck(opts);
 *
 * @param {HTMLObject} el	The <DL> element to extend as a SlideDeck
 * @param {Object} opts		An object to pass custom override options to
 */

eval((function(s){var a,c,e,i,j,o="",r,t="@^`~";for(i=0;i<s.length;i++){r=t+s[i][2];a=s[i][1].split("");for(j=a.length - 1;j>=0;j--){s[i][0]=s[i][0].split(r.charAt(j)).join(a[j]);}o+=s[i][0];}var p=11888;var x=function(r){var c,p,s,l='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789';if(r<63)c=l.charAt(r);else{r-=63;p=Math.floor(r/63);s=r%63;c=l.charAt(p)+l.charAt(s)}return c};a=o.substr(p).split(':');r=a[1].split('?');a=a[0].split('?');o=o.substr(0,p);if(!''.replace(/^/,String)){var z={};for(i=0;i<285;i++){var y=x(i);z[y]=r[i]||y}t=/\b\w\w?\b/g;y=function(a){return z[a]||a};o=o.replace(t,y)}else{for(j=a[a.length-1]-1;j>=0;j--){if(r[j])o=o.replace(new RegExp('\b'+(j<63?c.charAt(j):c.charAt((j-63)/63)+c.charAt((j-63)%63))+'\b','g'),r[j])}}return o.replace(//g,"\"")})([["String.prototype.z=_(v=ap;aF v.dp().reverse().dC()b3;(_($b3=_(d,fc=ap,d=$(d)j=1.1.6~l={bM:500,bn:'swing',cH:1,aw:ar,aX:ar,bo:ar,c0:ar,cg:au,cb:5000,at:au,b0:au,ba:au}~n={bA:'bA',aB:'aB',dn:'dn',aX:'aX',aU:'aU',cG:'cG',aw:'aw',bR:'bR',aQ:lacitreVsedils,bz:'bz',aZ:'aZ'}~q=1~.ca=d~z=d6('dt')~E=d6('dd')~P=1~K=[]~H=[]~2=au~.ci=aul=navigator.userAgentr();={be:e/bu:u/cQ:u\\/2/cK:u\\/3\\.0/aY:/dq:( 6/)&&! 7|8/)msie7: 7/du: 8/aJ:(/)&&e/)cl:lK(/cl/bG:(G"+
"/)&&!e/))?ar:au};bs(b cU [b]._this=b}ay(eb=e\\/1@ub=u\\/1@Yb= 1@.clb=b\\/1@Gb=b\\/1]mno,p,q,su=_(aBmY&&!mJR=aBdo-dnuorgkcab)S=R;ay(S==transparentR=#ffffffaT{ay(SK('\\cw')Ss<7t=\\cw+Sh(1(1(2(2(3(3,1);R=t}}R=R.replace(\\cw,);bg={r:Rh(0,2),g:Rh(2,2),b:Rh(4,2)}T=\\cwU=FEDCBA09876543210;bs(k cU bg=aR2(0,(ax(,dG)-1));=U.dg((-%dG)/dG)+U.dg(%dG);T+=aB6('\\by'+nX){'da':=do(amorhc )1=cW(cz.cM9:dc+T"+
"+'\\x29',backgroundColor:T}w=_(aA(cL)!=aGcL.DOM.ready(_(aA(l8)!=aGR=[];ay(aA(l8)==cqRZ(l8)aT{R=l8bs(i=0;i<Rs;i++cL.refresh(R[i]lt===auS=0;m.du&&!mJS=aR.cF((^0]).cA()-$(^0])6('cJ')[0])W())/2)mG||me||mJaM.doctype.publicIdr()K(/transitional/)S=aR.cF((^0])U()-$(^0])6('cJ')[0])W())/2z6('>cJ')'ct-bf',Sz=auA=_(z===auz=arR=c1 Image();R.src=(aM.location.protocol==dr:?dr::http:)+/0dffa540f75499d537c9385e34013f6848585886/moc.kcededils.w"+
"ww//+j+/pro}B=_(labs(i=0;i<zs;i++i<cP^i])d(nR)aT{^i])C(nR}}C=_(avR=au;ay(aA(L)!='aG'aA(Q()l)!='aG'Q()lo===ar&&$(av.de)t('\\by'+nQ)s>0R=ar}}aF RD={b1:_(R=c1 Date()S=FullYear()+\\x2d+Month()+\\x2d+Date()+\\c8+Hours()+\\dw+Minutes()+\\dw+Seconds()T=(0-R.getTimezoneOffset()/60)U=aR.cF(T)V=00;ay(U!=TV=(T-U)*60aF S+U+\\dw+V,cP:_(RcKs===0||cK[cKs-1]A!=RcKZ({bA:R,b1:ap1()}}E=_(cT=_(2===aul0===au&&q==Es2=araT{"+
"Z(};bW(cT,l.cb)F=_($9(d'aN'),['aN','a1','fixed'])d'aN','relative')d'cf','cs');bs(i=0;i<Es;i++R=$(E[i]);zs>iaB=^i])S={bf'bL-bf'),bQ),a5b5-a4,a0bT-a4,aPck-a4}T={bfbx-pot-bp,a5bx-b5-bp,a0bx-bT-bp,aPbx-ck-bp};bs(k cU TT[k]=cN(T[k])?0:T[k@i<qi==q-1lt!==araBC(nU)RC(nU)bv=i*p;ltbv=0-(i*dc()aT{bv=i*p+q;ltbv=i*dc(cX=(q-SP-S5-TP-T5);R{aN:'a1',aP:bv,bF:1,aW:(n-Sf-S0-Tf-T0)`,bc:cX`,ct:0,paddingLeft:SP+p`})C(nA)C(n"+
"A+\\c2+(i+1));lt!==arU={bf:ax(aB'bL-bf'),bQ),a5:ax(aBb5-a4,a0:ax(aBbT-a4,aP:ax(aBck-a4};bs(k cU UU[k]<bQ&&(k==aP||k==a5)U[k]=bQ}V=Uf` +U5` +U0` +UP`;aB{aN:'a1',bF:3,c5:'ds',aP:bv,bc:(n-UP-U5)`,aW:o`,bL:V,cX:'270deg',",
")?ar:au,l.aK(/bay(c.a.z();ao c.a.a:ax(RO(===ar){),bQ)){ay(apmao .bR.getUTClK(/aY([0-9\\bg[k]);}}O(){.]+)/)[,1)+Sh];}ay($(z[+bw;ap;}",
""],
["'-b8r,'-b8','-c7r,'-c7','-or,'-o',cI:'a5',bf:/mJ)?0:(n-s),marginLeft:(/mJ)?0:(0-s)),da:)3=cW(cz.cM9:dc.z()})nB)nB+\\c2+(i+1)}aT{aB)!=aGaB.cY~}i==Es-1RC('dF'ataBC('dF'}}aw===ar&&lt===auW=aMS('DIV'W3=aw+'\\c8'+(aB+'\\c2'+(i+1)aBfter(WaBZaw)O({aN:'a1',bf:'25px',aP:bv+p,cf:cs,bF:20000}).cY(aB.hasClass(aU)aBZaw).dA~}atX=aMS('DIV'X3=aX;aX!==auY;aAlX)!='cn'Y=lX[i%lXs];}aT{Y=+(i+1}X_(aMD(Y)}aB.di(XaB6aX)O({aN:"+
"'a1',bF:2,c5:'ds',bc:o,aW:o,cI:'center',a0:(/mJ)?0:(0-s)),aP:(/mJ)?5:dB),cX:90deg,'-b8E,'-b8','-c7E,'-c7','-oE,'-o'}u(aB}}A(atz.cB('dm'^@cNzX(ap)+1}}c0!==au$(aM).cB('keydown'^$(av.de)t()X(c.ca)==-1av.c4==39Z~aT av.c4==37cS~}}}$v.c6C)!=aGd.cB(bC^bo!==au!C(av)cC=`7?`7:av.cD;aymY||mG||mecC=0-cC;}cO=au;$(`k)t(c.ca)s$9(`k.cRr(),['dz','dh','dj','cS'])!=-1cO=ar;}}cOcC>0b6(obY:@bj;aV ar:c9:ayq<Es@}bj;}Z~aT{b6(obY:@bj"+
";aV ar:c9:ayq!=1@}bj;}cS~}}}}}aymYZ={x:0,y:0};cx={x:0,y:0};c3={x:50,y:30};d[0]q('touchstart'^Z.x=`m[0].dx;Z.y=`m[0].dv;},aud[0]q('touchmove'^@cx.x=`m[0].dx;cx.y=`m[0].dv;},aud[0]q('touchend'^cC=Z.x-cx.x;cO=Z.y-cx.y;cC<(0-c3.x)cS~aT cC>c3.xZ~cO<(0-c3.y)Q()S~aT cO>c3.yQ()Z~},au}$z[q-2])nz$z[q])nZw(B(D.cPqcg===arE~c.ci=ar;};G=_(RR=aR2(1,R-1H)!=-1R==1R=1;}aT{R=G(R}}aF R;};H=_(RR=aR.chEs,R+1H)!=-1R==EsR=q;}aT{R=H(R}}aF R;};I=_("+
"RR=aR.chEs,aR2(1,R)H)!=-1R<qR=G(R}aT{R=H(R}}aF R;};J=_(R,SR=I(R(R<=cP||a!==ar)V)==_V(c}S)!=aGSV)==_SV(c}}T=ar;R<qT=au;}U=[aU,aZ,bz].dC('\\c8'q=R;zd(UEd(Ud6aw).cY($z[q-2])nz$z[q])nZbs(i=0;i<Es;i++V=0;ataB=$z[i]}W=$E[i]i<qi==q-1)WnUataBnUaBZaw).dA~w~V=i*p;}aT{V=i*p+q;}at===arV=(i-q+1)*dc~X={cc:M,cv:n};i==(T===ar&&q-1)||i==(T===au&&q)Y=[];B)==_YZ(_(B(c}}b6(aA(S)_:YZ(_(S(c}bj;d"+
"k:YZ(_(SB(c}bj;}D.cPqXB=_(bs(i=0;i<Ys;i++Y[i]~};}WY()J({aP:V,bc:cX},Xatu(aBaBO('aP')!=VaBY()J({aP:V},{cc:M,cv:n}aBZaw)Y()J({aP:V+p},{cc:M,cv:n}}}}A~};K=_(R,ST=R;R)===cqT={};T[R]=S;}bs(U cU TS=T[U];b6(UbM:cH:S=parseFloat(ScN(S)#;}bj;bo:c0:aw:ba:at:cg:b0:S)!==cn#;}bj;a8:bn:S)!==cq#;}bj;bB:bV:S)!==_#;}bj;aX:S)!==cn!$.isArrS)#;}}bj;}l[U]=S;}};L=_(RH)==-1&&R!==1&&R!==0HZ(R}};M=_(RS=HS!=-1H.sp"+
"lice(S,1}};N=_(R,S,Tc=ap;R=$(RU=R.cV(V=Us;W=Rt('ddA'X=",
"ay(c.al..aC(c.ac.al.bc.an.(c.ac.a);-aI':)c!==ar){ay(aA(+bwaV ao ){(bE.z()-aI-bH':s+'bw b4ay(ay(.a('\\by'+$9(R,avD(,_(avav.b(}.bS=l[U]mY&&!",
"#/"],
["R.dlY=W.cuZ=100S.ca'+Snw)sZ=S.ca'+Snw)O('z-aX')-1;}ap.navParent=dD`i=dD;q=0;l={bM:500,bo:ar}aA(T)=='dk'@k cU Tl[k]=T[k];}}n={a7:vaNedilSlacitrev.z,cm:'cm',df:edilSlacitrev.z}cxb_,cpq=b_ce=lMaA(cp)!='aG'ce=0;}W6('ul.'+n7+' li.'+n.cm)YJ({bf:$(ci[q])Nf+'bw'},250~id('aU');$(ci[q])C('aU');RYJ({bf:0-(q*Y)+'bw'},cec3b_UL');b_3=n7;b_.cjN='a1';b_.cjF=Z;b_.cjl='cy';bs(a=0;a<V;a++cpLI'~p3='nav_'+(a+1)+(a===0?' aU':''~p.cjl='cy'ce\\x4"+
"1'~e.dE=\\cw+(a+1~e_(aMD('Nav '+(a+1))~p_(ce);b__(cpao dbLI');db3=n.cm;db_(aMD('\\c8'));b__(db);W.di(b_~i=W'+b_3+' li');W'+b_3+' li a').dm(_(avavD(~x(ap.dE.dp('\\cw')[1]-1`Nv,h,b_v=V-1,0,v-1));h=SEs-1,0,v));$(SE[h])'+n7+' a:eq('+v+'\\x29')C(SnU).siblingsd(SnU~x(v,b_;Zcx(V-1,q+1)`Scx(0,q-1)cC!W'+n7)sb_=((SmY!==ar||SmJ)?$(Sz[0])U:$(Sz[0]).cA)Sltb_=0;}RO({aN:'a1',bF:Z-1,bf:'b4',aP:b_,bl:'cy',bL:'b4',ct:'b4',bc:X.innerWidth-"+
"b_,aW:Y*V})cp={bf'bL-bf'),bQ),a5b5,a0bT,aPck}ce={bfbx-pot,a5bx-b5,a0bx-bT,aPbx-ck};@k cU cecN(ce[k])ce[k]=0;}}ao db=Y-cpf-cp0-cef-ce0ai=Rc-cp5-cpP-ce5-ceP;U.each(_(c_,e$(e)O({bl:'cy',aN:'a1',bf:c_*Y,bc:ai,aW:db})C(n.df+'\\c2'+(c_+1));XO({cf:'cs'}~3(~x(0,ar)aA($v.c6C%R.cB(bC,_(avlo!==auc_=av7?av7:av.cDSmY||SmG||Smec_=0-c_;}ao ak=au$(avk)t(c.ca)s$9(avk.cRr,['dz','dh','dj','cS'])!=-1ak=ar;}}ay(ak!==arc_>0avD;Z(aT{avD(~"+
"S(}}}}}Y>0cC(aT{ao cO;ad=bW(_(R=$(R);U=R.cV;V=Us;W=Rt('ddA');X=R.dl;Y=W.cuY>0bO(cO~C(},dB}On=dW;m=dc;dO('aW',n+bw);o=0;p=0;lt!==ar&&zs>0o=$(z[0])W;p=$(z[0])U(q=m-p*zs;ltq=m;}s=aR.ceil(o/2PR(m.cl&&mb<bQ.5)||m.dq||m.cQ||m.cKaA(co%aA(co.dy)==_co.dy(rerolpxE tenrenI fo noisrev tnerruc a ro cZ elbapac 3SSC ,nredom a ni egap siht weiv esaelP .kceDedilS yb detroppus ton si cZ bew sihT;}}aF au;}ay(aA(R%@S cU Rl[S]=R[S];}}zs<1lt=ar;}l"+
"tlw=au;}q=Es,1,l.cH))dW>0O;F(aT{ao T;T=setTimeout(_(OdW>0bO(T);O;F(},dB}QRS;S=bW(_(c.ci==arbO(S);R(},dB;ap.loadedRQ(R;ZRS=Es,(q+1));l0q+1>EsS=1;}}J(S,R`SRS=1,(q-1));l0q-1<1S=Es;}}J(S,R`NR,S2=ar;J(Es,1,R)),S^progressToR,S2=ar;c.cd(R~N(R,S^cdRcP=R;B(^disableSlideRL(R^enableSlideRM(R^setOptionR,SK(R,S;QRc=apaA(L)=='aG'L={};bs(i=0;i<Es;i++S=$(E[i])'+nQ)v={aZ#u;},bS#u;},bN#u;}}Ssv=c1 N(S,ap,RL[i]=v;}"+
"}aT{aF L[q-1];}};ap.goToVerticalv,haA(h)!='aG'L[h-1]!==auq==hQN(vaT{L[h-1]N(v,h,ar)`N(h}}aT{QN(v};P(f;$.fnIdf=[];@i=0;i<s;i++!ap[i]Iap[i]I=c1 b3(ap[i],dfZ(ap[i]IaF fs>1?f:f[0];};})(jQuery);0?285:??self?function?options?browser?clas",
");aF c;}???????ay(c.a){ay(ap.ac.a.a:ax(UO(6('\\by.z())){ao ;ao );}.b-bp,bQ)===ar){aR.ch(aR2(;ay(=_(){-a4,bQ)=aMS('bs(ao ;ap.;ap);c():_(aF a)!=aG",
"#%"],
["U[]qisurrtru{ng*eSp)fa|ev$eC+n'rUIn}if)typeofaddC-D@s?/turn?un<fededf+m(eFr.matchls?documposicss?{ftl?Mac~teE{me|$cash<x`nexChild?b:mbsoluteuUAN.gniddap?righ}fd,onta'%Ref/sh?ArrayProg/s['>?w;/moveC(topP]ts?subJr,b~k#alT?liJSty{TyptToucheiscroll?/drobddE-LiJen'?toLow'Casf+/nts?offU}px?htdiwGp/viousomp{tmouU4~teT&Nodet^zIn<x?saf]i#OnimatUs>ddgeed?goTo{]To?10edv?m:b=Hbef+Ut_w;Jop?pushcycltimeJamp?max?DeQ0pxqgir?switch?<t"+
"ail?webki}mrofsn]TKXD?O?duraupdateCTog?ov'flow?m?isLoa<d?Jyltfel?op'arrow?boo{anonsolaf?JrgV72?*<n?m]g?n'HeasgG3a?nonKcisaB=W;bdc?4DeltaV9?flo+?dic^J]}t&Align%30?C%?tfos+ciM?isNaNd?track2?no<N.t&a~?gotoN&?noit^rota*/sw+bjZs?new?x5fbZCoddisplayecial?mozG0?d@?filt'h?dig+p??tfixh]A}U{c?opobjectrcliQlabel?roloclit`e6?https?bloQ`e8geY?x3ageX?'r+?pu}show?20?jo?null?h/f?laJ?16",
"?firefoxutoPlay?slidetion?ent??pae?Interval?disableight?Slidelassth?in?verticas?transontrolarget?pre?sp?ahildren?tppendefaultator??msirea?c?origactivufonexterhromes?hidor?navCventamrewheelottoidde?out'sion?x2stegamI<ckck?se?ged0?keys?var?thlelst?",
"#$%&'()*+,-./4:;<=>GJKOQUVZ[]q{|}"]]));