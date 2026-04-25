from ui.widgets import banner


from services import (
    DEFAULT_MESSAGE_API_BASE_URL,
    MessageService,
    MessageServiceError,
)


def render() -> None:
    banner(
        "Form Widget",
        "Demo form untuk mengirim dan mengambil data dari endpoint say-hello.",
    )