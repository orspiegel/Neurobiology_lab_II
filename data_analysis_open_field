import scipy.io
import os
from scipy import stats

def load_mat_data(file):
    mat = scipy.io.loadmat(file)
    # print(len(mat))
    crossing_times = mat['crossing_times']
    grooming_start_stop = mat['grooming_start_stop']
    periphery_times = mat['periphery_times']
    mouse_data = {'crossing_times': crossing_times,
                  'grooming': grooming_start_stop,
                  'priphery_times': periphery_times}
    return mouse_data

def all_year_data_crossing(trails_per_year):
    """
    @input - all mat files from: curr year or from last year
    @output - list of all crossing vectors for that given year,
    the 1st in the mat file for each mat file.
    """

    union_cross_data = [load_mat_data(trail)['crossing_times'] for trail in trails_per_year]
    return union_cross_data

def all_year_data_grooming(trails_per_year):
    """
    @input - all mat files from: curr year or from last year
    @output - list of all grooming vectors for that given year,
    the 2nd in the mat file for each mat file.
    """
    union_grooming_data = [load_mat_data(trail)['periphery_times'] for trail in trails_per_year]
    return union_grooming_data

def all_year_data_periphery_crossing(trails_per_year):
    """
    @input - all mat files from: curr year or from last year
    @output - list of all periphery crossing vectors for that given year,
    the 3rd in the mat file for each mat file.
    """
    union_priph_data = [load_mat_data(trail)['grooming_start_stop'] for trail in trails_per_year]
    return union_priph_data

if __name__ == '__main__':
    # list of all curr year trails
    path_curr_year = "raw_data_package"
    curr_year_trails = os.listdir(path_curr_year)
    curr_paths = [os.path.join(path_curr_year, x) for x in curr_year_trails]
    # list of all last year trails
    path_former_year = "raw_data_former_year"
    former_year_trails = os.listdir(path_former_year)
    former_paths = [os.path.join(path_former_year, x) for x in former_year_trails]

    # all of 2022 trails in one set
    cross_curr_data_union = all_year_data_crossing(curr_paths)
    # all of 2021 trails in one set
    cross_former_data_union = all_year_data_crossing(former_paths)
    # now we can compare these 2 sets by checking their variance; by Kruskal because there are
    # dependencies inside the groups.
    cross_var_between_years = stats.kruskal(cross_curr_data_union, cross_former_data_union)
    print(f'Kruskal result for two years: {cross_var_between_years}')


