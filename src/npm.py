import log;
import subprocess as spc;
import json;

"""
Get info about dependencies for a package name and version
"""
def get_dependencies(name, version, data = "dependencies"):
    # Split at every space on command line
    commandLine = ["npm", "view", name + "@" + version, data, "--json"];

    res = spc.run(commandLine, stdout=spc.PIPE);
    json_str = res.stdout.decode("utf-8");
    json_obj = json.loads(json_str);

    # Construct object to describe dependencies for given package
    dependency_info = {
        "dependencies": [], # List of package name and versions dependent upon
        "invalid": 0 # Amount of invalid version lookups
    }

    for name in json_obj.keys():
        decoded_ver = decode_version(name, json_obj[name]);

        if decoded_ver:
            dependency_info["dependencies"].append({"name": name, "version": decoded_ver});
        else:
            dependency_info["invalid"] += 1;

    return dependency_info;

"""
Translate a version given as a dependency to a concrete version on format 1.2.3

All possible version identifiers can
be found at https://docs.npmjs.com/files/package.json#dependencies
"""
def decode_version(name, ver_str):
    name_format = "{}@{}".format(name, ver_str);
    get_versions_cmd = ["npm", "view", name_format, "version", "--json"];

    res = spc.run(get_versions_cmd, stdout=spc.PIPE);
    json_str = res.stdout.decode("utf-8");

    if(not json_str):
        # Invalid version OR reference outside npm
        return False;

    json_obj = json.loads(json_str);

    if(isinstance(json_obj, str)):
        # If only one mathcing version json_obj will be str
        version = json_obj;
    else:
        version = json_obj[-1];

    return version;

def get_dev_dependencies(name, version):
    return get_dependencies(name, version, devDependencies);