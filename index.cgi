#!/usr/bin/perl

BEGIN { push(@INC, ".."); };

use strict;
use warnings;
use Data::Dumper;

our (%text, %config, $module_name);

use WebminCore;

&init_config();
&ReadParse();

###########################
# head
###########################
&ui_print_header(undef, "Bare OS Client", "", "intro", 1, 1, 0, "");

my $err = &check_config();
if ($err) {
        &ui_print_endpage(
                $err." ". &text('no configuration found', "../config.cgi?$module_name"));
        }


###########################
# add client
###########################
if ($in{add}) {
	$in{host} !~ m/[\w+|\.|\-]+/ ? exit_error('host') : undef ;
	$in{password} !~ m/[\w+|\/|\+]+/ ? exit_error('password') : undef ;
	my $name =  $in{host} . '-fd';
	
	my $clients=list_clients();
	if ($clients->{$in{host}}){
		exit_error('client');
	}
	
	open(my $fh, '>>', $config{config_file}) or exit_error('write');
	
}

###########################
# main page
###########################

my $clients = list_clients();

print '<pre>';
print Dumper \%in;
print Dumper $clients;
print '</pre>';


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
	open(my $fh, '<', $config{config_file}) 
		or die "can't open config file " . $config{config_file};

	my @clients;
	my $next;	
	print '<pre>';
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
	}
	my %clients = map { $_ => 1 } @clients;
	return \%clients;
}

sub exit_error {
	my $message = { 'host' => "il faut un nom d'hôte",
					'password' => "il faut un mot de passe",
					'config' => "fichier de configuration non trouvé",
					'client' => 'client déjà présent',
					'write' => "impossible d'écrire le fichier de configuration",
				};
				
	print "Erreur: " . $message->{$_[0]};
	&ui_print_footer('/', "index");
	exit;	
}
