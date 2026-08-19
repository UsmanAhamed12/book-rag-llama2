import uvicorn
from alembic.config import Config

from alembic import command


def main() -> None:
    config = Config("alembic.ini")
    command.upgrade(config, "head")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
