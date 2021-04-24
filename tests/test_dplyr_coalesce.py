# https://github.com/tidyverse/dplyr/blob/master/tests/testthat/test-coalesce.R
import pytest

from datar.all import *
from .conftest import assert_iterable_equal

def test_missing_replaced():
    x = [NA, 1]
    out = coalesce(x, 1)
    assert out.tolist() == [1,1]

def test_common_type():
    out = coalesce(NA, 1)
    assert out == 1

    f = factor("x", levels=["x", "y"])
    out = coalesce(NA, f)
    assert out == f

def test_multiple_replaces():
    x1 = c(1, NA, NA)
    x2 = c(NA, 2, NA)
    x3 = c(NA, NA, 3)
    out = coalesce(x1, x2, x3)
    assert out.tolist() == [1,2,3]

def test_errors():
    # can still coalesce with a shorter or longer array
    out = coalesce([1,2,NA], [1,2])
    out[is_na(out)] = 100
    assert out.tolist() == [1.0,2.0,100.0]

    # works
    out = coalesce([1,2], letters[:2])
    assert out.tolist() == [1,2]

def test_with_dataframes():
    out = coalesce(
        tibble(x = c(NA, 1)),
        tibble(x = [1,2])
    )
    assert out.x.tolist() == [1,1]

    df1 = tibble(x = c(NA, 1, NA), y = c(2, NA, NA), z = c([1,2], NA))
    df2 = tibble(x = [1,2,3], y = c(3, 4, NA), z = c(NA, NA, NA))
    df3 = tibble(x = NA, y = c(30, 40, 50), z = [101,102,103])
    out = coalesce(df1, df2, df3)
    expect = tibble(x = c(1.0, 1.0, 3.0), y = c(2.0, 4.0, 50.0), z = c(1.0, 2.0, 103.0))
    assert out.equals(expect)

def test_no_rep():
    x = c(1,2,NA,NA,5)
    out = coalesce(x)
    assert_iterable_equal(x, out)
