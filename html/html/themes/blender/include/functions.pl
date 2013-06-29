#!/usr/bin/perl
###############################################################################
#                                                                             #
# IPFire.org - A linux based firewall                                         #
# Copyright (C) 2007  Michael Tremer & Christian Schmidt                      #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################
#																			  #
# Theme file for IPfire (based on ipfire theme)								  #
# Author kay-michael köhler kmk <michael@koehler.tk>						  #
#																			  #
# Version 1.0	March, 6th 2013		kmk										  #
#																			  #
# This script provides the subroutines for a IPfire theme					  #
#																			  #
# This theme is using of jquery and jquery-ui to manipulate the				  #
# given html code of other modules to get nicer and modern results.			  #
#																			  #
# beside, that a drop down menu list was added, some status information is	  #
# pulled via ajax and some html elements received a rewrite with jquery-ui	  #
#																			  #
###############################################################################

use File::Basename;

###############################################################################
#
# print menu html elements for submenu entries
# @param submenu entries
sub showsubmenu() {
	my $submenus = shift;
	
	print '<ul>';
	foreach my $item (sort keys %$submenus) {
		$link = getlink($submenus->{$item});
		next if (!is_menu_visible($link) or $link eq '');

		my $subsubmenus = $submenus->{$item}->{'subMenu'};
		print '<li>';
		print '<a href="'.$link.'">'.$submenus->{$item}->{'caption'}.'</a>';

		&showsubmenu($subsubmenus) if ($subsubmenus);
		print '</li>';
	}
	print "</ul>"
}

###############################################################################
#
# print menu html elements
sub showmenu() {
	#print '<div id="sf-menu-container"><ul class="sf-menu" id="menu">';
	print '<ul style="margin-bottom: 3em;" id="cssmenu" class="sf-menu">';
	foreach my $k1 ( sort keys %$menu ) {
		$link = getlink($menu->{$k1});
		next if (!is_menu_visible($link) or $link eq '');
		print '<li><a>'.$menu->{$k1}->{'caption'}.'</a>';
		my $submenus = $menu->{$k1}->{'subMenu'};
		&showsubmenu($submenus) if ($submenus);
		print "</li>";
	}
	print '</ul>';
END
;
}


###############################################################################
#
# Modify html elements when current script matches
# @param script name - when matching current script html elements will be modified
# @param elements to modify
sub modifyElementsAtScript {
	my $scriptName		= shift;
	my @elements 		= @_;
	my @tmp 			= split(/\./, basename($0));
	my $actualScript	= @tmp[0];
	
	if ($scriptName eq $actualScript) {
		print '<script> $(document).ready(function(){';
		print "\n/* modify elements for script $scriptName */\n";
		foreach my $element (@elements) {
			print '$("a[target='.$element.']").button();';
			print '$("iframe[name='.$element.']").attr("style","margin:10px");';
		}
		print '});</script>';
	}
}

###############################################################################
#
# Modify checkbox elements when current script matches
# @param script name - when matching current script checkbox elements will be modified
# @param elements to modify
sub modifyCheckboxElementsAtScript {
	my $scriptName		= shift;
	my @tmp 			= split(/\./, basename($0));
	my $actualScript	= @tmp[0];
	
	if ($scriptName eq $actualScript) {
		print '<script> $(document).ready(function(){';
		print "\n/* modify checkbox elements for script $scriptName */\n";
		print '$( "input[type=checkbox]" ).button();';
		print '});</script>';
	}
}

###############################################################################
#
# Add script to the defered script loader
# @param script name - the script to load
# @param type of script, eg. 'text/javascript'
my $deferedScripts = {};
sub addDeferedScriptLoad {
	my $scriptOrder		= shift;
	my $scriptName		= shift;
	my $scriptType		= shift;
	
	$deferedScripts->{$scriptOrder} = {$scriptName => $scriptType};
}

###############################################################################
#
# Print javascript code for defered load of script files
sub printDeferedScripts {

print <<END
<!-- begin defered loading -->
<script type="text/javascript">
(function(){
var psna = document.getElementsByTagName('script');
var psn = psna[psna.length-1];
var ds;
END
;

foreach my $scriptOrder (sort keys %$deferedScripts) {
	
	my $hash = $deferedScripts->{$scriptOrder};
	my ($scriptName, $scriptType) = each(%$hash);
	
print <<END
// creating defered loaded script element for $scriptName
var ds = document.createElement('script');
ds.type='$scriptType';
ds.async=true;
ds.src='$scriptName';
psn.parentNode.insertBefore(ds,psn);
END
;
}

print <<END
})();
</script>
<!-- end defered loading -->
END
;
}

