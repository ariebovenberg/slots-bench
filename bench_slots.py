import time
import pyperf
import sys
import os

PYVER = ".".join(map(str, sys.version_info[:3]))
# Determining whether to use __slots__ or __dict__ based on an environment variable
# is a bit weird, but it allows us to process the results into a nice table
# using the `pyperf compare_to` command at the end.
SLOTS = bool(int(os.environ["BENCH_SLOTS"]))  # 1 for __slots__, 0 for __dict__


# IMPORTANT: we benchmark the operation repeatedly, because the loop overhead
# is relatively high. This is recommended for microbenchmark (see pyperf docs).
def bench_getattr(loops, kls):
    range_it = range(loops)
    t0 = time.perf_counter()

    for _ in range_it:
        kls.a
        kls.b
        kls.c
        kls.d
        kls.e
        kls.f
        kls.g
        kls.h
        kls.i
        kls.j

    return time.perf_counter() - t0


runner = pyperf.Runner()


class A:
    __slots__ = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j")

    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.d = 4
        self.e = 5
        self.f = 6
        self.g = 7
        self.h = 8
        self.i = 9
        self.j = 10


class B:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.d = 4
        self.e = 5
        self.f = 6
        self.g = 7
        self.h = 8
        self.i = 9
        self.j = 10


CLS = A if SLOTS else B


# The first few created objects may not be representative since optimizations
# to object layout take a while to kick in
_ = [CLS() for _ in range(1000)]

runner.bench_time_func(f"getattr ({PYVER})", bench_getattr, CLS(), inner_loops=10)
