import logging
# logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger("main")

from tqdm import tqdm

from statemachine import StateMachine, State
import multiprocessing

# import logging.config
# from app.helper import settings
from ..helper import settings
from ..helper import db
from .utils.file import read_file, get_java_method_context, get_subfolder_path
from .parser.statement_parser import get_log_template

class LogStateMachine(StateMachine):
    expr = State('Expression', initial=True)
    str_literal = State('StringLiteral')
    char_literal = State('CharLiteral')
    str_slash = State('Slash in string')
    char_slash = State('Slash in char')
    logger_method = State('Logger Method')
    logger_level = State('Logger Level')
    logger_template = State('Logger Template')
    logger_quotation = State('Logger Quotation')
    logger_quotation_slash = State('Slash in logger quotation')
    forward_slash = State('ForwardSlash')
    multiline = State('Multi-line Comment')
    singleline = State('Single-line Comment')
    star = State("Multi-line Comment End *")
    end = State("Method End")
    
    receive_token = (
        expr.to(str_literal, cond="is_double_quotation")
        | expr.to(char_literal, cond="is_single_quotation")
        | expr.to(logger_method, cond="is_logger")
        | expr.to(forward_slash, cond="is_forward_slash")
        | expr.to(end, cond="is_block_end")
        | expr.to.itself(cond="is_trival")
        | expr.to.itself(on="discard_comments")
        | str_literal.to(str_slash, cond="is_slash")
        | str_literal.to(expr, cond="is_double_quotation")
        | str_literal.to.itself()
        | char_literal.to(char_slash, cond="is_slash")
        | char_literal.to(expr, cond="is_single_quotation")
        | char_literal.to.itself()
        | char_slash.to.itself()
        | str_slash.to(str_literal)
        | char_slash.to(char_literal)
        | logger_method.to(logger_level, cond='is_dot')
        | logger_method.to(expr)
        | logger_level.to(logger_template, cond="is_log_level", on='record_current')
        | logger_level.to(expr)
        | logger_template.to(expr, cond='is_semicolon', before='add_log_info', on="discard_comments", after="clear_record")
        | logger_template.to(logger_quotation, cond="is_double_quotation", on='record_current')
        | logger_template.to.itself(on='record_current')
        | logger_quotation.to(logger_quotation_slash, cond="is_slash", on="record_current")
        | logger_quotation.to(logger_template, cond="is_double_quotation", on="record_current")
        | logger_quotation.to.itself(on="record_current")
        | logger_quotation_slash.to(logger_quotation, on="record_current")
        | forward_slash.to(singleline, cond="is_forward_slash")
        | forward_slash.to(multiline, cond="is_star")
        | forward_slash.to(expr)
        | singleline.to(expr, cond="is_newline", on="add_comment_info", after="clear_record")
        | singleline.to.itself(on="record_current")
        | multiline.to(star, cond="is_star")
        | multiline.to.itself(on="record_current")
        | star.to(expr, cond="is_forward_slash", before="remove_last_record", on="add_comment_info", after="clear_record")
        | star.to(multiline)
    )
    
    def __init__(self, logger_name):
        self.block_depth = 1
        self.comments = []
        self.logger_name = logger_name
        self.unresolved_logs = []
        self.record = []
        self.logs = []
        super().__init__()
    
    def is_trival(self, letter):
        return letter in ' \t\n\r\v\f;'
    
    def is_double_quotation(self, token):
        return token == '"'
    
    def is_single_quotation(self, token):
        return token == '\''

    def is_logger(self, token):
        return token == self.logger_name
    
    def is_dot(self, token):
        return token == '.'
    
    def is_log_level(self, token):
        return token in settings.LOG_LEVEL
    
    def is_forward_slash(self, token):
        return token == '/'
    
    def is_block_end(self, token):
        if token == '}':
            self.block_depth -= 1
        elif token == '{':
            self.block_depth += 1
        return self.block_depth == 0
    
    def is_slash(self, token):
        return token == '\\'
    
    def is_semicolon(self, token):
        return token == ';'
    
    def is_star(self, token):
        return token == '*'
    
    def is_newline(self, token):
        return token == '\n'
    
    def record_current(self, token):
        self.record.append(token)
    
    def remove_last_record(self):
        self.record.pop()
    
    def add_log_info(self):
        log_info = ''.join(self.record)
        template, level = get_log_template(log_info)
        if template:
            self.logs.append((template, level, ''.join(self.comments)))
        
        
    def add_comment_info(self):
        comment_info = ''.join(self.record)
        self.comments.append(comment_info)
    
    def clear_record(self):
        self.record.clear()
        
    def discard_comments(self):
        self.comments.clear()
        
