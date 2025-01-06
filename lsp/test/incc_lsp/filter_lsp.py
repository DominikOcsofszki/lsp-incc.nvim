import re
import json
import sys


def process_lsp_stream(stream):
    """
    Reads and processes LSP JSON-RPC messages from a stream.
    """
    content_length_re = re.compile(r"Content-Length: (\d+)")
    buffer = ""

    while True:
        try:
            # Read a line from the input
            line = stream.readline()
            if not line:
                break

            buffer += line

            # Check for Content-Length header
            match = content_length_re.search(buffer)
            if match:
                content_length = int(match.group(1))
                buffer = buffer[match.end() :].lstrip()  # Remove the processed header

                # Read the JSON message
                while len(buffer) < content_length:
                    buffer += stream.read(content_length - len(buffer))

                # Extract and parse the JSON message
                json_message = buffer[:content_length]
                buffer = buffer[content_length:].lstrip()  # Remove the processed JSON

                try:
                    parsed_json = json.loads(json_message)
                    print(
                        json.dumps(parsed_json, indent=2)
                    )  # Pretty-print the JSON message
                except json.JSONDecodeError:
                    print("Invalid JSON:", json_message)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            break


if __name__ == "__main__":
    # Use standard input to read the stream
    process_lsp_stream(sys.stdin)
