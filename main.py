import sys

def encode_bulk_string(s):
    if s is None: return "$-1\r\n"
    return f"${len(s)}\r\n{s}\r\n"
def encode_simple_string(s): return f"+{s}\r\n"
def encode_error(msg): return f"-{msg}\r\n"
def encode_integer(n): return f":{n}\r\n"

def handle_command(args):
    cmd = args[0].upper()
    if cmd == "PING":
        return encode_simple_string("PONG") if len(args) == 1 else encode_bulk_string(args[1])
    elif cmd == "ECHO":
        return encode_bulk_string(args[1])
    elif cmd == "COMMAND":
        # TODO: Return +OK for COMMAND DOCS
        return encode_simple_string("OK")
        
    
    return encode_error(f"ERR unknown command '{cmd}'")
    # TODO: Return error for unknown commands
    

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
