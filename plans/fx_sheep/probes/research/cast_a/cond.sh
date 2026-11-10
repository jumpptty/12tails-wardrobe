#!/bin/sh
# condensed view of Sheep.cs lines $1-$2: drops the opaque-predicate noise, keeps line numbers
sed -n "$1,$2p;$2q" "${3:-C:/Users/Jump/Desktop/12tails/DecompiledSource/Sheep.cs}" | awk -v s="$1" '{n=s+NR-1; l=$0; gsub(/^[ \t]+/,"",l); if (l ~ /^if \([0-9]+ - [0-9]+ [!=]= -?[0-9]+\)$/) {skip=1; next} if (l=="{"||l=="}") next; if (skip && (l=="continue;"||l=="break;")) {skip=0; next} skip=0; gsub(/this\.\$self_\$[0-9]+\./,"S.",l); gsub(/this\.\$/,"$",l); print n": "l}'
