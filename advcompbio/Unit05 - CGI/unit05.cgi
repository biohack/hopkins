#!/usr/bin/perl
use strict;
use warnings;
use HTML::Template;
use CGI(':standard');
use unit05('table');
use unit05('summary');
#my $file = "test.faa";
my $file = "e_coli_k12_dh10b.faa";

if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}

my ($a,$b,$c,$d,$e)=summary();

if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}
my ($identity,$length,$amino)=table();

my @id = @$identity;
my @len = @$length;
my @aa = @$amino;
my %hash;
while (@id and @len and @aa) {
    $hash{shift @id} = [ shift @len, shift @aa];
}

my %sequence_data=%hash;
my $template = HTML::Template->new(filename => 'unit05.tmpl');
my @loop;  # the loop data will be put in here
# fill in the loop, sorted by fruit name
foreach my $seq_id (sort keys %sequence_data) {
        # get the length and mm from the data hash
    my ($seq_length, $mm) = @{$sequence_data{$seq_id}};
        # make a new row for this seq - the keys are <TMPL_VAR> names
        # and the values are the values to fill in the template.
        my %row = (
            id => $seq_id,
            sequence_length => $seq_length,
            mm => $mm
            );
        # put this row into the loop by reference
    push(@loop, \%row);
}
    # call param to fill in the loop with the loop data by reference.
$template->param(sequence_loop => \@loop);
$template->param(one=> $a);
$template->param(two=> $b);
$template->param(three=> $c);
$template->param(four=> $d);
$template->param(five=> $e);

# send the obligatory Content-Type
print "Content-Type: text/html\n\n";
# print the template
print $template->output;

