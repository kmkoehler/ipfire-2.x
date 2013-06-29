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


use strict;

# enable only the following on debugging purpose
#use warnings;
#use CGI::Carp 'fatalsToBrowser';

require '/var/ipfire/general-functions.pl';
require "${General::swroot}/lang.pl";
require "${General::swroot}/header.pl";

my %cgiparams=();
my %mainsettings=();
my %checked=();
my $errormessage='';


$cgiparams{'FX'} = 'off';
$cgiparams{'SPEED'} = 'off';
$cgiparams{'WINDOWWITHHOSTNAME'} = 'off';
$cgiparams{'REBOOTQUESTION'} = 'off';
$cgiparams{'REFRESHINDEX'} = 'off';
$cgiparams{'ACTION'} = '';
&Header::getcgihash(\%cgiparams);

&Header::showhttpheaders();
&General::readhash("${General::swroot}/main/settings",\%mainsettings);
if ($cgiparams{'ACTION'} eq "$Lang::tr{'save'}")
{
	open(FILE,"${General::swroot}/langs/list");
	my $found=0;
	while (<FILE>)
	{
		my $lang='';
		my $engname='';
		my $natname='';
		chomp;
		($lang,$engname,$natname) = split (/:/, $_,3);
		if ($cgiparams{'lang'} eq $lang)
		{
			$found=1;
		}
	}
	close (FILE);
	if ( $found == 0 )
	{
		$errormessage="$errormessage<P>$Lang::tr{'invalid input'}";
		goto SAVE_ERROR;
	}

        # Set flag if index page is to refresh whilst ppp is up.
        # Default is NO refresh.
        if ($cgiparams{'REFRESHINDEX'} ne 'off') {
            system ('/usr/bin/touch', "${General::swroot}/main/refreshindex");
        } else {
            unlink "${General::swroot}/main/refreshindex";
        }

        # Beep on ip-up or ip-down. Default is ON.
        if ($cgiparams{'PPPUPDOWNBEEP'} ne 'on') {
            $cgiparams{'PPPUPDOWNBEEP'} = 'off';
            system ('/usr/bin/touch', "${General::swroot}/ppp/nobeeps");
        } else {
            unlink "${General::swroot}/ppp/nobeeps";
        }

        # write cgi vars to the file.
	$mainsettings{'LANGUAGE'} = $cgiparams{'lang'};
	$mainsettings{'WINDOWWITHHOSTNAME'} = $cgiparams{'WINDOWWITHHOSTNAME'};
	$mainsettings{'REBOOTQUESTION'} = $cgiparams{'REBOOTQUESTION'};
	$mainsettings{'PPPUPDOWNBEEP'} = $cgiparams{'PPPUPDOWNBEEP'};
	$mainsettings{'FX'} = $cgiparams{'FX'};
	$mainsettings{'SPEED'} = $cgiparams{'SPEED'};
	$mainsettings{'THEME'} = $cgiparams{'theme'};
	$mainsettings{'REFRESHINDEX'} = $cgiparams{'REFRESHINDEX'};
	&General::writehash("${General::swroot}/main/settings", \%mainsettings);
	&Lang::reload($cgiparams{'lang'});
	SAVE_ERROR:
} else {
	if ($mainsettings{'WINDOWWITHHOSTNAME'}) {
		$cgiparams{'WINDOWWITHHOSTNAME'} = $mainsettings{'WINDOWWITHHOSTNAME'};
	} else {
		$cgiparams{'WINDOWWITHHOSTNAME'} = 'off';
	}
	
	if ($mainsettings{'REBOOTQUESTION'}) {
		$cgiparams{'REBOOTQUESTION'} = $mainsettings{'REBOOTQUESTION'};
	} else {
		$cgiparams{'REBOOTQUESTION'} = 'on';
	}

	if ($mainsettings{'PPPUPDOWNBEEP'}) {
		$cgiparams{'PPPUPDOWNBEEP'} = $mainsettings{'PPPUPDOWNBEEP'};
	} else {
		$cgiparams{'PPPUPDOWNBEEP'} = 'on';
	}

	if ($mainsettings{'FX'}) {
		$cgiparams{'FX'} = $mainsettings{'FX'};
	} else {
		$cgiparams{'FX'} = 'on';
	}

	if ($mainsettings{'THEME'}) {
		$cgiparams{'THEME'} = $mainsettings{'THEME'};
	} else {
		$cgiparams{'THEME'} = 'ipfire';
	}

	if($mainsettings{'REFRESHINDEX'}) {
		$cgiparams{'REFRESHINDEX'} = $mainsettings{'REFRESHINDEX'};
	} else {
		$cgiparams{'REFRESHINDEX'} = 'off';
	}
	if($mainsettings{'SPEED'}) {
		$cgiparams{'SPEED'} = $mainsettings{'SPEED'};
	} else {
	# if var is not defined it will be set to on because after installation var
	# is not set and the speedmeter should be displayed, it can only be deactivated
	# by manually setting the var to off
		$cgiparams{'SPEED'} = 'on';
	}
}

# Default settings
if ($cgiparams{'ACTION'} eq "$Lang::tr{'restore defaults'}")
{
	$cgiparams{'WINDOWWITHHOSTNAME'} = 'off';
	$cgiparams{'REBOOTQUESTION'} = 'on';
	$cgiparams{'PPPUPDOWNBEEP'} = 'on';
	$cgiparams{'REFRESHINDEX'} = 'off';
	$cgiparams{'FX'} = 'on';
	$cgiparams{'SPEED'} = 'on';
	$cgiparams{'THEME'} = 'ipfire';
}

