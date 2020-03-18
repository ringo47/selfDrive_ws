;; Auto-generated. Do not edit!


(when (boundp 'spinnaker_sdk_camera_driver::SpinnakerImageNames)
  (if (not (find-package "SPINNAKER_SDK_CAMERA_DRIVER"))
    (make-package "SPINNAKER_SDK_CAMERA_DRIVER"))
  (shadow 'SpinnakerImageNames (find-package "SPINNAKER_SDK_CAMERA_DRIVER")))
(unless (find-package "SPINNAKER_SDK_CAMERA_DRIVER::SPINNAKERIMAGENAMES")
  (make-package "SPINNAKER_SDK_CAMERA_DRIVER::SPINNAKERIMAGENAMES"))

(in-package "ROS")
;;//! \htmlinclude SpinnakerImageNames.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass spinnaker_sdk_camera_driver::SpinnakerImageNames
  :super ros::object
  :slots (_header _name _time ))

(defmethod spinnaker_sdk_camera_driver::SpinnakerImageNames
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:name __name) (let (r) (dotimes (i 0) (push "" r)) r))
    ((:time __time) (instance ros::time :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _name __name)
   (setq _time __time)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; string[] _name
    (apply #'+ (mapcar #'(lambda (x) (+ 4 (length x))) _name)) 4
    ;; time _time
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; string[] _name
     (write-long (length _name) s)
     (dolist (elem _name)
       (write-long (length elem) s) (princ elem s)
       )
     ;; time _time
       (write-long (send _time :sec) s) (write-long (send _time :nsec) s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; string[] _name
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _name (make-list n))
     (dotimes (i n)
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setf (elt _name i) (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
     ))
   ;; time _time
     (send _time :sec (sys::peek buf ptr- :integer)) (incf ptr- 4)  (send _time :nsec (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get spinnaker_sdk_camera_driver::SpinnakerImageNames :md5sum-) "e118cce7e10bceec739777176ef69931")
(setf (get spinnaker_sdk_camera_driver::SpinnakerImageNames :datatype-) "spinnaker_sdk_camera_driver/SpinnakerImageNames")
(setf (get spinnaker_sdk_camera_driver::SpinnakerImageNames :definition-)
      "Header      header
string[]    name
time        time

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :spinnaker_sdk_camera_driver/SpinnakerImageNames "e118cce7e10bceec739777176ef69931")


