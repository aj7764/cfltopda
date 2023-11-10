def convert_cfl_to_cfg(cfl):
    # For simplicity, let's manually create a CFG for a^n b^n
    cfl_to_cfg = {
        'S': ['', '']
    }
    return cfl_to_cfg


def convert_cfg_to_pda(CFG):
    pda = {
        'states': {'q0', 'q1', 'q2', 'qf'},  # Set of states
        'input_alphabet': {'a', 'b', ''},  # Input alphabet
        'stack_alphabet': {'Z0'},  # Stack alphabet
        'transitions': {
            ('q0', '', 'Z0'): {('q1', 'Z0')},  # Initial transition
            ('q1', 'a', 'Z0'): {('q1', 'aZ0')},  # Push 'a' to stack
            # Move on 'a' without stack change
            ('q1', 'a', 'a'): {('q1', 'aa')},
            # Invalid transition on 'a' with top 'b' in stack
            ('q1', 'a', 'b'): set(),
            # Move to state q2 after reading all 'a's
            ('q1', '', 'Z0'): {('q2', '')},
            # Remove 'a' from stack on 'b' read
            ('q2', 'b', 'a'): {('q2', '')},
            # Accept if stack is empty after all 'b's
            ('q2', 'b', 'Z0'): {('qf', 'Z0')},
        },
        'start_state': 'q0',  # Start state
        'accept_state': 'qf',  # Accept state
    }

    for non_terminal, productions in CFG.items():
        for production in productions:
            pda['input_alphabet'].update(set(production))
            if production == '':
                pda['transitions'][('q0', '', 'Z0')].add(
                    ('qf', 'Z0'))  # Accept epsilon
            else:
                pda['transitions'][('q0', '', 'Z0')].add(
                    ('q0', non_terminal + production))  # Transition to process input
    return pda


def display_pda(pda):
    print("\nPDA:")
    for key, value in pda.items():
        print(f"{key}: {value}")


def get_user_input_cfl():
    cfl = input("Enter the Context-Free Language (CFL): ")
    return cfl


if __name__ == "__main__":
    # Step 1: User input to define CFL
    cfl = get_user_input_cfl()

    # Step 2: Convert CFL to CFG
    CFG = convert_cfl_to_cfg(cfl)

    # Step 3: Convert CFG to PDA
    pda = convert_cfg_to_pda(CFG)
    display_pda(pda)
