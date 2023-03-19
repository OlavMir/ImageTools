from functools import wraps
from datetime import datetime
import traceback

def try_func(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        time_started = datetime.now()
        try:
            print(f"start {f.__name__}")
            res = f(*args, **kwargs)    
            return res            
        except Exception as e:
            print(f'{f.__name__} ERROR {str(e)} \n{traceback.format_exc()}\n')                
        finally:
            print(f'{f.__name__} completed in {datetime.now() - time_started}')
    return wrapper