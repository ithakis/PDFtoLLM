that the Longstaﬀ-Schwartz algorithm is powerful yet simple enough to price multi-
dimensional path-dependence interest rate products such as Bermudan swaption.
S
σ
T
FD American
LS American
Analytical European
Diﬀerence
16
0.25
1
4.153
4.069
3.653
0.084
16
0.25
2
4.294
4.258
3.583
0.037
16
0.45
1
5.035
5.080
4.853
-0.045
16
0.45
2
5.593
5.801
5.381
-0.208
18
0.25
1
2.652
2.610
2.399
0.041
18
0.25
2
2.975
2.970
2.581
0.005
18
0.45
1
3.890
3.997
3.832
-0.107
18
0.45
2
4.575
4.876
4.555
-0.301
20
0.25
1
1.610
1.596
1.492
0.013
20
0.25
2
2.031
2.055
1.826
-0.024
20
0.45
1
3.175
3.114
3.007
0.061
20
0.45
2
3.973
4.125
3.861
-0.152
22
0.25
1
0.933
0.925
0.886
0.007
22
0.25
2
1.367
1.403
1.274
-0.036
22
0.45
1
2.439
2.408
2.349
0.031
22
0.45
2
3.339
3.468
3.279
-0.129
Table 4.1: Comparison of Finite Diﬀerence and Longstaﬀ-Schwartz algorithm
As always, S denotes the spot price, T denotes the maturity and σ denotes the
volatility.
Other parameters in this comparison are interest rate r = 0.05, strike
price K = 20. The ‘Diﬀerence’ column refers to the diﬀerence in early exercise value
between two methods and early exercise value is the diﬀerence between American
option value and analytical European option value. The beneﬁt of employing the
Longstaﬀ-Schwartz algorithm here may not be so obvious, indeed, the major strength
of Longstaﬀ-Schwartz algorithm is to price multi-dimensional path dependent prod-
ucts; a detailed example of this case is in Section 5.2.2.
27
