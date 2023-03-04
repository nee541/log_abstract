from collections import namedtuple
import re
from glob import glob

from itertools import groupby

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

# file, start and end identify the log statement, file refers to the file that the log statement belogs to, start refers to the position of the start of the log statement, the same as end
LogInfo = namedtuple('LogInfo', ['template', 'parameter', 'level', 'comments', 'method', 'file', 'start', 'end'])

# must have re.VERBOSE/re.X flag, e.g. re.compile(JAVA_METHOD_PATTERN, re.X), otherwise it will not work.
# more info: https://docs.python.org/3/library/re.html#re.VERBOSE
JAVA_METHOD_PATTERN = r"""#(?:\/\*(?:(?!\/\*)[\s\S])*?\*\/)?    # comments before the java method, only /* */ comments allowed
                          #\s*?(@\w+)?\s*?          # method descriptors, e.g. @overload
                          (?:(?:public|private|protected|static|final|native|synchronized|abstract|transient)+\s+)+      # methods specifier
                          [$_\w<>\[\]\s]*          # methods return type, allowed to have generic
                          \s+[\$_\w]+              # method name
                          \([^\)]*\)?              # method arguments
                          \s*(?:throws)?.*         # method exceptions
                          \{?"""


# The read control of the java source code
SOURCE_CODE_READ_ARGS = {
    'mode': 'r',
    'encoding': 'utf-8'
}



# class LogTemplateMachine(StateMachine):
#     empty = State("String Literal Empty", initial=True)
#     in_str = State("Log Template")
#     slashed = State("Slashed character")
#     out_str = State("String END")
#     next = State("Next Parameter")
#     param = State("Log Parameter")
#     single = State("Single Quotation")
#     double = State("Double Quotation")
#     param_slashed = State("Parameter Slashed")
#     end = State("Machine End")
#     error = State("Error", enter="raise_error")
    
#     receive_letter = (
#         empty.to(in_str, cond="is_double_quotation")
#         | empty.to(param, cond="is_parameter", on="record_current")
#         | empty.to.itself(cond="is_whitespace")
#         | empty.to(error, on="debug")
#         | in_str.to(out_str, cond="is_double_quotation", on="add_to_template", after="clear_record")
#         | in_str.to(slashed, cond="is_slash", on="record_current")
#         | in_str.to.itself(on="record_current")
#         | slashed.to(in_str, on="record_current")
#         | out_str.to(empty, cond="is_plus")
#         | out_str.to(next, cond="is_comma")
#         | out_str.to(end, cond="is_end_right_parenthesis")
#         | out_str.to.itself(cond="is_whitespace")
#         | out_str.to(error, on="debug")
#         | next.to(param, cond="is_parameter", on="record_current")
#         | next.to.itself(cond="is_whitespace")
#         | next.to(error, before="debug")
#         | param.to(next, cond="is_comma", on="add_to_parameter", after="clear_record")
#         | param.to(single, cond="is_single_quotation", on="record_current")
#         | param.to(double, cond="is_double_quotation", on="record_current")
#         | param.to(end, cond="is_end_right_parenthesis", on="add_to_parameter", after="clear_record")
#         | param.to.itself(cond="is_parameter", on="record_current")
#         | param.to.itself(cond="is_whitespace")
#         | param.to(out_str, on="add_to_parameter", after="clear_record")
#         | single.to(param, cond="is_single_quotation", on="record_current")
#         # | single.to(param_slashed, cond="is_slash", on="record_current")
#         | single.to.itself()
#         | double.to(param, cond="is_double_quotation", on="record_current")
#         | double.to(param_slashed, cond="is_slash", on="record_current")
#         | double.to.itself(on="record_current")
#         | param_slashed.to(double, on="record_current")
#     )
    
#     def __init__(self):
#         self.record = []
#         self.template = ""
#         self.parameters = []
#         self.param_blocks = []
#         self.depth = 1
#         super().__init__()
    
#     def __str__(self):
#         s = ", ".join(self.parameters)
#         return f"[Current State is {self.current_state.id}]Template: \"{self.template}\", with parameters: {s}"
    
#     def is_single_quotation(self, letter):
#         return letter == "'"
    
#     def is_double_quotation(self, letter):
#         return letter == '"'
    
#     def is_whitespace(self, letter):
#         return letter in ' \t\n\r\v\f'
    
#     def is_slash(self, letter):
#         return letter == '\\'
    
#     def is_plus(self, letter):
#         return letter == '+'
    
#     def is_comma(self, letter):
#         return letter == ','
    
