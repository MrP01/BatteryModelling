import invoke
import sys


@invoke.task()
def run_trial(ctx, model="lithium-ion"):
    ctx.run(f"{sys.executable} playground/pybamm_trial.py {model}")
