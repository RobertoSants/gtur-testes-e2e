import os
import pytest


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:5173")


@pytest.fixture(autouse=True)
def pausa_final_para_video(page, request):
    yield
    if request.config.getoption("--video", default="off") != "off":
        page.wait_for_timeout(2000)