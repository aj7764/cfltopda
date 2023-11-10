from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def convert_cfl_to_cfg(cfl):
    # For simplicity, let's manually create a CFG for a^n b^n
    cfl_to_cfg = {
        'S': ['', '']
    }
    return cfl_to_cfg

def convert_cfg_to_pda(CFG):
    pda = {
        'states': {'q0', 'q1', 'q2', 'qf'},
        'input_alphabet': {'a', 'b', ''},
        'stack_alphabet': {'Z0'},
        'transitions': {
            ('q0', '', 'Z0'): {('q1', 'Z0')},
            ('q1', 'a', 'Z0'): {('q1', 'aZ0')},
            ('q1', 'a', 'a'): {('q1', 'aa')},
            ('q1', 'a', 'b'): set(),
            ('q1', '', 'Z0'): {('q2', '')},
            ('q2', 'b', 'a'): {('q2', '')},
            ('q2', 'b', 'Z0'): {('qf', 'Z0')},
        },
        'start_state': 'q0',
        'accept_state': 'qf',
    }

    for non_terminal, productions in CFG.items():
        for production in productions:
            pda['input_alphabet'].update(set(production))
            if production == '':
                pda['transitions'][('q0', '', 'Z0')].add(('qf', 'Z0'))
            else:
                pda['transitions'][('q0', '', 'Z0')].add(('q0', non_terminal + production))

    return pda

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    cfl = data['cfl']

    # Convert CFL to CFG
    CFG = convert_cfl_to_cfg(cfl)

    # Convert CFG to PDA
    pda_result = convert_cfg_to_pda(CFG)

    # Convert sets to lists before jsonify
    pda_result['states'] = list(pda_result['states'])
    pda_result['input_alphabet'] = list(pda_result['input_alphabet'])
    pda_result['stack_alphabet'] = list(pda_result['stack_alphabet'])

    # Convert tuple keys to strings in transitions dictionary
    pda_result['transitions'] = {str(key): list(value) for key, value in pda_result['transitions'].items()}

    return jsonify({"pda": pda_result})

if __name__ == '__main__':
    app.run(debug=True)


