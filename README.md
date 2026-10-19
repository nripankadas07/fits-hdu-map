# fits-hdu-map

Map FITS primary/IMAGE header, data and padding byte ranges without loading arrays.

For Astronomy archive ingestion maintainers. A rejected small FITS needs physical HDU boundaries and padding evidence before array interpretation.

## Quickstart

Python3.10+; zero runtime dependencies. Wheel builds require setuptools from the normal Python registry.

```sh
git clone https://github.com/nripankadas07/fits-hdu-map.git
cd fits-hdu-map
python3 -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/fits-hdu-map --make-example example.fits
.venv/bin/fits-hdu-map example.fits
```

Exit0: primary data is empty at byte2880; IMAGE data occupies bytes5760..5764 and padding ends at8640.

Example generators create only an explicitly named new file and refuse overwrite. Reports never modify the input. Windows equivalents use `.venv\Scripts\python.exe` and the installed `.exe`; Windows/macOS have not been executed by this release's Linux CI.

## Contract

80-byte printable ASCII cards with fixed-format structural values (logical/integer values right justified through column30; IMAGE string starts at column11), complete 2880-byte blocks, ordered primary SIMPLE/BITPIX/NAXIS and consecutive NAXISn, IMAGE extensions with EXTEND=T and PCOUNT=0/GCOUNT=1. Dimensions0..4, axis sizes0..1000000, BITPIX8/16/32/64/-32/-64. END and space header padding are required. Nonzero data padding is an exit1 finding. Byte ranges use exclusive ends; no arrays are allocated.

JSON reports go to stdout. Exit0 means the documented successful result, exit1 a valid finding/incomplete/rejected result, exit2 invalid/unsupported input, I/O or budget failure with stderr and no partial report. Ranges are half-open.

## Limits

8 MiB,32 HDUs,144 cards per header. No tables, random groups, compressed extensions, pixel interpretation, scaling, WCS, repair or complete FITS conformance validation. CHECKSUM/DATASUM are explicitly unverified. Nonstructural card values are not semantically validated.

## Verify

```sh
python3 -m unittest -v test_behavior
python3 -m compileall -q .
python3 -m pip wheel --no-deps --wheel-dir dist .
python3 -m venv /tmp/fits-hdu-map-check
/tmp/fits-hdu-map-check/bin/python -m pip install --no-deps dist/*.whl
python3 verify_installed.py /tmp/fits-hdu-map-check/bin/python
```

[Validation](VALIDATION.md), [research](RESEARCH.md), [contributing](CONTRIBUTING.md), [support](SUPPORT.md), [security](SECURITY.md), [MIT license](LICENSE).

Original implementation, prose and invented fixtures developed with AI assistance. No measured performance-superiority or verified production-adoption claim.
