# Updating this overview

This repository presents selected results from an active research project. The private development repository remains the authoritative engineering record.

For a new evidence snapshot:

1. Record the experiment date, source commit and original archive hashes. Check proposed files for private details and third-party licence notices.
2. Add original numeric records under a new dated evidence directory. Preserve existing evidence bytes. Describe any transformation or redaction explicitly.
3. Update the result tables, limitations and provenance together. Distinguish physical measurements from offline-only changes, proposed work and historical results.
4. Update the reviewed file hashes in `evidence/manifest.json`, then run `python tools/verify_results.py` and check every relative link and image.

New acceptance criteria require an explicit dated explanation. Historical pass/fail decisions remain associated with the criteria used for those experiments.

Keep local exports, credentials, recordings and build products out of the public tree. `.gitignore` helps avoid accidental additions; it does not inspect file contents or remove an already committed file.

The repository intentionally omits live deployment commands and programming images. Contributions to hardware control belong in the development project and require its physical qualification process.
