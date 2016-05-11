Flow
====

*Flow* is a high frequency algorithmic trading module that uses machine learning to self regulate and self optimize for maximum return.

The current approach uses a stack of financial indicators which is consumed by a Q-learning algorithm which determines an Agent's action at a given step in the stream of financial quotes.

Flow uses an idea called Scopes which is essentially a sampling of the time series quotes to discover trends along any sort of time interval. At every moment, the Supervisor ensures there is at least one Agent looking for an opportunity to boost profits.

Currently trades CAD/USD from quotes taken from January 2016. A fork that actually ties into a trading platform practice account has also been developed - this fork actually makes a profit before accounting for spread.

Installation
-----------

1. Clone the project:

   `$ git clone https://-yazan@bitbucket.org/-yazan/flow.git && cd flow`

2. Pip-install dependencies. For example using a `virtualenv`:

   `$ virtualenv env && source env/bin/activate && pip install -r requirements.txt`

Usage
-----
1. To live stream transactions, open a second terminal window and:

   `$ tail -f -n 40 logs/bankroll.log`

2. Now to run Flow, back to the first tab:

   `$ python python/executive.py`

3. The simulation should begin to run.

Contributing
------------
1. Fork it
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

Authors
------------
Yazan Obeidi

Matthew Robichaud

Contributors
------------
Micheal Broughton 

Copyright
------------
2016, Yazan Obeidi
