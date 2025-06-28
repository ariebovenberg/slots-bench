import gc
import tracemalloc


def memory_compare(n_attrs):
    """Test the memory usage of slots vs no slots."""
    attrnames = [f"field_{i}" for i in range(n_attrs)]

    def init(self):
        for n in attrnames:
            setattr(self, n, None)

    class A:
        __slots__ = attrnames
        __init__ = init

    class B:
        __init__ = init

    # The first objects may be larger due to implementation details.
    [A() for _ in range(1_000)]
    [B() for _ in range(1_000)]

    size_w_slots = sizeof_by_tracemaloc(A)
    size_w_dict = sizeof_by_tracemaloc(B)
    print(
        f"__slots__ saves (with {n_attrs} attrs): {size_w_dict - size_w_slots:.2f} bytes per object"
    )


def sizeof_by_tracemaloc(klass):
    """Get the size of object instances of a class using tracemalloc."""
    gc.collect()  # clear freelists
    tracemalloc.start()
    _ = [klass() for _ in range(1_000_000)]
    return (
        tracemalloc.get_traced_memory()[0]
        / 1_000_000  # divide to get the size per object
    ) - 8  # subtract 8 bytes for the overhead of the list itself


if __name__ == "__main__":
    for i in range(1, 30):
        memory_compare(i)
