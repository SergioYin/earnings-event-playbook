# Contributing

Keep changes local-first, deterministic, and dependency-free unless there is a clear public maintenance reason to change that constraint.

Before proposing a release, run:

```bash
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m earnings_event_playbook selfcheck
```

Do not add broker integrations, live data fetching, order routing, credential handling, or workflow files.
