# State of Decision Tree Algorithms: June 2026

## Executive Summary

Decision tree research in 2026 is best understood as a set of algorithms for
constructing recursive partitions. The central questions are still algorithmic:
how to choose a split, when to stop splitting, how to prune, how to handle
continuous and categorical attributes, how to build trees at scale, how to
combine many trees, and when exact optimization is worth its cost.

This report deliberately excludes non-tree predictors and package-level
comparisons. The focus is on algorithms whose learned object is a decision tree,
a regression tree, a model tree, or an ensemble of decision trees. Within that
scope, the field has six major lines:

| Line | Core question | Representative algorithms |
| --- | --- | --- |
| Classical top-down induction | How should a greedy tree choose each split? | AID, CHAID, ID3, C4.5, CART, QUEST, GUIDE, conditional inference trees |
| Pruning and regularization | How should a grown tree be simplified? | Cost-complexity pruning, pessimistic pruning, MDL pruning, reduced-error pruning |
| Structural variants | What shape and split family should the tree use? | Binary trees, multiway trees, oblique trees, model trees, logistic model trees |
| Tree ensembles | How should many trees be combined? | Bagging, random forests, ExtraTrees, rotation forests, boosted trees |
| Exact and sparse trees | Can the whole tree be optimized globally? | OCT, OSDT, GOSDT, DL8.5, MurTree, SAT and mixed-integer formulations |
| Specialized tree algorithms | How should splitting change for a statistical target? | Quantile trees, survival trees, causal trees, isolation trees, streaming trees |

The practical center of the field remains simple: greedy top-down trees are fast,
readable, and unstable; pruning controls complexity; ensembles reduce variance
or bias; exact optimization gives smaller and more faithful trees when scale
permits. The research frontier is not about replacing trees with other model
families. It is about making tree induction more statistically principled, more
scalable, more constrained, more target-specific, and more globally optimal.

## Scope and Evidence Base

This literature review is current to June 6, 2026. The accompanying bibliography
contains 105 references, all selected for their relevance to decision-tree
algorithms or tree-specific ensembles. The source list covers classical tree
induction, split criteria, pruning, oblique trees, model trees, scalable tree
construction, random forests, boosted trees, optimal sparse trees, Bayesian
trees, survival trees, causal trees, streaming trees, and anomaly-detection
trees.

The inclusion boundary is intentionally strict:

| Included | Excluded |
| --- | --- |
| Algorithms that output a tree or ensemble of trees | Non-tree predictors |
| Split criteria and tree-growing procedures | General tabular prediction comparisons |
| Pruning, stopping, and regularization methods | Package feature comparisons |
| Exact, approximate, and scalable tree construction | Methods whose final model is not a tree |
| Target-specific tree algorithms | Post-hoc explanations of unrelated models |

This report is a synthesis, not a benchmark paper. It emphasizes algorithmic
ideas, failure modes, and how the main families relate to one another.

## Classical Top-Down Induction

Classical tree induction is built around recursive partitioning. At each node,
the algorithm evaluates candidate splits, chooses one, partitions the data, and
recurses until a stopping rule fires. The resulting tree is then often pruned.

Early automatic interaction detection methods framed recursive partitioning as a
statistical analysis tool for survey and categorical data [@morgan1963aid;
@kass1980chaid]. Hunt, Marin, and Stone supplied an early computational view of
induction [@hunt1966experiments]. ID3 made entropy and information gain the
standard machine-learning presentation of top-down tree induction
[@quinlan1986id3]. CART established the statistical workhorse formulation:
binary recursive partitioning, impurity reduction, surrogate splits, regression
trees, and cost-complexity pruning [@breiman1984cart]. C4.5 extended ID3 with
continuous attributes, missing values, gain ratio, pruning, and rule extraction
[@quinlan1993c45; @quinlan1996continuous].

The classical algorithms differ mainly in split scoring and tree shape:

| Algorithm | Split style | Main contribution |
| --- | --- | --- |
| AID | Multiway statistical splits | Early recursive interaction detection for survey data |
| CHAID | Chi-square based multiway splits | Categorical interaction detection with merging |
| ID3 | Information gain | Entropy-based top-down induction |
| C4.5 | Gain ratio and threshold search | Continuous attributes, missing values, pruning, rules |
| CART | Gini, squared error, twoing, deviance | Binary trees, regression trees, surrogate splits, cost-complexity pruning |
| QUEST | Statistical tests | Reduced split-selection bias |
| GUIDE | Residual and chi-square diagnostics | Unbiased split selection and interaction detection |
| Conditional inference trees | Permutation tests | Separates variable selection from split-point selection |

The common limitation is greediness. A locally good split can prevent a globally
better small tree. That limitation explains why pruning, ensembles, and exact
optimization all became major branches of the field.

