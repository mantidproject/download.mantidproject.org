function getOS() {
  var os = "";
  if (navigator.appVersion.indexOf("Win") != -1 || navigator.userAgent.indexOf('Windows NT 6.2') > -1) os = "Windows";
  if (navigator.appVersion.indexOf("Mac") != -1) os = "OSX";
  if (navigator.appVersion.indexOf("X11") != -1 || navigator.appVersion.indexOf("Linux") != -1) os = "Linux";
  return os;
}

function updateInstructionsURL(os) {
  if (os == "Linux") $('#release_notes').append(' It is recommended to use <a href="ubuntu.html">apt-get</a> or <a href="redhat.html">yum</a> to install Mantid on Ubuntu/Red Hat.');
}

function windowsXPWarning() {
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
}

$(document).ready(function() {
  windowsXPWarning()
  os = getOS();
  updateInstructionsURL(os);
  winUpgradeWarning = $(".windows-upgrade");
  // Show source code download for Linux distros.
  if (os == "Linux")
  {
    $('#latest .button').attr("href",$("#latest .Source").attr("href")).text("Download source code");
    $('#nightly .button').attr("href",$("#nightly .Source").attr("href")).text("Download source code")
    $('#paraview .button').attr("href",$("#paraview .Source").attr("href")).text("Download source code")

    $(".Source").closest('li').remove();
    winUpgradeWarning.hide()
  }
  else
  {
    osClass = "." + osType.toLowerCase(); // Grab OS name only (e.g. not 7/8)

    $('#latest .button').attr("href",$("#latest " + osClass).attr("href")).append($('#latest ' + osClass).text());
    $('#nightly .button').attr("href",$("#nightly " + osClass).attr("href")).append($('#nightly ' + osClass).text());;
    $('#paraview .button').attr("href",$("#paraview " + osClass).attr("href"));

    $(osClass).closest('li').remove();
    if (os == "Windows") winUpgradeWarning.show();
    else winUpgradeWarning.hide();

  }
});
