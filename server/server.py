import sys
import os
import math
import re
import grpc
import logging
from concurrent import futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from proto import calculator_pb2, calculator_pb2_grpc

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

class CalculatorService(calculator_pb2_grpc.CalculatorServiceServicer):
    def Calculate(self, request, context):
        expr = request.expression.strip()
        logging.info(f"[SERVER] Nhận biểu thức: {expr}")

        if not expr:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Biểu thức không được để trống")
            return calculator_pb2.CalculatorResponse() 
            
        if not re.match(r'^[\d\s\+\-\*\/\^\(\)\.a-zA-Z,_]*$', expr):
            
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Biểu thức chứa ký tự không hợp lệ")
            return calculator_pb2.CalculatorResponse()

        try:
            expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
            expr = re.sub(r'\)(\d)', r')*\1', expr)
            expr = re.sub(r'\)([a-zA-Z])', r')*\1', expr)

            safe_math = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
            safe_math.update({"abs": abs, "pow": pow})

            result = eval(expr, {"__builtins__": None}, safe_math)

            return calculator_pb2.CalculatorResponse(result=float(result))
        except ZeroDivisionError:
            logging.error(f"Lỗi chia cho 0: '{expr}'")
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Lỗi tính toán: Không thể chia cho 0")
        except SyntaxError:
            logging.error(f"Lỗi cú pháp: '{expr}'") 
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Lỗi cú pháp: Biểu thức không hợp lệ")
        except Exception as e:
            logging.error(f"Lỗi không xác định '{expr}': {e}") 
            context.abort(grpc.StatusCode.INTERNAL, f"Lỗi máy chủ: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorService(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("✅ Server đang chạy tại cổng 50051...")
    server.start()
    server.wait_for_termination()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logging.info("🛑 Server dừng thủ công.")
        server.stop(0)

if __name__ == "__main__":
    serve()

