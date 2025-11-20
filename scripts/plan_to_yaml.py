#!/usr/bin/env python3
"""
Simple JSON -> YAML dumper tailored for Terraform plan JSON output.
Produces readable YAML without external dependencies (no PyYAML required).
Usage: python3 scripts/plan_to_yaml.py plan.json plan.yaml
"""
import sys
import json

def quote_str(s):
    import json as _json
    return _json.dumps(s)

def is_simple_key(s):
    # allow safe unquoted keys/values when alphanumeric and limited punctuation
    return all(c.isalnum() or c in '-_./' for c in s)

def dump(node, indent=0, out=sys.stdout):
    prefix = ' ' * indent
    if node is None:
        out.write('null\n')
    elif isinstance(node, bool):
        out.write('true\n' if node else 'false\n')
    elif isinstance(node, (int, float)):
        out.write(str(node) + '\n')
    elif isinstance(node, str):
        if node == '':
            out.write('""\n')
        elif is_simple_key(node):
            out.write(node + '\n')
        else:
            out.write(quote_str(node) + '\n')
    elif isinstance(node, list):
        if not node:
            out.write('[]\n')
        else:
            for item in node:
                out.write(prefix + '- ')
                if isinstance(item, (dict, list)):
                    out.write('\n')
                    dump(item, indent + 2, out)
                else:
                    import io
                    buf = io.StringIO()
                    dump(item, 0, buf)
                    s = buf.getvalue().rstrip('\n')
                    out.write(s + '\n')
    elif isinstance(node, dict):
        if not node:
            out.write('{}\n')
        else:
            for k, v in node.items():
                key = k
                out.write(prefix + str(key) + ': ')
                if isinstance(v, (dict, list)):
                    out.write('\n')
                    dump(v, indent + 2, out)
                else:
                    import io
                    buf = io.StringIO()
                    dump(v, 0, buf)
                    s = buf.getvalue().rstrip('\n')
                    out.write(s + '\n')
    else:
        out.write(quote_str(str(node)) + '\n')


def main():
    if len(sys.argv) != 3:
        print('Usage: plan_to_yaml.py input.json output.yaml', file=sys.stderr)
        sys.exit(2)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    with open(infile, 'r') as f:
        data = json.load(f)
    with open(outfile, 'w') as out:
        dump(data, 0, out)

if __name__ == '__main__':
    main()
