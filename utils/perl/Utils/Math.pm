##################################################################
package Utils::Math;
##################################################################

use Exporter; require DynaLoader; require AutoLoader;
@ISA = qw(Exporter DynaLoader);
@EXPORT = qw(min max);

use Math::Trig;

sub min($$){
    my $a = shift;
    my $b = shift;
    return $b if ! defined $a;
    return $a if ! defined $b;
    return $a<$b?$a:$b;
}

sub max($$){
    my $a = shift;
    my $b = shift;
    return $b if ! defined $a;
    return $a if ! defined $b;
    return $a>$b?$a:$b;
}
