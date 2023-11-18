import numba
from numba import njit, types
from numba.typed import Dict as NDict, List as NList
from numba.types import ListType, int32, int64, unicode_type, uint32, UniTuple, boolean as Nboolean, Set as NSet


T_ListType = ListType(int32)
T_ListType_64 = ListType(int64)
T_Tuple_type_3 = UniTuple(int64, 3)
T_Tuple_type_2 = UniTuple(int64, 2)
T_boolean = Nboolean
neasted_list_type = ListType(T_ListType_64)
neasted_tuple_list_type = ListType(T_Tuple_type_3)
