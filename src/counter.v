// counter.v - N-bit synchronous up-counter with enable and synchronous reset.
// Example design for the EE6019 open chip flow.
`timescale 1ns / 1ps
`default_nettype none

module counter #(
    parameter WIDTH = 8
) (
    input  wire             clk,
    input  wire             rst,     // synchronous, active high
    input  wire             en,      // count when high
    output reg  [WIDTH-1:0] count,
    output wire             wrap     // high for the cycle count is all ones and en is high
);

    always @(posedge clk) begin
        if (rst)
            count <= {WIDTH{1'b0}};
        else if (en)
            count <= count + 1'b1;
    end

    assign wrap = en & (&count);

endmodule

`default_nettype wire
