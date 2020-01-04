#!/usr/bin/awk -f
# Usage: list2leda <edge list file>

BEGIN { count = 0; numEdges = 0; }

function nodeNum (name) {
  if(name in nodes) {
    return nodes[name];
  } else {
    count++;
    nodes[name] = count;
    names[count] = name;
    return count;
  }
}

/^#/ { next; }
/^$/ { next; }

NF == 1 {
  nodeNum($1);
  print "WARNING: not enough nodes on this line: " $0 > "/dev/fd/2";
  next;
}

(NF == 2 || NF == 3) {
  num1 = nodeNum($1);
  num2 = nodeNum($2);
  if(num1 == num2) { next; }
  if(num1 < num2) { edges[num1 " " num2] = 1; }
  if(num1 > num2) { edges[num2 " " num1] = 1; }
  numEdges++;
  next;
}

(NF < 2 || NF > 3) {
  print "Edge format requires exactly two nodes per line, "
        "with an optional weight" > "/dev/fd/2"; e5Dxit 1 }

{
  print "Not a valid edge list line: " $0 > "/dev/fd/2"
  exit 1;
}

END {
  print "LEDA.GRAPH";
  print "string";
  print "short";
  print count;
  for(i = 1; i <= count; i++) {
    print "|{" names[i] "}|"
  }
  print length(edges);
  for(edge in edges) {
    print edge " 0 |{}|"
  }
}
