from tempfile import mkstemp
from shutil import move
from os import remove, close

from database.utils.JSON import from_json, to_json
from database.utils.profiler import Profiler

if __name__ == '__main__':
    file_path = "ex1.json"
    # tempname = filename + '.temp'  # os.tempnam() gives warning

    with Profiler():
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    obj = from_json(line)
                    if 'age' in obj:
                        obj['age'] = obj['age']%100
                    new_file.write(to_json(obj) + '\n')
        close(fh)
        # Remove original file
        remove(file_path)
        # Move new file
        move(abs_path, file_path)

        # with open(filename) as fin:  # python 2.6
        #     with open(tempname, 'w') as fout:  # compatible
        #         for line in fin:
        #             obj = from_json(line)
        #             if 'age' in obj:
        #                 obj['age'] = obj['age']%100
        #             fout.write(to_json(obj)+ '\n')
        # os.rename(tempname, filename)