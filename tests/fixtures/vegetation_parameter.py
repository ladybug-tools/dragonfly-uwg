import pytest


@pytest.fixture
def default():
    return {
        'vegetation_albedo': 0.25,
        'vegetation_start_month': 0,
        'vegetation_end_month': 0,
        'tree_latent_fraction': 0.7,
        'grass_latent_fraction': 0.5,
    }


@pytest.fixture
def correct():
    return {
        'vegetation_albedo': 0.5,
        'vegetation_start_month': 4,
        'vegetation_end_month': 11,
        'tree_latent_fraction': 0.3,
        'grass_latent_fraction': 0.4,
    }
