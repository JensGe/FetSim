from common import local
from common import settings as s


def test_save_uuid_to_pickle():
    uuid = "12345678-90ab-cdef-0000-000000000000"

    local.save_uuid_to_pickle(uuid)

    assert local.file_exists(s.uuid_file)
    assert local.get_pickle_uuid() == uuid
