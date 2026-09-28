#!/bin/bash
# Download remaining files that couldn't be fetched from this environment
# (French .gouv.fr sites and BLS are firewalled)
#
# Run this script from a machine with unrestricted internet access.

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== BLS SOC 2018 to ISCO-08 crosswalk ==="
echo "Note: BLS only provides SOC 2010 -> ISCO-08. We already have that from danielruss/codingsystems."
echo "If you also need the official BLS version:"
curl -o "$DIR/ISCO_SOC_Crosswalk_BLS.xls" \
  "https://www.bls.gov/soc/ISCO_SOC_Crosswalk.xls"

echo ""
echo "=== DARES FAP 2021 (PCS-ROME correspondence) ==="
echo "Option A: From data.gouv.fr"
curl -L -o "$DIR/arborescence-fap-2021.xlsx" \
  "https://www.data.gouv.fr/fr/datasets/r/f1be98eb-0414-4648-a683-7dbed3ebaca7"

echo ""
echo "Option B: From DARES OpenDataSoft API (full CSV)"
curl -o "$DIR/fap2021_nomenclature.csv" \
  "https://data.dares.travail-emploi.gouv.fr/api/explore/v2.1/catalog/datasets/dares_nomenclature_fap2021/exports/csv?delimiter=%2C&list_separator=%2C&quote_all=false&with_bom=true"

echo ""
echo "=== France Travail ROME data ==="
curl -L -o "$DIR/rome_referentiel.zip" \
  "https://www.francetravail.org/files/live/sites/peorg/files/documents/Statistiques-et-analyses/Open-data/ROME/ROME_ArboPrworescence.xlsx"

echo ""
echo "Done. Check downloaded files in: $DIR"
