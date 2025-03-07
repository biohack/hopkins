#!/usr/bin/perl -w
use strict;
use DBI;
use Config::IniFiles;

=d
[Database]
DB = 'shwang26_chado'
[Host]
Host = 'localhost'
[User]
User = 'shwang26'
[Password]
Password = 'Hopkins1002'
=cut
my $cfg = Config::IniFiles->new( -file => "./data.ini" );
  print "The value is " . $cfg->val( 'Database', 'DB' ) . ".\n"
    if $cfg->val( 'Database', 'DB' );


my $hello = $cfg -> val('Host','loc');
print "\$hello: $hello\n";
$hello =~ s/'//gi;
print "\$hello: $hello\n";
my $dsn = 'DBI:mysql:database=shwang26_chado;host=localhost';
my $user = 'shwang26';
my $pass = 'Hopkins1002';
my $dbh = DBI->connect($dsn, $user, $pass, { RaiseError => 1, PrintError => 1 });

my $qry = qq{
SELECT feature_id, uniquename
FROM feature
};



my $dsh = $dbh -> prepare($qry);
$dsh-> execute();

## iterate through the results
while ( my $row = $dsh->fetchrow_hashref ) {
#    print "$$row{feature_id}\t$$row{uniquename}\n";
}

$dsh -> finish();
$dbh -> disconnect();
