#!/usr/bin/perl

BEGIN { push(@INC, ".."); };

use strict;
use warnings;
use Data::Dumper;

our (%text, %config, $module_name);

use WebminCore;

&init_config();


if ($in{add}) {
	$in{host} !~ m/[\w+|\.|\-]+/ ? die : undef ;
	$in{password} !~ m/[\w+|\/|\+]+/ ? die : undef ;
	my $name =  $in{host} . '-fd';
	
	my $err = check_config();
	die if ($err);	

	my $clients=list_clients();
	if ($clients->{$in{host}}){
		die "client already exists!";
	}
	
	open(my $fh, '>>', $config{config_file}) or die;
	
}

###########################
# display page (unused)
###########################
&ui_print_header(undef, "Bare OS Client", "", "intro", 1, 1, 0, "");

print Dumper \%config;

my $err = &check_config();
if ($err) {
        &ui_print_endpage(
                $err." ". &text('no configuration found', "../config.cgi?$module_name"));
        }

&ui_print_footer('/', "index");


###########################
# subs
###########################
# looks for config file
sub check_config {
	if ( -f $config{config_file} ){
		return undef	
	}
	return &text('configuration file not found', $config{config_file} )
}

# list clients from config file
sub list_clients {
	open(my $fh, '<', $config{config_file}) or die "can't open config file";

	my @clients;
	my $next;	
	while (<$fh>){
		next if m/^\n/;
		next if m/^\s*#/;
		if ( m#Client\s*{# ){
			$next=1;
			next;
		}
		if ( m#Name\s*=\s*"?(.*)-fd# and $next){
			push @clients, $1;
			$next=0;
		}
		
	my %clients = map { $_ => 1 } @clients;
	
	return \%clients;
	}
}
