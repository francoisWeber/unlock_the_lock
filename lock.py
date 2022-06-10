import numpy as np

# use a matrix encoding every positive rotations
rotations_ = [np.eye(4)] # on 1 wheel
rotations_ += [np.sum(np.eye(4)[i: (i+2)], axis=0).reshape(1, -1) for i in range(3)] # on 2 contiguous wheels
rotations_ += [np.sum(np.eye(4)[i: (i+3)], axis=0).reshape(1, -1) for i in range(2)] # on 3 contiguous wheels
rotations_ += [np.sum(np.eye(4)[i: (i+4)], axis=0).reshape(1, -1) for i in range(1)] # on 4 contiguous wheels
rotations_pos = np.concatenate(rotations_, axis=0)
rotations_neg = - rotations_pos
ROTATIONS = np.concatenate([rotations_pos, rotations_neg], axis=0)

def get_next_states(current_state):
    next_states = 1 + ((ROTATIONS + np.array(current_state) - 1) % 9)
    return next_states.astype(int).tolist()

def unlock(current_state, target_state, steps=[]):
    if current_state == target_state:
        return steps
    else:
        # generate all possible new states from the current one
        possible_next_states = get_next_states(current_state)
        best_steps = None
        for i, next_state in enumerate(possible_next_states):
            if len(steps) == 0:
                print("a")
            new_step = ROTATIONS[i]
            if len(steps) > 0 and np.abs(new_step + steps[-1]).sum() == 0:
                continue
            steps_ = unlock(next_state, target_state, steps + [new_step])
            if best_steps is None or len(steps_) < best_steps:
                best_steps = steps_
        return best_steps
        

if __name__ == "__main__":
    print(unlock([1, 1, 1, 1], [2, 2, 3, 3]))

