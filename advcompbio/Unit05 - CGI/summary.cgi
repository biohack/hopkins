#!usr/bin/perl
use strict;
use warnings;
#use Bio::Tools::Seqstats;
use CGI;
my $file = "test.faa";
#my $file = "e_coli_k12_dh10b.faa";

if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}

summary();

if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}
my ($identity,$length,$amino)=&table();
my @id = @$identity;
my @len = @$length;
my @aa = @$amino;
#my @id=table();
foreach(@id){
    print $_."\n";
}
foreach(@len){
    print $_."\n";
}
foreach(@aa){
    print $_,"\n";
}
cgi(\@id,\@len,\@aa);

use HTML::Template;
=d
my %sequence_data = (
    Apple => ['Red', 'Round'],
    Orange => ['Orange', 'Round'],
    Pear => ['Green or Red', 'Pear-Shaped'],
    Banana => ['Yellow', 'Curved'],
    );
=cut
sub cgi{
    my ($one, $two, $three)=@_;
    my @id = @$one;
    my @len = @$two;
    my @aa = @$three;
    my %hash;
#my %sequence_data=%hash;
    while (@id and @len and @aa) {
	$hash{shift @id} = [ shift @len, shift @aa];
    }
    
    my %sequence_data=%hash;
    my $template = HTML::Template->new(filename => 'f.tmpl');
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
# send the obligatory Content-Type
    print "Content-Type: text/html\n\n";
# print the template
    print $template->output;
}

sub table{
    my $printable = 0;
    my $count = 0;
    my $seq_num=0;
    my @seq_id;
    my $sequence='';
    my $string_length=0;
    my @len;
    my $len_num=0;
    my $string_counter=0;
    my @aa_seq;
    my $amino_seq='';
    #If $printable = 1, print line; otherwise, don't print
    while (<INPUT>) {
        #If line matches the sequence ID (aka if line is header)...
	if ($_ =~ /^>gi\|(\d+)\|ref/){
            $count++;
            #Place sequence ID into array...
            $seq_id[$seq_num]=$1;
            $seq_num++;
            #Reset sequence length...
            $string_length=0;
            #Reset sequence counter (0 = new sequence; !0 = same sequence)
            $string_counter=0;
	    $amino_seq='';
	}else{
            #Otherwise (aka sequence), store length of line/sequence...
	    $string_length+=length();
	    $amino_seq.=$_;
#	    print $amino_seq."\n";
	    $len[$len_num]=$string_length;
	    $aa_seq[$len_num]=$amino_seq;
            #If same sequence (!0), then store updated string_length to prior array position
	    if($string_counter!=0){
		$len_num--;
		$len[$len_num]=$string_length;
		$aa_seq[$len_num]=$amino_seq;
	    }
            #Progress along array position...
	    $len_num++;
            #Add to sequence counter...
	    $string_counter++;
	}
    }
    return (\@seq_id, \@len, \@aa_seq);
}

sub summary{

    my $min_protein_length = undef;
    my $max_protein_length = 0;
    my $hypothetical_count = 0;

    ## variables needed to get an average protein length
    my $protein_count = 0;
    my $sum_protein_size = 0;

    ## temporary variables to use while iterating through the file
    my $current_seq = undef;

    ## iterate through the file line-by-line
    while ( my $line = <INPUT> ) {
	## look for new entry lines and match the annotation portion
	if ( $line =~ /^\>\S+(.+)/ ) {
	    my $product = $1;
	    $protein_count++;
	    
	    $hypothetical_count++ if $product =~ /hypothetical/i;
	    
	    ## do we have a sequence to process?  this would only be false at the beginning of the file
	    if ( defined $current_seq ) {
		## make sure there's no whitespace in our sequence that could throw off the length
		$current_seq =~ s/\s//g;
		
		$sum_protein_size += length($current_seq);
		$max_protein_length = length($current_seq) if length($current_seq) > $max_protein_length;
		
		if ( ! defined $min_protein_length || length($current_seq) < $min_protein_length ) {
		    $min_protein_length = length($current_seq);
		}
	    }
	    
	    ## we're finished processing, so now reset to build this sequence
	    $current_seq = '';

	} else {
	    ## if this isn't a header line, add it to the current sequence
	    $current_seq .= $line;
	}
    }
    
    ## since we were processing the building sequence when we encountered a new > symbol, the last
    #   sequence in the file would go unprocessed unless we handle it now
    #   NOTE: this should normally be a subroutine called both here and within the loop, but we're
    #   assuming you don't know that yet.
    $current_seq =~ s/\s//g;
    
    $sum_protein_size += length($current_seq);
    $max_protein_length = length($current_seq) if length($current_seq) > $max_protein_length;
    
    if ( ! defined $min_protein_length || length($current_seq) < $min_protein_length ) {
	$min_protein_length = length($current_seq);
    }


    ## now print the results.
    my $avg_protein_length = sprintf("%.1f", $sum_protein_size / $protein_count );
    
    print "gene count: $protein_count\n";
    print "min protein length: $min_protein_length\n";
    print "max protein length: $max_protein_length\n";
    print "average protein_length: $avg_protein_length\n";
    print "hypothetical genes: $hypothetical_count\n";
}	
