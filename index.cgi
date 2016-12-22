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
# display head
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
	$in{os} !~ m/windows|linux/ ? exit_error('os') : undef;
	my $name =  $in{host} . '-fd';
	
	my $clients=list_clients();
	if ($clients->{$in{host}}){
		exit_error('client');
	}
	
	open(my $fh, '>>', $config{config_file}) 
		or exit_error('write');

	print $fh qq(Client {
  Name = $in{host}-fd
  Password = $in{password}
  Address = $in{host}
  FDPort = 9102
  Catalog = MyCatalog
  File Retention = 30 days
  Job Retention = 6 months
}
);
	my $fileset='Linux-Base';

	if ( $in{os} eq 'windows' ) {
		$fileset='Windows-Base';
	}
	
	print $fh qq(Job {
	  Name = "$in{host}-Full"
  JobDefs = DefaultJob
  Type = Backup
  Level = Full
  Client = $in{host}-fd
  FileSet = $fileset
  Schedule = Full_Inc
  Storage = File
  Pool = Full
  Messages = Standard
}
Job {
	  Name = "$in{host}-Inc"
  JobDefs = DefaultJob
  Type = Backup
  Level = Incremental
  Client = $in{host}-fd
  FileSet = $fileset
  Schedule = Full_Inc
  Storage = File
  Pool = Incremental
  Messages = Standard
}
);	
	close $fh;
	my $bcout = qx(echo reload | /usr/bin/bconsole)
		or print "<strong>Reload configuration failed</strong>";
	
	print "\nHôte ajouté.\n";
	&ui_print_footer('/', "index");
	exit;
}

###########################
# main page
###########################

my $clients = list_clients();

# print '<pre>';
# print Dumper \%in;
# print Dumper $clients;
# print '</pre>';


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
					'client' => 'Le client est déjà configuré',
					'write' => "impossible d'écrire le fichier de configuration",
					'os' => "OS non défini",
				};
				
	print "Erreur: " . $message->{$_[0]};
	&ui_print_footer('/', "index");
	exit;	
}


