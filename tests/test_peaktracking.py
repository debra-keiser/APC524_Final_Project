import numpy as np

from src.Peak_Tracking import (calc_diff,extend_matrix_length)

def test_calc_diff():
    """Check that difference is calculated correctly and nan is not included"""
    dummy_tracked_matrix = np.empty((4,29))
    dummy_tracked_matrix[0:3,:] = np.array([[164., 237., 362., 436., 585., 658., 716., 927.,   np.nan,  989., 1247., 1282.,
                   1314.,   np.nan, 1552.,   np.nan,   np.nan, 1682., 1843., 1875., 1901., 2146.,
                   2181., 2216., 2445., 2473., 2513., 2535., 2771.],
                 [165., 237., 361., 435., 589., 664.,   np.nan,  930.,  963.,  988.,   np.nan,   np.nan,
                   1308., 1500., 1533., 1553., 1659., 1685., 1849., 1881., 1911.,   np.nan, 2195.,
                   np.nan, 2449., 2479., 2515., 2545., 2769.],
                 [165., np.nan, 361., 435., 590., 657.,  719.,  928.,  961.,  989.,   np.nan, 1284.,
                   1313., 1497., 1527., 1553., 1657., 1687., 1843., 1874., 1904.,   np.nan, 2184.,
                   2222., 2463.,   np.nan, 2511.,   np.nan, 2770.]])


    dummy_diff_0 = calc_diff(3, 0, 240, dummy_tracked_matrix)
    dummy_diff_1 = calc_diff(3, 1, 240, dummy_tracked_matrix)
    assert dummy_diff_0 == -75
    assert dummy_diff_1 == -3

def test_extend_matrix_length():
    """Check that the returned matrix has extended its length by 1 and 'nan' is added as the new elements"""
    dummy_tracked_matrix = np.array([[164., 237., 362., 436., 585., 658., 716., 927.,   np.nan,  989., 1247., 1282.,
                   1314.,   np.nan, 1552.,   np.nan,   np.nan, 1682., 1843., 1875., 1901., 2146.,
                   2181., 2216., 2445., 2473., 2513., 2535., 2771.],
                 [165., 237., 361., 435., 589., 664.,   np.nan,  930.,  963.,  988.,   np.nan,   np.nan,
                   1308., 1500., 1533., 1553., 1659., 1685., 1849., 1881., 1911.,   np.nan, 2195.,
                   np.nan, 2449., 2479., 2515., 2545., 2769.],
                 [165., np.nan, 361., 435., 590., 657.,  719.,  928.,  961.,  989.,   np.nan, 1284.,
                   1313., 1497., 1527., 1553., 1657., 1687., 1843., 1874., 1904.,   np.nan, 2184.,
                   2222., 2463.,   np.nan, 2511.,   np.nan, 2770.]])
    old_shape = dummy_tracked_matrix.shape
    new_tracked_matrix = extend_matrix_length(dummy_tracked_matrix, 3)
    new_shape = new_tracked_matrix.shape
    assert new_shape[1] == old_shape[1]+1
    assert np.isnan(new_tracked_matrix[0][3]) == True




    