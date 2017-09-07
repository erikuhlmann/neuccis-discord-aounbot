# NEU CCIS AounBot

Just a set of scripts to manage ranks and stuff.  Not super clean but does the
job well enough for us.

## Usage

Make sure you have Python 3 and `screen` installed and on your path.

Write startup scripts with names matching the glob `auth-*.sh` (which won't be
kept in version control), and then run `./start.sh`.  That makes screen sessions
and then returns.

## Help Wanted

* Randomly post copypasta in random channels.

* Scrape [/r/programmingcirclejerk](https://reddit.com/r/programmingcirclejerk) for posts containing any of ["go", "rust", "generics", "node"] with greater than some number of upvotes.

* Announce tweets from certain Northeastern accounts.
