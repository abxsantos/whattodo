import pytest


@pytest.fixture
def board_dict():
    return {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }


@pytest.fixture
def expected_board_dict():
    return {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": False,
                "created_at": "2020-12-26 15:13:56",
            },
            {
                "description": "my added task",
                "status": False,
                "created_at": "2020-12-26 00:00:00",
            },
        ],
    }


@pytest.fixture
def expected_status_change_board_dict():
    return {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
            {
                "description": "my second task",
                "status": True,
                "created_at": "2020-12-26 15:13:56",
            },
        ],
    }


@pytest.fixture
def expected_empty_board_dict():
    return {
        "name": "personal",
        "tasks": [],
    }


@pytest.fixture
def expected_removed_task_board_dict():
    return {
        "name": "personal",
        "tasks": [
            {
                "description": "my first task",
                "status": False,
                "created_at": "2020-12-26 15:13:45",
            },
        ],
    }

