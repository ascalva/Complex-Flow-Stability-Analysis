#!/usr/bin/perl
#
# filename: clean.pl
#
# @author: Alberto Serrano (axs4986)
#
# purpose: Cleans csv data file by filtering out all points that do not
#          exist within a specificed region.
#
# run: perl clean.pl [csv file]
#

use strict;
use warnings;

# Initialize filenames
my $file_in  = $ARGV[0] or die "Need to get CSV file on the command line\n";
my $file_out = 'out.csv';

# Open input/output files
open my $data, '<', $file_in  or die "Could not open '$file_in'  $!\n";
open my $out , '>', $file_out or die "Could not open '$file_out' $!\n";

# Initialize x, y, z positions
my $x_pos = 24;
my $y_pos = 25;
my $z_pos = 26;

# Initialize bounding values
my $x_min = 1.0;
my $x_max = 1.1;
my $y_min = 1.0;
my $y_max = 1.1;
my $z_val = 0.01;

# Remove and output header
my $header = <$data>;
print $out "$header\n";

# Iterate through file, line-by-line
while (my $line = <$data>)
{
    chomp $line;
    my @fields = split "," , $line;

    # Bound z-values
    if( $fields[$z_pos] == $z_val )
    {
        # Bound x-values
        if( $fields[$x_pos] >= $x_min && $fields[$x_pos] <= $x_max )
        {
            # Bound y-values
            if( $fields[$y_pos] >= $y_min && $fields[$y_pos] <= $y_max )
            {
                # Outout data line within bounding box
                print $out "$line\n";
            }
        }
    }
}

close $file_in;
close $file_out;
