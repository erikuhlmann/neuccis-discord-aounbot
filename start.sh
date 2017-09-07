#!/bin/bash

echo 'Starting all services...'
for f in auth-*.sh; do
	echo Starting $f...
	screen -dmS aoun-$f ./$f
done
