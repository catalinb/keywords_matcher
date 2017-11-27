#!/bin/bash
KMATCHER_SETTINGS=settings.cfg env/bin/gunicorn keywords_matcher:app --workers=8 --bind=localhost:8080 --worker-class=meinheld.gmeinheld.MeinheldWorker
