=================================================
Software Engineering, softer than Social Sciences
=================================================

If you occasionally browse Hacker News or other aggregator sites for interesting blog posts, articles and links on software development, data-science, and computing, you can’t help but also see the software-engineering crowd discusing various topics and subjects that are not exactly their primary field of education. At best, the recurrence and acceptance of such off-topic discussions stands witness for the fact that computing-enthusiasts are not narrow-minded and not only interested in their own field, but are attracted to problem-solving on a large scale. 

But, more often than I would like, I perceive a certain snobbism of the crowd. A typical attitude seems to be, that math — above all — and also natural sciences like physics and chemistry were hard science and the superior (or only truly acceptable way of gaining insight). Social science and studies already were doubtable, soft and generally not capable of giving satisfaction. This can reach extremes and the disdain can also encompass business and economical questions as well as fields closely associated with natural sciences, such as medicine or psychology. Consequentially, “the other, soft side” is pictured as either doomed, or ready for disruption, just waiting for folks and entrepreneurs based in STEM to pick the low-hanging fruits and shatter the “cargo-cult” of soft sciences.

This might be an exagerated compilation of reactions to articles on the bubonic plague, issues of diversity, or psychologies’ replication problem. Yet, I suppose, that many geeks would agree with at least some of the statements I outlined above. After all, people in software engineering are part of the STEM club. We program; the idea that outputs are deterministically deduced from precise inputs are our version of “actio is reactio”. We model the world in equations or data-structures and attain higher truths. Thus, “hard science” is the team we cheer for. But then, software engineering is so “soft”, that it would hardly make the cut for a social science!


Empiricism
==========

When I studied physics, a lot of teaching focused on landmark experiments. I often found this tedious. For example, when being introduced to the ideal gas law, an equation that expresses the product of pressure and volume of a gas, by the product of the  number of particles, the temperature and a constant R (concisely put pV=nRT), our lecturer introduced us to

* the law of Boyle-Mariotte (for constant temperature and number of particles, the product of pressure and volume is constant).
* the law of Gay-Lussac (for constant pressure and constant number of particles, the ratio of volume / temperature is constant.
* the second law of Gay-Lussac (for constant volume and constant no. of particles, the ratio of p / T is constant).
* the law of homogeneity (for constant temparture and constant pressure, the fraction of volume / number of particles is constant).

Each of these laws, we learned, was derived from an experiment with the initial conditions of keeping 2 quantities constant and manipulating a 3rd to observe the 4th. The ideal gas law was discovered by assembling several small theories into a unifying one. We also learned about the limits of the ideal gas law, the necessity of alternative equations for various gases. Learning about thermodynamics did not only involve learning about some axioms of natural law and deducing from them.

The same basically is true for any other physics-subject I got in touch with. Teaching quantum mechanics means teaching about both, the Schödinger Equation and experiments (like Stern-Gerlach, or Lyman series and many other experiments). Teaching relativity means talking about the Lorentz-Transformation, but also about the Michelson-Morley experiment.

| What is the Michelson-Morley experiment, that verifies/falsifies object oriented programming?

Today, the accepted framework for science is that, which was outlined by philosopher Karl Popper: Falsifiability. Roughly speaking, it is the idea that a scientific theory is a predictive and falsifiable  hypothesis. Based on a scientific theory, one must be able to forecast something, that hasn’t been measured yet (the predictive aspect) and that we must be able to design an experiment to check whether the prediction is not false (falsifiability). Popper talks about falsification over verification, because the important aspect is the rejection of a hypothesis, not so much a verification. I.e. it is kind of hard to tell how general a scientific theory is, but we can be fairly certain by falsifying it in large domains that it is a useful theory for our day-to-day work.

For example, the hypothesis “All numbers not divisible by 2 are prime numbers” would lead to a prediction that 15 is a prime number, we can falsify this claim, since 15 = 3 x 5, thus the theory is false. The hypothesis “A flying spaghetti monster created earth” is not a scientific theory, because it doesn’t allow us to predict anything that would be  falsifiable.

Popper’s falsification is the foundation of empiric science. It builds the constant rhythm we have in natural science, theory-finding followed by validation. Apart from formal sciences (math, logic, …) that are not rooted in our physical world, all major branches of science build upon empiricism.

Empiricism and Software Engineering
===================================

When software engineers/developers think about soft sciences, like psychology, they are often not aware that psychology is an empirical science. Thus soft is a misleading categorization. In fact, saying that physics is a hard science and psychology is a soft science, is really a confusion of labels, because physics allows probably for easier control of experiments and data, and thus allows for easier falsification that psychology, where experiments are limited heavily by the number of participants one can sign up for a study, multivariate data sets (the question whether wine-drinkers are more live longer because they drink wine, or because they are on average better-off and can afford for better health care overall).

As a physicist who had some exposure to live-sciences before focussing on software engineering and data-science, I have never experienced a field that was less interested in falsifiability and empirical evidence than software engineering.

As a physicist who had some exposure to live-sciences before focussing on software engineering and data-science, I have never experienced a field that was less interested in falsifiability and empirical evidence than software engineering.

When my physics classes taught physics by introducing hypotheses and experiments in parallel. Whenever I learn about a software development concept, it either is rooted in pure math (and therefore doesn’t need to be backed by empirical evidence) or it is just reported as experience of the authors. I have yet to see an introduction to object oriented programming for example that backs up claims about its superiority over procedural programming by empirical evidence. Even if empirical studies can be conducted, the notion of empiricism is so fringe, that they hardly are mentioned outside of academia. Either you can proof it (Church-Turing Thesis) or you look for plausibilities, not falsification. For example: Are microservices better than monolithical architecturs? It is plausible, that monoliths are harder to maintian, but it is also plausible that microservices introduce integration problems and might lead to a lack of coherence.

At the end of the day it seems, that the IT crowd is content with anectotes and arguments of plausibility.
Replication Crisis in Psychology

Now, when Hacker News threads with hundreds of comments talk about the replication crisis of psychology, I can’t help but feel a little embarassed of my club. Sure enough, replication is an important extension of the need for falsification, it adds reliability to it. Yet, hearing software developers — who are generally disinterested in empirical studies of their own field — criticise a lack of reproducibility in empirical sciences is at least a bit hypocritical.

Aren’t we cross-validating our ideas?
-------------------------------------

Even though Software engineering doesn’t even pretend to closely follow the ideals of empiric research, one might argue, that software engineering wisdom and anecdotes are indeed backed by empiric evidence in the form of experience that people acquire in the course of their careers. If microservices wouldn’t work out at all, people would probably stop building their 2nd or 3rd microservice. Thus:

If a software engineering practice survives for years, we might consider it to be evidently beneficial.

Yet, in psychology this might not be so different. Even though psychologists experiment and conclude from experimentally acquired data (with the associated problems of replication), they also apply results of their research in their daily work (many psychologists work in HR, as consultants or coaches, etc.). So the empiric sciences share an informal layer of “cross-validation” in their method toolbox with software engineering, but additionally use empiric falsification for prominent claims.

Determinists in a Stochastic World
----------------------------------
...

Conclusion
==========
We, as softwar engineers, should be careful to fall victim to our own hybris. Other disciplines have people with backgrounds that differ from ours, but this doesn’t mean that they are naïve. Also, dealing with software, programmers are prone to have a very deterministic mindset. Our world however is stochastic and rarely reaches the level of determinism that we are used to when debugging how our code is executed on that CPU.