## Split Criteria

Split criteria define what a tree is optimizing locally. For classification, the
classical criteria include entropy, information gain, gain ratio, Gini impurity,
misclassification impurity, twoing, and chi-square tests. For regression, the
standard criterion is reduction in squared error or variance, though absolute
error, quantile loss, deviance, and target-specific losses are also possible.

Different criteria encode different biases:

| Criterion family | Typical use | Bias or caveat |
| --- | --- | --- |
| Information gain | ID3-style classification | Favors high-cardinality attributes |
| Gain ratio | C4.5-style classification | Corrects some high-cardinality bias but can prefer small intrinsic value |
| Gini impurity | CART classification | Fast and usually close to entropy in behavior |
| Chi-square tests | CHAID and interaction trees | Natural for categorical predictors and multiway splits |
| Permutation tests | Conditional inference trees | Reduces variable-selection bias |
| Squared-error reduction | Regression trees | Sensitive to outliers |
| Log-rank and survival scores | Survival trees and forests | Designed for censored outcomes |
| Treatment-effect heterogeneity | Causal trees and forests | Splits for causal contrast rather than prediction error |

QUEST, GUIDE, and conditional inference trees are especially important because
they expose a subtle problem: split selection is not just about finding a
threshold. The algorithm must also decide which variable receives a chance to
split. If that decision is biased toward variables with many possible cutpoints,
the tree can look accurate while encoding a selection artifact [@loh1997quest;
@loh2002guide; @hothorn2006ctree].

## Stopping and Pruning

Stopping and pruning are the first line of defense against overfitting. A
top-down tree can keep splitting until every leaf is pure, but that usually
produces a brittle model. Tree algorithms therefore regulate complexity through
pre-pruning, post-pruning, or both.

Pre-pruning stops tree growth early using rules such as maximum depth, minimum
samples per leaf, minimum impurity reduction, or statistical significance tests.
It is cheap, but it can stop before a useful interaction appears. Post-pruning
grows a larger tree and then removes branches using validation error,
cost-complexity penalties, pessimistic error estimates, or description-length
criteria [@quinlan1987simplifying; @quinlan1989mdl; @mingers1989empirical;
@esposito1997surveypruning].

CART's cost-complexity pruning remains the cleanest canonical example. It
minimizes empirical loss plus a penalty proportional to the number of terminal
nodes. Varying the penalty generates a nested sequence of subtrees, and a
validation procedure selects the preferred complexity [@breiman1984cart]. Recent
work on optimal pruning shows that even pruning, often treated as a settled
engineering detail, still contains nontrivial algorithmic complexity
[@harviainen2025pruning].

## Structural Variants

Classical CART-style trees are axis-aligned and binary: each internal node asks a
question of the form `x_j <= t`. That format is readable and computationally
convenient, but it is not the only tree structure.

Multiway trees split a categorical attribute into more than two branches. They
can be compact for nominal variables, but they can also fragment data quickly.
Oblique trees use linear combinations of features, such as `w'x <= t`, and can
represent tilted decision boundaries with fewer nodes. OC1 is the classic
oblique-tree system [@murthy1994oc1]. Model trees place a local model in each
leaf. M5 and M5' use tree structure to partition the input space and fit local
linear regression behavior [@quinlan1992m5; @wang1997m5prime]. Logistic model
trees do the analogous thing for classification [@landwehr2005lmt].

These variants trade readability against compactness:

| Variant | Strength | Cost |
| --- | --- | --- |
| Axis-aligned binary tree | Simple rules and fast search | May need many nodes for diagonal boundaries |
| Multiway categorical tree | Compact categorical splits | Can create small leaves quickly |
| Oblique tree | Compact geometric boundaries | Harder split optimization and less transparent rules |
| Model tree | Smooth local regression behavior | Leaf model adds interpretive burden |
| Logistic model tree | Local linear classification inside leaves | More complex fitting and explanation |

The key lesson is that "decision tree" is not a single model class. Tree
algorithms differ in split geometry, leaf prediction, branching factor, and
search procedure.

## Scalable Tree Construction

Large-data tree induction created its own algorithmic literature before modern
hardware made brute-force threshold search easier. The central challenge is that
naive tree construction repeatedly scans and sorts data for candidate splits.
Scalable algorithms reduce sorting, reduce passes over data, or restructure the
split search.

SLIQ introduced pre-sorted attribute lists and a breadth-first construction
strategy for scalable classification [@mehta1996sliq]. SPRINT removed memory
constraints more aggressively and supported parallel construction through
attribute lists [@shafer1996sprint]. RainForest separated sufficient statistics
from raw data so the algorithm could decide splits using compact AVC sets
[@gehrke1998rainforest]. PUBLIC integrated building and pruning so that
subtrees unlikely to survive pruning could be avoided [@rastogi1998public].
BOAT used bootstrapped samples to construct an optimistic tree and then
corrected it with data passes [@gehrke1999boat].

