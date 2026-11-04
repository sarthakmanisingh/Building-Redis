import sys

def encode_bulk_string(s):
    if s is None:
        return "$-1\r\n"
    return f"${len(s)}\r\n{s}\r\n"

def encode_simple_string(s):
    return f"+{s}\r\n"

def handle_command(args):
    cmd = args[0].upper()
    if cmd == "PING":
        if len(args) == 1:
            return encode_simple_string("PONG")
        return encode_bulk_string(args[1])
    elif cmd == "ECHO":
        return encode_bulk_string(args[1:][0])
        # TODO: Return args[1] as a bulk string
        pass
    return f"-ERR unknown command '{cmd}'\r\n"

def parse_args(line):
    args, current, in_q = [], "", False
    for ch in line:
        if ch == '"': in_q = not in_q
        elif ch == ' ' and not in_q:
            if current: args.append(current); current = ""
        else: current += ch
    if current: args.append(current)
    return args

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    sys.stdout.write(handle_command(parse_args(line)))
    sys.stdout.flush()
