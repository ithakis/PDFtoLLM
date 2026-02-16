Markov Functional Market Model
and Standard Market Model
Tiantang Sun
St Hugh’s College
University of Oxford
A dissertation submitted in partial fulﬁllment for the degree of
Master of Science in Mathematical and Computational Finance
Trinity 2008


This dissertation is dedicated to
My parents


Acknowledgements
First of all, I would like to thank Dr. Ben Hambly for taking me to do
this project. His supervision of the project as well as his comments on
the draft has been invaluable. Of course, it goes without saying that his
ﬁxed income lectures during the master course were also excellent.
There are also many friends who I want to thank for their help throughout
the master course at Oxford, particularly my thanks goes to Wu Chen and
Li Shanshan for their continuous encouragement and support on both my
study and job seeking. I thank Jonathan Buckler for being a nice ﬂatmate
and for his help on checking the grammar and spelling. Also, I would like
to express my thanks to Matthew Clarke, who is a Manchester alumnus
of mine, for his comment on the draft of the paper and for, simply, being
a great friend at Oxford.
Last, but not least, I would like to thank my parents for their understand-
ing, trust and more importantly for their love.


Abstract
The introduction of so called Market Models (BGM) in 1990s has devel-
oped the world of interest rate modelling into a fresh period. The obvious
advantages of the market model have generated a vast amount of research
on the market model and recently a new model, called Markov functional
market model, has been developed and is becoming increasingly popular.
To be clearer between them, the former is called standard market model
in this paper.
Both standard market models and Markov functional market models are
practically popular and the aim here is to explain theoretically how each
of them works in practice. Particularly, implementation of the standard
market model has to rely on advanced numerical techniques since Monte
Carlo simulation does not work well on path-dependent derivatives. This
is where the strength of the Longstaﬀ-Schwartz algorithm comes in. The
successful application of the Longstaﬀ-Schwartz algorithm with the stan-
dard market model, more or less, adds another weight to the fact that the
Longstaﬀ-Schwartz algorithm is extensively applied in practice.


Contents
1
Introduction
1
2
Interest Rate Modelling
4
2.1
Short rate modelling
. . . . . . . . . . . . . . . . . . . . . . . . . . .
4
2.2
HJM modelling framework . . . . . . . . . . . . . . . . . . . . . . . .
7
2.3
Standard market model . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.3.1
LIBOR market model (LMM) . . . . . . . . . . . . . . . . . .
11
2.3.2
Existence of arbitrage-free strong Markov market model
. . .
13
2.3.3
Change of Numeraire . . . . . . . . . . . . . . . . . . . . . . .
14
2.3.4
Valuation in the standard market model
. . . . . . . . . . . .
15
3
Markov functional market model
18
3.1
Deﬁnition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
3.2
Implying the functional form of the numeraire . . . . . . . . . . . . .
20
3.3
Swap Markov functional model
. . . . . . . . . . . . . . . . . . . . .
22
4
Longstaﬀ-Schwartz algorithm
25
4.1
Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
25
4.2
Valuation algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
4.3
A numerical example . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
5
Model implementation and numerical result
28
5.1
Bermudan swaption . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
5.2
Implementation of LMM . . . . . . . . . . . . . . . . . . . . . . . . .
29
5.2.1
Simulating the LIBOR rate
. . . . . . . . . . . . . . . . . . .
29
5.2.2
LongstaﬀSchwartz algorithm
. . . . . . . . . . . . . . . . . .
30
5.3
Implementation of Markov Functional model . . . . . . . . . . . . . .
31
5.3.1
Polynomial ﬁtting . . . . . . . . . . . . . . . . . . . . . . . . .
32
5.3.2
Integrating against Gaussian . . . . . . . . . . . . . . . . . . .
32
i


5.3.3
Expectation calculation
. . . . . . . . . . . . . . . . . . . . .
33
5.3.4
Non-parametric implementation . . . . . . . . . . . . . . . . .
33
5.3.5
Numerical results . . . . . . . . . . . . . . . . . . . . . . . . .
34
6
Conclusion
35
Bibliography
37
ii


Chapter 1
Introduction
The trading volume in interest rate derivatives, in both the over-the-counter (OTC)
and exchange-traded markets, has been growing rapidly since the 1980s. Pricing inter-
est rate derivatives accurately, however, is usually more diﬃcult than valuing equity
and foreign exchange derivatives; one of the reasons is because an individual interest
rate has a more complicated behaviour than that of a stock price or an exchange
rate. It is, thus, fundamentally important to model interest rate, the non-traded un-
derlying asset in the ﬁxed income market, eﬀectively in the hope of correctly pricing
its derivatives. Traditionally, there are three perspectives in modelling interest rates,
namely, short rate models, instantaneous forward rate modelling and market models.
So far, there has been a large number of classical short rate models, such as Va-
sicek Model [37], Cox, Ingersoll & Ross (CIR) Model [9], Ho-Lee Model [17] and
Hull-White-Vasicek Model [18], which have attracted much attention from both the
academic and practitioners due to their tractability and transparency (see Section
2.1). As a result, short rate models have been widely used and it is still being popu-
lar in the banking industry. On the other hand, most short rate models involve only
one source of uncertainty, namely one-factor short rate models, making all rates per-
fectly correlated and hence they are not accurate in modelling shifts in the yield curve
that are signiﬁcantly diﬀerent at diﬀerent maturities [38].This drawback of the short
rate model tends to be more obvious for complex products which may well depend on
the diﬀerence between yields of diﬀerent maturities; even though extended two-factor
short rate models can, to some extent, allow for a richer yield curve structure, there
is another more severe weakness of short rate models. The volatility structure in the
short rate models, after being made time-dependent, is nonstationary, which, conse-
quently, leads to model calibration inconsistent; this apparently is signiﬁcant from a
practical point of view [19].
A major breakthrough in arbitrage-free modelling of interest rate was the approach
1


to the term structure modelling proposed in [16] by Heath, Jarrow and Morton and it
is now often referred to as the HJM modelling framework. The distinguishing feature
of the HJM framework is that it covers a large number of previously proposed models
and that instead of modelling a short-term interest rate, instantaneous forward rates
are modelled; hence the diﬃculty of calibration that short rate models have is resolved
naturally [39]. Though it is even possible to take real data for the random movement
of the forward rates and incorporate into pricing derivatives, a vital weakness of the
HJM modelling framework is that it can be relatively ineﬃcient to price derivatives
especially for callable products, as it requires a certain degree of smoothness with
respect to the tenor of the bond prices and their volatilities [38](see Section 2.2).
An alternative way of modelling interest rates in an arbitrage-free bond market that
has been increasingly popular is to take market traded rates as the underlying vari-
ables in the model. The foundation of this construction was built in [35] where the
focus was on the eﬀective annual interest rate. The idea was further developed in [6]
by Brace, Gatarek and Musiela focusing directly on modelling forward LIBORs, which
is often considered as a milestone in so called the Market Model. In the meantime,
similar development was independently done in [26] by Jamshidian but more attention
instead was paid to modelling swap rates. Generally speaking, Market Models, also
known as BGM models, are essentially arbitrage-free term structure models which
are formulated directly in terms of market observable rates, like LIBORs and swap
rates, their volatilities and correlations. By enforcing the log-normality of the for-
ward LIBOR (or swap) rate under the corresponding forward martingale measure,
market models are then compatible with the common practice of pricing standard
ﬁxed income products, such as caps and swaptions, through justiﬁed Black’s formula
(see Section 2.3.4).
Whereas it is easy to specify the standard Market Models so as to have market prices
ﬁtted exactly and model calibration is therefore trivial, Market Models do have a
rather undesirable characteristic. To accurately implement a Market Model, it has to
be done by Monte Carlo simulation because of the high dimensionality of the model
caused by each LIBOR (or swap) rate typically having its own stochastic driver [23].
This is consequently problematic for pricing even non-callable, path-dependent prod-
ucts since it is computationally expensive to generate enough Monte Carlo paths to
get a suﬃciently accurate price so that the ‘Greeks’ (risk sensitivities) will be ac-
curately usable in risk management. Not surprisingly, this problem becomes more
serious for callable products because simulation is usually poor in performing calcu-
lations backwards in time. Moreover, in the case of currencies, such as Yen, with very
2


low interest rates, market option prices cannot be simply given by Black’s formula,
consequently, calibrating Market Models is almost as cumbersome as the case of short
rate models (see, for example, [1]).
By now, there have been several approaches proposed to overcome the practical dif-
ﬁculties standard Market Models face (see, for example, [33] [13] [27]). This paper
partially focuses on another recent developed model which cannot only ﬁt the observed
prices of liquid instruments similarly as in the standard Market Models but which also
enjoys a low-dimensional property in pricing derivatives. This approach, primarily
proposed in [24] [21] [20], is termed the Markov-Functional Market Model since
its deﬁning characteristic is that zero-coupon bond (ZCB), also called pure discount
bond, prices are at any time a function of some low-dimensional Markovian process
in some martingale measure. This then implies an eﬃcient implementation as it need
only track the driving Markov process. The second main goal of this paper lies on
explaining the usage of the Longstaﬀ-Schwartz algorithm [29], one of the most
successful algorithms developed to price American style products, together with the
standard Market Model to price high dimensional ﬁxed income instruments .
The organisation of this paper is as follows. While the ﬁrst two sections of Chapter 2
are devoted to concisely describing short rate modelling and the HJM approach, sec-
tion 3 examines the standard Market Model with more details. Though it is possible
to use the Markov-Functional Market Model to price European style products, the
focus of whole Chapter 3 is predominatingly on pricing multi-temporal (such as Amer-
ican style) products. Chapter 4 succinctly describes the famous Longstaﬀ-Schwartz
algorithm which is a powerful tool in pricing multi-temporal products, indicating
that the implementation of the standard market model pricing complex interest rate
derivatives is indeed possible. In Chapter 5, implementation of the standard market
model and the Markov-Functional Market Model will be presented with some nu-
merical results, pricing a Bermudan swaption as an example, in order to make the
theoretical comparison into numerical. Finally, the conclusion is in Chapter 6.
3


