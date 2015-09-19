(function animate() {
  var $uni = document.getElementsByClassName('unicorn')[0];
  var text = $uni.innerHTML;
  var color_steps = 360 / text.length;
  var newCont = "";
  var time = 0;
  var timestep = $uni.dataset.score;

  for (var text_index =0; text_index < text.length; text_index++) {
    newCont += "<span style='color:hsl(" + text_index * color_steps +
      ", 100%, 50%)'>" + text.charAt(text_index) + "</span>";
  }

  $uni.innerHTML = newCont; // Replace with new content
  var $ch = $uni.getElementsByTagName('span'); // character

  setInterval(function(){
    time -= timestep;
    time = time % 360;
    for (var ch_index = 0; ch_index < $ch.length; ch_index += 1) {
      current_ch = $ch[ch_index];
      var hue = (time + (color_steps * ch_index)) % 360;
      current_ch.style.color = "hsl(" + hue + ", 100%, 50%)";
    }
  }, 50);
})();

(function ensure_frameless() {
  // http://stackoverflow.com/a/326076
  function in_frame() {
    try {
      return window.self !== window.top;
    } catch (e) {
      return true;
    }
  }
  function retarget_anchors() {
    var local_links = document.getElementsByTagName('a');
    var local_link;
    for (var index = 0; index < local_links.length; index += 1) {
      local_link = local_links[index];
      href = local_link.href
      if (href.indexOf(document.location.origin) == 0) {
        local_link.setAttribute("target", "_blank");
      }
    }
  }
  if (in_frame()) {
    retarget_anchors();
  }
})();
