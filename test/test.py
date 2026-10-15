# SPDX-FileCopyrightText: 2026 MD. KAMRUL ISLAM
# SPDX-License-Identifier: Apache-2.0
"""Use only shared top-level ports, for RTL and gate-level simulation."""
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer


@cocotb.test()
async def test_project(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    cocotb.start_soon(Clock(dut.clk, 20, unit="ns").start())
    model = 0

    async def step(enable=0, reset=False):
        nonlocal model
        await FallingEdge(dut.clk)
        dut.ui_in.value = enable
        dut.rst_n.value = int(not reset)
        await RisingEdge(dut.clk)
        model = 0 if reset else ((model + enable) & 0xFF)
        await Timer(8, unit="ns")  # allow the gate-level outputs to settle
        assert int(dut.uo_out.value) == model, f"count: expected {model}"
        expected_wrap = int(bool(enable) and model == 255)
        assert int(dut.uio_out.value) == expected_wrap, "wrap or unused output"
        assert int(dut.uio_oe.value) == 1, "only uio[0] should drive an output"
        return expected_wrap

    for _ in range(3):
        await step(reset=True)
    for _ in range(5):
        await step()
    wraps = 0
    for _ in range(266):
        wraps += await step(enable=1)
    assert wraps == 1, f"expected one wrap indication, saw {wraps}"
    for _ in range(20):
        await step()
    for _ in range(7):
        await step(enable=1)
    await step(enable=1, reset=True)
    await step()
    for _ in range(5):
        await step(enable=1)
    # Disabling en at terminal count suppresses wrap and holds count at 255.
    await step(reset=True)
    for _ in range(255):
        await step(enable=1)
    for _ in range(3):
        await step()
    await step(enable=1)
    assert model == 0
    dut._log.info("PASS: reset, counting, overflow, hold and wrap masking")
