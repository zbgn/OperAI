M_AI_Intro

# Informations

dummy0 = inspector dummy version
dummy1 = phantom dummy version

# Validation tests
Launch server.py with following arguments:<br>
Argument 1:
- 0: dummy0 vs dummy1
- 1: dummy0 vs phantom
- 2: inspector vs dummy1
- 3: inspector vs phantom
- no argument: classic dummy0 vs dummy1
<a/><a>
    Argument 2:
- int which represent the number of matchs for the validation test
- no argument: launch 10 matchs for the validation test
<a/>
    Example: `python ./server.py 2 15` Launch a inspector vs dummy1 validation test with 15 games<br>
<br>
The results are in the validation_tests.txt file.
