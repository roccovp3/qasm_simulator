//this is a comment
qreg q[0]; //create a qubit to operate on
creg c[0]; //classical bit register to store measurement

h q[0];

measure q[0] -> c[0];