The scalable-tree literature is still conceptually useful. It shows that tree
induction is not only a statistical problem; it is also a data-structures and
systems problem. Even when a modern implementation hides the details, the
algorithmic bottlenecks remain the same: split search, sorting, sufficient
statistics, memory locality, and distributed synchronization.

## Randomized and Bagged Trees

Bagging reduces variance by training trees on bootstrap samples and averaging
their predictions [@breiman1996bagging]. Random forests add feature
randomization at each split, making the individual trees less correlated
[@breiman2001randomforests]. ExtraTrees push randomization further by choosing
random split thresholds rather than optimizing every threshold [@geurts2006extratrees].
Rotation forests transform feature subsets before fitting trees
[@rodriguez2006rotation]. Mondrian forests use a stochastic partition process
that supports online updates [@lakshminarayanan2014mondrian].

The core algorithmic idea is variance control through decorrelation. A single
deep tree has low bias and high variance. An average of many decorrelated trees
keeps much of the low bias while reducing variance. The decorrelation can come
from bootstrap sampling, feature subsampling, randomized thresholds, transformed
feature spaces, or stochastic partition processes.

Random forests also support statistical extensions because a forest can be read
as an adaptive local weighting scheme. This interpretation underlies confidence
intervals, quantile estimates, causal forests, and generalized forests
[@wager2014rfci; @mentch2016uncertainty; @meinshausen2006quantile;
@wager2018causalforest; @athey2019grf].

## Boosted Decision Trees

Boosted decision trees are tree ensembles built sequentially. Each new tree is
fit to emphasize the examples or residuals not handled well by previous trees.
The algorithmic object is still an additive ensemble of trees.

AdaBoost gave the first iconic boosting procedure: repeatedly fit weak
classifiers, reweight examples, and combine the weak learners into a strong
classifier [@schapire1990strength; @freund1997adaboost]. When the weak learner
is a decision stump or shallow decision tree, the resulting model is a boosted
tree ensemble. Gradient boosting generalized this idea by viewing boosting as
functional gradient descent: each tree approximates a descent direction in
function space [@mason1999gradientboost; @friedman2001gbm]. Stochastic gradient
boosting added subsampling to improve regularization and computation
[@friedman2002stochastic]. Tutorials and comparative surveys clarify how loss,
learning rate, tree depth, subsampling, and early stopping interact
[@natekin2013tutorial; @bentejac2021comparative].

Algorithmically, boosted trees differ from random forests in their error
strategy:

| Ensemble | Training order | Main effect |
| --- | --- | --- |
| Bagged trees | Independent trees | Variance reduction |
| Random forests | Independent randomized trees | Variance reduction with decorrelation |
| ExtraTrees | Independent highly randomized trees | More decorrelation, sometimes more bias |
| Boosted trees | Sequential additive trees | Bias reduction and functional optimization |

Boosted trees are powerful but sensitive to regularization. Learning rate,
number of trees, tree depth, leaf size, subsampling, and loss function determine
whether the ensemble is a smooth additive approximation or an overfit sequence
of corrections.

## Optimal and Sparse Trees

The exact decision-tree problem is hard. Hyafil and Rivest proved that
constructing an optimal binary decision tree is NP-complete [@hyafil1976npcomplete].
The consequence is not that optimal trees are hopeless. It is that exact
algorithms must exploit structure, bounds, discretization, caching, or
restricted objectives.

Modern optimal-tree algorithms use several strategies:

| Strategy | Examples | Basic idea |
| --- | --- | --- |
| Mixed-integer optimization | OCT, MIP formulations | Encode split choices and leaf assignments as an optimization problem |
| SAT and MaxSAT | SAT-based optimal trees | Encode tree consistency and objective constraints logically |
| Dynamic programming | MurTree and related methods | Reuse subproblem solutions over feature subsets and label states |
| Branch-and-bound | DL8.5, OSDT, GOSDT | Search the tree space with lower bounds and pruning |
| Sparse objectives | OSDT, GOSDT | Penalize leaves or depth to find compact accurate trees |

OCT made modern optimization-based trees highly visible [@bertsimas2017oct].
MIP formulations, SAT encodings, OSDT, GOSDT, DL8.5, and MurTree then pushed
different parts of the scalability and optimality frontier
[@verwer2019mip; @narodytska2018sat; @hu2019osdt; @lin2020gosdt;
@aglin2020dl85; @demirovic2022murtree]. Recent work extends the same basic
question to nonlinear metrics, pruning, survival objectives, quantile
objectives, and hypersurface splits [@demirovic2020nonlinear;
@bertsimas2022survival; @harviainen2025pruning; @odtquantile2026;
@he2025hodt].

