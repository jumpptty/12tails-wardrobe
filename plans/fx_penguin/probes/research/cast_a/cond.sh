#!/bin/sh
# Read only: a condensed view of Penguin.cs lines $1-$2 (line numbers kept), the opaque predicates and bare braces removed.
#   sh checks/fx_penguin_research/cast_a/cond.sh 23892 24557
F=${3:-C:/Users/Jump/Desktop/12tails/DecompiledSource/Penguin.cs}
awk -v a="$1" -v b="$2" 'NR>=a && NR<=b {printf "%d\t%s\n", NR, $0}' "$F" \
  | grep -v -P '\t\s*[{}]\s*$|continue;\s*$|if \(-?\d+ [-+] -?\d+ [!=]= -?\d+\)\s*$|// Token|MethodImpl|^\d+\t\s*$' \
  | sed -E 's/this\.\$self_\$[0-9]+\./S./g; s/\$([A-Za-z]+)\$[0-9]+/\1/g; s/^([0-9]+)\t\s+/\1  /' | cut -c1-240
