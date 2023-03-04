from antlr4 import *
from antlr4.error.ErrorListener import ConsoleErrorListener

if __name__ is not None and "." in __name__:
    from .JavaExpressionLexer import JavaExpressionLexer
    from .JavaExpressionParser import JavaExpressionParser
    from .JavaExpressionListener import JavaExpressionListener
else:
    from JavaExpressionLexer import JavaExpressionLexer
    from JavaExpressionParser import JavaExpressionParser
    from JavaExpressionListener import JavaExpressionListener

import logging

class MyErrorListener(ConsoleErrorListener):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("parser")

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.logger.error(f"line {line}:{column} {msg}")

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        self.logger.warning("Ambiguity error")

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        self.logger.warning("Attempting full context error")

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        self.logger.warning("Context sensitivity error")

def get_log_template(statement):
    # print(statement)
    lexer = JavaExpressionLexer(InputStream(statement))
    
    parser = JavaExpressionParser(CommonTokenStream(lexer))
    error_listener = MyErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    tree =  parser.expression()
    listerer = JavaExpressionListener()
    walker = ParseTreeWalker()
    walker.walk(listerer, tree)
    # print(tree.toStringTree(recog=parser))
    return listerer.template, listerer.log_level

if __name__ == '__main__':
    error_log4 = """
    debug(
        "read-0arg uri:{}, contentLength:{}, position:{}, readValue:{}, "
            + "thread:{}, timeUsedMilliSec:{}",
        uri, contentLength, byteRead >= 0 ? nextReadPos - 1 : nextReadPos,
        byteRead, threadId,
        endTime - startTime)
    """
    error_log5 = """
        debug(
            "Using OBSBlockOutputStream with buffer = {}; block={};"
                + " queue limit={}",
            blockOutputBuffer,
            partSize,
            blockOutputActiveBlocks)
        """
    error_log6 = """
    warn(OBSConstants.MAX_THREADS
            + " must be at least 2: forcing to 2.")"""
    error_log7 = "error(e.getMessage())"

    error_log8 = """
    debug(String.format(
        "file size [%d] - file count [%d] - directory count [%d] - "
            + "file path [%s]",
        summary[0], summary[1], summary[2], newKey))
    """
    error_log9 = """
    info("Bytes read: " +
            Math.round((double) bytesRead / Unit.MB) + "MB")
            """
    error_log10 = """debug("No node to choose.")"""
    error_log11 = """error("Error reported on file " + f + "... exiting",
          new Exception())"""
    error_log12 = """
    error("Got error reading edit log input stream " +
          streams[curIdx].getName() + "; failing over to edit log " +
          streams[curIdx + 1].getName(), prevException)"""
    error_log13 = """
    info("verifyFileReplicasOnStorageType: for file " + path +
            ". Expect blk" + locatedBlock +
          " on Type: " + storageType + ". Actual Type: " +
          locatedBlock.getStorageTypes()[0])"""
    
    print(get_log_template(error_log9))
    print(get_log_template(error_log10))
    print(get_log_template(error_log11))
    print(get_log_template(error_log12))
    print(get_log_template(error_log13))