#!/usr/bin/perl

=head1 DESCRIPTION

From Unit 06, homework question #5:

This is the entire annotated genome of E. coli K12. Create an page called 'search.html' in your
web area that contains a valid HTML5 page and a single search box, where users can enter a
gene product name they wish to search for. Make your form submit to a script you create called
'search_product.cgi'. This script should read through that gbk file looking for any ./product.
tags that contain the exact search string, and use a template you create called
'search_product.tmpl' to display the results. The results should show not only the matched
product names but their corresponding locus_tag entries as well. So if I searched for 'glutamate
synthase' I'd expect to get an HTML page that contains a data table that looks like this:
  
=cut

use strict;
use warnings;
use CGI(':standard');
use HTML::Template;

my $q = new CGI;
print $q->header( -type => 'text/html' );

my $tmpl = HTML::Template->new( filename => './search_product.tmpl' );

my $fasta_file = 'e_coli_k12_dh10b.gbk';
#my $fasta_file = 'example.txt';

open(INPUT, $fasta_file) || die "ERROR: can't read input FASTA file: $!";
my $counter=0;
my @locus;
my $locus_tag='';
my @product;
my $product_tag='';

#Set $search to HTML textbox
#my $search= lc(param('search_name');
my $search= param('search_name');

print p("Your search term was: ",$search);

chomp($search);
while ( <INPUT> ) {
    if(/locus_tag="(.+?)"/){
	$locus_tag=$1;
#	print $locus_tag."\n";
    }elsif(/product="(.+?)"/){
	$product_tag=$1;
#	if(/($search)/){
#Match HTML search term, regardless of lower/upper case
	if(/($search)/i){
	    $product[$counter] = $product_tag;
	    $locus[$counter]=$locus_tag;
	    $counter++;
	    $locus_tag='';
	}
    }
}
#Print number of matches/search results
print p("You have ", scalar(@product), "results.");

my %gbk_hash;

while (@locus and @product) {
    $gbk_hash{shift @locus} = [shift @product];
}

#The loop data will be put in here
my @loop; 

#Fill in the loop, sorted by product name
foreach my $locus_num (sort keys %gbk_hash){
    # get the length and mm from the data hash
    my ($product) = @{$gbk_hash{$locus_num}};

    # make a new row for this seq - the keys are <TMPL_VAR> names
    # and the values are the values to fill in the template.
    my %row = (
	locus_tag => $locus_num,
	product_name => $product
	);
    # put this row into the loop by reference
    push(@loop, \%row);
}

$tmpl->param(gbk_loop => \@loop);

print $tmpl->output;
exit(0);
