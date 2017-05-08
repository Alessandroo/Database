from database.application.function_mapper import get_db_functions

if __name__ == '__main__':
    print(get_db_functions())
    a = get_db_functions()
    print(a)
    print(a.find_item('update'))

# if __name__ == '__main__':
#     list1 = {}
#     print("via Dict")
#     with Profiler():
#         for i in range(int(1e7)):
#             list1[i] = 10 * i
#     print("get Elem")
#     with Profiler():
#         print(list1[int(1e6 + 1)])
#     # list2 = []
#     # print("via Tuple")
#     # with Profiler():
#     #     for i in range(int(1e7)):
#     #         list2.append((i, i * 10))
#     # print("get Elem")
#     # with Profiler():
#     #     print(list2[list2.index((int(1e6 + 1), int(1e6 + 1)*10))])
#
#     print('size ' + str(sys.getsizeof(list1) / 2 ** 20))
#     # print('size ' + str(sys.getsizeof(list2) / 2 ** 10))
