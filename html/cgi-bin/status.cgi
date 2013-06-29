#!/usr/bin/perl
###############################################################################
#                                                                             #
# IPFire.org - A linux based firewall                                         #
# Copyright (C) 2013  IPFire Team                                             #
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
# status.cgi (based on speed.cgi)											  #
# Used by: theme blender													  #
#																			  #
# Version 1.0	March 6th 2013												  #
#																			  #
# This script provides status ipfire server status information via ajax calls #
#																			  #
# Author kay-michael köhler (michael@koehler.tk)							  #
#																			  #
###############################################################################
#use warnings;
#use CGI::Carp 'fatalsToBrowser';
require '/var/ipfire/general-functions.pl';
require "${General::swroot}/lang.pl";
require "${General::swroot}/header.pl";

my $uptime = `/usr/bin/uptime`;
my $status = &Header::connectionstatus();

# unload HTML css information from connection information
$status =~ s/<span>//g;
$status =~ s/<\/span>//g;
# grep/reformat text from connection information
$status =~ s/(\S+)[\s|\S]+(\d+d)\s(\d+)h\s(\d+)m\s(\d+)s[\s|\S]+/$1#$2 $3:$4:$5/i;
# grep/reformat text from uptime information
$uptime =~ s/([\d\:\w]+)\s+(\w+)\s+([\d\s\w\,\:]+),\s+(\d+\susers?),\s+load averages?:\s(\d+\.\d+),\s(\d+\.\d+),\s(\d+\.\d+)[\s|\S]*/$1#$2#$3#$4#$5#$6#$7/i;

print "pragma: no-cache\n";
print "Content-type: text/xml\n\n";
print "<?xml version=\"1.0\"?>\n";
print <<END
<status>
	<conn>$status</conn>
	<uptime>$uptime</uptime>
</status>
END
;