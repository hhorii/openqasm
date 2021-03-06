/*
 * quantum ripple-carry adder
 * Cuccaro et al, quant-ph/0410184
 */
OPENQASM 3;
include "stdgates.inc";

gate majority a, b, c {
    cx c, b;
    cx c, a;
    ccx a, b, c;
}

gate unmaj a, b, c {
    ccx a, b, c;
    cx c, a;
    cx a, b;
}

qubit cin[1], a[4], b[4], cout[1];
bit ans[5];
bit a_in[4] = "0001";  // a = 0001
bit b_in[4] = "1111";  // b = 1111
// initialize qubits
reset cin;
reset a;
reset b;
reset cout;

// set input states
for i in [0: 3] {
  if(a_in[i]) x a[i];
  if(b_in[i]) x b[i];
}
// add a to b, storing result in b
majority cin[0], b[0], a[0];
for i in [0: 2] { majority a[i], b[i + 1], a[i + 1]; }
cx a[3], cout[0];
for i in [2: -1: 0] { unmaj a[i],b[i+1],a[i+1]; }
unmaj cin[0], b[0], a[0];
measure b[0:3] -> ans[0:3];
measure cout[0] -> ans[4];
