# Results

## Lookup speed

(on MacOS 15.5, Apple M1 Pro, Python 3.13.3)

Optimized Python build

| Benchmark         | `__dict__`       | `__slots__`           |
|-------------------|:----------------:|:---------------------:|
| getattr (3.13.3)  | 4.36 ns          | 4.17 ns: 1.05x faster |
| getattr (3.12.11) | 4.62 ns          | 4.75 ns: 1.03x slower |
| getattr (3.11.13) | 4.56 ns          | 4.39 ns: 1.04x faster |
| getattr (3.10.18) | 14.6 ns          | 13.5 ns: 1.08x faster |
| getattr (3.9.23)  | 13.2 ns          | 12.8 ns: 1.04x faster |

Unoptimized Python build

| Benchmark         | `__dict__`          | `__slots__`           |
|-------------------|:-------------------:|:---------------------:|
| getattr (3.13.3)  | 6.20 ns             | 6.20 ns: (not faster) |
| getattr (3.12.11) | 8.72 ns             | 8.22 ns: 1.06x faster |
| getattr (3.11.13) | 7.07 ns             | 7.07 ns: (not faster) |
| getattr (3.10.18) | 29.4 ns             | 14.3 ns: 2.05x faster |
| getattr (3.9.23)  | 28.6 ns             | 12.9 ns: 2.21x faster |

# Requirements to run the benchmarks

- `uv` installed
- `pyenv` installed

For both `uv` and `pyenv`, install the Python versions listed above.

# Running the benchmarks

```bash
./run_full_benches.sh
```


