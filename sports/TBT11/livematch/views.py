# # import cv2
# from django.shortcuts import render, redirect
# from django.template import loader
#
# from django.views.decorators import gzip
# from django.http import StreamingHttpResponse, HttpResponse
# # import cv2
# import threading
#
# def Home(request):
#     if request.user.is_authenticated:
#         response =  {}
#         template = loader.get_template("livematch/livematch.html")
#
#         return HttpResponse(template.render(response, request))
#     else:
#         return redirect('/login')
# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start()
#
#     def __del__(self):
#         self.video.release()
#
#     def get_frame(self):
#         image = self.frame
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()
#
#     def update(self):
#         while True:
#             (self.grabbed, self.frame) = self.video.read()
#
#
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#
#
# @gzip.gzip_page
# def livecam(request):
#     response = None
#     try:
#         cam = VideoCamera()
#         print(cam)
#         response = StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:  # This is bad! replace it with proper handling
#         return redirect('/')
#     return response