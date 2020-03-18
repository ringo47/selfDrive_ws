
(cl:in-package :asdf)

(defsystem "spinnaker_sdk_camera_driver-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "SpinnakerImageNames" :depends-on ("_package_SpinnakerImageNames"))
    (:file "_package_SpinnakerImageNames" :depends-on ("_package"))
  ))