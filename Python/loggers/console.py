from datetime import date, datetime
class ConsoleLogger:
    def log_error(self, message):
        print("[ERROR] {}: {}".format(datetime.now(), message))

    def log_info(self, message):
        print("[INFO] {}: {}".format(datetime.now(), message))