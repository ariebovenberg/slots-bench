# Results

Results obtained on MacOS 15.5, Apple M1 Pro. 
Similar results were obtained on x86_64 MacOS.

## Lookup speed

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

## Memory savings

Memory savings depend on the number of attributes in the class. 
Below is a table showing the lower and upper bounds of memory savings:

| version | min. memory savings | max memory savings |
|---------|---------------------|--------------------|
| 3.9     | 80                  | 216                |
| 3.10    | 80                  | 216                |
| 3.11    | 40                  | 64                 |
| 3.12    | 32                  | 56                 |
| 3.13    | 40                  | 64                 |

# Requirements to run the benchmarks

- `uv` installed
- `pyenv` installed

For both `uv` and `pyenv`, install the Python versions listed above.

# Running the benchmarks

```bash
./run_full_benches.sh
```

# Methodology

## Lookup speed

Microbenchmarks require special attention. To get maximum accuracy,
I've used `pyperf` and their recommended approach to microbenchmarks.

## Memory savings

Measuring memory savings is a bit tricky given the latest changes to object layout.
Both `sizeof` and `pympler` cannot be used to measure the new memory layout,
until these issues are resolved:

- https://github.com/python/cpython/issues/128762
- https://github.com/pympler/pympler/issues/170

So, I used `tracemalloc` to measure the memory usage of the objects.
By allocating a large number of objects, you can get a good estimate
of the actual memory savings.
