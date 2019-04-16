import argparse
import queue

from thread_worker import ThreadWorker

from pathlib import Path

from validate_directory import ValidateDirectory

thread_pool = []
work_queue = None


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    global work_queue
    work_queue = _create_work_queue(args.source)
    _initialize_threads(args)

    for thread in thread_pool:
        thread.join()


def _create_arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source", required=True, help="directory, which contains the files", action=ValidateDirectory)
    parser.add_argument("--workers", required=False, help="specify the number of threads", default=8, type=int)
    parser.add_argument("--target", required=True, help="directory, which will contain the output files",
                        action=ValidateDirectory)

    return parser


def _initialize_threads(args):

    for x in range(args.workers):
        _thread = ThreadWorker(x, args.target, work_queue.pop)
        _thread.start()
        thread_pool.append(_thread)


def _create_work_queue(source_dir):
    _work_queue = queue.Queue()
    source_dir = Path(source_dir)

    for file in source_dir.iterdir():
        if not file.is_file():
            continue
        _work_queue.put(file)

    return _work_queue


if __name__ == "__main__":
    main()
