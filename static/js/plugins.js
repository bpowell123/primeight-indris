
// remap jQuery to $
(function($){

//onLoad
$(document).ready(doSomething);

//resize image bar
function doSomething() {
   $(".kwick", this).animate({ "width": ($("#kwick").width()/5) }, 200);
   //$(".tags").multiSelect();
   //get_location();
};

var resizeTimer;
$(window).resize(function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(doSomething, 100);
});

//fluid16 functions
var fluid = {
Ajax : function(){
	$("#loading").hide();
	var content = $("#ajax-content").hide();
	$("#toggle-ajax").bind("click", function(e) {
        if ( $(this).is(".hidden") ) {
            $("#ajax-content").empty();

            $("#loading").show();
            $("#ajax-content").load("/static/data/ajax-response.html", function() {
            	$("#loading").hide();
            	content.slideDown();
            });
        }
        else {
            content.slideUp();
        }
        if ($(this).hasClass('hidden')){
            $(this).removeClass('hidden').addClass('visible');
        }
        else {
            $(this).removeClass('visible').addClass('hidden');
        }
        e.preventDefault();
    });
},
Toggle : function(){
	var default_hide = {"grid": true };
	$.each(
		["grid", "paragraphs", "blockquote", "list-items", "section-menu", "tables", "forms", "login-forms", "search", "articles", "accordion", "videos", "whitlist", "whitlistDetail", "yahoopipes", "facebook"],
		function() {
			var el = $("#" + (this == 'accordon' ? 'accordion-block' : this) );
			if (default_hide[this]) {
				el.hide();
				$("[id='toggle-"+this+"']").addClass("hidden")
			}
			$("[id='toggle-"+this+"']")
			.bind("click", function(e) {
				if ($(this).hasClass('hidden')){
					$(this).removeClass('hidden').addClass('visible');
					el.slideDown();
				} else {
					$(this).removeClass('visible').addClass('hidden');
					el.slideUp();
				}
				e.preventDefault();
			});
		}
	);
},
Kwicks : function(){
	var animating = false;
    $("#kwick .kwick")
        .bind("mouseenter", function(e) {
            if (animating) return false;
            animating == true;
            $("#kwick .kwick").not(this).animate({ "width": (($("#kwick").width() - 485)/4) }, 200);
            $(this).animate({ "width": 485 }, 200, function() {
                animating = false;
            });
        });
    $("#kwick").bind("mouseleave", function(e) {
        $(".kwick", this).animate({ "width": ($("#kwick").width()/5) }, 200);
    });
},
SectionMenu : function(){
	$("#section-menu")
        .accordion({
            "header": "a.menuitem"
        })
        .bind("accordionchangestart", function(e, data) {
            data.newHeader.next().andSelf().addClass("current");
            data.oldHeader.next().andSelf().removeClass("current");
        })
        .find("a.menuitem:first").addClass("current")
        .next().addClass("current");
},
Accordion: function(){
	$("#accordion").accordion({
        'header': "h3.atStart"
    }).bind("accordionchangestart", function(e, data) {
        data.newHeader.css({
            "font-weight": "bold",
            "background": "#fff"
        });

        data.oldHeader.css({
            "font-weight": "normal",
            "background": "#eee"
        });
    }).find("h3.atStart:first").css({
        "font-weight": "bold",
        "background": "#fff"
    });
}
}
jQuery(function ($) {
	if($("#accordion").length){fluid.Accordion();}
	if($("[id$='ajax']").length){fluid.Ajax();}
	if($("[id^='toggle']").length){fluid.Toggle();}
	if($("#kwick .kwick").length){fluid.Kwicks();}
	if($("#section-menu").length){fluid.SectionMenu();}
});

//List Right Pane Slide



//feedback slider
$(function(){
    $('.slide-out-div').tabSlideOut({
        tabHandle: '.handle',                           //class of the element that will become your tab
        pathToTabImage: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAB6CAMAAAD6ZuGjAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAADNQTFRF/4UA/////+HA/6RA/8KA//jw/5ww/5Qg/40Q/9Kg//Dg/+nQ/6tQ/7Ng/9mw/7tw/8qQkreX7QAAAoBJREFUeNrsV9mO5DAIDL6vxPn/rx3ASVrb0gCrae3LLA/uSKlOYlxUwbb9jz9jiHfP8lyBCHR1/RYHChAm/aQOEEXgAYDfNiJATyKwRIgpAMBRlL0mRCIu6FnZERaHJX/44tOW6cob+j48vMWPgTm8xcdY4zNmM6mw1MBTilyWcRmPhYEQs5LDGPCU8wngRCDAvi4mQJGTfl9G+gQB2F8U9rYnNhFYHj7gX8RcdiQ4p6lD2zQKHSFg6awqkwnOUdWjpqfBMczcSN4I7LJSbGUs1h6KpBB7rohaBd64obBnlgNGdgofE71wJ0GZMh893eYFaaYCN16cSIrEVOANy3zcuLQ6LTLDqbhOXPrAPGUt4ZcKOaWwa19pd8lEnZkNqOK9BeYdfWDbLVpvKYVEkDDP+GjL93nk3RatXONdpZoAvDSsaWdtE6ntdcJNPut+26VXimtA9JdI7bIhdRapimYc/p0Xfj6Se4sff+N6YkN5ula5DNo6GmyRksLHenthUwQ5PcwsH6LZ69kK8FLkDDLQQStXf6jxEWs/5eHUhu+xha41kOESiqJrFHrXnj/Itlwbim1QZXSPrMpO0ShWs85AOd+U50SuVLos9oVkke0ry/bBDdLyua50Uu0GGlqu21291hYycCgWh7sOBMSRoat5jNBQzWAYfUZ1pNVyOVMflZJRrbwJOBux51AnhQoXzaq66X4i8NQ60obVxydTZZHKZJUMLLJpsl/Z2GOkWSLO3K/2srHXBQzy9EFpdNQ6Tq37KNzjxqhOSDxZc+Ojn/d+oN3MIlkczrans8zLjrJnGZeNwEFNAjqcOruWaO0ARvuLVsFZOwkz0DwX/Yr4EmAAR7UOrwupS6oAAAAASUVORK5CYII=',  //path to the image for the tab //Optionally can be set using css
        imageHeight: '122px',                           //height of tab image           //Optionally can be set using css
        imageWidth: '40px',                             //width of tab image            //Optionally can be set using css
        tabLocation: 'right',                           //side of screen where tab lives, top, right, bottom, or left
        speed: 300,                                     //speed of animation
        action: 'click',                                //options: 'click' or 'hover', action to trigger animation
        topPos: '250px',                                //position from the top/ use if tabLocation is left or right
        leftPos: '20px',                                //position from left/ use if tabLocation is bottom or top
        fixedPosition: true                             //options: true makes it stick(fixed position) on scroll
    });

});

//feedback submit without refresh
  $(function() {
    $('.error').hide();
    $(".button").click(function() {
      // validate and process form here

      $('.error').hide();
  		var msg = $('textarea#msg').val();
  		var email = $("input#email").val();
  		if (email == "") {
            $("label#email_error").show();
            $("input#email").focus();
        return false;

      }
        var dataString = 'email='+ email + '&message=' + msg;
        var response_message = "Thank you for your feedback!";
		  //alert (dataString);return false;
//		  $.ajax({
//          type: "POST",
//          url: "/sendmail/",
//          data: dataString,
//          success: function() {
//          	alert("hi");
//            $('#form-wrap').html("<div id='response-message'></div>");
//            $('#response-message').html("<p>" + response_message +"</p>")
//            .hide()
//          }
//        });

//			$.post("/sendmail/", {
//			        name: "Monty",
//			        food: "Spam"
//			    },
//			    function(data) {
//			        alert(data);
//			    }
//			);
//        return false;

    });
  });

//Geolocation
function get_location() {
  if (Modernizr.geolocation) {
    navigator.geolocation.getCurrentPosition(show_map);
  } else {
    // no native support; maybe try Gears?
  }
}

function show_map(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  var altitude = position.coords.altitude;
  var accuracy = position.coords.accuracy;
  var timestamp = position.timestamp;
  alert("lat: " + latitude + " lon:" + longitude + " alt:" + altitude + " acc:" + accuracy + " time:" + timestamp);
  // let's show a map or do something interesting!
}

//Whit List Sortable
$(document).ready(
	function () {
		$('a.closeEl').bind('click', toggleContent);
		$('input#add').bind('click', addItem);
		$('div.groupWrapper').sortable(
			{
				placeholder: 'ui-state-highlight',
				accept: 'groupItem',
				helperclass: 'sortHelper',
				activeclass : 	'sortableactive',
				hoverclass : 	'sortablehover',
				handle: 'div.itemHeader',
				tolerance: 'pointer',
				onChange : function(ser)
				{
				},
				onStart : function()
				{
					$.iAutoscroller.start(this, document.getElementsByTagName('body'));
				},
				onStop : function()
				{
					$.iAutoscroller.stop();
				}
			}
		);
	}
);
var toggleContent = function(e)
{
	var i = this.id;
	var rightPane = $('div.rightPane', 'div#whitlistDetail');
	var targetContent = $('div#form-wrap' + i, 'div#whitlistDetail');
	if (targetContent.css('display') == 'none') {
		rightPane.hide(300);
		targetContent.slideDown(300);
		if ($(this).html() != 'close X') {
			$(this).html('[-]');
		}
	} else {
		targetContent.hide(300);
		rightPane.slideDown(300);
		if ($(this).html() != 'close X') {
			$(this).html('[+]');
		}
	}
	return false;
};
var addItem = function(e)
{
	/*alert('adding item');*/
	$("body").load("/newitem/");
};
function serialize(s)
{
	serial = $.SortSerialize(s);
	alert(serial.hash);
};

//MultiSelect
	// render the html for a single option
	function renderOption(id, option)
	{
		var html = '<label><input type="checkbox" name="' + id + '[]" value="' + option.value + '"';
		if( option.selected ){
			html += ' checked="checked"';
		}
		html += ' />' + option.text + '</label>';

		return html;
	}

	// render the html for the options/optgroups
	function renderOptions(id, options, o)
	{
		var html = "";

		for(var i = 0; i < options.length; i++) {
			if(options[i].optgroup) {
				html += '<label class="optGroup">';

				if(o.optGroupSelectable) {
					html += '<input type="checkbox" class="optGroup" />' + options[i].optgroup;
				}
				else {
					html += options[i].optgroup;
				}

				html += '</label><div class="optGroupContainer">';

				html += renderOptions(id, options[i].options, o);

				html += '</div>';
			}
			else {
				html += renderOption(id, options[i]);
			}
		}

		return html;
	}

	// Building the actual options
	function buildOptions(options)
	{
		var multiSelect = $(this);
		var multiSelectOptions = multiSelect.next('.multiSelectOptions');
		var o = multiSelect.data("config");
		var callback = multiSelect.data("callback");

		// clear the existing options
		multiSelectOptions.html("");
		var html = "";

		// if we should have a select all option then add it
		if( o.selectAll ) {
			html += '<label class="selectAll"><input type="checkbox" class="selectAll" />' + o.selectAllText + '</label>';
		}

		// generate the html for the new options
		html += renderOptions(multiSelect.attr('id'), options, o);

		multiSelectOptions.html(html);

		// variables needed to account for width changes due to a scrollbar
		var initialWidth = multiSelectOptions.width();
		var hasScrollbar = false;

		// set the height of the dropdown options
		if(multiSelectOptions.height() > o.listHeight) {
			multiSelectOptions.css("height", o.listHeight + 'px');
			hasScrollbar = true;
		} else {
			multiSelectOptions.css("height", '');
		}

		// if the there is a scrollbar and the browser did not already handle adjusting the width (i.e. Firefox) then we will need to manaually add the scrollbar width
		var scrollbarWidth = hasScrollbar && (initialWidth == multiSelectOptions.width()) ? 17 : 0;

		// set the width of the dropdown options
//		if((multiSelectOptions.width() + scrollbarWidth) < multiSelect.outerWidth()) {
//			multiSelectOptions.css("width", multiSelect.outerWidth() - 2/*border*/ + 'px');
//		} else {
//			multiSelectOptions.css("width", (multiSelectOptions.width() + scrollbarWidth) + 'px');
//		}

		// Apply bgiframe if available on IE6
		if( $.fn.bgiframe ) multiSelect.next('.multiSelectOptions').bgiframe( { width: multiSelectOptions.width(), height: multiSelectOptions.height() });

		// Handle selectAll oncheck
		if(o.selectAll) {
			multiSelectOptions.find('INPUT.selectAll').click( function() {
				// update all the child checkboxes
				multiSelectOptions.find('INPUT:checkbox').attr('checked', $(this).attr('checked')).parent("LABEL").toggleClass('checked', $(this).attr('checked'));
			});
		}

		// Handle OptGroup oncheck
		if(o.optGroupSelectable) {
			multiSelectOptions.addClass('optGroupHasCheckboxes');

			multiSelectOptions.find('INPUT.optGroup').click( function() {
				// update all the child checkboxes
				$(this).parent().next().find('INPUT:checkbox').attr('checked', $(this).attr('checked')).parent("LABEL").toggleClass('checked', $(this).attr('checked'));
			});
		}

		// Handle all checkboxes
		multiSelectOptions.find('INPUT:checkbox').click( function() {
			// set the label checked class
			$(this).parent("LABEL").toggleClass('checked', $(this).attr('checked'));

			updateSelected.call(multiSelect);
			multiSelect.focus();
			if($(this).parent().parent().hasClass('optGroupContainer')) {
				updateOptGroup.call(multiSelect, $(this).parent().parent().prev());
			}
			if( callback ) {
				callback($(this));
			}
		});

		// Initial display
		multiSelectOptions.each( function() {
			$(this).find('INPUT:checked').parent().addClass('checked');
		});

		// Initialize selected and select all
		updateSelected.call(multiSelect);

		// Initialize optgroups
		if(o.optGroupSelectable) {
			multiSelectOptions.find('LABEL.optGroup').each( function() {
				updateOptGroup.call(multiSelect, $(this));
			});
		}

		// Handle hovers
		multiSelectOptions.find('LABEL:has(INPUT)').hover( function() {
			$(this).parent().find('LABEL').removeClass('hover');
			$(this).addClass('hover');
		}, function() {
			$(this).parent().find('LABEL').removeClass('hover');
		});

		// Keyboard
		multiSelect.keydown( function(e) {

			var multiSelectOptions = $(this).next('.multiSelectOptions');

			// Is dropdown visible?
			if( multiSelectOptions.css('visibility') != 'hidden' ) {
				// Dropdown is visible
				// Tab
				if( e.keyCode == 9 ) {
					$(this).addClass('focus').trigger('click'); // esc, left, right - hide
					$(this).focus().next(':input').focus();
					return true;
				}

				// ESC, Left, Right
				if( e.keyCode == 27 || e.keyCode == 37 || e.keyCode == 39 ) {
					// Hide dropdown
					$(this).addClass('focus').trigger('click');
				}
				// Down || Up
				if( e.keyCode == 40 || e.keyCode == 38) {
					var allOptions = multiSelectOptions.find('LABEL');
					var oldHoverIndex = allOptions.index(allOptions.filter('.hover'));
					var newHoverIndex = -1;

					// if there is no current highlighted item then highlight the first item
					if(oldHoverIndex < 0) {
						// Default to first item
						multiSelectOptions.find('LABEL:first').addClass('hover');
					}
					// else if we are moving down and there is a next item then move
					else if(e.keyCode == 40 && oldHoverIndex < allOptions.length - 1)
					{
						newHoverIndex = oldHoverIndex + 1;
					}
					// else if we are moving up and there is a prev item then move
					else if(e.keyCode == 38 && oldHoverIndex > 0)
					{
						newHoverIndex = oldHoverIndex - 1;
					}

					if(newHoverIndex >= 0) {
						$(allOptions.get(oldHoverIndex)).removeClass('hover'); // remove the current highlight
						$(allOptions.get(newHoverIndex)).addClass('hover'); // add the new highlight

						// Adjust the viewport if necessary
						adjustViewPort(multiSelectOptions);
					}

					return false;
				}

				// Enter, Space
				if( e.keyCode == 13 || e.keyCode == 32 ) {
					var selectedCheckbox = multiSelectOptions.find('LABEL.hover INPUT:checkbox');

					// Set the checkbox (and label class)
					selectedCheckbox.attr('checked', !selectedCheckbox.attr('checked')).parent("LABEL").toggleClass('checked', selectedCheckbox.attr('checked'));

					// if the checkbox was the select all then set all the checkboxes
					if(selectedCheckbox.hasClass("selectAll")) {
						multiSelectOptions.find('INPUT:checkbox').attr('checked', selectedCheckbox.attr('checked')).parent("LABEL").addClass('checked').toggleClass('checked', selectedCheckbox.attr('checked'));
					}

					updateSelected.call(multiSelect);

					if( callback ) callback($(this));
					return false;
				}

				// Any other standard keyboard character (try and match the first character of an option)
				if( e.keyCode >= 33 && e.keyCode <= 126 ) {
					// find the next matching item after the current hovered item
					var match = multiSelectOptions.find('LABEL:startsWith(' + String.fromCharCode(e.keyCode) + ')');

					var currentHoverIndex = match.index(match.filter('LABEL.hover'));

					// filter the set to any items after the current hovered item
					var afterHoverMatch = match.filter(function (index) {
						return index > currentHoverIndex;
					});

					// if there were no item after the current hovered item then try using the full search results (filtered to the first one)
					match = (afterHoverMatch.length >= 1 ? afterHoverMatch : match).filter("LABEL:first");

					if(match.length == 1) {
						// if we found a match then move the hover
						multiSelectOptions.find('LABEL.hover').removeClass('hover');
						match.addClass('hover');

						adjustViewPort(multiSelectOptions);
					}
				}
			} else {
				// Dropdown is not visible
				if( e.keyCode == 38 || e.keyCode == 40 || e.keyCode == 13 || e.keyCode == 32 ) { //up, down, enter, space - show
					// Show dropdown
					$(this).removeClass('focus').trigger('click');
					multiSelectOptions.find('LABEL:first').addClass('hover');
					return false;
				}
				//  Tab key
				if( e.keyCode == 9 ) {
					// Shift focus to next INPUT element on page
					multiSelectOptions.next(':input').focus();
					return true;
				}
			}
			// Prevent enter key from submitting form
			if( e.keyCode == 13 ) return false;
		});
	}

	// Adjust the viewport if necessary
	function adjustViewPort(multiSelectOptions)
	{
		// check for and move down
		var selectionBottom = multiSelectOptions.find('LABEL.hover').position().top + multiSelectOptions.find('LABEL.hover').outerHeight();

		if(selectionBottom > multiSelectOptions.innerHeight()){
			multiSelectOptions.scrollTop(multiSelectOptions.scrollTop() + selectionBottom - multiSelectOptions.innerHeight());
		}

		// check for and move up
		if(multiSelectOptions.find('LABEL.hover').position().top < 0){
			multiSelectOptions.scrollTop(multiSelectOptions.scrollTop() + multiSelectOptions.find('LABEL.hover').position().top);
		}
	}

	// Update the optgroup checked status
	function updateOptGroup(optGroup)
	{
		var multiSelect = $(this);
		var o = multiSelect.data("config");

		// Determine if the optgroup should be checked
		if(o.optGroupSelectable) {
			var optGroupSelected = true;
			$(optGroup).next().find('INPUT:checkbox').each( function() {
				if( !$(this).attr('checked') ) {
					optGroupSelected = false;
					return false;
				}
			});

			$(optGroup).find('INPUT.optGroup').attr('checked', optGroupSelected).parent("LABEL").toggleClass('checked', optGroupSelected);
		}
	}

	// Update the textbox with the total number of selected items, and determine select all
	function updateSelected() {
		var multiSelect = $(this);
		var multiSelectOptions = multiSelect.next('.multiSelectOptions');
		var o = multiSelect.data("config");

		var i = 0;
		var selectAll = true;
		var display = '';
		multiSelectOptions.find('INPUT:checkbox').not('.selectAll, .optGroup').each( function() {
			if( $(this).attr('checked') ) {
				i++;
				display = display + $(this).parent().text() + ', ';
			}
			else selectAll = false;
		});

		// trim any end comma and surounding whitespace
		display = display.replace(/\s*\,\s*$/,'');

		if( i == 0 ) {
			multiSelect.find("span").html( o.noneSelected );
		} else {
			if( o.oneOrMoreSelected == '*' ) {
				multiSelect.find("span").html( display );
				multiSelect.attr( "title", display );
			} else {
				multiSelect.find("span").html( o.oneOrMoreSelected.replace('%', i) );
			}
		}

		// Determine if Select All should be checked
		if(o.selectAll) {
			multiSelectOptions.find('INPUT.selectAll').attr('checked', selectAll).parent("LABEL").toggleClass('checked', selectAll);
		}
	}

	$.extend($.fn, {
		multiSelect: function(o, callback) {
			// Default options
			if( !o ) o = {};
			if( o.selectAll == undefined ) o.selectAll = true;
			if( o.selectAllText == undefined ) o.selectAllText = "Select All";
			if( o.noneSelected == undefined ) o.noneSelected = 'Select options';
			if( o.oneOrMoreSelected == undefined ) o.oneOrMoreSelected = '% selected';
			if( o.optGroupSelectable == undefined ) o.optGroupSelectable = false;
			if( o.listHeight == undefined ) o.listHeight = 150;

			// Initialize each multiSelect
			$(this).each( function() {
				var select = $(this);
				var html = '<a href="javascript:;" class="multiSelect"><span></span></a>';
				html += '<div class="multiSelectOptions" style="position: absolute; z-index: 99999; visibility: hidden;"></div>';
				$(select).after(html);

				var multiSelect = $(select).next('.multiSelect');
				var multiSelectOptions = multiSelect.next('.multiSelectOptions');

				// if the select object had a width defined then match the new multilsect to it
				multiSelect.find("span").css("width", $(select).width() + 'px');

				// Attach the config options to the multiselect
				multiSelect.data("config", o);

				// Attach the callback to the multiselect
				multiSelect.data("callback", callback);

				// Serialize the select options into json options
				var options = [];
				$(select).children().each( function() {
					if(this.tagName.toUpperCase() == 'OPTGROUP')
					{
						var suboptions = [];
						options.push({ optgroup: $(this).attr('label'), options: suboptions });

						$(this).children('OPTION').each( function() {
							if( $(this).val() != '' ) {
								suboptions.push({ text: $(this).html(), value: $(this).val(), selected: $(this).attr('selected') });
							}
						});
					}
					else if(this.tagName.toUpperCase() == 'OPTION')
					{
						if( $(this).val() != '' ) {
							options.push({ text: $(this).html(), value: $(this).val(), selected: $(this).attr('selected') });
						}
					}
				});

				// Eliminate the original form element
				$(select).remove();

				// Add the id that was on the original select element to the new input
				multiSelect.attr("id", $(select).attr("id"));

				// Build the dropdown options
				buildOptions.call(multiSelect, options);

				// Events
				multiSelect.hover( function() {
					$(this).addClass('hover');
				}, function() {
					$(this).removeClass('hover');
				}).click( function() {
					// Show/hide on click
					if( $(this).hasClass('active') ) {
						$(this).multiSelectOptionsHide();
					} else {
						$(this).multiSelectOptionsShow();
					}
					return false;
				}).focus( function() {
					// So it can be styled with CSS
					$(this).addClass('focus');
				}).blur( function() {
					// So it can be styled with CSS
					$(this).removeClass('focus');
				});

				// Add an event listener to the window to close the multiselect if the user clicks off
				$(document).click( function(event) {
					// If somewhere outside of the multiselect was clicked then hide the multiselect
					if(!($(event.target).parents().andSelf().is('.multiSelectOptions'))){
						multiSelect.multiSelectOptionsHide();
					}
				});
			});
		},

		// Update the dropdown options
		multiSelectOptionsUpdate: function(options) {
			buildOptions.call($(this), options);
		},

		// Hide the dropdown
		multiSelectOptionsHide: function() {
			$(this).removeClass('active').removeClass('hover').next('.multiSelectOptions').css('visibility', 'hidden');
		},

		// Show the dropdown
		multiSelectOptionsShow: function() {
			var multiSelect = $(this);
			var multiSelectOptions = multiSelect.next('.multiSelectOptions');
			var o = multiSelect.data("config");

			// Hide any open option boxes
			$('.multiSelect').multiSelectOptionsHide();
			multiSelectOptions.find('LABEL').removeClass('hover');
			multiSelect.addClass('active').next('.multiSelectOptions').css('visibility', 'visible');
			multiSelect.focus();

			// reset the scroll to the top
			multiSelect.next('.multiSelectOptions').scrollTop(0);

			// Position it
			var offset = multiSelect.position();
			multiSelect.next('.multiSelectOptions').css({ top:  offset.top + $(this).outerHeight() + 'px' });
			multiSelect.next('.multiSelectOptions').css({ left: offset.left + 'px' });
		},

		// get a coma-delimited list of selected values
		selectedValuesString: function() {
			var selectedValues = "";
			$(this).next('.multiSelectOptions').find('INPUT:checkbox:checked').not('.optGroup, .selectAll').each(function() {
				selectedValues += $(this).attr('value') + ",";
			});
			// trim any end comma and surounding whitespace
			return selectedValues.replace(/\s*\,\s*$/,'');
		}
	});

	// add a new ":startsWith" search filter
	$.expr[":"].startsWith = function(el, i, m) {
		var search = m[3];
		if (!search) return false;
		return eval("/^[/s]*" + search + "/i").test($(el).text());
	};

})(window.jQuery);



// usage: log('inside coolFunc',this,arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console){
    console.log( Array.prototype.slice.call(arguments) );
  }
};



// catch all document.write() calls
//(function(doc){
//  var write = doc.write;
//  doc.write = function(q){
//    log('document.write(): ',arguments);
//    if (/docwriteregexwhitelist/.test(q)) write.apply(doc,arguments);
//  };
//})(document);

$(function() {
  $("#sortable").sortable({
	  placeholder: 'ui-state-highlight'
  });
  $("#sortable").disableSelection();
});