#     def is_end_right_parenthesis(self, letter):
#         if letter == ")":
#             self.depth -= 1
#             if self.depth == 0:
#                 return True
#         return False
    
#     def is_parameter(self, letter):
#         if letter == "(":
#             self.depth += 1
#             return True
#         else:
#             return letter in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$[].<>()/%=!&|^~<>+-*/?:'
    
#     def record_current(self, letter):
#         self.record.append(letter)
        
#     def add_to_template(self):
#         self.template += ''.join(self.record)
    
#     def add_to_parameter(self):
#         self.parameters.append(''.join(self.record))
    
#     def clear_record(self):
#         self.record.clear()
    
#     def raise_error(self):
#         print("Raise an error")
        
#     def debug(self, letter):
#         print(letter)
#         print(self.current_state.id)



def read_file(filepath: str) -> str:
    """read the file and return its full context

    Args:
        filepath (str): the relative or absolute path to the file

    Returns:
        str: the context of the file
        If the file is not found, return None
    """
    with open(filepath, **SOURCE_CODE_READ_ARGS) as f:
        lines = f.readlines()
    return ''.join(lines)
            

def get_java_method_context(source_code: str):
    """Receive the source code and return the list of (start, end) positions of the method which refers to the declaration of the method
    And the scope is [start, end).

    Args:
        source_code (str): the java source code
    
    Returns:
        list(tuple(int, int)): the list of (start, end) positions of the method, the start and end are the index of the source_code
        If the method is not found, return None
    """
    obj = re.compile(JAVA_METHOD_PATTERN, re.X)
    methods = []
    for result in obj.finditer(source_code):
        methods.append((result.start(), result.end()))
        
    return methods
    

def get_subfolder_path(folder_path: str, pattern: str) -> list:
    """Receive the folder path and return the list of subfolder path which matches the pattern

    Args:
        folder_path (str): the folder path
        pattern (str): the pattern of the subfolder name

    Returns:
        list(str): the list of subfolder path
    """
    folder = os.path.abspath(folder_path)
    matched_files = [ str(path) for path in glob(os.path.join(folder, pattern), recursive=True)]
    return matched_files
    
        
# def get_template_from_statement(statement):
#     template_state = LogTemplateMachine()
#     forward = 0
#     level = ""
#     while forward < len(statement) and statement[forward] in string.ascii_letters:
#         forward += 1
#     level = statement[0:forward]
#     if level not in settings.LOG_LEVEL:
#         print(f"Error: {level} is not allowed")
#     while forward < len(statement) and statement[forward] != '(':
#         forward += 1
#     if forward > len(statement):
#         print("Error")
#     # statement[forward] == '('
#     forward += 1
#     while forward < len(statement) and not template_state.end.is_active:
#         template_state.receive_letter(statement[forward])
#         forward += 1
#     if template_state.template == "":
#         print(statement)
#         # print(f"{level} {template_state.template} {template_state.parameters}")
    
#     return template_state.template, template_state.parameters, level



        


# def scheduler(folder_path, pattern="**/*.java"):
#     folder = pathlib.Path(folder_path)
#     method_id = 0
#     with ThreadPool() as pool:
#         items = folder.glob(pattern)
#         with db.DBase(settings.DB_NAME) as dbase:
#             dbase.create_tables()
#             for result in pool.imap_unordered(extract_log, items):
#                 fp = str(result[1].resolve())
#                 for method_log in result[0]:
#                     if len(method_log[0]) != 0 or len(method_log[2]) != 0:
#                         dbase.insert_into_table(settings.SQL_INSERT_TABLE_METHOD, (method_id, method_log[1], fp))
#                     for log in method_log[0]:
#                         intention = ""
#                         dbase.insert_into_table(settings.SQL_INSERT_TABLE_LOGS, (log[0], json.dumps(log[1]), log[2], log[3], intention,method_id))
#                     for log in method_log[2]:
#                         dbase.insert_into_table(settings.SQL_INSERT_TABLE_UNRESOLVED_LOGS, (log, method_id))
#                     method_id += 1
#                     if method_id % 10 == 0:
#                         print(method_id)
                
            


if __name__ == '__main__':
    from tqdm import tqdm
    folder_path = "./../resources/hadoop_source_code"
    file_pattern = "**/*hdfs*/**/*.java"
    print("Getting subfolder path")
    fps = get_subfolder_path(folder_path, file_pattern)
    progress_bar = tqdm(range(len(fps)), total=len(fps), desc="Extracting logs", unit="files", ncols=None)
    for fp, _ in zip(fps, progress_bar):
        if not fp.endswith(".java") or not "hdfs" in fp:
            print(fp)
    progress_bar.close()