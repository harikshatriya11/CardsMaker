# from django.shortcuts import render, redirect
# from django.template import loader
#
# from django.views.decorators import gzip
# from django.http import StreamingHttpResponse, HttpResponse
# import cv2
# import threading
#
# def HomeLiveCam(request):
#     if request.user.is_authenticated:
#         response =  {}
#         template = loader.get_template("livematch/livematch.html")
#
#         return HttpResponse(template.render(response, request))
#     else:
#         return redirect('/login')
#
# import socket
# import cv2
# import pickle
# import struct
# import imutils
#
# def client_socket(request):
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host_ip = '192.168.1.14'
#     port = 8002
#     client_socket.connect((host_ip, port))
#     data = b""
#     payload_size = struct.calcsize("Q")
#     print('payload_size:',payload_size)
#     while True:
#         while len(data) < payload_size:
#             print('data:',data)
#             packet = client_socket.recv(4*1024)
#             if not packet:break
#             data+=packet
#             packed_msg_size = data[:payload_size]
#             data = data[payload_size:]
#             msg_size = struct.unpack("Q", packed_msg_size)[0]
#         while len(data) < msg_size:
#             data += client_socket.recv(4*1024)
#         frame_data = data[:msg_size]
#         data = data[msg_size:]
#         frame = pickle.loads(frame_data)
#         cv2.imshow("Receiving...", frame)
#         key = cv2.waitKey(10)
#         if key == 13:
#             break
#     client_socket.close()
#
#
# def server_socket(request):
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host_ip = '192.168.1.14'
#     port = 8002
#     socket_address = (host_ip, port)
#     server_socket.bind(socket_address)
#     server_socket.listen(5)
#     print('socket now listening')
#     while True:
#         client_socket, addr = server_socket.accept()
#         if client_socket:
#             vid = cv2.VideoCapture(0)
#             while(vid.isOpened()):
#                 img, frame = vid.read()
#                 a = pickle.dumps(frame)
#                 message = struct.pack("Q", len(a))+a
#                 client_socket.sendall(message)
#                 cv2.imshow('Sending .... ', frame)
#                 key = cv2.waitKey(10)
#                 if key == 13:
#                     client_socket.close()
# # def showframe(request):
# #     while True:
# #         while len(data) < payload_size:
# #             packet = client_socket.recv(4*1024)
# #             if not packet:break
# #             data+=packet
