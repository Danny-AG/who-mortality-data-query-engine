#!/bin/sh

# Deploy database
cd postgres
bash postgres-build.sh
bash postgres-run.sh

# Deploy pipeline
cd ../
python -m pipeline.run_pipeline
