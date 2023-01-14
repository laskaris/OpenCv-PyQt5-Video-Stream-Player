videoSource = "rtspsrc location=rtsp://192.168.1.100/stream.sdp ! rtph264depay ! avdec_h264 ! videoconvert ! appsink sync=false drop=true "
appTitle = "OpenCv Video"
logo = "init/logo.jpg"
ip = "192.168.1.100"
port = 2000