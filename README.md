# A first look at extras in PyPI ecosystem

## What is extras

From [PEP 508](https://peps.python.org/pep-0508/), *"A dependency specification always specifies a distribution name. It may include extras, which expand the dependencies of the named distribution to enable optional features."*

In other words, extras are optional part of a package distribution, which may include additional dependencies. 
Extras are specified in [environment markers](https://peps.python.org/pep-0508/#environment-markers) of a dependency specification. Environment markers allow a dependency specification to provide a rule that describes when the dependency should be used. Environment markers include a "extra" variable, which is used by wheels to signal which specifications apply to a given extra in the wheel `METADATA` file. For instance, the following is an *extra specification*:
```shell
"annoy (>=1.16.3) ; extra == 'similarity'"
```
The above dependency specification is part of `requires_dist` of `txtai 3.5.0`. It specifies an extra `similarity` which requires dependency `annoy`. We refer `similarity` as *extra* and `annoy` as *extra dependency*. 

Distributions can specify as many extras as they wish, and each extra results in the declaration of extra dependencies of the distribution when the extra is used in a dependency specification. 
For instance, the following is an *extra adoption*:
```shell
requests[security]
```
Extras union in the dependencies they define with the dependencies of the distribution they are attached to. The example above would result in requests being installed, and requests own dependencies, and also any dependencies that are listed in the “security” extra of requests. If multiple extras are listed, all the dependencies are unioned together.   

## Aim

We aim to investigate extra from its prevalence, package cha

### RQ1: How prevalent do packages use extras?
1. The annual trend of distribution and packages with *extra specification*.
2. The annual trend of distribution and packages with *extra adoption*. 
3. the number of dependency specifications for each extra

### RQ2: What kinds of packages sepcify extras?
1. the number of dependency specifications: specified vs. non-specified
2. popularity
3. dependency size


### RQ3: Why do packages specify extras?

### RQ4: Why don't packages adopt extras?


https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies