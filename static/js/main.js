function getOS() {
  var osName = "UNIX"; // Unknown OS likely to be UNIX variant
  if (navigator.appVersion.indexOf("Win") != -1 || navigator.userAgent.indexOf('Windows NT 6.2') > -1) osName = "Windows 7/8";
  if (navigator.appVersion.indexOf("Mac") != -1) osName = "Mac";
  if (navigator.appVersion.indexOf("X11") != -1 || navigator.appVersion.indexOf("Linux") != -1) osName = "Ubuntu";
  return osName;
}

$(document).ready(function() {

  if (navigator.userAgent.indexOf('Windows NT 5.1') != -1)
  {
    $('#latest p:first').replaceWith('<p id="error"><b>Note:</b> Windows XP is no longer supported. Last supported release <b>(3.1.1)</b> can be downloaded below:</p>');
    $('#latest .button').attr("href","http://sourceforge.net/projects/mantid/files/3.1/mantid-3.1.1-win32.exe/download");
    $('#nightly .button').attr("href","http://sourceforge.net/projects/mantid/files/3.1/mantid-3.1.1-win32.exe/download");
    $('#paraview .button').attr("href","http://download.mantidproject.org/download.psp?f=kits/mantid/Python27/3.0/ParaView-3.98.1-Windows-32bit.exe");
    $('.button').append("Windows XP");
    $('.win32').closest('li').remove();
    return;
  }

  osName = getOS();
  osClass = "." + osName.split(" ")[0].toLowerCase(); // Grab OS name only (e.g. not 7/8)

  // Replace the download buttons href with the correct download URL for latest and nightly releases
  $('#latest .button').attr("href",$("#latest "+osClass).attr("href"));
  $('#nightly .button').attr("href",$("#nightly "+osClass).attr("href"));
  $('#paraview .button').attr("href",$("#paraview " + osClass).attr("href"));

  // Show .deb download by default.
  if (osName == "Ubuntu")
  {
    $('#latest .button').append(" Linux (.deb)");
    $('#nightly .button').append(" Linux (.deb)");
    $('#paraview .button').append(" Linux (.deb)");
  }
  else
  {
    $('.button').append(osName)
  }
  $(osClass).closest('li').remove();
});
