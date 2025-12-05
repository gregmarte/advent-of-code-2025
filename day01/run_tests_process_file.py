import os
import importlib.util
import sys


def load_process_file():
    here = os.path.dirname(__file__)
    lp_path = os.path.join(here, "lock_picker.py")
    spec = importlib.util.spec_from_file_location("lock_picker", lp_path)
    if spec is None:
        raise ImportError(f"Could not load spec for {lp_path}")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"Could not load loader for {lp_path}")
    spec.loader.exec_module(module)
    return module.process_file


def main():
    process_file = load_process_file()
    base = os.path.dirname(__file__)
    test_files_e1 = ["tests/test01.txt", "tests/test02.txt", "tests/test03.txt", "tests/test04.txt"]
    test_files_e2 = ["tests/test05.txt", "tests/test06.txt", "tests/test07.txt", "tests/test08.txt"]

    for rel in test_files_e1:
        fp = os.path.join(base, rel)
        print(f"Running: {fp}")
        result = process_file(fp)
        print(f" -> Returned: {result}\n")
        if result != 1:
            print(f"🛑 Test failed for '{rel}': expected 1, got {result}")
            sys.exit(2)

    for rel in test_files_e2:
        fp = os.path.join(base, rel)
        print(f"Running: {fp}")
        result = process_file(fp)
        print(f" -> Returned: {result}\n")
        if result != 2:
            print(f"🛑 Test failed for '{rel}': expected 2, got {result}")
            sys.exit(2)

    print("All tests passed.")


if __name__ == '__main__':
    main()
