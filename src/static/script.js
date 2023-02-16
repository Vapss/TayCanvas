var csvFile = "../static/canvas.csv";
var counter = 0;
var loadingol = 0;

$(window).on("scroll", function() {
var scrollHeight = $(document).height();
var scrollPosition = $(window).height() + $(window).scrollTop();
if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
loadImage(1);
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

function loadImage(justone) {
var imgstyle = "display: none;";
if ((loadingol == 0) || (justone == 0)) {
loadingol = 1;
counter++;

    if (justone == 0) {    
        imgstyle = "";
    }

    $.get(csvFile, function(data) {
        var lines = data.split('\n');
        for (var i = 1; i < lines.length; i++) { // start at index 1 to skip column headings
          var fields = lines[i].split(',');
          if (fields.length === 3) { // check for 3 fields instead of 2
            var songName = fields[2].trim();
            var albumName = fields[1].trim();
            var videoUrl = fields[0].trim();
            var div = $('<div><p>' + songName + '</p><p>' + albumName + '</p></div>');
            var video = $('<video autoplay loop muted><source src="' + videoUrl + '" type="video/mp4"></video>');
            gallery.append(div);
            gallery.append(video);
          }
        }
      });
      
}
}

/Scroll to top when arrow up clicked BEGIN/
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
/Scroll to top when arrow up clicked END/