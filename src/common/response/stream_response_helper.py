import asyncio
import json


class Stream_response_helper:
    async def stream_response(data: str, event: str):
        lines = []
        if event:
            lines.append(f"event: {event}")
        for line in data.splitlines():
            lines.append(f"data: {line}")
        lines.append("")  # End of event
        return ("\n".join(lines) + "\n").encode("utf-8")

    async def fake_sse():
        """A simple async generator to stream dummy text tokens."""
        tokens = ["Hello", " from", " SSE", " world!"]
        for token in tokens:
            await asyncio.sleep(0.5)  # Simulate delay
            yield await Stream_response_helper.stream_response(
                json.dumps({"token": token}), event="message"
            )
        yield await Stream_response_helper.stream_response("[DONE]", event="done")
