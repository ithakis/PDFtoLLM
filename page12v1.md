Solving (2.5) with B ( T, T ) = 0 gives

$$B ( t , T ) = & \frac { 1 - e ^ { - k ( T - t ) } } { k } .$$

Substituting (2.6) into (2.4) gives

$$A ( T , T ) - A ( t , T ) = \int _ { t } ^ { T } \left [ \theta ( u ) B ( u , T ) - \frac { \sigma ^ { 2 } B ( u , T ) ^ { 2 } } { 2 } \right ] d u .$$

Solving (2.7) with A ( T, T ) = 0 leads to

$$A ( t , T ) = \int _ { t } ^ { T } \left [ - \, \theta ( u ) B ( u , T ) + \frac { \sigma ^ { 2 } B ( u , T ) ^ { 2 } } { 2 } \right ] d u .$$

Fitting the observed initial forward price f ∗ (0 , T ) results

$$f ^ { * } ( 0 , T ) = - \frac { \partial } { \partial T } \log P ^ { * } ( 0 , T ) = - A _ { T } ( 0 , T ) + B _ { T } ( 0 , T ) r _ { 0 } ,$$

where A T , B T denote the first derivative of A, B with respect to T .

From (2.6) and (2.8) respectively, it is easy to, differentiating with respect to T , get

$$B _ { T } = e ^ { - k ( T - t ) } ,$$

and

$$\text { and } \\ A _ { T } \ = \ \frac { \partial } { \partial T } \Big ( \int _ { t } ^ { T } \left [ \, - \theta ( u ) B ( u , T ) + \frac { \sigma ^ { 2 } B ( u , T ) ^ { 2 } } { 2 } \Big ] d u \right ) \\ \, = \, \Big ( - \theta ( T ) B ( T , T ) ^ { 2 } + \int _ { 0 } ^ { 2 } \Big [ \, - \theta ( u ) B _ { T } ( u , T ) + \sigma ^ { 2 } B _ { T } ( u , T ) B ( u , T ) \Big ] \, d u \\ \, = \, \int _ { 0 } ^ { T } \left [ \, - \theta ( u ) B _ { T } ( u , T ) + \sigma ^ { 2 } B _ { T } ( u , T ) B ( u , T ) \right ] d u . \\ \text { Hence (2.9) becomes}$$

Hence (2.9) becomes

$$f ^ { * } ( 0 , T ) & \ = \ r _ { 0 } B _ { T } ( 0 , T ) - A _ { T } ( 0 , T ) \\ & = \ r _ { 0 } e ^ { - k T } - \frac { \sigma ^ { 2 } } { k } \int _ { 0 } ^ { T } e ^ { - k ( T - u ) } ( 1 - e ^ { - k ( T - u ) } ) d u + \int _ { 0 } ^ { T } \theta ( u ) e ^ { - k ( T - u ) } d u \\ & = \ r _ { 0 } e ^ { - k T } - \frac { \sigma ^ { 2 } } { 2 k ^ { 2 } } ( 1 - e ^ { - k T } ) ^ { 2 } + \int _ { 0 } ^ { T } \theta ( u ) e ^ { - k ( T - u ) } d u \\ & = \ r _ { 0 } e ^ { - k T } - \frac { \sigma ^ { 2 } } { 2 } B ( 0 , T ) ^ { 2 } + \int _ { 0 } ^ { T } \theta ( u ) e ^ { - k ( T - u ) } d u$$

Setting

$$x ( T ) = \colon r _ { 0 } e ^ { - k T } + \int _ { 0 } ^ { T } \theta ( u ) e ^ { - k ( T - u ) } d u ,$$