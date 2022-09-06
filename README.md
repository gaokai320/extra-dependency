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

**What is the advantage of extras? Why extras are proposed? What problems do extras aim to solve?**


## Aim

### RQ1: How prevalent do packages use extras?
1. The annual trend of distribution and packages with *extra specification*.
2. The annual trend of distribution and packages with *extra adoption*. 
3. the number of dependency specifications for each extra

### RQ2: What kinds of packages sepcify extras?
1. the number of dependency specifications: specified vs. non-specified   
Hypothesis: packages with more dependency specifications are more likely to specify extras

2. dependency size   
Hypothesis: packages with more large dependencys are more likely to specify extras

3. dependency-file relationships   
Hypothesis: packages with less coupled dependency-file relationships are more likely to specify extras   
dependency-file relationships: extra dependencies are only used in limited files. 

4. Any other possible factors

5. We may fit a logestic regression model on these factor? 

### RQ3: What kinds of extras do packages specify?
Categorize extras accoding to their names, for example, development extras, alternative backends, 

### RQ3: Why do packages specify extras?

Mining packages' code repositories or email survey

### RQ4: What problems do developers face when using extras?

Analyzing issues in Python projects that mentioned "extras". Issues can be related to specification and adoption. 


## Method

### Data Collection
We need to filter some package, since some package are rarely used by others.

https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies