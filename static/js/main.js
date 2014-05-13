function getOS() {
  var osName = "UNIX"; // Unknown OS likely to be UNIX variant
  if (navigator.appVersion.indexOf("Win") != -1 || navigator.userAgent.indexOf('Windows NT 6.2') > -1) osName = "Windows 7/8";
  if (navigator.appVersion.indexOf("Mac") != -1) osName = "Mac";
  if (navigator.appVersion.indexOf("X11") != -1 || navigator.appVersion.indexOf("Linux") != -1) osName = "Ubuntu";
  return osName;
}

$(document).ready(function() {
  osName = getOS();
  osClass = "." + osName.split(" ")[0].toLowerCase(); // Grab OS name only (e.g. not 7/8)
  // Replace the download buttons href with the correct download URL for latest and nightly releases
  $('#latest .button').attr("href",$("#latest "+osClass).attr("href"));
  $('#nightly .button').attr("href",$("#nightly "+osClass).attr("href"));
  $('#paraview .button').attr("href",$("#paraview "+osClass).attr("href"));
  $('.button').append(osName)
  // Hide the related OS download link (in 'Alternative downloads') for each button.
  $(osClass).closest('li').remove();
});
