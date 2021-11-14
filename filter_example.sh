java -jar parser.jar -s tmp/Patch-Explainer-Test/ -f csv | xargs -n1 -d '\n' python3 kh_filter.py "smaller than zero"
