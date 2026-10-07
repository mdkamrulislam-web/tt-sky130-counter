## How it works

An 8-bit synchronous counter increments on each rising edge of `clk` while
`ui[0]` (`en`) is high. `uo[7:0]` shows its value, from 0 to 255, then back to 0.
When enable is low the count holds. Driving `rst_n` low resets the count to zero
on the next rising edge; reset takes priority over enable.

`uio[0]` (`wrap`) is high while count is 255 and enable is high. During continuous
counting this lasts one clock period every 256 clocks, before the overflow edge.
It is combinational, rather than a registered pulse after overflow.
`uio[7:1]` are inputs and their output data is tied to zero.

This is the EE6019 teaching example, prepared from the official SKY130 Verilog
template. It has not been submitted to any shuttle.

## How to test

1. Select the design and apply a clock (the build target is 50 MHz).
2. Hold `rst_n` low through at least one rising edge, then release it.
3. Set `ui[0]` high: `uo[7:0]` counts upwards and wraps after 255.
4. Observe `uio[0]` high at count 255 while enable is high.
5. Set `ui[0]` low: count holds and wrap goes low.
6. Apply reset again to return the count to zero.

Keep enable stable around the clock edge. A real push button needs
synchronisation and debouncing; this minimal example assumes synchronous enable
from the controller or testbench.

The cocotb test checks reset, more than 256 increments, hold, mid-count reset,
and wrap suppression at terminal count. It uses only top-level ports so the same
checks can run on the gate-level netlist.

## External hardware

None beyond the demo board/controller and a clock source. An optional logic
analyser connected to `uio[0]` makes the wrap indication visible.
