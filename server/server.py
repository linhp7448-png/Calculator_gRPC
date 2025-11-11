import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServiceServicer):
    def Add(self, request, context):
        return calculator_pb2.CalcReply(result=request.num1 + request.num2)

    def Subtract(self, request, context):
        return calculator_pb2.CalcReply(result=request.num1 - request.num2)

    def Multiply(self, request, context):
        return calculator_pb2.CalcReply(result=request.num1 * request.num2)

    def Divide(self, request, context):
        if request.num2 == 0:
            context.set_details("Division by zero!")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return calculator_pb2.CalcReply()
        return calculator_pb2.CalcReply(result=request.num1 / request.num2)

