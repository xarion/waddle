import requests


def get_metadata():
    metadata_server = "http://metadata/computeMetadata/v1/instance/"
    metadata_flavor = {'Metadata-Flavor': 'Google'}
    gce_id = requests.get(metadata_server + 'id', headers=metadata_flavor).text
    gce_name = requests.get(metadata_server + 'hostname', headers=metadata_flavor).text
    gce_machine_type = requests.get(metadata_server + 'machine-type', headers=metadata_flavor).text
    gce_zone = requests.get(metadata_server + 'zone', headers=metadata_flavor).text
    return {"gce_id": gce_id,
            "gce_name": gce_name,
            "gce_machine_type": gce_machine_type,
            "gce_zone": gce_zone}