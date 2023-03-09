//this is a comment
qreg q[1];
creg c[1];
qreg q[0];
creg c[0];
h q[1];
sdg q[1];
tdg q[1];
h q[0];
sdg q[0];
tdg q[0];
t q[0];
h q[0];
t q[1];
u(pi/  2, pi /  2, pi /2) q[0];
h q[1];
measure q[1] -> c[1];
measure q[0] -> c[0];
