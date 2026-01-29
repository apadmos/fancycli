from __future__ import annotations

import readline
import shlex
import inspect
from typing import List, Tuple, Callable, Optional


class AutoCompleteApp:

    def __init__(self, menu: dict):
        self.menu = menu
        self.states = []

    def _setup_readline_completion(self) -> None:
        """Configure readline for Tab completion on both GNU readline and libedit.

        macOS Python often uses libedit which needs a different binding string.
        """
        doc = getattr(readline, "__doc__", "") or ""
        if "libedit" in doc:
            # macOS' libedit compatibility layer
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            # GNU readline (Linux, many others)
            readline.parse_and_bind("tab: complete")

        # Treat whitespace as delimiters so we complete the current word
        readline.set_completer_delims(" \t\n;")

        # Install the completer callback
        readline.set_completer(self._completer)

    def _completer(self, text: str, state: int):
        # Compute tokens before the current word using the line buffer and begidx
        buf = readline.get_line_buffer()
        begidx = getattr(readline, 'get_begidx', lambda: len(buf))()
        before = buf[:begidx]
        completed_tokens = [t for t in before.strip().split() if t]

        # Determine sub-menu based on completed tokens
        sub_menu = self._follow_to_sub_menu(completed_tokens)
        keys = list(sub_menu.keys()) if isinstance(sub_menu, dict) else []

        # Candidates for current text prefix
        candidates = [k for k in keys if k.startswith(text)] if text else keys

        try:
            return candidates[state]
        except IndexError:
            return None

    def _follow_to_sub_menu(self, keywords: List[str]):
        sub_menu = self.menu
        for kw in keywords:
            if isinstance(sub_menu, dict) and kw in sub_menu:
                sub_menu = sub_menu[kw]
            else:
                return {}
        return sub_menu if isinstance(sub_menu, dict) else {}

    def _resolve_command(self, tokens: List[str]) -> Tuple[Optional[Callable], List[str], Optional[str]]:
        """Resolve tokens to a callable and its positional args.

        Returns (callable_or_none, args, error_message_or_none)
        """
        sub = self.menu
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if isinstance(sub, dict) and t in sub:
                sub = sub[t]
                i += 1
            else:
                break
        if callable(sub):
            return sub, tokens[i:], None
        # If we consumed all tokens but ended on a dict, it's incomplete path
        if isinstance(sub, dict):
            available = " ".join(list(sub.keys()))
            return None, [], f"Incomplete command. Options: {', '.join(sub.keys())}"
        return None, [], "Unknown command"

    def _execute_callable(self, func: Callable, args: List[str]) -> None:
        """Execute callable with basic arity checking. Args are strings.
        """
        try:
            sig = inspect.signature(func)
        except (TypeError, ValueError):
            # Fallback if signature cannot be obtained
            sig = None
        try:
            func(*args)
        except TypeError as te:
            if sig is not None:
                print(f"TypeError: {te}. Usage: {getattr(func, '__name__', str(func))}{sig}")
            else:
                print(f"TypeError: {te}.")
        except Exception as e:
            print(f"Error executing command: {e}")

    def run(self) -> int:
        self._setup_readline_completion()

        print("Tab completion demo. Try typing 's' then press Tab. Type 'exit' to quit.")
        while True:
            try:
                line = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not line or not line.strip():
                continue

            line = line.strip()
            if line in {"exit", "quit"}:
                break

            try:
                tokens = shlex.split(line)
            except ValueError as ve:
                print(f"Input parse error: {ve}")
                continue

            func, args, err = self._resolve_command(tokens)
            if func is not None:
                self._execute_callable(func, args)
            else:
                if err:
                    print(err)
                else:
                    print("Unknown command. Use Tab to explore available options.")

        return 0


if __name__ == "__main__":
    def print_x(x):
        print(x)


    def merge(x, y):
        print(x, y)


    def merge_void():
        print("merge void")


    menu = {
        "print": {
            "left": print_x,
            "right": print_x,
        },
        "void": {
            "one": merge_void,
            "right": lambda x: print(x),
        },
        "merge": merge
    }
    ac = AutoCompleteApp(menu)
    ac.run()
