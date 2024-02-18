
from typing import Dict, List
import re


class Ini_Parser():
    """
        I wrote this small .ini Parser because existing parsers were buggy and
        ConfigParser does not allow for duplicate keys, of which FL has a lot.

        It's dumb but it works for freelancer if you just want to see what an
        ini-file contains. There is one dict for each "block" in the ini-file, e.g. this:

        [FactionProps]
        affiliation = gd_z_grp
        npc_ship = gd_z_ge_fighter4_d9
        npc_ship = gd_z_ge_fighter4_d10
        space_costume = comm_br_elite
        space_costume = ge_male6_head, comm_br_darcy

        would be one dict. Each key in the ini-block is added to the dict, but with
        a list instead of a single string / tuple as value. So this would create
        a dict like this:

        {"affiliation" : ["gd_z_grp"], "npc_ship" : ["gd_z_ge_fighter4_d9", "gd_z_ge_fighter4_d10"], space_costume : ["comm_br_elite", "ge_male6_head", "comm_br_darcy"]}
    """

    def read(self, ini_path):
        # Get string from file
        try:
            with open(ini_path, "r") as ini_file:
                content = ini_file.read()
            return self.parse(content)
        except:
            return []
        

    def parse(self, file_content : str):
        # This will looks like
        # [{key: [values], key2: [values]}, {...}, ...]
        result = []

        # newlines seem to be reliable enough
        blocks = re.split(r"\r\r|\n\n", file_content)
        for block in blocks:
            block_dict = {}
            entries = re.split(r"\r|\n", block)
            for entry in entries:
                # Empty lines, block names, comments
                if entry == "" or bool(re.search(r"\[", entry)) or entry.startswith(";") or entry.startswith("#"):
                    continue
                key = entry.split("=")[0].strip()
                values = entry.split("=")[1].strip()
                if key in block_dict.keys():
                    block_dict[key] += values.split(", ")
                else:
                    block_dict[key] = values.split(", ")
            if block_dict != {}:
                result.append(block_dict)
                print("LAST BLOCK: ", result[-1])
        
        return result