# Verifier repair —19 October2026

Initial CI at0f42359ec34195b5e831a6b7a080530f4d0f0f64 failed in installed-console validation. Run39211357905/job117925254015 showed FileNotFoundError under the hosted Python directory. The verifier resolved the virtual-environment Python symlink before locating its sibling console command, losing the virtual environment. Use an absolute path without resolving that symlink. All five preparations were rerun with symlinks=True, matching the CI environment. Behavior tests, compilation, wheel and installed success/failure checks passed. The current remote CI must still pass before merge. No checks were disabled.

## Required FITS keyword columns

Default765f513145ac9dbf3e07083380e735264573f939 generated SIMPLE/BITPIX numeric/logical values starting at column11. NASA's primary header guide requires fixed format for required keyword values: logical/integer fields end at column30. Generator now right justifies those fields; the strict mapper checks structural field placement and the IMAGE string field. A regression asserts actual generated columns and rejects the old free-format placement. Existing byte-extent expectations remain unchanged. Version0.1.1 also retains the earlier venv verifier fix. Reference: https://fits.gsfc.nasa.gov/users_guide/users_guide/node20.html .
