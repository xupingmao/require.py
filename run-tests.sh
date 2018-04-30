#!/bin/bash
cp require.py test/require.py
pushd test
# run tests
python test-main.py

# do some cleanings
rm require.py
# back
popd

# end