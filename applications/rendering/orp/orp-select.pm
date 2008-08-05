# OR/P - Osmarender in Perl
# -------------------------
#
# Selection Module
#
# (See orp.pl for details.)
#
# This module contains the implementation for the various styles of
# object selection supported in <rule> elements.

use strict;
use warnings;

our $index_way_tags;
our $index_node_tags;
our $debug;

# for collision avoidance / proximity filter
my $used_boxes = {};

sub select_elements_without_tags
{
    my ($oldsel, $e) = @_;
    my $newsel = Set::Object->new();
    foreach ($oldsel->members())
    {
        next if defined($e) and ref($_) != $e;
        $newsel->insert($_) unless defined($_->{"tags"});
    }
    return $newsel;
}


sub select_elements_with_any_tag
{
    my ($oldsel, $e) = @_;
    my $newsel = Set::Object->new();

    foreach ($oldsel->members())
    {
        next if defined($e) and ref($_) != $e;
        $newsel->insert($_) if defined($_->{"tags"});
    }
    return $newsel;
}

sub select_elements_with_given_tag_value
{
    my ($oldsel, $e, $v);
    my $newsel = Set::Object->new();
    my $seek = {};
    $seek->{$_} = 1 foreach(split('\|', $v));
outer:
    foreach ($oldsel->members())
    {
        next if defined($e) and ref($_) ne $e;
        foreach my $value(values(%{$_->{"tags"}}))
        {
            if (defined($seek->{$value}))
            {
                $newsel->insert($_);
                next outer;
            }
        }
    }
    return $newsel;
}

sub select_elements_with_given_tag_key
{
    my ($oldsel, $e, $k) = @_;
    my $newsel = Set::Object->new();
    my @keys_wanted = split('\|', $k);

outer:
    foreach ($oldsel->members())
    {
        next if (defined($e) and ref($_) ne $e);
        foreach my $key(@keys_wanted)
        {
            if (defined($_->{"tags"}->{$key}))
            {
                $newsel->insert($_);
                next outer;
            }
        }
    }

    return $newsel;
}

sub select_elements_without_given_tag_key
{
    my ($oldsel, $e, $k) = @_;
    my $newsel = Set::Object->new();
    my @keys_wanted = split('\|', $k);


outer:
    foreach ($oldsel->members())
    {
        next if defined($e) and ref($_) ne $e;
        foreach my $key(@keys_wanted)
        {
            next outer if (defined($_->{"tags"}->{$key}));
        }
        $newsel->insert($_);
    }

    return $newsel;
}

# e=way or node, s not supptd, v must not contain ~
sub select_elements_with_given_tag_key_and_value_fast
{
    my ($oldsel, $e, $k, $v) = @_;
    my @values_wanted = split('\|', $v);
    my $newsel = Set::Object->new();
    my @keys_wanted = split('\|', $k);

    foreach my $key(split('\|', $k))
    {
        # retrieve list of objects with this key from index.
        my @objects = 
            ($e eq 'way') ? @{$index_way_tags->{$key}||[]} : 
            ($e eq 'node') ? @{$index_node_tags->{$key}||[]} : 
            (@{$index_way_tags->{$key}||[]}, @{$index_node_tags->{$key}||[]});

        debug(sprintf('%d objects retrieved from index for e="%s" k="%s"', 
            scalar(@objects), $e, $k)) if ($debug->{"indexes"});

        # process only those from oldsel that have this key.
outer:
        foreach (@objects)
        {   
            next unless ($oldsel->contains($_));
            foreach my $value(@values_wanted)
            {   
                if ($_->{"tags"}->{$key} eq $value)
                {   
                    $newsel->insert($_);
                    next outer;
                }   
            }   
        } 
    }
    return $newsel;
}

