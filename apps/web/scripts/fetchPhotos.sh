#!/usr/bin/env bash

set -euo pipefail

tail -n +2 ../../docs/image_attributions.csv | while read -r photo_description; do \
    echo $photo_description;
    ./scripts/fetchPhoto.sh "$photo_description"; \
done
