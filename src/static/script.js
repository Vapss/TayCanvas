var csvFile = "../static/canvas.csv";
var counter = 0;
var loadingol = 0;
var gallery = $('#gallery');

$(window).on("scroll", function() {
  var scrollHeight = $(document).height();
  var scrollPosition = $(window).height() + $(window).scrollTop();
  if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
    loadImage(3);
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

function loadImage(count) {
  var imgstyle = "display: none;";
  if ((loadingol == 0) || (count !== 3)) {
    loadingol = 1;
    counter++;

    if (count !== 3) {
      imgstyle = "";
    }

    $.get(csvFile, function(data) {
      var lines = data.split('\n');
      for (var i = 1 + (counter-1)*count; i <= count*counter; i++) {
        if (i >= lines.length) {
          $('#loading').hide();
          $('.wrap-infinite-link').hide();
          break;
        }
        var fields = lines[i].split(',');
        if (fields.length === 3) {
          var songName = fields[2].trim();
          var albumName = fields[1].trim();
          var videoUrl = fields[0].trim();
          var div = $('<div><p>' + songName + '</p><p>' + albumName + '</p></div>');
          var video = $('<video width="480" height="270" autoplay loop muted><source src="' + videoUrl + '" type="video/mp4"></video>');
          gallery.append(div);
          gallery.append(video);
        }
      }
      loadingol = 0;
    });
  }
}

$(window).scroll(function() {
  var height = $(window).scrollTop();
  if (height > 100) {
    $('#back2Top').fadeIn();
  } else {
    $('#back2Top').fadeOut();
  }
});

$(document).ready(function() {
  $("#back2Top").click(function(event) {
    event.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "slow");
    return false;
  });
});