Chapter 2
Interest Rate Modelling
2.1
Short rate modelling
The class of short rate models is, in fact, a special case of arbitrage-free models of the
term structure for which the short rate (rt)t≥0 is, in the risk neutral measure Q , a
(time-inhomogeneous) Markov process [22]. Normally, though not necessarily, short
rate models are driven by a univariate Brownian motion and this class of models,
due to their convenient numerical implementation property, has been signiﬁcantly
important historically.
Almost all the short rate models are speciﬁed through a stochastic diﬀerential equa-
tion (SDE)
drt = µ(t, r)dt + σ(t, r)dWt,
where W is a Brownian motion in the risk neutral measure Q and functions µ and
σ are carefully chosen to make the model particularly tractable, in a sense that the
solution process is, most often, a Gaussian process and therefore the model can be
analytically developed further, and arbitrage-free.
By the risk neutral pricing formula, the price of a zero-coupon bond (ZCB) P(t, T),
maturing at T, at time t (t < T) is given by
P(t, T) = EQ
h
exp
 −
Z T
t
rs ds
 Ft
i
,
(2.1)
where Ft is the augmented natural ﬁltration generated by the Brownian motion W.
The Markov property of r ensures that (2.1) is a function of the triple (rt, t, T) for
all pairs (t, T). In other words, the state of the market at t is completely determined
by the pair (rt, t). It is this property that allows one to price derivatives by most
standard numerical methods such as simulation and ﬁnite-diﬀerence algorithms (see
4


[10] [11] [15] in this regard). A simpliﬁed version of the Hull-White-Vasicek (HWV)
model takes the form
drt =
 θ(t) −krt

dt + σdWt,
(2.2)
where k, σ are constants but θ, the mean reversion level, is a deterministic function
of time. This simpliﬁed form is a suitable candidate for a quick example showing the
imperfect calibration property of the short rate models as well as the tractability of
short rate models in terms of the exsitence of close-form bond prices.
Theorem 2.1. The bond prices in short rate model with
µ(t, r) = α(t)r + β(t),
σ2(t, r) = γ(t)r + δ(t),
are of the form
P(t, T) = exp

A(t, T) −B(t, T)rt

,
(2.3)
where equations A(t, T) and B(t, T), respectively, satisfy
At −βB + 1
2δ(t)B2 = 0,
and
Bt + α(t)B −1
2γ(t)B2 + 1 = 0.
At, Bt denote the ﬁrst derivative of A, B with respect to t, with the boundary condtions
A(T, T) = 0, B(T, T) = 0.
By Theorem 2.11, in the simpliﬁed HWV model, it immediately follows that
α(t) = −k,
β(t) = θ(t).
γ(t) = 0,
δ(t) = σ2.
Whence for equations A and B they become
At = θ(t)B(t, T) −1
2σ2B(t, T)2,
(2.4)
Bt = kB(t, T) −1.
(2.5)
1For the proof of this standard result see, for example, Chapter 21 of [5] or Chapter 3 of [7]
5


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


then
x(T) = f ∗(0, T) + σ2
2 B(0, T)2.
(2.10)
Observe that
dx
dT = −kr0e−kT + θ(T) −k
Z T
0
θ(u)e−k(T−u) du = −kx(T) + θ(T),
i.e.
θ(T) = dx
dT + kx(T).
So using (2.10) gives
θ(T)
=
∂
∂T
 f ∗(0, T) + σ2
2 B(0, T)2
+ k

f ∗(0, T) + σ2
2 B(0, T)2
=
f ∗
T(0, T) + σ2BT(0, T)B(0, T) + k