The right use case is not maximum-scale prediction. It is small, sparse,
auditable prediction where the tree itself is the final artifact and the cost of
global search is justified by the value of a compact model.

## Target-Specific Trees

Many important tree algorithms change the split criterion to match a statistical
target.

Quantile regression forests estimate conditional distributions rather than only
conditional means [@meinshausen2006quantile]. Random survival forests adapt
tree ensembles to right-censored time-to-event outcomes [@ishwaran2008rsf].
Causal trees and causal forests split to expose treatment-effect heterogeneity
rather than ordinary predictive accuracy [@athey2016causaltrees;
@wager2018causalforest]. Generalized random forests extend the same local
weighting idea to broader estimating-equation targets [@athey2019grf].
Isolation forests invert the usual supervised framing: anomalies are points
that are isolated quickly by random splits [@liu2008isolation; @liu2012isolation].

These algorithms are not small variations on CART. Their split criteria,
estimation targets, and validation logic are different. A survival tree should
not be evaluated like an ordinary regression tree, and a causal tree should not
be judged only by predictive accuracy.

## Streaming Trees

Streaming tree algorithms address the case where data arrive over time and the
tree cannot be rebuilt from scratch after every example. The central tool is a
statistical bound that decides when enough evidence has accumulated to commit to
a split.

The Very Fast Decision Tree algorithm uses the Hoeffding bound to choose splits
from streaming data [@domingos2000vfdt]. CVFDT adapts this idea to changing data
streams by maintaining alternate subtrees when drift is detected
[@hulten2001cva]. ADWIN supplies an adaptive-window drift detector
[@bifet2007adwin]. Adaptive random forests combine streaming trees with ensemble
logic and drift handling [@gomes2017arf].

Streaming trees make the trade-off explicit: the algorithm sacrifices full-batch
optimality for incremental updates, memory bounds, and adaptation to drift. That
is a real algorithmic regime, not just a faster implementation of batch CART.

## Current Algorithmic Picture

The current state of decision tree algorithms can be summarized as follows:

| Need | Algorithmic family to study first |
| --- | --- |
| A readable single model | CART, C4.5, GUIDE, conditional inference trees |
| A compact globally searched model | OSDT, GOSDT, DL8.5, MurTree, OCT |
| Low-variance prediction | Bagging, random forests, ExtraTrees |
| Additive predictive power | AdaBoost with stumps, gradient boosted trees, stochastic gradient boosting |
| Large-scale tree induction | SLIQ, SPRINT, RainForest, PUBLIC, BOAT |
| Online learning | VFDT, CVFDT, adaptive random forests |
| Censored outcomes | Survival trees and random survival forests |
| Treatment-effect heterogeneity | Causal trees and generalized random forests |
| Conditional distributions | Quantile regression forests |
| Anomaly detection | Isolation forests |

For a literature-review repository, the most useful emphasis is the evolution of
the induction problem itself:

1. Greedy split selection made trees practical.
2. Pruning made individual trees less brittle.
3. Randomization and averaging made trees stable.
4. Sequential additive fitting made tree ensembles highly accurate.
5. Exact optimization made small trees more faithful to a global objective.
6. Target-specific criteria turned trees into tools for survival, causal,
   streaming, quantile, and anomaly problems.

## Demo Notebook Plan

The notebooks should teach algorithmic mechanics rather than package features:

| Notebook | Algorithmic focus |
| --- | --- |
| `01_classical_cart_pruning.ipynb` | CART growth, impurity, depth control, and cost-complexity pruning |
| `02_ensembles_random_forest_boosting.ipynb` | Bagging, random forests, ExtraTrees, and boosted decision trees |
| `03_split_criteria_id3_cart.ipynb` | Entropy, information gain, gain ratio, Gini impurity, and threshold search |
| `04_hoeffding_tree_stream_demo.ipynb` | Hoeffding-bound split decisions for streaming tree induction |

## Open Problems

Several algorithmic questions remain active:

1. How far can exact sparse-tree algorithms scale without losing their global
   optimality guarantees?
2. Which split criteria best balance selection bias, statistical power, and
   computational cost for mixed continuous and categorical data?
3. Can oblique and model trees become easier to optimize while staying readable?
4. How should optimal-tree methods handle missing values, monotonic constraints,
   fairness constraints, and censored outcomes in one coherent objective?
5. Can uncertainty estimates for forests become reliable enough for routine
   decision-making?
6. Can streaming trees adapt to drift without constantly replacing useful old
   structure?
7. Which pruning objectives best predict human auditability, not just test
   error?

The field is mature because the basic recursive-partitioning idea is old. It is
still active because each real constraint - scale, interpretability, streaming,
causality, censoring, sparsity, and global optimality - changes the tree
construction problem in a substantive way.

