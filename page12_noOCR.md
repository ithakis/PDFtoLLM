Solving (2.5) with B(T, T) = 0 gives
B(t, T) = 1 −e−k(T−t)
k
.
(2.6)
Substituting (2.6) into (2.4) gives
A(T, T) −A(t, T) =
Z T
t
h
θ(u)B(u, T) −σ2B(u, T)2
2
i
du.
(2.7)
Solving (2.7) with A(T, T) = 0 leads to
A(t, T) =
Z T
t
h
−θ(u)B(u, T) + σ2B(u, T)2
2
i
du.
(2.8)
Fitting the observed initial forward price f ∗(0, T) results
f ∗(0, T) = −∂
∂T log P ∗(0, T) = −AT(0, T) + BT(0, T)r0,
(2.9)
where AT, BT denote the ﬁrst derivative of A, B with respect to T.
From (2.6) and (2.8) respectively, it is easy to, diﬀerentiating with respect to T, get
BT = e−k(T−t),
and
AT
=
∂
∂T
 Z T
t
h
−θ(u)B(u, T) + σ2B(u, T)2
2
i
du

=
−θ(T)B(T, T) + σ2B(T, T)2
2
+
Z T
0

−θ(u)BT(u, T) + σ2BT(u, T)B(u, T)

du
=
Z T
0

−θ(u)BT(u, T) + σ2BT(u, T)B(u, T)

du.
Hence (2.9) becomes
f ∗(0, T)
=
r0BT(0, T) −AT(0, T)
=
r0e−kT −σ2
k
Z T
0
e−k(T−u)(1 −e−k(T−u))du +
Z T
0
θ(u)e−k(T−u)du
=
r0e−kT −σ2
2k2(1 −e−kT)2 +
Z T
0
θ(u)e−k(T−u)du
=
r0e−kT −σ2
2 B(0, T)2 +
Z T
0
θ(u)e−k(T−u)du
Setting
x(T) =: r0e−kT +
Z T
0
θ(u)e−k(T−u)du,
6
