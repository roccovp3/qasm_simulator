qreg a;qreg c;creg b;creg d; //test
h a;

h c;
measure a -> b;
measure c -> d;


