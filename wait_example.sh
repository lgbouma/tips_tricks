#!/usr/bin/env bash

# here wait_example_sublevel.sh has some of its own background processes that
# it calls. this approach starts a subshell; puts it in the background; and
# waits for it to complete before proceeding to the print statement.

( echo 'hi0'; source wait_example_sublevel.sh; wait ) & wait

echo 'hi1'
