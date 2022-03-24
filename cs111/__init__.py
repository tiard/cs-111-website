import argparse
import os
import pathlib
import shutil
import subprocess

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def css(options):
    sass_path = BASE_DIR / 'cs111.scss'
    static_dir = BASE_DIR / 'cs111' / 'django' / 'static' / 'css'
    os.makedirs(static_dir, exist_ok=True)
    static_path = static_dir / 'cs111.css'
    subprocess.run(['sass', '--no-source-map', sass_path, static_path],
                   cwd=BASE_DIR)

def favicon(options):
    favicon_dir = BASE_DIR / 'favicon'
    subprocess.run(['latexmk'], cwd=favicon_dir)
    favicon_path = BASE_DIR / 'favicon' / 'favicon.png'
    static_dir = BASE_DIR / 'cs111' / 'django' / 'static'
    shutil.copy(favicon_path, static_dir)

def parse(args):
    parser = argparse.ArgumentParser(prog='cs111')

    subparsers = parser.add_subparsers(dest='subparser_name')
    parser_css = subparsers.add_parser('css', help='css help')
    parser_favicon = subparsers.add_parser('favicon', help='favicon help')

    return parser.parse_args(args)
    
def main(args):
    options = parse(args)

    if options.subparser_name == 'css':
        css(options)
    if options.subparser_name == 'favicon':
        favicon(options)
