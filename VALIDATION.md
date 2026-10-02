# Validation record

Scope: Direct requirements without exact versions and URL/includes/options needing review.

Local checks to rerun:

```sh
python -m unittest discover -s tests -v
python cli.py --help
python -m compileall -q review.py cli.py tests
```

Check the exact public GitHub commit and its workflow run separately after publishing. Tests use synthetic input; no production system or external target is exercised. This is not dependency resolution, hash verification, vulnerability scanning or a full pip requirements grammar parser.

## Current source result (2026-10-02)

- Python 3.14.6: 7/7 unit and CLI integration tests passed.
- Tests include the specific malformed-input, incomplete-review and declaration cases added during the source audit.
- Direct requirements use packaging's requirement grammar. Wildcard equality and arbitrary equality are not considered one exact version. Markers, extras, line continuations and common hash options are parsed; included files, URLs and installer options remain separate review prompts. No dependencies are downloaded by the analyzer.
- Test input is synthetic. No external target, live credential or production cluster is exercised.
- The public commit and its corresponding GitHub workflow must be verified separately after this update.
