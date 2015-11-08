#!/usr/bin/perl
use strict;

open(RFD0, "F.dict");
my %fdict = {};
my $firstline = 1;
while(<RFD0>){
    chomp;
    if($firstline){
        $firstline = 0;
        next;
    }
    my ($zh, $en) = split/\t/;
    $fdict{$zh} = $en;
}
close(RFD0);



open(RFD, "M.dict");
$firstline = 1;
my %mdict = {};
while(<RFD>){
    chomp;
    if($firstline){
        $firstline = 0;
        next;
    }
    my ($zh, $en) = split/\t/;
    $mdict{$zh} = $en;
}
close(RFD);

open(RFD1, "result");
my $firstline = 1;
while(<RFD1>){
    chomp;
    my $line = $_;
    if($firstline){
        $firstline = 0;
        next;
    }

    print $line."\t";
    my @array = split/\t/;

    my $form = $array[7];
    if($fdict{$form}){
        print $fdict{$form};
    } else {
        print "__MISSING__";
    }
    print "\t";


    my $target = $array[4];

    my @target_arr = split(/、|\s+/,$target);

    my $count = 1;
    foreach my $t(@target_arr){

        if($mdict{$t}){
            print $mdict{$t}." ";
        } elsif($t =~ m/[\d\%\.]+/){
            print $t;
            if($count >= 2 && $count < scalar(@target_arr)) {
                print "、";
            }
        } else {
            print "__MISSING__ ";
        }
        $count++;
    }
    print "\n";

}
