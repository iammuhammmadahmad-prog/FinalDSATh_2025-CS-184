# EduAlloc – Algorithmic Decision Support for Educational Resource Allocation (Under Developement)

Python-based decision-support prototype implementing custom data structures (`dsa_lib/`) and algorithmic optimization modules (`modules/edualloc/`) on synthetic datasets, with a Django dashboard (`apps/dashboard/`).

## Quick Start (Standalone Benchmarks & Tests)

No external dependencies are required to run the core data structures, algorithmic modules, tests, or CLI benchmarks:

```bash
python3 -m unittest discover -s tests -v
python3 run_benchmarks.py
```

## Running the Django Dashboard

```bash
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
