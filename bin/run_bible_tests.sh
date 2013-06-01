# run core tests
bin/run_tests.sh

# run bible-dependent tests
python  -m unittest "$@" test.test_bible
