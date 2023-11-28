var csvFile = "../static/canvastaynew.csv";
var counter = 0;
var loadingInProgress = false;
var gallery = $('#gallery');
var imagesPerLoad = 3; // define number of images to load per scroll

$(window).on("scroll", function() {
  var scrollHeight = $(document).height();
  var scrollPosition = $(window).height() + $(window).scrollTop();
  if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
    loadImages(imagesPerLoad);
  }
});

$(document).ready(function() {
  var isTouchDevice = 'ontouchstart' in document.documentElement;
  if (isTouchDevice) {
    $('#loading').hide();
  } else {
    $('.wrap-infinite-link').hide();
  }
});

function loadImages(count) {
  // check if images are already being loaded or not, and if count is valid
  if (!loadingInProgress && count > 0) {
    loadingInProgress = true;
    counter++;

    $.get(csvFile, function(data) {
      var lines = data.split('\n');
      for (var i = 1 + (counter-1)*count; i <= count*counter; i++) {
        if (i >= lines.length) {
          // hide loading and infinite scroll link if all images are loaded
          $('#loading').hide();
          $('.wrap-infinite-link').hide();
          break;
        }
        var fields = lines[i].split(',');
        if (fields.length === 3) {
          var songName = fields[2].trim();
          var albumName = fields[1].trim();
          var canvasUrl = fields[0].trim();

          // create div to display song and album names
          var div = $('<div>').addClass('image-info')
                              .append($('<p>').text(songName))
                              .append($('<p>').text(albumName));

          // create video element for canvas image
          var video = $('<video>').attr('width', '320')
                                  .attr('height', '480')
                                  .attr('autoplay', 'true')
                                  .attr('loop', 'true')
                                  .attr('muted', 'true')
                                  .append($('<source>').attr('src', canvasUrl)
                                                       .attr('type', 'video/mp4'));

          // append image div and video to gallery
          gallery.append(div);
          gallery.append(video);
        }
      }
      loadingInProgress = false;
    });
  }
}

$(window).scroll(function() {
  // fade in "back to top" button when scrolling down
  var height = $(window).scrollTop();
  if (height > 100) {
    $('#back2Top').fadeIn();
  } else {
    $('#back2Top').fadeOut();
  }
});

$(document).ready(function() {
  // add smooth scrolling to "back to top" button
  $("#back2Top").click(function(event) {
    event.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  });
});