import os
from wrappers import try_func

@try_func
def get_files_list(root: str, endswith: tuple = None) -> list[str]:
    """
    getting all paths files from folder
    """
    print(f"Get files {endswith} from folder {root}")
    files_counter = 0
    result = []
    for (dirname, subshare, fileshare) in os.walk(root):
        files_counter += len(fileshare)
        for fname in fileshare:
            if endswith:
                if fname.endswith(endswith):
                    result.append(os.path.join(dirname, fname))
            else:
                result.append(os.path.join(dirname, fname))
    print(f"\t Load {len(result)} list paths")
    return result