###############################################################################
#
# print page opening html layout
# @param page title
# @param boh
# @param extra html code for html head section
# @param suppress menu option, can be numeric 1 or nothing.
#		 menu will be suppressed if param is 1
sub openpage {
	my $title = shift;
	my $boh = shift;
	my $extrahead = shift;
	my $suppressMenu = shift;
	my @tmp = split(/\./, basename($0));
	my $scriptName = @tmp[0];
	my $h2 = gettitle($menu);

	@URI=split ('\?',  $ENV{'REQUEST_URI'} );
	&General::readhash("${swroot}/main/settings", \%settings);
	&genmenu();

	$title = "IPFire - $title";
	if ($settings{'WINDOWWITHHOSTNAME'} eq 'on') {
		$title =  "$settings{'HOSTNAME'}.$settings{'DOMAINNAME'} - $title"; 
	}

print <<END
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Strict//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd'>
<html xmlns='http://www.w3.org/1999/xhtml'>
<head>
<title>$title</title>
	$extrahead
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<link rel="shortcut icon" href="/favicon.ico" />
	
	<link href="/themes/blender/include/css/style.css" rel="stylesheet" type="text/css"  />
	<link href="/themes/blender/include/css/ui-blender-dark/jquery-ui-1.10.2.custom.css" rel="stylesheet" type="text/css" />
	<link href="/themes/blender/include/css/superfish/superfish.css" rel="stylesheet" type="text/css" />
	
	<!--[if gte IE 9]>
		<style type="text/css">
			gradient {
				filter: none;
			}
		</style>
	<![endif]-->

<script type="text/javascript" src="/themes/blender/include/js/jquery-1.9.1.min.js"></script>
<script type="text/javascript" src="/themes/blender/include/js/jquery-ui-1.10.2.custom.min.js"></script>

<script type="text/javascript" src="/themes/blender/include/js/swapvisibility.min.js"></script> 
<script type="text/javascript" src="/themes/blender/include/js/superfish/hoverIntent.min.js"></script>
<script type="text/javascript" src="/themes/blender/include/js/superfish/superfish.min.js"></script>
<script type="text/javascript" src="/themes/blender/include/js/superfish/supersubs.min.js"></script>
END
;

if ($settings{'FX'} ne 'off') {
print <<END
	<meta http-equiv="Page-Enter" content="blendTrans(Duration=0.5,Transition=12)" />
	<meta http-equiv="Page-Exit" content="blendTrans(Duration=0.5,Transition=12)" />
END
;
}


print <<END

<!-- modifications with the present html elements -->
<script type="text/javascript">
	\$(document).ready(function(){
		
		jQuery('#cssmenu').supersubs({
			minWidth: 12,   // minimum width of sub-menus in em units
			maxWidth: 37,   // maximum width of sub-menus in em units
			extraWidth: 1     // extra width can ensure lines don't sometimes turn over due to slight rounding differences and font-family
			}).superfish({
			//useClick: true
			 delay: 700,                            // one second delay on mouseout
			//animation:   {opacity:'show',height:'show'},  // fade-in and slide-down animation 
			speed: 'fast',                          // faster animation speed 
			autoArrows: false
		});

		\$( "input[type=submit]" ).button().css('font-weight','bold');
		\$( "input[type=reset]" ).button();
		\$( "input[type=button]" ).button().css('font-weight','bold');
		\$( "input[type=image]" ).button().css('padding','.4em .4em');
		/*\$( "#radiogrp1" ).buttonset();*/
	});
</script>


END
;

print <<END
</head>
<body>
END
;

print <<END
<!-- IPFIRE HEADER -->
	<div id="header">
		<div id="header_inner" class="fixed">
			<div id="logo">
END
;
	if ($settings{'WINDOWWITHHOSTNAME'} eq 'on') {
		print "<h1><span>$settings{'HOSTNAME'}.$settings{'DOMAINNAME'}</span></h1><br />"; 
	} else {
		print "<h1><span>IPFire</span></h1><br />";
	}

print <<END
				<h2>$h2</h2>
			</div>
		</div>
	</div>
<div id="main">
	<div id="main_inner" class="fixed">
END
;

&showmenu() if ($suppressMenu != 1);

print <<END
		<div id="primaryContent_2columns">
			<div id="columnA_2columns">
END
;
}

