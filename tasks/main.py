import os
import inspect
def DEBUG(format="", linChar=""):
    # Get the current frame
    frame = inspect.currentframe()
    # Get the caller's frame (where DEUG is called)
    caller_frame = frame.f_back
    # Extract file name and line number
    file_name = os.path.basename(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno
    # Return formatted string
    print( f"{file_name}, line {line_number} ::{linChar} {format}")
