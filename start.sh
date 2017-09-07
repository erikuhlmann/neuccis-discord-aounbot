#!/bin/bash

echo 'Starting all services...'
for f in auth-*.sh; do
	screen -S aoun-$f ./$f
done