###############################################################################
#
# print page opening html layout without menu
# @param page title
# @param boh
# @param extra html code for html head section
sub openpagewithoutmenu {

	openpage(shift,shift,shift,1);
	return;
}


###############################################################################
#
# print page closing html layout
sub closepage () {
	my $status = &connectionstatus();

	$uptime = `/usr/bin/uptime`;
	$status =~ s/<span>//g;
	$status =~ s/<\/span>//g;
	$status =~ s/(\S+)[\s|\S]+(\d+d)\s(\d+)h\s(\d+)m\s(\d+)s[\s|\S]+/$1<br \/>$2 $3:$4:$5/i;
	$uptime =~ s/([\d\:\w]+)\s+(\w+)\s+([\d\s\w\,\:]+),\s+(\d+\susers?),\s+load averages?:\s(\d+\.\d+),\s(\d+\.\d+),\s(\d+\.\d+)[\s|\S]*/$1#$2#$3#$4#$5#$6#$7/i;
	@auptime = split(/#/, $uptime);

print <<END
		<!-- closepage begin -->
			</div>
	</div>
END
;

print <<END
	 <div id="secondaryContent_2columns">
		<div id="columnC_2columns">
			<table cellspacing="5"  class="statusdisplay">
			<tr valign="top">
				<td style="font-weight: bold;">Time</td>
				<td><span id="serverTime">@auptime[0]</span></td>
			</tr>
			<tr valign="top">
				<td style="font-weight: bold;">Status</td>
				<td><span id="inetConnection">$status</span></td>
			</tr>
			<tr valign="top">
				<td style="font-weight: bold;">Uptime</td>
				<td>Service <span id="serverUptime">$auptime[1]<br />$auptime[2]</span></td>
			</tr>
			<tr valign="top">
				<td style="font-weight: bold;">Load</td>
				<td><span id="serverLoad">$auptime[3]<br />$auptime[4] $auptime[5] $auptime[6]</span></td>
			</tr>
END
;

if ($settings{'SPEED'} ne 'off') {
print <<END
			<tr valign="top" >
				<td style="font-weight: bold;">Traffic</td>
				<td id="bandwidthCalculationContainer">In <span id="rx_kbs"></span><br />Out <span id="tx_kbs"></span></td>
			</tr>
END
;
}

print <<END
			</table>
		</div>
	</div>
END
;


print <<END
	</div>
</div>
END
;


&modifyElementsAtScript('system', 			("cpubox","loadbox"));
&modifyElementsAtScript('memory', 			("memorybox","swapbox"));
&modifyElementsAtScript('services', 		("processescpubox","processesmemorybox"));
&modifyElementsAtScript('media', 			("sdabox"));
&modifyElementsAtScript('netexternal', 		("red0box"));
&modifyElementsAtScript('netinternal', 		("green0box"));
&modifyElementsAtScript('netother', 		("gatewaybox","fwhitsbox"));
&modifyElementsAtScript('hardwaregraphs', 	("thermaltempbox","sdabox"));

#&modifyCheckboxElementsAtScript('gui');

if ($settings{'SPEED'} ne 'off') {
	&addDeferedScriptLoad(20,'/themes/blender/include/js/refreshinetinfo.min.js','text/javascript');

#print <<END
#	<script type="text/javascript" src="/themes/blender/include/js/refreshinetinfo.min.js"></script>
#END
#;

}

&printDeferedScripts;

print <<END

</body>
</html>
<!-- closepage end -->
END
;
}

###############################################################################
#
# print big box opening html layout
sub openbigbox
{
}

###############################################################################
#
# print big box closing html layout
sub closebigbox
{
}

###############################################################################
#
# print box opening html layout
# @param page width
# @param page align
# @param page caption
sub openbox
{
	$width = $_[0];
	$align = $_[1];
	$caption = $_[2];

#<div class="post" align="$align">
print <<END
<!-- openbox -->
		<div class="post" style='text-align=$align;'>
END
;

	if ($caption) { print "<h3>$caption</h3>\n"; } else { print "&nbsp;"; }
}

###############################################################################
#
# print box closing html layout
sub closebox
{
	
print <<END
	</div>
	<br class="clear" />
	<!-- closebox -->
END
;
}

1;