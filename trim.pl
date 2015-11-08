#!/usr/bin/perl

open(RFD, "fdict");
while(<RFD>){

    chomp;
    my @arr = split/\s+/;
    if(scalar(@arr)<2){
        next;
    }

    print join("\t", @arr)."\n";
}

close(RFD)
