import os
import pickle

from HealthAnalysis.data_manager_google import DataManagerGoogle
from HealthAnalysis.data_manager_apple import DataManagerApple
from HealthAnalysis.data_manager_samsung import DataManagerSamsung


def get_hourly_steps(steps):

    for time_struct, step in steps:
        pass



def main():
    data_manager = DataManagerGoogle('google_data/')
    step_list = data_manager.get_steps()
    counts = get_hourly_steps(step_list)

    print('0 to 23: {0}'.format(counts))

    os.makedirs('line_data', exist_ok=True)
    with open('line_data/hours.pickle', 'wb') as f:
        pickle.dump((hours, counts), f)


if __name__ == '__main__':
    main()
