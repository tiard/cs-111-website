import argparse
import os
import pathlib
import subprocess

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def css(options):
    sass_path = BASE_DIR / 'cs111.scss'
    static_dir = BASE_DIR / 'cs111' / 'django' / 'static' / 'css'
    os.makedirs(static_dir, exist_ok=True)
    static_path = static_dir / 'cs111.css'
    subprocess.run(['sass', '--sourcemap=none', sass_path, static_path],
                   cwd=BASE_DIR)

def parse(args):
    parser = argparse.ArgumentParser(prog='cs111')

    subparsers = parser.add_subparsers(dest='subparser_name')
    parser_css = subparsers.add_parser('css', help='css help')

    return parser.parse_args(args)
    
def main(args):
    options = parse(args)

    if options.subparser_name == 'css':
        css(options)
