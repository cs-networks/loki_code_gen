#!/usr/bin/env python3
"""
    ──────────────▐█████───────
    ──────▄▄████████████▄──────
    ────▄██▀▀────▐███▐████▄────
    ──▄██▀───────███▌▐██─▀██▄──
    ─▐██────────▐███─▐██───██▌─
    ─██▌────────███▌─▐██───▐██─
    ▐██────────▐███──▐██────██▌
    ██▌────────███▌──▐██────▐██
    ██▌───────▐███───▐██────▐██
    ██▌───────███▌──▄─▀█────▐██
    ██▌──────▐████████▄─────▐██
    ██▌──────█████████▀─────▐██
    ▐██─────▐██▌────▀─▄█────██▌
    ─██▌────███─────▄███───▐██─
    ─▐██▄──▐██▌───────────▄██▌─
    ──▀███─███─────────▄▄███▀──
    ──────▐██▌─▀█████████▀▀────
    ──────███──────────────────
Loki - Code Generator for the Avengers Project.
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import argparse
import sys
import json
import os
import chevron


def lowercase(text, render):
    # inject data into scope
    return render(text).lower()

def main():  # pylint: disable=too-many-statements
    """Loki - Code Generator for the Avengers Project.
    """
    logger = logging.getLogger("Loki Code Generator")

    # Console Logger
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Parse settings from command line
    parser = argparse.ArgumentParser(description="Code Generator for the Avengers Project.")
    args_basic = parser.add_argument_group("Basic")
    args_basic.add_argument("-d", "--debug", action="store_true", help="Display detailed informations during processing.")
    args_basic.add_argument("-l", "--log", action="store_true", help="Writes log messages to a logfile.")

    args_loki = parser.add_argument_group("Loki")
    args_loki.add_argument("-i", "--input", help="Data-file containing all information for the template.")
    args_loki.add_argument("-o", "--over_write", action="store_true", help="Overwrites output files without asking.")

    try:
        args = parser.parse_args()

        if args.log:
            fh = TimedRotatingFileHandler('logs/loki.log', when='midnight', backupCount=10)
            fh.suffix = '%Y_%m_%d.log'
            fh.setFormatter(formatter)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)

        if args.debug:
            logger.setLevel(logging.DEBUG)

        if args.input is not None:
            try:
                with open(args.input) as json_file:
                    logger.debug("Opening Source file: %s", args.input)
                    data = json.load(json_file)
            except OSError as err:
                logger.exception("ERROR: %s", err)
                sys.exit(1)
        else:
            logger.fatal("No Input File given.")
            sys.exit(1)

        for item in data['meta_data']:
            if args.over_write:
                try:
                    logger.debug("Checking for Outputfile: %s", item['output'])
                    os.remove(item['output'])
                except OSError:
                    pass
            else:
                logger.debug("Checking for Outputfile: %s", item['output'])
                if os.path.isfile(item['output']):
                    logger.fatal("Ouput File allready exists.")
                    sys.exit(1)

            try:
                logger.debug("Processing Source file: %s", args.input)
                with open(item['template'], 'r') as template:
                    logger.debug("Processing Template file: %s", item['template'])
                    with open(item['output'], 'w') as results_file:
                        logger.debug("Write Output file: %s", item['output'])
                        input_data = data['data']
                        input_data['lowercase'] = lowercase
                        results_file.write(chevron.render(template, input_data))

            except OSError as err:
                logger.exception("ERROR: %s", err)
                sys.exit(1)

    except Exception as e:  # pylint: disable=broad-except
        logger.exception("ERROR: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