$checked{'WINDOWWITHHOSTNAME'}{'off'} = '';
$checked{'WINDOWWITHHOSTNAME'}{'on'} = '';
$checked{'WINDOWWITHHOSTNAME'}{$cgiparams{'WINDOWWITHHOSTNAME'}} = "checked='checked'";

$checked{'REBOOTQUESTION'}{'off'} = '';
$checked{'REBOOTQUESTION'}{'on'} = '';
$checked{'REBOOTQUESTION'}{$cgiparams{'REBOOTQUESTION'}} = "checked='checked'";

$checked{'PPPUPDOWNBEEP'}{'off'} = '';
$checked{'PPPUPDOWNBEEP'}{'on'} = '';
$checked{'PPPUPDOWNBEEP'}{$cgiparams{'PPPUPDOWNBEEP'}} = "checked='checked'";

$checked{'REFRESHINDEX'}{'off'} = '';
$checked{'REFRESHINDEX'}{'on'} = '';
$checked{'REFRESHINDEX'}{$cgiparams{'REFRESHINDEX'}} = "checked='checked'";

$checked{'FX'}{'off'} = '';
$checked{'FX'}{'on'} = '';
$checked{'FX'}{$cgiparams{'FX'}} = "checked='checked'";

$checked{'SPEED'}{'off'} = '';
$checked{'SPEED'}{'on'} = '';
$checked{'SPEED'}{$cgiparams{'SPEED'}} = "checked='checked'";

&Header::openpage($Lang::tr{'gui settings'}, 1, '');
&Header::openbigbox('100%', 'left', '', $errormessage);

if ($errormessage) {
	&Header::openbox('100%','left',$Lang::tr{'error messages'});
	print "<font class='base'>${errormessage}&nbsp;</font>\n";
	&Header::closebox();
}

&Header::openbox('100%','left',$Lang::tr{'gui settings'});

my $sSelectLang = '';
my $id=0;
open(FILE,"${General::swroot}/langs/list");
while (<FILE>)
{
	my $lang='';
	my $engname='';
	my $natname='';
        $id++;
        chomp;
        ($lang,$engname,$natname) = split (/:/, $_, 3);
	$sSelectLang .= "<option value='$lang' ";
	if ($lang =~ /$mainsettings{'LANGUAGE'}/)
	{
		$sSelectLang .= " selected='selected'";
	}
	$sSelectLang .= <<END
>$engname ($natname)</option>
END
;
}

my $sSelectTheme = '';
my $dir = "/srv/web/ipfire/html/themes";
local *DH;
my ($item, $file);
my @files;

# Foreach directory create am theme entry to be selected by user

opendir (DH, $dir);
while ($file = readdir (DH)) {
	next if ( $file =~ /^\./ );
	push (@files, $file);
}
closedir (DH);

foreach $item (sort (@files)) {
	if ( "$mainsettings{'THEME'}" eq "$item" ) {
		$sSelectTheme .= "<option value='$item' selected='selected'>$item</option>\n";
	} else {
		$sSelectTheme .= "<option value='$item'>$item</option>\n";
	}
}


print <<END
<style type="text/css">
label {
	width:100%;
	margin:.4em;
}
</style>
<form method='post' action='$ENV{'SCRIPT_NAME'}'>
<div>
<div style="width:40%;float:left;margin:.4em .4em 0 0">
	<strong>$Lang::tr{'display'}</strong>
	<div style="font-size: 80%;margin:.4em">
		<input type='checkbox' name='FX' id="FX" $checked{'FX'}{'on'} />
		<label for="FX">$Lang::tr{'display webinterface effects'}</label>
		<br />
		<input type='checkbox' name='WINDOWWITHHOSTNAME' id='WINDOWWITHHOSTNAME' $checked{'WINDOWWITHHOSTNAME'}{'on'} />
		<label for="WINDOWWITHHOSTNAME">$Lang::tr{'display hostname in window title'}</label>
		<br />
		<input type='checkbox' name='REBOOTQUESTION' id='REBOOTQUESTION' $checked{'REBOOTQUESTION'}{'on'} />
		<label for="REBOOTQUESTION">$Lang::tr{'reboot question'}</label>
		<br />
		<input type='checkbox' name='REFRESHINDEX' id='REFRESHINDEX' $checked{'REFRESHINDEX'}{'on'} />
		<label for="REFRESHINDEX">$Lang::tr{'refresh index page while connected'}</label>
		<br />
		<input type='checkbox' name='SPEED' id="SPEED" $checked{'SPEED'}{'on'} />
		<label for="SPEED">$Lang::tr{'show ajax speedmeter in footer'}</label>
	</div>
	<strong>$Lang::tr{'sound'}</strong>
	<div style="margin:.4em;font-size: 80%">
		<input type ='checkbox' name='PPPUPDOWNBEEP' id='PPPUPDOWNBEEP' $checked{'PPPUPDOWNBEEP'}{'on'} />
		<label style="width:100%" for='PPPUPDOWNBEEP'>$Lang::tr{'beep when ppp connects or disconnects'}</label>
	</div>
</div>

<div style="width:40%;float:right;margin:.4em 0 0 0">
	<strong>$Lang::tr{'languagepurpose'}</strong>
	<div style="margin:.4em">
		<select style="width:100%" name='lang'>
		$sSelectLang
		</select>
	</div>

	<strong>$Lang::tr{'theme'}</strong>
	<div style="margin:.4em">
		<select style="width:100%" name='theme'>
			$sSelectTheme
		</select>
	</div>
</div>
</div>
<br class="clear" />
<div style="float:right">
	<input type='submit' name='ACTION' value='$Lang::tr{'restore defaults'}' />
	<input type='submit' name='ACTION' value='$Lang::tr{'save'}' />
</div>




</form>
END
;
&Header::closebox();
&Header::closebigbox();
&Header::closepage();



