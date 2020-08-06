from binaryninja import PluginCommand
from binaryninja.binaryview import BinaryView
from binaryninja.enums import SegmentFlag

class BugRepro(BinaryView):
    name = "BugRepro"
    long_name = "Database save/load bug repro"

    def __init__(self, data):
        BinaryView.__init__(self, file_metadata=data.file, parent_view=data)

    def init(self):
        # Map file contents at 0x100
        length = len(self.parent_view)
        self.add_auto_segment(
            0x100, length,
            0, length,
            SegmentFlag.SegmentReadable
        )

        return True

    @classmethod
    def is_valid_for_data(cls, data):
        return True

BugRepro.register()

def add_user_segment(data):
    data.add_user_segment(
        0x80, 0x40,
        0, 0,
        SegmentFlag.SegmentReadable
    )

PluginCommand.register(
    "Add user segment to trigger bug",
    "Run this, save the bndb, then load it again",
    add_user_segment
)
