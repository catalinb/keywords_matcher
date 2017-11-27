# Flask keywords matcher
A simple REST service for matching a list of keywords built using flask and python3.

## Setup
The app requires python3 to run and you will probably want to to install the
dependencies in a virtual environment.

```sh
$ python3 -m venv env
$ source env/bin/activate
```

Install the required dependencies:
```sh
$ pip install -r requirements.txt
```

Run the App:
```sh
$ python run.py
```

## API
```
GET /parse?text=<input_text>
```
Returns a JSON with the list of matched keywords.

## Configuration
By default, the app runs in debug mode, listens on port 8080 and loads the list
of keywords from data/phrases. A custom configuration file can be passed
via the *KMATCHER_SETTINGS* environment variable. See *settings.cfg* for
a sample configuration file.

## Running on multiple workers
The app can run on multiple workers using gunicorn:
```sh
$ KMATCHER_SETTINGS=settings.cfg env/bin/gunicorn keywords_matcher:app --workers=8 --bind=localhost:8080 --worker-class=meinheld.gmeinheld.MeinheldWorker
```

## Tests
``` nosetests --nocapture ```

## Throughput

Number of workers: 2

|             | Average latency | Max latency | Requests per second |
|-------------|-----------------|-------------|---------------------|
| /parse      | 24.60ms         | 99.34ms     | 8110                |
| /parse_slow | 162.42ms        | 791ms       | 1228                |

Number of workers: 4

|             | Average latency | Max latency | Requests per second |
|-------------|-----------------|-------------|---------------------|
| /parse      | 14.92ms         | 44.08ms     | 13384.49            |
| /parse_slow | 86.49ms         | 190ms       | 2270                |

Number of workers: 8

|             | Average latency | Max latency | Requests per second |
|-------------|-----------------|-------------|---------------------|
| /parse      | 12.63ms         | 82.81ms     | 16410.23            |
| /parse_slow |  74.14ms        | 173.62ms       | 2686.17          |

Measurements were done on a macbook pro 2017 using wrk:
```sh
$ wrk -d20s -t10 -c200 http://localhost:8080/parse_slow\?text\=I+have+a+sore+throat+and+headache.+This+is+some+random+text.
$ wrk -d20s -t10 -c200 http://localhost:8080/parse\?text\=I+have+a+sore+throat+and+headache.+This+is+some+random+text.
```

### Discussion
**/parse_slow** is slow (surprise!) because it does a n^2 lookup.  
**/parse** is handled using a finite state machine built using the aho corasick algorithm. The lookup is linear in the length of the input string plus the number of matches.

Testing the automaton lookup time separately, the throughput for a single thread was several orders of magnitude higher, therefore
I think the current throughput is limited by the web framework and not the lookup mechanism.

### Logging
I should have added logging, but I didn't.





