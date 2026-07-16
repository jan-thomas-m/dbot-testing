#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Parse terraform.tf and print required_providers as source/version.

Inspired by https://gist.github.com/straubt1/95a834b82ffebb4db63d8509dd4ce0e4

See https://github.com/hashicorp/terraform/issues/27264 regarding the zh: hashes

"""

import os
import re
import shutil
import sys


def parse_required_providers(filepath: str) -> list[str]:
    """Parse required_providers from a terraform file.

    Args:
        filepath: str - path to the terraform.tf file

    Returns:
        list[str] - list of providers in 'source/version' format
    """

    try:
        content = open(filepath).read()
    except FileNotFoundError as e:
        print(f"Error opening file {filepath}: {e}")
        sys.exit(1)
        # return []

    results = []
    for source, constraint in re.findall(
        r'source\s*=\s*"([^"]+)"\s*version\s*=\s*"([^"]+)"', content
    ):
        version = re.search(r'[\d.]+', constraint).group()
        parts = version.split(".")
        while len(parts) < 3:
            parts.append("0")
        results.append(f"# {source} {constraint}")
        results.append(f"{source}/{'.'.join(parts)}")
    return results


if __name__ == "__main__":
    # for provider in parse_required_providers("./terraform/terraform.tf"):
    #     print(provider)
    local_mirror = "./local_mirror"
    tf_file_path = "./terraform/terraform.tf"

    arch = f"{os.uname().sysname}_{os.uname().machine}".lower()
    # print(os.uname())
    tf_path = os.path.dirname(tf_file_path)
    tf_file = os.path.basename(tf_file_path)

    os.chdir(tf_path)

    for path in ['.terraform', '.terraform.lock.hcl', 'terraform.rc', local_mirror]:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except Exception as e:
                print(f"Error removing {path}: {e}")

    try:
        os.mkdir(local_mirror)
    except FileExistsError:
        pass

    provider = parse_required_providers(tf_file)
    for item in provider:
        if item.startswith('#'):
            continue
        org, name, version = item.split('/', 3)
        # print(item)
        # print(org)
        # print(name)
        # print(version)
        # print()
        provider_dir = f"{local_mirror}/registry.terraform.io/{org}/{name}/{version}/{arch}"

        os.makedirs(provider_dir, exist_ok=True)

        with open(f"{provider_dir}/terraform-provider-{name}_v{version}_x5", "w") as f:
            f.write("")

        # print(f"mkdir -p {provider_dir}")
        # print(f"touch {provider_dir}/terraform-provider-{name}_v{version}_x5")
        # print()

print(f"( cd {tf_path} && terraform init -plugin-dir {local_mirror} )")
