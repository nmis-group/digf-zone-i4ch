const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    var ia: usize = 0;
    var ib: usize = 1;
    var ic: usize = 1;
    while (ic  <= 50) : (ic = ia+ib, ia = ib, ib = ic) {
        try stdout.print("{d}\n", .{ia});
        }
}
