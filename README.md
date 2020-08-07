This plugin exists solely to demonstrate a bug in certain versions of Binary
Ninja. It does nothing else useful.

The bug in question appears on newer versions of Binary Ninja. I can't quantify
that further than to say that it is not present in version 1.1.1338-dev and is
present in version 2.1.2263, which I'm aware is a huge range.

The bug happens when using a BinaryView that creates an auto segment. To trigger
it, create a user segment with a start address before the auto segment. Then,
save and reload the bndb, and observe that the user segment has taken the start
address of the auto segment, and the portion of the auto segment which it now
overlaps (which, if the user segment is larger, is all of it) no longer exists.

Detailed repro steps:
 1. Open any data file in Binary Ninja. (`demo-files/` contains a 4-byte and a
    256-byte test file, each containing sequentially increasing byte values to
    make it easy to see what's going on.)
 2. Switch to the BinaryView provided by this plugin, "Database save/load bug
    repro" and to Linear Disassembly.
 3. Observe that the file contents are mapped as a read-only auto segment at
    address 0x100. This is correct behavior.
 4. Click "Tools > Add user segment to trigger bug". Observe that a new
    read-only user segment of length 0x40 is mapped at 0x80. This is also
    correct behavior.
 5. Save an analysis database, then immediately open that analysis database.
    Again select this plugin's BinaryView with Linear Disassembly.
 6. Observe that the user segment which was previously at 0x80 has magically
    moved to 0x100 and that the auto segment (or portion of an auto segment)
    which previously occupied 0x100-0x13f no longer is mapped. This is the bug.
    Saving and reloading an analysis database should not change segment
    mappings at all.
