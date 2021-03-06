import sys
import os

sys.path.append('../devel/phd')

import lab.simulation.simulation as sim
import lab.simulation.forcings as forcings
import lab.simulation.systems as systems
import lab.simulation.integrators as integrators

from slackclient import SlackClient
# instantiate Slack client
sc = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

DATA_PATH = os.environ.get('BASE_DATA_PATH')

point_const = sim.SystemState(coords=[8]*32)
point_const.perturbate()
constant_force = forcings.ConstantForcing()
system = systems.Lorenz96()
int_method = integrators.RungeKutta4()

simulator_const = sim.Simulator(
    system_state=point_const,
    forcing=constant_force,
    int_method=int_method,
    system=system
)

runner = sim.SimulationRunner(
    simulator=simulator_const,
    integration_time=1001000,
    chunk_length_time=1000,
    write_all_every=10,
    write_one_every=0
)

outfiles = runner.run(
    data_base_path=DATA_PATH,
    custom_suffix='init'
)

for outfile in outfiles:
    sc.api_call(
        "chat.postMessage",
        channel="#l96lrt",
        text="Simulation {} done!".format(outfile)
    )

