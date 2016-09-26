import ast, _ast, argparse
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('-v', '--verbose', action="store_true")
args = parser.parse_args()

with open(args.file) as f:
    x = f.read()

tree = ast.parse(x)

def render(node) -> str:
    if args.verbose: print(node)
    x = _render(node)
    if args.verbose: print(x)
    return x

def _render(node) -> str:
    if type(node) is _ast.arg:
        return render(node.annotation) + " " + node.arg
    if type(node) is _ast.Import:
        return "\n".join(["#include<"+x.name+">" for x in node.names])
    if type(node) is _ast.Call:
        if node.func.id is "consider":
            return render(node.args[1]) + " " + render(node.args[0])
        elif node.func.id is "namespace":
            return "using namespace " + render(node.args[0])
        else:
            return render(node.func) + "(" + ", ".join([render(x) for x in node.args]) + ")"
    if type(node) is _ast.If:
        return "if (" + render(node.test) + ") {\n" + "\n".join([render(x) for x in node.body]) + ";\n} else {\n" + "\n".join([render(x) for x in node.orelse]) + ";\n}"
    if type(node) is _ast.FunctionDef:
        return render(node.returns) + " " + node.name + " (" + ", ".join([render(x) for x in node.args.args]) + ") {\n" + "\n".join([render(x) + ";" for x in node.body]) + "\n}"
    if type(node) is _ast.Return:
        return "return " + render(node.value)
    if type(node) is _ast.Add:
        return "+"
    if type(node) is _ast.Sub or type(node) is _ast.USub:
        return "-"
    if type(node) is _ast.Mult:
        return "*"
    if type(node) is _ast.Div:
        return "/"
    if type(node) is _ast.FloorDiv:
        return "/"
    if type(node) is _ast.Mod:
        return "%"
    if type(node) is _ast.And:
        return "&&"
    if type(node) is _ast.Or:
        return "||"
    if type(node) is _ast.Gt:
        return ">"
    if type(node) is _ast.Lt:
        return "<"
    if type(node) is _ast.GtE:
        return ">="
    if type(node) is _ast.LtE:
        return "<="
    if type(node) is _ast.Eq:
        return "=="
    if type(node) is _ast.BitAnd:
        return "&"
    if type(node) is _ast.BitOr:
        return "|"
    if type(node) is _ast.RShift:
        return ">>"
    if type(node) is _ast.LShift:
        return "<<"
    if type(node) is _ast.BoolOp:
        return (" "+render(node.op)+" ").join([render(x) for x in node.values])
    if type(node) is _ast.BinOp:
        return " ".join([render(node.left), render(node.op), render(node.right)])
    if type(node) is _ast.Compare:
        return " ".join([render(node.left)]+[render(node.ops[x]) + " " + render(node.comparators[x]) for x in range(len(node.comparators))])
    if type(node) is _ast.UnaryOp:
        return render(node.op)+render(node.operand)
    if type(node) is _ast.Expr:
        return render(node.value)
    if type(node) is _ast.Module:
        return "\n".join([render(x)+";" for x in node.body])
    if type(node) is _ast.Name:
        return node.id
    if type(node) is _ast.Num:
        return str(node.n)
    if type(node) is _ast.Assign:
        return ", ".join([render(x) for x in node.targets]) + " = " + render(node.value)
    if type(node) is _ast.AugAssign:
        return render(node.target) + " " + render(node.op) + "= " + render(node.value)
    if type(node) is _ast.Str:
        return '"'+node.s+'"'
    raise TypeError(type(node))

print(render(tree))