f ∗(0, T) + σ2
2 B(0, T)2
.
Thus even in this simpliﬁed case, {θ(t)}0≤t≤T could be found but not so straight-
forwardly from observed forward rate curve and hence bond prices will match the
observed market prices at anytime t∗, t∗= 0 in this case, before the maturity. In
practice, to better calibrate the model, k, σ will be allowed to be time-dependent as
well; consequently calibration would have to employ numerical techinques which are
often computationally intensive and unstable. Nevertheless, substituting the expres-
sion for θ into (2.8), simplifying algebraically, gives
A(t, T) = log
P ∗(0, T
P ∗(0, t)

+ B(t, T)f ∗(0, t) −σ2
4kB(t, T)2(1 −e−2kt).
(2.11)
Whence the close-form of ZCB price, in this special case, follows naturally by substi-
tuting (2.11) into (2.3)
P(t, T) = P ∗(0, T)
P ∗(0, t) exp

B(t, T)f ∗(0, t) −σ2
4kB(t, T)2(1 −e−2kt) −rtB(t, T)

,
where B(t, T) can be found from (2.6) and P ∗(0, T), P ∗(0, t) are usually observable
from the market.
2.2
HJM modelling framework
The HJM modelling framework relies on exogenously specifying the dynamics of in-
stantaneous continuously compounded forward rates f(t, T). For any ﬁxed maturity
T < T ∗, the dynamics of the forward rate f(t, T) are
df(t, T) = α(t, T)dt + σ(t, T)dWt,
7


where α(t, T) ∈R, σ(t, T) ∈Rd are adapted stochastic processes and W is a d-
dimensional standard Brownian motion with respect to the underlying real probability
measure P. It is also assumed that
Z T
0
α(t, T) dt < ∞,
and
Z T
0
σ2
i (t, T) dt < ∞
∀1 ≤i ≤d.
Hence, it is equivalent, for every ﬁxed T < T ∗where T ∗> 0 is the horizon date, to
have
f(t, T) = f(0, T) +
Z t
0
α(s, T) ds +
Z t
0
σ(s, T) dWs,
(2.12)
for some Borel-measurable function f(0, ·) : [0, T ∗] →R and stochastic processess
α(·, T) and σ(·, T). It is worthwhile noticing that in the HJM setting, for any ﬁxed
maturity T < T ∗, the initial condition f(0, T) is determined by the current yield
curve, which can be estimated using observed market prices of bonds and/or other
relevant instruments; this is exactly why calibration in this setting becomes trivial.
As in Section (2.1), P(t, T) denotes the price at time t < T of a unit ZCB maturing
at time T < T ∗. By the deﬁnition of the forward rate, P(t, T) can be recovered from
the formula
P(t, T) = exp

−
Z T
t
f(t, u) du

.
(2.13)
Theorem 2.2 (HJM Drift Condition Theorem). In the HJM forward rate modelling
framework, the bond market is arbitrage free under the risk neutral measure Q if
α(t, T) = σ(t, T) ·
Z T
t
σ(t, s) ds
∀0 ≤t ≤T.
(2.14)
A more general form of this result is
α(t, T) =
d
X
i=1

σi(t, T) ·
Z T
t
σi(t, s) ds

∀0 ≤t ≤T,
(2.15)
where d is the number of stochastic drivers.
Proof. The proof2 of (2.14) begins with deriving the bond prices dynamics in the real
measure P.
It is easy to see that (2.13) can also be written in the following two forms
log P(t, T) = −
Z T
t
f(t, u) du,
(2.16)
2Proving (2.15) is relatively straightforward based on proof of (2.14)
8


−
Z t
0
f(0, u) du = log P(t, T) +
Z T
t
f(0, u) du.
(2.17)
Substituting (2.12) into (2.16) gives
log P(t, T)
=
−
Z T
t
f(t, u) du
=
−
Z T
t

f(0, u) +
Z t
0
α(s, u) ds +
Z t
0
σ(s, u) dWs

du
=
−
Z T
t
f(0, u) du −
Z T
t
Z t
0
α(s, u) ds du −
Z T
t
Z t
0
σ(s, u) dWs du.
Then substituting (2.17) into the above expression gives
log P(t, T)
=
−
Z T
t
f(0, u) du −
Z T
t
Z t
0
α(s, u) ds du −
Z T
t
Z t
0
σ(s, u) dWs du
=
Z t
0
f(0, u) du −
Z T
0
Z t
0
α(s, u) ds du +
Z t
0
Z t∧u
0
α(s, u) ds du
+ log P(0, T) −
Z T
0
Z t
0
σ(s, u) dWs du +
Z t
0
Z t∧u
0
σ(s, u) dWs du.
By Fubine’s Theorem
Z T
0
Z t
0
α(s, u) ds du =
Z t
0
Z T
s
α(s, u) du ds,
Z T
0
Z t
0
σ(s, u) dWs du =
Z t
0
Z T
s
σ(s, u) du dWs.
Hence
log P(t, T)
=
Z t
0
f(0, u) du +
Z t
0
Z t∧u
0
α(s, u) ds du +
Z t
0
Z t∧u
0
σ(s, u) dWs
|
{z
}
⋆
du
+ log P(0, T) −
Z t
0
Z T
s
α(s, u) du ds −
Z t
0
Z T
s
σ(s, u) du dWs
Note that ⋆= f(u, u) = ru therefore
log P(t, T)
=
log P(0, T) +
Z t
0
ru du −
Z t
0
Z T
s
α(s, u) du ds −
Z t
0
Z T
s
σ(s, u) du dWs
:=
log P(0, T) +
Z t
0
ru du +
Z t
0
A(s, T) ds +
Z t
0
S(s, T) dWs
Now write P(t, T) = elog P(t,T) = eXt and applying Itˆo formula gives
dP(t, T)
=
eXtdX + 1
2eXtd < X >t
=
P(t, T)

rt + A(t, T)dt + S(t, T)dWt

+ 1
2P(t, T)||S(t, T)||2dt
9


Hence in the HJM setting, the bond prices dynamics follow
dP(t, T) = P(t, T)

rt + A(t, T) + 1
2||S(t, T)||2
dt + P(t, T)S(t, T)dWt,
(2.18)
where A(t, T) = −
R T
t α(t, s) ds and S(t, T) = −
R T
t σ(t, s) ds.
It is important to note that the truth of (2.18) is independent of the measure used,
then under the risk neutral measure Q, where the discounted bond prices are mar-
tingales, the bond prices have the short rate r as the drift. Namely, under Q (2.18)
is reduced to
dP(t, T) = P(t, T)

r(t)dt + S(t, T) · d ˜Wt

,
(2.19)
where ˜Wt is a Q-martingale. Meanwhile, it is also true, under Q, to have
A(t, T) + 1
2 ||S(t, T)||2 = 0.
Equivalently
−
Z T
t
α(t, s) ds + 1
2
Z T
t
σ(t, s) ds ·
Z T
t
σ(t, s) ds = 0.
Diﬀerentiating w.r.t T gives the result
α(t, T) = σ(t, T) ·
Z T
t
σ(t, s) ds
It is, thus, obvious to see that in an arbitrage-free market the drift of the forward
rate is completely determined by the volatility. This, however, causes some paths of
forward rate, except some special cases where the coeﬃcient σ follows a deterministic
function, to explode if log-normality is embedded in forward rates [36]. That is to
say the HJM framework can easily lead to non-Markovian forward rate models, which
strongly limits its practical application in pricing interest rate derivatives.
2.3
Standard market model
The introduction of market models presented an extraordinarily fresh way of thinking,
one that directly models the market interest rates. As a result, when the option price
is given by Black’s formula (see Section 2.3.3), the link between the SDE governing
the evolution of the appropriate market interest rates and the terminal distributions
of these rates is clear; this deduces an easy speciﬁcation of market models such that
they can exactly match market prices [22]. Describing LIBOR market model serves
as a good example of explaining standard market models since that was what the
ﬁrst market models did.
10


2.3.1
LIBOR market model (LMM)
Let T0 < T1 < . . . < Tn be a sequence of ﬁxed dates for i = 1, . . . , n and δi = Ti−Ti−1,
the corresponding forward LIBORs are deﬁned as
Li(t) = P(t, Ti−1) −P(t, Ti)
δP(t, Ti)
.
(2.20)
To be able to use P(·, Tn) as a numeraire later, deﬁne
˜Pi(t) := P(t, Ti)
P(t, Tn)
∀i = 0, 1, . . . , n
(2.21)
and
πi(t) :=
iY
j=1
(1 + δjLj(t)).
(2.22)
In (2.22), since the product over the empty set is unity so π0 = 1. For convenience,
without loss of generality, also deﬁne ˜Pn+1 ≡1 and Ln+1 ≡0. Then from (2.20) and
(2.21) it immediately follows that
˜Pi(t) =

1 + δi+1Li(t)

˜Pi+1(t).
(2.23)
Furthermore by using (2.22)
˜Pi(t) =
n
Y
j=i+1
 1 + δjLj(t)

= πn(t)
πi(t) .
Let {W i
t }t≥0, i = 1, . . . , n, be a set of n correlated Brownian motions, with dW i
t dW j
t =
ρijdt, under the forward measures F where, if choose P(t, Tn) as a numeraire, all the
tradable discounted by P(t, Tn) are martingales, namely, all ˜Pi(t) are martingales.
Then under F,the forwrad LIBORs Li(t) must satisfy
dLi(t) = µi(t, L)Li(t)dt + σi(t)Li(t)dW i
t .
(2.24)
Since ˜Pi(t) are martingales under F, applying Itˆo to (2.23) gives
d ˜Pi(t) = [1 + δi+1Li+1(t)]d ˜Pi+1(t) + δi+1 ˜Pi+1(t)dLi+1(t) + δi+1d ˜Pi+1(t)dLi+1(t)(2.25)
Then substituting (2.24) into (2.25) yields
d ˜Pi(t)
=
[1 + δi+1Li+1(t)]d ˜Pi+1(t) + δi+1 ˜Pi+1(t)

µi+1(t, L)Li+1(t)dt + σi+1(t)Li+1(t)dW i+1
t

+ δi+1σi(t)Li+1(t)dW i+1
t
d ˜Pi+1
=
[1 + δi+1Li+1(t)]d ˜Pi+1(t) + δi+1 ˜Pi+1(t)σi+1(t)Li+1(t)dW i+1
t
+ δi+1 ˜Pi+1(t)µi+1(t, L)Li+1(t)dt + δi+1σi+1(t)Li+1(t)dW i+1
t
d ˜Pi+1
11


Thus for d ˜Pi(t) to be a martingale, it requires,∀i = 0, · · · , n −1,
d ˜Pi(t) =
 1 + δi+1Li(t)

d ˜Pi+1(t) + δi+1 ˜Pi+1(t)σi+1(t)Li+1(t)dW i+1
t
(2.26)
and
δi+1 ˜Pi+1(t)µi+1(t, L)Li+1(t)dt + δi+1σi+1(t)Li+1(t)dW i+1
t
d ˜Pi+1 = 0,
i.e.
µi+1(t, L) ˜Pi+1(t)dt = −σi+1(t)dW i+1
t
d ˜Pi+1.
(2.27)
Now multiplying (2.26) by πi(t), by backward induction, gives
πi(t)d ˜Pi(t)
=
πi(t)
 1 + δi+1Li(t)

d ˜Pi+1(t) + πi(t)δi+1 ˜Pi+1(t)σi+1(t)Li+1(t)dW i+1
t
=
πi+1(t)d ˜Pi+1(t) +

πi+1(t)
1 + δi+1Li+1(t)

δi+1Li+1(t) ˜Pi+1(t)σi+1(t)dW i+1
t
=
n
X
j=i+1
πj(t) ˜Pj(t)

δjLj(t)
1 + δjLj(t)

σj(t)dW j
t
thus
d ˜Pi(t) = ˜Pi(t)
n
X
j=i+1
πj(t) ˜Pj(t)
πi(t) ˜Pi(t)

δjLj(t)
1 + δjLj(t)

σj(t)dW j
t ,
i.e.
d ˜Pi(t) = ˜Pi(t)
n
X
j=i+1

δjLj(t)
1 + δjLj(t)

σj(t)dW j
t .
(2.28)
Now substituting (2.28) into (2.27), by backward induction again, yields
µi(t, L) ˜Pi(t)dt = −σi(t)dW i
t ˜Pi(t)
n
X
j=i+1
δjLj(t)
1 + δjLj(t)σj(t)dW j
t .
Then the drift condition in LMM is
µi(t, L) = −
n
X
j=i+1

δjLj(t)
1 + δjLj(t)

σi(t)σj(t)ρij.
Finally, the original SDE (2.24) becomes
dLi(t) =
h
−
n
X
j=i+1

δjLj(t)
1 + δjLj(t)

σi(t)σj(t)ρij
i
Li(t)dt + σi(t)Li(t)dW i
t .
(2.29)
The procedure for deriving the swap-rate market models (SMM) is identical to that
for LIBOR market models except that the algebra is slightly more complicated. The
12


result is stated below (for a detailed derivation see Chapter 18 of [22]).
For each i = 1, · · · , n, the forward par swap rates yi, in the forward measure F, satisfy
the SDE of the form
dyi
t = −

n
X
j=i+1
Γj−1
t
˜P j
t
Γi−1
t
˜P i
t
 δj−1yj
t
1 + δj−1yj
t

σi
tσj
tρij

yi
tdt + σi
tyi
tdW i
t ,
(2.30)
where as always P(t, T) denotes ZCBs, dW i
t dW t
i = ρijdt
and
˜P i
t :=
n
X
j=i
δj
P(t, Tj)
P(t, Tn),
and, for 1 ≤i ≤n
yi
t := P(t, Ti−1) −P(t, Tn)
Pn
j=i δjP(t, Tj)
,
Γi
t :=
iY
j=1
(1 + δjyj+1
t
).
Also, ˜P n+1 ≡yn+1 :≡0 and Γ0 ≡1.
2.3.2
Existence of arbitrage-free strong Markov market model
To show that the market model is strong Markov and consistent with a full arbitrage-
free term structure model, a few general SDE theories are stated below. These results
are so classical that almost any Stochastic Calculus text contains their proof, see, for
example, [22] [28]
Deﬁnition 2.3. On a ﬁltered probability space (Ω, {Ft}, F, P), Rn is adapted to {Ft}.
X is a strong Markov process if, given any almost surely (a.s.) ﬁnite {Ft} stopping
time τ, any Γ ∈B(Rn), and any t ≥0,
P(Xτ+t ∈Γ|Fτ) = P(Xτ+t ∈Γ|Xτ)
a.s.
(2.31)
An equivalent formulation to (2.31) is the following standard result which is ap-
pealing when verifying the strong Markov property.
Theorem 2.4. The process X is strong Markov if and only if, for a.s. ﬁnite {Ft}
stopping times τ and all t > 0,
E[f(Xτ+t)|Fτ] = E[f(Xτ+t)|Xτ]
(2.32)
for all bounded continuous functions f.
13


In fact, the strong Markov property of the solution process for a locally Lipschitz
SDE (σ, b) is inherited from the strong Markov property of the driving Brownian
motion. The following theorem conﬁrms this connection.
Theorem 2.5. If the SDE (σ, b) is locally Lipschitz and let (Ω, {Ft}, F, P, W, X) be
some solution. Then the solution process X is strong Markov, i.e. (2.32) holds, for
all bounded continuous functions f and all a.s. ﬁnite Ft stopping time τ.
The following theorem shows that there are indeed processes L and y satisfying
the SDE (2.29) and (2.30) and hence it is a necessary condition for the model to be
arbitrage-free.
Theorem 2.6. Suppose that, for i = 1, · · · , n, the functions σi : Rn × R →R are
bounded on any time interval [0, t]. Then strong existence and pathwise uniqueness
hold for the SDE (2.29) and (2.30). Furthermore, the solution processes L and y are
strong Markov processes.
The suﬃcient condition is easily veriﬁed by noting that from (2.28) ˜Pi can be
written as a Dolean exponential,
˜Pi(t) = ˜Pi(0) exp
 Z t
0
n
X
j=i+1
 δjLj(s)
1 + δjLj(s)

σj(s)dW j
s

and similarly for SMM
˜P i
t = ˜P i
0 exp
 Z t
0
n
X
j=i+1
Γj−1
s
˜P j
s
Γi−1
s
˜P i
s
 δj−1yj
s
1 + δj−1yj
s

σj
sdW j
s

and observe that the exponential term has bounded quadratic variation over any time
interval [0, t], hence, by Novikov’s condition, ˜Pi(t) and ˜P i
t are indeed true martingales.
2.3.3
Change of Numeraire
Changing numeraire is a very important technique in mathematical ﬁnance and it,
most often, can dramatically simplify the calculation especially when pricing complex
products. This section gives a rather brief examination of changing numeraire which
will be used frequently throughout the rest of the paper (for details of change of
numeraire, see Chapter 9 in [36]).
A numerarie is the unit of account in which other assets are denominated [36].
In principle, any positively priced asset can be taken as a numeriare and hence all
other assets are denominated by the chosen numeraire. In a ﬁxed income market, a
convenient choice of numeraire is a ZCB maturing at time T and the associated risk
neutral measure is often called the T-forward measure.
14


Theorem 2.7 (Change of numeraire). Let N(t) be a numeraire and QN be the as-
sociated measure equivalent to the real world measure P such that the asset prices St
Nt
are QN martingales. Then for an arbitrary numeraire U, there exists an equivalent
measure QU such that any contingent claim XT has price
V (t, St) = UtEQUXT
UT
Ft

and moreover
dQU
dQN |Ft = UTN0
NTU0
,
and (S/U)t are martingales under QU.
Theorem 2.8 (Change of risk neutral measure). Let M(t) and N(t) be the prices of
two assets denominated in a common currency and let σ(t) = (σ1(t), · · · , σd(t)) and
ν(t) = (ν1(t), · · · , νd(t)) denote their respective volatility vector process:
d(D(t)M(t)) = D(t)M(t)σ(t) · dW(t),
d(D(t)N(t)) = D(t)N(t)ν(t) · dW(t),
where D(t) := exp(−
R t
0 r(s) ds) is called the discount process.
If taking N(t) as the numeraire then
dSN(t) = SN(t)[σ(t) −ν(t)] · dW N(t).
2.3.4
Valuation in the standard market model
Based on the results in the last two sections, the common market practice of pricing
vanilla style (path independent) products is to assume ∀t ∈[0, Ti], δ = Ti −Ti−1
dLi(t, Ti) = Li(t, Ti)σi(t)d ˜W i,
dyk
n(t) = yk
n(t)σn,k(t)d ˜W k
n,
where ˜W is a 1-dimensional Qi Brownian motion, and σi(t), σn,k(t) is some determin-
istic function. Then a caplet, one leg of a cap, at t ∈[0, Ti], with strike K, is priced
by
Proposition 2.9 (Black’s formula3).
Capli(t) = δP(t, Ti)

Li(t, Ti)N(d1) −KN(d2)

,
(2.33)
3proof, based on changing numeraire, is standard, see, for example,[36]
15


where
d1,2 = log Li(t,Ti)
K
± 1
2Σ2
i (t, Ti)
Σi(t, Ti)
and
Σ2
i (t, Ti) =
Z Ti
t
σ2
i (s) ds
with N being the standard normal cumulative distribution function
N(x) =
1
√
2π
Z x
−∞
e−z2/2 dz,
∀x ∈R.
Whence a cap settled in arreas at times Ti, i = 0, · · · , n where Ti −Ti−1 = δi, T0 = T
is priced, by deﬁnition,
Cap(t) =
n
X
i=1
Capli(t) =
n
X
i=1
δiP(t, Ti)

Li(t, Ti−1)N(d3) −KN(d4)

,
(2.34)
where for every i = 0, · · · , n −1
d3,4 = log Li(t,Ti−1)
K
± 1
2Σ2
i (t, Ti−1)
Σi(t, Ti−1)
and
Σ2
i (t, Ti−1) =
Z Ti−1
t
σ2
i (s) ds.
Then by cap-ﬂoor parity, which is an immediate consequence of the no-arbitrage
property,
Cap(t) −Floor(t) =
n
X
i=1
 P(t, Ti−1) −(1 + kδi)P(t, Ti)

,
the price of the ﬂoor is easily calculated.
In an almost identical fashion, Black’s formula for a payer’s swaption V for the period
between [k, n], struck at K with swap rates yk
n(t), is
V k
n (t) = Sk
n(t)(yk
n(t)N(d+) −KN(d−)),
where
d± = log yk
n(t)
K
± 1
2Σ2
k,n
Σk,n
and
Σ2
k,n =
Z Tk
t
σ2
k,n(s) ds.
Obviously, pricing non-callable ﬁxed income products by Black’s formula is just like
using the Black-Scholes formula for pricing vanilla products in the equity market. In
16


both cases, a rather simple structure of volatility of the underlying variable is a major
assumption, without which the valuation has to switch to numerical methods. While
generally this switch works relatively well in the equity market for most common
exotic products, it does not work so well in the ﬁxed income market. This is because
the full market model (i.e. SDE (2.29) or (2.30)) has to be used if the exotic product
depends on multiple market interest rates (LIBOR or swap rate) in a non-linear way,
which then leads to a very high dimensional problem. For example, pricing a 10 year
Bermudan swaption exercisable quarterly involves solving a 39-dimensional problem.
Thereby, Monte Carlo simulation, the only feasible numerical method left in this high
dimensional case, could be ineﬃcient without speciﬁc numerical technique, especially
when pricing and hedging strong path dependent products.
This practical drawback of the standard market model has generated considerable
research interest and so far it has been solved relatively well. In Section 5.2.2, it
will show how to use the Longstaﬀ-Schwartz algorithm to make the standard market
model implementation practically possible. By no means is the Longstaﬀ-Schwartz
algorithm the only way of doing this, it just, to a certain degree, tends to be more
popular than other methods proposed in [3], [2] and [8].
17


Chapter 3
Markov functional market model
Generally speaking, a ‘good’ pricing model for derivatives should, at least from a
practical perspective, have the following properties:
1. arbitrage-free;
2. well-calibrated, accurately pricing as many relevant liquid instruments as pos-
sible without overﬁtting;
3. be realistic and transparent in its properties;
4. allows an eﬃcient implementation [20].
As can be seen from Chapter 2, short rate modelling, the forward rate modelling in
the HJM framework and standard market model have not been able to meet all these
four criterion. Motivated by this observation, a general class of Markov-functional
interest rate models has been introduced and received growing attention particularly
from practitioners. It is because the Markov-Functional Market Model complements
short rate models and standard market models in a way that it allows an eﬃcient
implementation and permits accurate calibration of the model through more freedom
in choosing the functional form. In addition, the remaining freedom to specify the law
of the driving Markov process enables the model to be realistic. The vital assumption
in the Markov-Functional Market Model is that the uncertainity can be captured by
some low dimensional (time-inhomogeneous) Markov process {mt : 0 ≤t ≤α∗},
in that, for any t, the state of the economy at t is summarised via mt and clearly
this is the deﬁning feature of any practically implementable model [20]. α∗is some
time on which the value of the derivative, Vα∗, will have been determined from the
evolution of the asset prices hence only prior evolution of the economy up to α∗need
be considered.
18


3.1
Deﬁnition
Let (N, M) be a numeraire pair for the economy E where the numeraire N, itself a
price process, is of the form
Nt = Nt(mt)
0 ≤t ≤α∗
and the measure M, often called the martingale measure, is equivalent to the real
world measure P and such that (PtT/Nt) is martingale. Assume that the process m
is a Markov process under the measure M and that ZCBs are of the form
Pt,S = Pt,S(mt),
0 ≤t ≤αS ≤S
for some boundary curve αS : [0, α∗] →[0, α∗].
αS
t=T
Time t
T
Maturity T
T
Figure 3.1: Boundary curve
For almost all practical applications, the boundary curve (see Figure 3.1) is ap-
propriately chosen to be of the form
αS =
 S,
if S ≤T,
T,
if S > T,
(3.1)
for some constant T so that the model need not be deﬁned over the whole time domain
0 ≤t ≤S < ∞[20].
19


Then by the fundamental asset pricing formula the value of a derivative, with payoﬀ
VT at T, at any time t prior to α∗is given by
Vt = NtE[N −1
T VT|Ft]
(3.2)
for any t ≤T ≤α∗
Under these assumptions, it is suﬃcient to completely specify the Markov-Functional
Market Model with the knowledge of
• the law of the process m under M,
• PαSS(mαS), for S ∈[0, α∗], the functional form of the discount factors on the
boundary αS
• the functional form of the numeraire Nt(mt) for 0 ≤t ≤α∗.
That is to say it is not necessary to explicitly specify the functional form of discount
factors on the interior of the region bounded by αS. Thus, via the martingale property
for numeraire-rebased assets under M, discount factors on the interior of the region
bounded by αS can be recovered by
PtS(mt) = Nt(mt)EM
hPαSS(mαS)
NαS(mαS)
Ft
i
.
(3.3)
3.2
Implying the functional form of the numeraire
Deﬁning the payment dates for the swap associated with the rate yi by Si
j, j =
1, 2, · · · , mi; though not strictly necessary, for convenience it is assumed that, for
all i, j, either Si
j > Tn or Si
j = Tk, for some k > i.
This assumption generally
holds for many common practical products and in the case where it does not hold
one can always introduce auxiliary swap rates yk to make it hold. To construct a
one-dimensional Markov-Functional Market Model which correctly prices options on
the swaps associated with these forward rates, we need also to assume that the ith
forward rate at Ti, yi
Ti, is a monotonic increasing function of the variable mTi. To
simplify calculation, PVBP-digital swaptions, which have a simple payoﬀstructure,
are used because calibrating the model to vanilla swaptions is equivalent to calibrating
it to the inferred market prices of digital swaptions [12]. The PVBP-digital swaption
corresponding to yi, with strike K, has payoﬀat Ti of
˜V i
Ti(K) = Bi
TiI{yi
Ti>K}
20


where
Bi
t :=
n
X
j=i
δjPtSj
is called the present value of a basis point (PVBP) of the swap corresponding to
the swap rate yi and it represents the value of ﬁxed leg of the swap if the ﬁxed leg
were unity [22]. Applying (3.2), its value at time zero is given by
˜V i
0(K) = N0(m0)EM
h
ˆBi
Ti(mTi)I{yi
Ti(mTi)>K}
i
,
(3.4)
where
ˆBi
Ti(mTi) = Bi
Ti(mTi)
NTi(mTi).
Then to determine the functional form of NTi(mTi), it involves working backward
iteratively from the terminal time Tn. It is natural to assume that NTk(mTk), k =
i + 1, · · · , n, have been already determined and to assume
ˆPTiS(mTi) = PTiS(mTi)
NTi(mTi)
for relevant S > Ti, is known, having been determined by (3.3) and known (condi-
tional) distributions of mTk, k = i, · · · , n. This then implies that ˆBi
Ti is also known.
Now consider yi
Ti which can be written as
yi
Ti =
N −1
Ti −PTiSiniN −1
Ti
P i
TiN −1
Ti
.
(3.5)
Simplifying (3.5) algebraically gives
NTi(mTi) =
1
ˆBi
Ti(mTi)yi
Ti(mTi) + ˆPTiSini(mTi)
.
(3.6)
Hence, ﬁnding the functional form yi
Ti(mTi) will be suﬃcient to determine NTi(mTi).
Since yi
Ti is assumed to have monotonicity with respect to mTi, there exists a unique
value of K, say Ki(m∗), such that the following holds
{mTi > m∗} = {yi
Ti > Ki(m∗)}.
(3.7)
Now deﬁne
Ji
0(m∗) = N0(m0)EM
 ˆBi
Ti(mTi)I{mTi>m∗}

.
(3.8)
21


Then, for any given m∗, the value of Ji
0(m∗) can be calculated using the known
distribution of mTi under M. Moreover, the value of K can be found using market
prices such that
Ji
0(m∗) = ˜V i
0(K).
(3.9)
It is not hard to see that the value of K satisfying (3.9) is precisely Ki(m∗) by com-
paring (3.4) and (3.8). Finally, the functional form of yi
Ti(mTi) can be obtained by
noticing that it is equivalent to knowing Ki(m∗) for any m∗from (3.7).
Standard market practice is to use Black’s formula (Proposition 2.9) to ﬁnd swap-
tion prices V i
0(K).
In fact, the techniques above can be applied more generally,
especially for currencies with a large volatility skew, meaning volatility is highly de-
pendent on the strike K, these techniques are still applicable. This is one of the major
strengths of the Markov functional market model, working well for currencies such as
yen in which it is not suitable to model rates through a log-normal process.
3.3
Swap Markov functional model
This section takes the swap Markov functional model, suitable for pricing swap based
products, as an example to show generally how to construct the Markov-Functional
Market Model. To keep the notation simple, a special case of a cancellable swap is
considered for which the ith forward swap rate yi starts on date T1 and has coupons
precisely at dates S1, · · · , Sn with exercise times at T1, · · · , Tn. As before, denote by
δi the accrual factor for the period [Ti, Si]. Then it follows that
yi
t = PtTi −PtSn
Bi
t
,
where Bi
t is, as before, the present value of a basis point (PVBP) of the swap. It
is worthwhile to note that in this case the last par swap rate yn is just the forward
LIBOR, Ln, for the period [Tn, Sn]. To be consistent with Black’s formula, assume
that yn is a log-normal martingale under the swaption measure Sn, i.e.
dyn
t = σn
t yn
t dWt,
(3.10)
where W is a standard Brownian motion under Sn and σn is some deterministic
function. From (3.10), it is equivalent to have
yn
t = yn
0

−1
2
Z t
0
(σn
u)2 du + mt

,
22


where m, a deterministic time-change of a Brownian motion, satisﬁes
dmt = σn
t dWt.
(3.11)
That is to say m is taken as the driving Markov process of the model, which is the
ﬁrst stage to completely specify the model. As previously indicated, the boundary
curve αS, for this case, is exactly of the form in (3.1) and we only need the functional
form of PTiTi(mTi) for i = 1, 2, · · · , n, namely the unit map, and PTnSn(mTn) on the
boundary. In this case, by deﬁnition, it follows that
PTnSn(mTn) =
1
1 + δnyn
Tn
,
and this immediately yields
PTnSn =
1
1 + δnyn
0

−1
2
R t
0 (σn
u)2 du + mt
,
which then completes the second stage of specifying the swap Markov functional
market model. To ﬁnd the functional form of the numeraire P·Sn at times Ti, i =
1, · · · , n −1, we need only follow the procedures in Section 3.2. For this new model,
the value of a PVBP-digital swaption with strike K and corresponding to yi is given
by
˜V i
0(K) = P0Sn(m0)ESn
h Bi
Ti(mTi)
PTiSn(mTi)
I{yi
Ti(mTi)>K}
i
.
Assuming the market price obtained from the Black’s formua yields
˜V i
0(K) = Bi
0(m0)N(d2),
(3.12)
where
d2 = log(yi
0/K)
ˆσi√Ti
−1
2 ˆσip
Ti.
Proceeding as in Section 3.2, let m∗∈R and for i < n, evaluate by numerical
integration
Ji
0(m∗)
=
P0Sn(x0)ESn
h Bi
Ti(mTi)
PTiSn(mTi)I{mTi>m∗}
i
=
P0Sn(x0)ESn
h
ESn Bi
Ti+1(mTi+1)
PTi+1Sn(mTi+1)
FTi

I{mTi>m∗}
i
=
P0Sn(x0)
Z ∞
m∗
h Z ∞
−∞
Bi
Ti+1(u)
PTi+1Sn(u)φmTi+1|mTi (u) du
i
φmTi(v) dv
23


where φmTi denotes the transition density function of mTi and according to (3.11),
φmTi+1|mTi denotes the normal conditional density function of mTi+1 given mTi with
mean mTi and variance
R Ti+1
Ti
(σn
u)2 du .
Then
yi
Ti(m∗) = Ki(m∗),
where Ki(m∗) solves
Ji
0(m∗) = ˜V i
0(Ki(m∗)).
(3.13)
Whence, having found Ji
0(m∗) numerically, Ki(m∗) can be recovered from (3.12)
yi
Ti(m∗) = yi
0exp
h
−1
2(˜σi)2Ti −˜σip
TiN −1 Ji
0(m∗)
Bi
0(m0)
i
.
Finally, the value of PTiSn(m∗) can now be calculated by using (3.6).
Here, the focus is on the case of one-dimensional Markov process mt, which is suﬃ-
cient for most important interest rate derivatives. The generalisation to the multi-
dimension case is not diﬃcult and necessary for some particular products, for example,
Bermudan callable spread option; however working in the multi-dimensional case is
still at a relative early stage and some details can be found in [23] [22].
Since the Markov functional market model has successfully transformed the high di-
mensional standard market model into a low dimensional (1-dim here) problem, the
numerical methods do not have to rely on Monte Carlo simulation only. Numeri-
cal results of, employing one-dimensional Markov functional market model, pricing
Bermudan swaptions will be presented in Section 5.3.5.
24


Chapter 4
Longstaﬀ-Schwartz algorithm
The Longstaﬀ-Schwartz algorithm is, so far, arguably the most widely adopted method
for pricing multi-dimensional American-style ﬁnancial instruments in both equity and
ﬁxed income market. This is mainly because on one hand it can be applied to a
large number of common exotic derivatives; on the other hand it has been demon-
strated that it is rather eﬀective in numerical implementation (see, for instance, [25]
[32]). It is the use of least squares to estimate the conditional expected payoﬀto
the option-holders from continuation that makes the approach a worthwhile substi-
tute for traditional ﬁnite diﬀerence methods when pricing high-dimensional prod-
ucts. Discussion here focuses on describing the general valuation framework using
the Longstaﬀ-Schwartz algorithm but the argument is equally well applicable to any
speciﬁc product with some minor modiﬁcation.
4.1
Notation
As before, the framework is based on an underlying complete probability space
(Ω, F, P) with ﬁnite time horizon [0, T].
To be consistent with the no arbitrage
paradigm, it is assumed that there exists an equivalent martingale measure Q for the
economy; also deﬁne F = {Ft : t ∈[0, t]} to be the augmented ﬁltration generated
by the the relevant price processes for the securities and assume F = FT. Let K be
the strike price with discrete exercisable times 0 < t1 ≤t2 ≤· · · ≤tk = T; in case of
continuously exercisable products the method can also be used by taking suﬃciently
large K. In addition, let I(w, s; t, T) denote the path of cash ﬂows generated by the
security, conditional on the product not being exercised at or prior to time t and on
the holder of the security pursuing the optimal stopping strategy for all s, t < s ≤T.
25


4.2
Valuation algorithm
At each exercisable time tk, investors are able to know the cash ﬂow from immediate
exercise and the value of immediate exercise simply equals this cash ﬂow. Of course,
the continuation cash ﬂows are not known at tk, however, the fundamental asset
pricing formula implies that the value of continuation can be obtained by taking the
expectation, in the risk neutral measure Q , of the remaining discounted cash ﬂows
I(w, s; tk, T). More speciﬁcally, the value of continuation C(w; tk) at time tk is simply
C(w; tk) = EQ
h
K
X
j=k+1
exp
 −
Z tj
tk
r(w, s) ds

I(w, tj; tk, T) |Ftk
i
,
(4.1)
where r(w, t) is the riskless interest rate, possibly in a stochastic form. Hence, the
problem of optimal exercise is reduced to comparing the immediate exercise value
I(w, s; t, T) and the continuation value C(w; tk) in the sense that exercise occurs as
soon as I ≥C > 0. As mentioned earlier, in the Longstaﬀ-Schwartz algorithm least
squares are used, working backwards, to approximate C(w; tk) at tK−1, tK−2, · · · , t1.
To be more speciﬁc, it is assumed1 that the unknown functional form of C(w; tK−1) in
(4.1) can be expressed as a linear combination of a countable set of FtK−1 measurable
basis functions.
4.3
A numerical example
To quickly show an example of how the Longstaﬀ-Schwartz algorithm works, results
of pricing an American put option using the Longstaﬀ-Schwartz algorithm are com-
pared with that of using an implicit ﬁnite diﬀerence technique, a popular method of
great accuracy in pricing low-dimensional path dependent products.
In ﬁnite diﬀerence, 60,000 time steps and 1000 stock price steps are used to dis-
cretize the Black-Scholes PDE. The L-S simulation is based on 10,000 paths and 50
exercise points. As shown in the table, the diﬀerence between the two methods is
quite small and it is believed that the results will be even closer if more simulation
paths are used. It is worthwhile noting that the diﬀerences in early exercise value
could be either positive or negative, which indicates that Longstaﬀ-Schwartz algo-
rithm is capable of replacing the ﬁnite-diﬀerence to price path-dependent products.
This is probably why L-S algorithm is being used intensively in practice when pricing
high-dimensional path-dependent derivatives. In Chapter 5, it will become clearer
1This assumption can be formally justiﬁed, for details, see the original work [29]
26


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


Chapter 5
Model implementation and
numerical result
Having focused on the theoretical development of the standard Market Model and the
Markov Functional Market Model, we are ready to carry out model implementations
and present some numerical results, based on pricing an important ﬁxed income
derivative Bermudan swaption. The aim is to show that with the help of the Longstaﬀ-
Schwartz algorithm, implementing the standard Market Model (LMM/BGM) to price
Bermudan swaption, a high-dimensional problem, is indeed possible. Meanwhile, the
Markov functional market model, as will be seen, reaches a strong agreement with
the BGM model on valuation results.
5.1
Bermudan swaption
A ﬁnancial instrument is called Bermudan if it has multiple exercise dates, namely,
there are times Ti at which the holder of a Bermudan may choose between diﬀerent
payments or underlying products. A Bermudan swaption is a swaption that has a
maturity date equal to the last reset date of the underlying swap and that has an initial
lockout period in which exercise is prohibited.
Eﬀectively speaking, a Bermudan
swaption is equivalent to a Bermudan option on a coupon bond with strike equal to
the par value of the bond and, as an option on a coupon bond, a Bermudan swaption
clearly has positive probability of early exercise.
Let 0 = T0 < T1 < · · · < Tn = T denote a given tenor structure and V (T1, · · · , Tn; T1)
denote the price of a Bermudan swaption initiated at T1. Then by deﬁnition
V (Ti, · · · , Tn; Ti) := max
 V (Ti, · · · , Tn; Ti), ˆV (Ti, · · · , Tn; Ti)

i = 0, · · · , n
28


where ˆV (Ti, · · · , Tn; Ti) denotes the value of a swap with ﬁxing dates Ti, · · · , Tn−1
and payment dates Ti+1, · · · , Tn, observed at Ti ; and V (Tn; Tn) := 0. Moreover, with
a given numeraire N and a corresponding equivalent martingale measure QN
V (Ti+1, · · · , Tn; Ti) = N(Ti)EQNV (Ti+1, · · · , Tn; Ti+1)
N(Ti+1)
|FTi

.
5.2
Implementation of LMM
This section is to show, step by step, how to price a Bermudan swaption in LMM using
Monte Carlo simulation with the application of the Longstaﬀ-Schwartz algorithm.
The volatility structure can simply be ﬂat but more complex volatility term structure
can be obtained from principal component analysis (PCA) of correlation matrix and
adjusting to calibrated volatilities (see [34] on this topic).
5.2.1
Simulating the LIBOR rate
Recall the SDE (2.29) that LIBOR rate follows under forward measure F
dLi(t) =
h
−
n
X
j=i+1

δjLj(t)
1 + δjLj(t)

σi(t)σj(t)ρij
i
Li(t)dt + σi(t)Li(t)dW i
t .
Since Bermudan swaptions are path-dependent and SDE (2.29) cannot be integrated
exactly, the Euler-Maruyama method (Euler scheme) needs to be applied here to
simulate the LIBOR rate path [15]. For a better discretization, it is necessary to
apply the Euler scheme to log L(t); applying Itˆo’s lemma to the above SDE (2.29)
gives
d log Li(t) =
h
−
n
X
j=i+1

δjLj(t)
1 + δjLj(t)

σi(t)σj(t)ρij −σ2
i
2
i
dt + σi(t)dW i
t
which is then suitable to be discretized, using the Euler scheme, as
Li+1(t) = Li(t) exp
h
−
n
X
j=i+1

δjLj(t)
1 + δjLj(t)σj(t)ρij

σi(t)h −σ2
i
2 + σi(t)
√
hZi
t
i
where, following the same notation as in Section 2.3, i = 0, 1, · · · , n, and Z1, Z2, · · · Zn
are independent n-dimensional standard normal random vectors; h is ﬁxed time step
[14].
29


5.2.2
LongstaﬀSchwartz algorithm
When applying the Longstaﬀ-Schwartz algorithm in the process of pricing a Bermudan
swaption, the procedures are divided into the following steps.
1. Simulating a large number of paths (D) of the underlying LIBOR rates so that
values of regression coeﬃcients are smooth. To control the discretization bias
and to approximate continuous exercise, the number of simulation steps (N)
is chosen equal to the number of exercise dates. Let disc(t) be the discrete
discounting factor at time t. Consider a payer Bermudan swaption Vs,n(Ti) with
lockout date Ts exercise dates Ti, i = s, · · · , n −1, Tn = T and δ = Ti+1 −Ti
then, by deﬁnition,
Vs,n(Ti, T) =
n−1
X
k=i
P(Ti, Tk+1)δ[Lk(Ti) −K],
where Lk(Ti) is the forward LIBOR rate observed at Ti for period (Tk, Tk+1), K
is the strike price and P(Tk, Tk+1) is the ZCB price at Ti for period (Tk, Tk+1).
2. To ﬁnd the Bermudan swaption price, it is necessary to carry out dynamic pro-
gramming backward from the ﬁnal exercise time Tn−1 as a Bermudan swaption
is strongly path-dependent. Let I(Tn−1), at time Tn−1, be the maximum of the
value of exercising the option and zero, i.e.
I(Tn−1) = max(Vn−1,n(Tn−1), 0).
Furthermore, deﬁne stop rule (sr) as the optimal stopping time along a given
path (d) of the LIBOR rate process and the stop rule ﬁrstly is set equal to the
ﬁnal exercise time, sr = Tn−1.
3. Working backwards, at time Tn−1, make a regression of the basis functions of
state variables at that time on Y (d) where
Y (Tn−1) = I(sr) × disc(Ti)
disc(sr)
.
Again, stop rule (sr) is the next stopping time along a given path.
Basis
functions, denoted by Xj(Ti) j = 1 · · · J, are chosen to be quadratic func-
tions of the current value of the underlying swap Vi,n(Ti) and discounting factor
disc(Ti). Regression coeﬃcients, calculated from ordinary least square regres-
sion, of Xj(Ti) are called βj(Ti).
30


4. Then we are ready to compare the continuation value C(Ti) = P βj(Ti)Xj(Ti),
corresponding to the estimated conditional expectation of the the payoﬀ, with
the immediate exercise value I(Ti) = max(Vi,n(Ti), 0). If I(Ti) > C(Ti), then
present time is an optimal stopping time and I is set to Vi,n(Ti) and stop rule
is set to Tn−1 i.e.
I(sr) = Vi,n(Ti),
sr(d) = Tn−1.
5. Steps 3 and 4 are repeated for all (Tn−1 −1) ≤Ti ≤Ts, Ts is the lockout date,
until one reaches the ﬁrst exercise time of the swaption and all coeﬃcients βj(Ti)
have been calculated.
6. Finally, the value of the swaption can be calculated by discounting the value at
the optimal stopping time back to present time and it is calculated as
1
D
D
X
d=1
W(sr)/disc(sr).
Once again, (sr) is the variable that keeps tracking optimal stopping time along
a given path.
5.3
Implementation of Markov Functional model
The implementation of the Markov Functional model replies heavily on numerical
integration, as seen from Section 3.3, when calculating expectations. It is, however,
not advisable to apply simple numerical integration schemes such as trapezoid rule or
Simpson’s rule on a grid of ﬁxed spacing for the Markov process m because, though
yielding reasonably accurate prices, Greeks would become very unstable [30]. More-
over, such simple numerical integration scheme on a ﬁxed grid would lead to spiking
integrands, in which case the numerical integration is inaccurate when the calculation
date is approaching a ﬁxing date. To overcome these problems, Hunt and Kennedy
introduced an idea by ﬁrstly ﬁtting a polynomial to the payoﬀfunction deﬁned on the
grid and then calculate analytically the integral of the polynomial against the Gaus-
sian distribution [30]. This is better as the only error in the integration comes from
the polynomial ﬁt and the ﬁtting error can be controlled, by choosing a suﬃciently
high order of polynomial, as the integration of the polynomial is done analytically
[30].
31


5.3.1
Polynomial ﬁtting
There are many ways of ﬁtting a polynomial but in this case it is better to use Neville’s
algorithm1 as suggested in [30].
Given a number of points of mi and a set of functions values fi a polynomial that
passes through these values can be computed recursively. Let Pi,··· ,i+n denote the
polynomial deﬁned using the points mi, · · · , mi+n. Then a high order polynomial is
generated by
Pi,··· ,i+n = (m −mi+n−1)Pi,··· ,i+n + (mi −m)Pi,··· ,i+n
mi −mi+n
(5.1)
and Pi = fi. Each polynomial can then be written as Pi,··· ,i+n = Pn
k=0 ci,kmk. Using
(5.1) a recurrence formula for the coeﬃcients ci,k is as follows:
ci,n = ci,n−1 −ci+1,n−1
mi −mi+n
,
ci,k = mici+1,k −mi+nci,k + ci,k−1 −ci+1,k−1
mi −mi+n
∀k ∈[1, n −1],
ci,0 = mici+1,0 −mi+nci,0
mi −mi+n
.
5.3.2
Integrating against Gaussian
Recall the Markov process m deﬁned in (3.11)
dmt = σn
t dWt
has Gaussian density functions. Whence, calculating integrals against a Gaussian
density can be broken down to evaluating for diﬀerent powers mk of polynomial P in
the following integral
G(k; h, µ, σ) =
Z h
∞
mk exp

−1
2( m−µ
σ2 )2
σ
√
2π
dm.
Then using integration by part, the following recurrence relation 2 for G in terms of
k can be found
G(k) = µG(k −1) + (k −1)σ2G(k −2) −σ2hk−1exp

−1
2( h−µ
σ2 )2
σ
√
2π
with3 G(0) = N( h−µ
σ ) and G(−1) = 0
1for details on this algorithm see, for example, [14]
2more details can be found in [14]
3As in Proposition 2.9, N is the standard normal cumulative distribution function
32


5.3.3
Expectation calculation
Given a grid on which the Markov process is deﬁned, option values can be calculated
by taking expectations of the value function against the Gaussian density. Suppose
several option values have already been calculated at time Tn+1 at grid points mj,
then the following procedure can lead to calculating option values at time Tn for grid
points mi.
• given an order M, the approximating polynomial P(j−M/2),··· ,(j+1+M/2) for the
interval [mj, mj+1] is ﬁtted through the points mj−M/2, · · · , mj+1+M/2, where
M/2 denotes the integer division;
• Then calculate the expectation E(f(m, Tn+1)|mi) by adding the integrals of the
approximating polynomials against the Gaussian density over all the intervals
[mj, mj+1];
• ﬁnally, doing this for all mi [30].
The ﬁtting of polynomials generally works well for approximating smooth function.
Some option payoﬀs, however, are determined as the maximum of two functions,
implying that the payoﬀis smooth except at the crossover point where the payoﬀ
function may have a kink (a non-diﬀerentiable point). Since polynomials are “stiﬀ”
they will tend to ﬁt functions with a kink poorly; the way to resolve this is to ﬁt the
polynomials to both underlying functions and to split the integration interval at the
crossover point, with the use of suitable approximating polynomial on either side of
the crossover point [30].
5.3.4
Non-parametric implementation
Implying functional form of the numeraire discount bond in the Markov functional
model can also be done by, in econometric term, non-parametric ﬁt of the functional
forms. The implementation procedure presented above (and in Section 3.3) is of high
accuracy for most Markov functional models (including equity Markov functional
models). It is when ﬁtting derivatives with very long maturities (50 or more) there
might be a problem of ﬁtting a large number of functional forms, usually 200 or more.
In this case, the accumulation of numerical error can be problematic.
An alternative approach for determining functional form is to use semi-parametric
functional form, meaning ﬁxing a functional form, with several free parameters, which
is ﬂexible enough to provide a good ﬁt to the observed market price [30]. In addition,
33


for a suitable choice of the functional form, the prices of discount bonds and options
on discount bonds can be calculated analytically, eliminating a source of errors in the
calibration procedure. It is beyond the content of this project to show exactly how
this approach works and some details can be found in [30].
5.3.5
Numerical results
Below it compares the Bermudan swaption pricing results using diﬀerent models.
Since Bermudan swaptions are not liquid derivatives, it is hard to obtain its latest
quoted market prices. To ensure that the models give sensible correct answers, the
practical product data used here with strike 2%, 3%, 4%, 5% is the same as in [31],
which is a ﬁve year semi-annually exercisable USD Bermudan swaption, evaluated in
2003. The data about the swaption with strike 6.24% is quoted from [20], which is
a 30-year DEM (German Mark) Bermudan swaption, evaluated in 1998, exercisable
every ﬁve years. But the main point is, as can be seen, the price diﬀerence between
diﬀerent models is generally small and even neglectable to a certain degree.
Strike
European
Bermudan(SMM)
Bermudan(LMM)
Bermudan(MF)
2%
37.060
42.230
40.542
42.095
3%
74.050
105.320
103.410
107.200
4%
187.450
244.330
242.270
245.200
5%
446.380
506.580
500.930
504.800
6.24%
482.500
569.800
572.500
566.900
Table 5.1: Bermudan swaption prices (in basis point)
This can show that the Markov functional model is a qualiﬁed substitute for the
standard market model to price exotic interest rate derivatives of high dimensional-
ity. Without the help of advanced numerical/computational technique improving the
eﬃciency of the standard market model, given the large number of paths having to
be simulated , it might be appealing to price multi exercisable strong path dependent
interest rate derivatives using the Markov functional model.
34


Chapter 6
Conclusion
It is, with little doubt, becoming increasingly important to eﬀectively model interest
rate given the continuous booming of the ﬁxed income market with a growing number
of complicated interest derivatives being traded. Short rate modelling is still playing a
part, though with obvious drawbacks, since that is how people ﬁrstly start modelling
interest rate traditionally and by now it has been relatively well understood. More
importantly, it is practically easy to implement achieving a high eﬃciency especially
with modern advanced computing technique, such as parallel computing. The HJM
modelling framework looks attractive from a theoretical point of view but its critical
practical limitation makes it infeasible to use in reality. Both the standard market
model (BGM) and the Markov functional model have obvious advantage of pricing
complex derivatives over short rate models and the HJM modelling framework hence
it is not surprising that they have received a lot of attention especially from the bank-
ing industry.
BGM model used to be impractical to price American style products due to Monte
Carlo simulation’s low speed and incompatibility with backward calculation; the in-
troduction of the Longstaﬀ-Schwartz algorithm, a regression-based approach, has
successfully made this practically possible. The success of the LongstaﬀSchwartz
algorithm is largely due to its general suitability combined with its applicability in
both high-dimensional models and multiple exercise times. As a result, it has further
increased the popularity of standard market model, at least, in terms of interest rate
derivatives pricing.
Motivated by the reduction of dimension of the BGM model, the Markov functional
model has been developed with the aim of pricing interest rate derivatives more ef-
fectively and eﬃciently. Having managed to reduce the dimension of the model, the
Markov-Functional Market Model generally enjoys a low dimension of one or two and
still prices multi-temporal products fairly accurately, having little diﬀerence from the
35


standard market model.
As has been seen, the one-factor Markov functional model and multi-factor stan-
dard market model are very similar in terms of pricing and dynamics, which agrees
with the result shown in [4]. With respect to eﬃciency, Markov functional model,
arguably, tends to slightly outperform the standard market model due to the low
dimensional property. Advanced numerical and modern powerful computing tech-
niques (see [32][15] in this regard) have, however, made this computational eﬃciency
gap between these two models neglectably narrow [31].
Currently, much attention has been paid to the derivative pricing itself; analysing
ﬁnancial instruments is not about pricing only and hedging, to some extent, is more
important than pricing particularly from a practical point of view. So a possible
future work could be looking at the hedging performance comparison between the
Markov functional model and the standard market model. This is particularly of in-
terest because implementation for both models might have to be adjusted to improve
accuracy and eﬃciency when calculating Greeks. In addition, whether increasing the
number of model factor signiﬁcantly aﬀects the hedge performance is still up to de-
bate; some recent general results in this area can be found in [31]. This is probably
why neither the Markov functional model nor the standard market model has been
extensively applied in practical risk management.
The Markov functional model, nevertheless, represents a creatively fresh idea of mod-
elling interest rate by trying to eliminate the weakness of other available models while
retaining the strength. The study of the Markov functional model has just begun in
recent years, though having already attracted much research attention, there is still
much more to be analysed theoretically and numerically. It is quite possible, with
further development, the Markov functional model can play a leading role in the study
of modelling interest rate and ﬁxed income products.
36


Bibliography
[1] L. Andersen and J. Andreasen. Volatility Skews and Extensions of the
Libor Market Model. Working Paper, General Re Financial Products, 1998.
[2] L. Andersen and M. Broadie. Primal-Dual Simulation Algorithm for Pricing
Multidimensional American Options.
Management Science, 50(9):1222–1234,
2004.
[3] L.B.G. ANDERSEN.
A Simple Approach to the Pricing of Bermu-
dan Swaptions in the Multi-Factor Libor Market Model.
Working Paper,
http://ssrn.com/abstract=155208, 1999.
[4] M.N. Bennett and J.E. Kennedy. A Comparison of Markov-Functional
and Market Models: The One-Dimensional Case. The Journal of Derivatives
(Winter 2005).
[5] T. Bj¨ork. Arbitrage Theory in Continuous Time. Oxford University Press,
USA, 2004.
[6] A. Brace, D. Gatarek, and M. Musiela. The Market Model of Interest
Rate Dynamics. Mathematical Finance, 7(2):127–155, 1997.
[7] D. Brigo and F. Mercurio. Interest Rate Models-Theory and Practice: With
Smile, Inﬂation and Credit. Not Avail, 2006.
[8] P. Carr and G. Yang. Simulating Bermudan interest rate derivatives. Quan-
titative Analysis in Financial Markets: Collected Papers of the New York Uni-
versity Mathematical Finance Seminar, Volume II, 2001.
[9] J.C. Cox, J.E. Ingersoll, and S.A. Ross. A theory of the term structure
of interest rates. Econometrica, 53(2):385–407, 1985.
[10] D. Duffie. Dynamic Asset Pricing Theory. Princeton University Press, NJ,
1996.
37


[11] D.J. Duffy. Finite diﬀerence methods in ﬁnancial engineering: a partial dif-
ferential equation approach. Chichester, England; Hoboken, NJ: John Wiley &
Sons, 2006.
[12] B. Dupire. Pricing with a smile. Risk, 7(1):18–20, 1994.
[13] B. Flesaker and LP Hughston. Positive interest. Risk, 9(1):46–49, 1996.
[14] C.P. Fries. Mathematical Finance. Theory, Modeling, Implementation, 2007.
[15] P. Glasserman. Monte Carlo Methods in Financial Engineering. Springer,
2004.
[16] D. Heath, R. Jarrow, and A. Morton. Bond Pricing and the Term Struc-
ture of Interest Rates: A New Methodology for Contingent Claims Valuation.
Econometrica, 60(1):77–105, 1992.
[17] T.S.Y. Ho and S.B. Lee. Term structure movements and pricing interest rate
contingent claims. Journal of Finance, 41(5):1011–1029, 1986.
[18] J. Hull and A. White. Pricing interest-rate-derivative securities. Review of
Financial Studies, 3(4):573–592, 1990.
[19] J.C. Hull.
Options, Futures, and Other Derivatives. Prentice Hall.
ISBN:
0-13-149908-4, 2006.
[20] P. Hunt, J. Kennedy, and A. Pelsser. Markov-functional interest rate
models. Finance and Stochastics, 4(4):391–408, 2000.
[21] PJ Hunt and JE Kennedy. Implied interest rate pricing models. Finance
and Stochastics, 2(3):275–293, 1998.
[22] P.J. Hunt and JE Kennedy. Financial Derivatives in Theory and Practice.
Wiley, 2004.
[23] P.J.
Hunt
and
J.E.
Kennedy.
Longstaﬀ-Schwarz,
Eﬀective Model
Dimensionality
and
Reducible
Markov-Functional
Models.
SSRN:
http://ssrn.com/abstract=627921, 2005.
[24] PJ Hunt, JE Kennedy, and EM Scott. Terminal swap-rate models. work-
ing paper, ABN-Amro Bank and University of Warwick, 1996.
38


[25] P. Jackel. Using a non-recombining tree to design a new pricing method for
Bermudan swaptions, 2000.
[26] F. Jamshidian. LIBOR and swap market models and measures. Finance and
Stochastics, 1(4):293–330, 1997.
[27] Y. Jin and P. Glasserman. Equilibrium positive interest rates: a uniﬁed
view. Review of Financial Studies, 14(1):187–214, 2001.
[28] I. Karatzas and S.E. Shreve. Brownian Motion and Stochastic Calculus.
Springer, 1991.
[29] FA Longstaff and ES Schwartz. Valuing American options by simulation:
a simple least-squares approach. Review of Financial Studies, 14(1):113–147,
2001.
[30] A. Pelsser. Eﬃcient Methods for Valuing Interest Rate Derivatives. Springer,
2000.
[31] R. PIETERSZ and A. PELSSER. A Comparison of Single Factor Markov-
Functional and Multi Factor Market Models.
ERIM Report Series Reference
No. ERS-2005-008-F&A. Available at SSRN: http://ssrn.com/abstract=902498,
2005.
[32] V. PITERBARG. A Practitioner’s Guide to Pricing and Hedging Callable Li-
bor Exotics in Forward Libor Models. SSRN: http://ssrn.com/abstract=427084,
2003.
[33] V. PITERBARG.
Pricing and Hedging Callable Libor Exotics in Forward
Libor Models. Journal of Computational Finance, 8(2):65–119, 2004.
[34] R. Rebonato.
On the Simultaneous Calibration of Multifactor Lognormal
Interest Rate Models to Black Volatilities and to the Correlation Matrix. Journal
of Computational Finance, 2(4):5–27, 1999.
[35] K. Sandmann and D. Sondermann.
On the stability of log-normal inter-
est rate models and the pricing of Eurodollar futures. DISCUSSION PAPER
B,University of Bonn, 1, 1993.
[36] S.E. Shreve. Stochastic calculus for ﬁnance. 2, Continuous-time models. New
York: Springer, 2004.
39


[37] O. Vasicek. An equilibrium characterization of the term structure. Journal of
Financial Economics, 5(2):177–188, 1977.
[38] P. Wilmott. Derivatives, The theory and practice of Financial Engineering.
John Wiley & Sons, 1998.
[39] P. Wilmott. Paul Wilmott Introduces Quantitative Finance. Wiley, 2001.
40
