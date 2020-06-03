# special functions, initializations

print "1", 2;
print -1;

A = zeros(7);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(7);   # create 10x10 matrix filled with ones on diagonal and zeros elsewher

x = 4;
y = 2;

x += y;

y = 3;
print x;
print y;

print B.*I;
print A.+I;

print 1 - 2;

E1 = [ [ 1, 2, 3],
       [ 4, 5, 6],
       [ 7, 8, 9] ];

A = -B;
A[1,3] = A[1,2] + 3 ;

print A;

print A';

print 1 <= 2;

N = 10;
M = 20;
for i = 1:N {
    for j = i:M {
        print i, j;
    }
}


k = 15;

while(k>0) {
    if(k<5)
        print 1;
    else if(k<10)
        print 2;
    else
        print 3;
    k = k - 1;
}
