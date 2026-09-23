## Summary

Describe the SDK behavior, documentation, or release workflow change.

## Checklist

- [ ] I kept this change within the supported server SDK scope.
- [ ] I did not add browser/client-side patterns that expose CALL-E API keys.
- [ ] I did not include private collaboration links or unconfirmed public repository references.
- [ ] I updated tests, examples, or docs when behavior changed.
- [ ] I updated the changelog when the change affects package users.
- [ ] I ran the relevant local checks.

## Local checks

```bash
bash scripts/validate.sh
```
