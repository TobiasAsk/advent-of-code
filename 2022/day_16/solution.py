import re
import sys
from functools import cache


VALVE_PATTERN = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnels* leads* to valves* ([\w\s,]*)")


class Network:

    def __init__(
            self, tunnels: dict[str, list[str]],
            flow_rates: dict[str, int]):
        self.tunnels = tunnels
        self.flow_rates = flow_rates

    @cache
    def get_max_pressure(
            self, valve: str,
            remaining_minutes: int,
            open_valves: frozenset[str],
            player_turn: bool):

        if remaining_minutes == 0:
            if player_turn:
                return self.get_max_pressure('AA', 26, open_valves, False)
            return 0

        open_valve_option = (self.flow_rates[valve] * (remaining_minutes-1) + self.get_max_pressure(
            valve, remaining_minutes-1, open_valves | {valve}, player_turn)
            if self.flow_rates[valve] > 0 and valve not in open_valves
            else 0)

        move_to_other_options = [self.get_max_pressure(
            v, remaining_minutes-1, open_valves, player_turn) for v in self.tunnels[valve]]

        return max(move_to_other_options + [open_valve_option])

    @classmethod
    def from_file(cls, file_name):
        tunnels, flow_rates = {}, {}
        with open(file_name) as network_input_file:
            for line in network_input_file:
                valve_info_match = VALVE_PATTERN.search(line.strip())
                valve_name, flow_rate = valve_info_match.group(
                    1), int(valve_info_match.group(2))
                neighbor_names = valve_info_match.group(3).split(', ')

                flow_rates[valve_name] = flow_rate
                tunnels[valve_name] = neighbor_names

            return Network(tunnels=tunnels, flow_rates=flow_rates)


def main():
    file_name = sys.argv[1]
    network = Network.from_file(file_name)
    max_pressure = network.get_max_pressure('AA', 26, frozenset(), True)
    sys.stdout.write(f'Max pressure is {max_pressure}\n')


if __name__ == "__main__":
    main()
