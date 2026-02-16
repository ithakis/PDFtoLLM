Solving (2.5) with B(T,T) = 0 gives

$$B(t,T) = \frac{1 - e^{-k(T-t)}}{k}. (2.6)$$

Substituting (2.6) into (2.4) gives

$$A(T,T) - A(t,T) = \int_{t}^{T} \left[ \theta(u)B(u,T) - \frac{\sigma^{2}B(u,T)^{2}}{2} \right] du.$$
 (2.7)

Solving (2.7) with A(T,T) = 0 leads to

$$A(t,T) = \int_{t}^{T} \left[ -\theta(u)B(u,T) + \frac{\sigma^{2}B(u,T)^{2}}{2} \right] du.$$
 (2.8)

Fitting the observed initial forward price  $f^*(0,T)$  results

$$f^*(0,T) = -\frac{\partial}{\partial T} \log P^*(0,T) = -A_T(0,T) + B_T(0,T)r_0, \tag{2.9}$$

where  $A_T, B_T$  denote the first derivative of A, B with respect to T.

From (2.6) and (2.8) respectively, it is easy to, differentiating with respect to T, get

$$B_T = e^{-k(T-t)},$$

and

$$A_{T} = \frac{\partial}{\partial T} \left( \int_{t}^{T} \left[ -\theta(u)B(u,T) + \frac{\sigma^{2}B(u,T)^{2}}{2} \right] du \right)$$

$$= -\theta(T)B(T,T) + \frac{\sigma^{2}B(T,T)^{2}}{2} + \int_{0}^{T} \left[ -\theta(u)B_{T}(u,T) + \sigma^{2}B_{T}(u,T)B(u,T) \right] du$$

$$= \int_{0}^{T} \left[ -\theta(u)B_{T}(u,T) + \sigma^{2}B_{T}(u,T)B(u,T) \right] du.$$

Hence (2.9) becomes

$$f^{*}(0,T) = r_{0}B_{T}(0,T) - A_{T}(0,T)$$

$$= r_{0}e^{-kT} - \frac{\sigma^{2}}{k} \int_{0}^{T} e^{-k(T-u)} (1 - e^{-k(T-u)}) du + \int_{0}^{T} \theta(u)e^{-k(T-u)} du$$

$$= r_{0}e^{-kT} - \frac{\sigma^{2}}{2k^{2}} (1 - e^{-kT})^{2} + \int_{0}^{T} \theta(u)e^{-k(T-u)} du$$

$$= r_{0}e^{-kT} - \frac{\sigma^{2}}{2}B(0,T)^{2} + \int_{0}^{T} \theta(u)e^{-k(T-u)} du$$

Setting

$$x(T) =: r_0 e^{-kT} + \int_0^T \theta(u) e^{-k(T-u)} du,$$