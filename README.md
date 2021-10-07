# Memcached Lite
To start the server and client, execute `make run` command in shell.
This will start the server, run testcases and start interactive client shell.
The shell should look similar to the below content when started.
```
nohup python3 ./main.py &1> server.log
sleep 2
appending output to nohup.out
python3 -m unittest test_cases.py
.........
----------------------------------------------------------------------
Ran 9 tests in 0.070s

OK
python3 ./repl.py
**** Client ****
```
Use `close` as input to close the interactive shell.

The test cases include connections made from pymemcache client and locally developed client with an interesting case of writing data beyond the buffer size specified for sockets.
A 10MB value limit has been set at server and client which can be disabled by setting `limit = False` in `const.py`. 

