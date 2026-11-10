#!/bin/sh
# print Penguin.cs lines A..B with their numbers, dropping junk predicates and lone braces (read only)
F=${F:-C:/Users/Jump/Desktop/12tails/DecompiledSource/Penguin.cs}
awk -v a="$1" -v b="$2" 'NR>=a && NR<=b && !/^[ \t]*if \(-?[0-9]+ - -?[0-9]+ [!=]= -?[0-9]+\)[ \t]*$/ && !/^[ \t]*[{}][ \t]*$/ && !/^[ \t]*continue;[ \t]*$/ {sub(/^[ \t]+/,""); print NR": "$0}' "$F"