def get_log_context(source_code, method):
    """Receive the java method and process to get full LogInfo that can be used to generate the log description

    Args:
        method (str): Java method
    
    Returns:
        list(LogInfo): the list of LogInfo that can be used to generate the log description
        If the method is not found, return None
    """
    start, end = method
    log_state = LogStateMachine("LOG")
    forward = end
    
    while not log_state.end.is_active and forward < len(source_code):
        while source_code[forward] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$':
            forward += 1

        if end == forward:
            forward = end + 1
        log_state.receive_token(source_code[end:forward])
        end = forward
    # print(source_code[start:end])
    method_code = source_code[start:end]
    logs = log_state.logs
    return logs, method_code

def extract_log(fp):
    sc = read_file(fp)
    methods = get_java_method_context(sc)
    logs = []
    for method in methods:
        logs.append(get_log_context(sc, method))
        
    return logs, fp

def scheduler(folder_path, pattern, options=None):
    method_id = 0
    log_id = 0
    file_number = 1
    with multiprocessing.Pool(processes=multiprocessing.cpu_count(), maxtasksperchild=100) as pool:
        items = get_subfolder_path(folder_path, pattern=pattern)
        progress_bar_iter = tqdm(range(len(items)), desc=f"Extracting Logs", unit="file", ncols=None, bar_format="{l_bar}{bar:20}{r_bar}{bar:-20b}",)
        with db.DBase(settings.DB_NAME) as dbase:
            if options == settings.OPTION_RESET:
                dbase.remove_tables()
            dbase.create_tables()
            first = True
            for result, _ in zip(pool.imap_unordered(extract_log, items, chunksize=100), progress_bar_iter):
                fp = result[1]
                for method_log in result[0]:
                    if len(method_log[0]) != 0:
                        summary = ""
                        dbase.insert_into_table(settings.SQL_INSERT_TABLE_METHOD, (method_id, method_log[1], fp, summary))
                        logger.info(f"Insert method: ({method_id}, {method_log[1]}, {fp}, {summary})")
                    for log in method_log[0]:
                        intention = ""
                        if log[2]:
                            logger.info(f"Get log with comment: ({log[0]}, {log[1]}, {log[2]}, {intention}, {method_id})")
                        if not dbase.attribute_exists("logs", "template", log[0]):
                            dbase.insert_into_table(settings.SQL_INSERT_TABLE_LOGS, (log[0], log[1], log[2], intention, log_id, method_id))
                            logger.info(f"Insert log: ({log[0]}, {log[1]}, {log[2]}, {intention}, {log_id}, {method_id})")
                        else:
                            logger.info(f"Log template {log[0]} already exists")
                        log_id += 1
                        
                        # if log_id % 100 == 0:
                        #     print(f"log id: {log_id}")
                    
                    if len(method_log[0]) != 0:
                        method_id += 1
                        first = True
                    if method_id % 100 == 0 and first:
                        # print(f"method id: {method_id}")
                        first = False
                file_number += 1
                # if file_number % 100 == 0:
                #     print(f"file number: {file_number}")
        
        progress_bar_iter.close()

if __name__ == "__main__":
    scheduler(settings.FOLDER_PATH, settings.FILE_PATTERN, settings.OPTION_RESET)
    print("Hello World!")