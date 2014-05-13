function getOS() {
  var osName = "UNIX"; // Unknown OS likely to be UNIX variant
  if (navigator.appVersion.indexOf("Win") != -1) osName = "Windows 7/8";
  if (navigator.appVersion.indexOf("Mac") != -1) osName = "OSX";
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

  // Improve usability on OSX by updating the text to use the code name (e.g. Mavericks).
  url = $('.osx').attr("href");
  osxName = url.substring(url.lastIndexOf("-")+1,url.lastIndexOf(".")); // Obtain the OSX version from the download url.
  osxName = osxName.replace(/([a-z])([A-Z])/g, '$1 $2'); // Insert a space where caps is, e.g. MountainLion becomes Mountain Lion
  $('.osx').text(osxName);

  // Add the correct supported OSX version for each download button.
  if (osName == "OSX") $('.button').append(osxName)
  else $('.button').append(osName)

  // Hide the related OS download link (in 'Alternative downloads') for each button.
  $(osClass).closest('li').remove();
  $(osClass).hide();
});
