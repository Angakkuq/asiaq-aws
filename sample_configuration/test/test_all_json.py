"""Validates all json files for syntax"""
from unittest import TestCase
import json
import os
import os.path


class DiscoJsonTests(TestCase):
    """Validates all json files for syntax"""
    @staticmethod
    def test_all_json():
        """Validates all json files for syntax"""
        where = ["iam/"]
        except_extensions = ["grp", "rst", "DS_Store"]
        files = [
            os.path.join(dirpath, filename)
            for path in where
            for dirpath, _, filenames in os.walk(path)
            for filename in filenames
            if filename.split(".")[-1] not in except_extensions]

        for filename in files:
            with open(filename, "r") as file_buffer:
                contents = file_buffer.read()
                if contents == "":
                    # some bucket logging configuration files are intentionally left blank
                    # in order to overwrite default logging configuration
                    # e.g., iam/s3/prod/REGION.disco.s3audit.prod.logging
                    continue
                try:
                    json.loads(contents)
                except ValueError as ex:
                    raise ValueError("Invalid JSON in {0}: {1}".format(filename, repr(ex)))

        # print a summary; only appears if we do `nosetests -s`
        print "JSON-validated {0} files".format(len(files))