# e=node, s=way, v must not contain ~
sub select_nodes_with_given_tag_key_and_value_for_way_fast
{
    my ($oldsel, $k, $v) = @_;
    my @values_wanted = split('\|', $v);
    my $newsel = Set::Object->new();
    my @keys_wanted = split('\|', $k);

    foreach my $key(split('\|', $k))
    {
        # process only those from oldsel that have this key.
outer:
        foreach my $way(@{$index_way_tags->{$key}||[]})
        {   
            foreach my $value(@values_wanted)
            {   
                if ($way->{"tags"}->{$key} eq $value)
                {   
                    foreach (@{$way->{'nodes'}})
                    {
                        next unless ($oldsel->contains($_));
                        $newsel->insert($_);
                    }   
                }   
            }
        } 
    }
    return $newsel;
}

sub select_elements_with_given_tag_key_and_value_slow
{
    my ($oldsel, $e, $k, $v, $s) = @_;
    my @values_wanted = split('\|', $v);
    my $newsel = Set::Object->new();
    my @keys_wanted = split('\|', $k);

outer:
    foreach ($oldsel->members())
    {   
        next if defined($e) and ref($_) ne $e; 
        # determine whether we're comparing against the tags of the object
        # itself or the tags selected with the "s" attribute.
        my $tagsets;
        if ($s eq "way")
        {   
            $tagsets = []; 
            foreach my $way(@{$_->{"ways"}})
            {   
                push(@$tagsets, $way->{"tags"});
            }   
        }   
        else
        {   
            $tagsets = [ $_->{"tags"} ];
        }   

        foreach my $key(@keys_wanted)
        {   
            foreach my $value(@values_wanted)
            {   
                foreach my $tagset(@$tagsets)
                {   
                    my $keyval = $tagset->{$k};
                    if (($value eq '~' and !defined($keyval)) or
                        ($value eq $keyval and defined($keyval)))
                    {   
                        $newsel->insert($_);
                        next outer;
                    }   
                }   
            }   
        }   
    } 
    
    return $newsel;
}

# this implements a very simple proximity selection. it works only for nodes and
# draws an imaginary box around the node. then it checks all "used" boxes in the
# same proximity class and unselects the object if a collision is detected. 
#
# otherwise, the object remains selected and its box is stored.
#
# there are many FIXMEs: 
# 1. the box is computed based on lat/lon so will have different sizes on the map
#    at different latitudes.
# 2. any object that is selected is considered to have "used" its box. this mechanism
#    only works when the proximity filter is on the last selection rule (which then
#    only contains drawing code). If subsequent rules further reduce the object set,
#    then the boxes are "used" nonetheless.
# 3. the order in which the objects are processed is more or less random (as the 
#    storage is backed by a perl hash). it will be identical for identical input
#    data, but as soon as input data varies a bit, the order might change completely.

sub select_proximity
{
    my ($oldsel,$hp, $vp, $pc) = @_;
    my $newsel = Set::Object->new();
    $pc = "default" if ($pc eq "");
    foreach ($oldsel->members())
    {
        # proximity stuff currently only works for nodes; copy others
        if (ref($_) ne "node")
        {
            $newsel->insert($_);
            next;
        }
        
        my $bottom = $_->{'lat'} - $hp;
        my $left = $_->{'lon'} - $vp;
        my $top = $_->{'lat'} + $hp;
        my $right = $_->{'lon'} + $vp;
        my $intersect = 0;

        foreach my $ub(@{$used_boxes->{$pc}})
        {
            if ((($ub->[0] > $bottom && $ub->[0] < $top) || ($ub->[2] > $bottom && $ub->[2] < $top) || ($ub->[0] <= $bottom && $ub->[2] >= $top)) &&
               (($ub->[1] > $left && $ub->[1] < $right) || ($ub->[3] > $left && $ub->[3] < $right) || ($ub->[1] <= $left && $ub->[3] >= $right)))
            {
                # intersection detected; skip this object.
                $intersect = 1;
                debug("object skipped due to collision in class '$pc'");
                last;
            }
        }
        next if ($intersect);
        $newsel->insert($_);
        debug("object added in class '$pc'");
        push(@{$used_boxes->{$pc}}, [ $bottom, $left, $top, $right ]);
    }
    delete $used_boxes->{$pc} if ($pc eq "default");
    return $newsel;
}

1;
