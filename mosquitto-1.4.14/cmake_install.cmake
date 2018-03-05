# Install script for directory: /Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

if("${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/etc/mosquitto" TYPE FILE FILES
    "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/mosquitto.conf"
    "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/aclfile.example"
    "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/pskfile.example"
    "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/pwfile.example"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/lib/cmake_install.cmake")
  include("/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/client/cmake_install.cmake")
  include("/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/src/cmake_install.cmake")
  include("/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/man/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/Users/Szc/Documents/workspace/CSE222A/MQTT_on_QUIC/mosquitto-1.4.14/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
